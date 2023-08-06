#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Rico Sennrich

"""Use operations learned with learn_bpe.py to encode a new text.
The text will not be smaller, but use only a fixed vocabulary, with rare words
encoded as variable-length sequences of subword units.

Reference:
Rico Sennrich, Barry Haddow and Alexandra Birch (2015). Neural Machine Translation of Rare Words with Subword Units.
Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (ACL 2016). Berlin, Germany.
"""

from __future__ import unicode_literals, division

import sys
import os
import inspect
import codecs
import io
import argparse
import re
import warnings
import random
from collections import Counter
import tempfile
from multiprocessing import Pool, cpu_count
from kolibri import Component
import tqdm
from kolibri.tokenizer.bpe_functions import *
import copy

# hack for python2/3 compatibility
from io import open
argparse.open = open

class BPE(Component):
    provides = ["vocabulary"]
    requires = ["tokens"]
    name = "subword_vocabulary"
    defaults = {
        "merges": -1,
        "separator": '@@',
        "version": "0.2",
        "vocab": None,
        "glossaries": None,
        "codes_file":None,
        "num_symbols": 10000,
        "min_frequency" : 2,
        "verbose" : False,
        "is_dict" : False,
        "total_symbols" : False,
        "num_workers" :1,
        "output_file": "corpus.bpe",
        "dropout":0
    }
    def __init__(self, config={}):

        super().__init__(config)
        merges = self.component_config['merges']
        codes_file = self.component_config["codes_file"]

        if codes_file:
            codes=open(codes_file, encoding='utf-8')
            codes.seek(0)
            offset=1

            # check version information
            firstline = codes.readline()
            if firstline.startswith('#version:'):
                self.version = tuple([int(x) for x in re.sub(r'(\.0+)*$','', firstline.split()[-1]).split(".")])
                offset += 1
            else:
                self.version = (0, 1)
                codes.seek(0)

            self.bpe_codes = [tuple(item.strip('\r\n ').split(' ')) for (n, item) in enumerate(codes.read().rstrip('\n').split('\n')) if (n < merges or merges == -1)]

            for i, item in enumerate(self.bpe_codes):
                if len(item) != 2:
                    sys.stderr.write('Error: invalid line {0} in BPE codes file: {1}\n'.format(i+offset, ' '.join(item)))
                    sys.stderr.write('The line should exist of exactly two subword units, separated by whitespace\n')
                    sys.exit(1)

            # some hacking to deal with duplicates (only consider first instance)
            self.bpe_codes = dict([(code,i) for (i,code) in reversed(list(enumerate(self.bpe_codes)))])

            self.bpe_codes_reverse = dict([(pair[0] + pair[1], pair) for pair,i in self.bpe_codes.items()])

        self.separator = self.component_config['separator']

        self.vocab = self.component_config['vocab']

        self.glossaries = self.component_config['glossaries'] if self.component_config['glossaries'] else []

        self.glossaries_regex = re.compile('^({})$'.format('|'.join(self.component_config['glossaries']))) if self.component_config['glossaries'] else None

        self.cache = {}
        self.outfile=open(self.component_config["output_file"], 'w', encoding='utf-8')

    def fit(self, X, y, x_val, y_val):
        """Learn num_symbols BPE operations from vocabulary, and write to outfile.
        """

        # version 0.2 changes the handling of the end-of-word token ('</w>');
        # version numbering allows bckward compatibility
        self.outfile.write('#version: '+self.component_config["version"]+'\n')

        vocab = Counter()

        num_workers=self.component_config["num_workers"]
        num_symbols=self.component_config["num_symbols"]
        total_symbols=self.component_config["total_symbols"]
        min_frequency=self.component_config["min_frequency"]
        verbose=self.component_config["verbose"]
        if num_workers == 1:
            for i, line in enumerate(X):
                for word in line:
                    if word:
                        vocab[word] += 1
        elif num_workers > 1:
            size = len(X)
            chunk_size = int(size / num_workers)
            offsets = [i*chunk_size for i in range(num_workers + 1)]
            offsets[-1]=size

            vocab_files = []
            pool = Pool(processes=num_workers)
            for i in range(num_workers):
                tmp = tempfile.NamedTemporaryFile(delete=False)
                tmp.close()
                vocab_files.append(tmp)
                pool.apply_async(self._get_vocabulary, (X, tmp.name, offsets[i], offsets[i + 1]))
            pool.close()
            pool.join()
            import pickle
            for i in range(num_workers):
                with open(vocab_files[i].name, 'rb') as f:
                    vocab += pickle.load(f)
                os.remove(vocab_files[i].name)
        else:
            raise ValueError('`num_workers` is expected to be a positive number, but got {}.'.format(num_workers))

        vocab = dict([(tuple(x[:-1]) + (x[-1] + '</w>',), y) for (x, y) in vocab.items()])
        sorted_vocab = sorted(vocab.items(), key=lambda x: x[1], reverse=True)

        stats, indices = get_pair_statistics(sorted_vocab)
        big_stats = copy.deepcopy(stats)

        if total_symbols:
            uniq_char_internal = set()
            uniq_char_final = set()
            for word in vocab:
                for char in word[:-1]:
                    uniq_char_internal.add(char)
                uniq_char_final.add(word[-1])
            sys.stderr.write('Number of word-internal characters: {0}\n'.format(len(uniq_char_internal)))
            sys.stderr.write('Number of word-final characters: {0}\n'.format(len(uniq_char_final)))
            sys.stderr.write(
                'Reducing number of merge operations by {0}\n'.format(len(uniq_char_internal) + len(uniq_char_final)))
            num_symbols -= len(uniq_char_internal) + len(uniq_char_final)

        # threshold is inspired by Zipfian assumption, but should only affect speed
        threshold = max(stats.values()) / 10
        for i in range(num_symbols):
            if stats:
                most_frequent = max(stats, key=lambda x: (stats[x], x))

            # we probably missed the best pair because of pruning; go back to full statistics
            if not stats or (i and stats[most_frequent] < threshold):
                prune_stats(stats, big_stats, threshold)
                stats = copy.deepcopy(big_stats)
                most_frequent = max(stats, key=lambda x: (stats[x], x))
                # threshold is inspired by Zipfian assumption, but should only affect speed
                threshold = stats[most_frequent] * i / (i + 10000.0)
                prune_stats(stats, big_stats, threshold)

            if stats[most_frequent] < min_frequency:
                sys.stderr.write('no pair has frequency >= {0}. Stopping\n'.format(min_frequency))
                break

            if verbose:
                sys.stderr.write(
                    'pair {0}: {1} {2} -> {1}{2} (frequency {3})\n'.format(i, most_frequent[0], most_frequent[1],
                                                                           stats[most_frequent]))
            self.outfile.write('{0} {1}\n'.format(*most_frequent))
            changes = replace_pair(most_frequent, sorted_vocab, indices)
            update_pair_statistics(most_frequent, changes, stats, indices)
            stats[most_frequent] = 0
            if not i % 100:
                prune_stats(stats, big_stats, threshold)

    def _get_vocabulary(self, data, begin, end):
        import pickle

        vocab = Counter()
        for line in  tqdm.tqdm(data[begin:end]):
            for word in line:
                if word:
                    vocab[word] += 1
        with open(self.component_config["output_file"], 'wb') as f:
            pickle.dump(vocab, f)

    def transform(self, X):
        Xt=None
        if sys.version_info < (3, 0):
            print("Parallel mode is only supported in Python3.")
            sys.exit(1)
        num_workers=self.component_config["num_workers"]
        dropout=self.component_config["dropout"]
        if num_workers == 1:
            Xt=[self.segment_tokens(line, dropout) for line in X]

        elif num_workers > 1:
            Xt=[None]*len(X)
            size = len(X)
            chunk_size = int(size / num_workers)
            offsets = [i*chunk_size for i in range(num_workers + 1)]
            offsets[-1]=size

            pool = Pool(processes=num_workers)

            for i in range(num_workers):
                pool.apply_async(self._process_lines, ( X, Xt,  dropout, offsets[i], offsets[i + 1]))
            pool.close()
            pool.join()

        else:
            raise ValueError('`num_workers` is expected to be a positive number, but got {}.'.format(num_workers))
        return Xt


    def segment_tokens(self, tokens, dropout=0):
        """segment a sequence of tokens with BPE encoding"""
        output = []
        for word in tokens:
            # eliminate double spaces
            if not word:
                continue
            new_word = [out for segment in self._isolate_glossaries(word)
                        for out in encode(segment,
                                          self.bpe_codes,
                                          self.bpe_codes_reverse,
                                          self.vocab,
                                          self.separator,
                                          self.version,
                                          self.cache,
                                          self.glossaries_regex,
                                          dropout)]

            for item in new_word[:-1]:
                output.append(item + self.separator)
            output.append(new_word[-1])

        return output

    def _isolate_glossaries(self, word):
        word_segments = [word]
        for gloss in self.glossaries:
            word_segments = [out_segments for segment in word_segments
                                 for out_segments in isolate_glossary(segment, gloss)]
        return word_segments

    def _process_lines(self, X, Xt, dropout, begin, end):
            Xt[begin:end]= [self.segment_tokens(line, dropout) for line in X[begin:end]]


def encode(orig, bpe_codes, bpe_codes_reverse, vocab, separator, version, cache, glossaries_regex=None, dropout=0):
    """Encode word based on list of BPE merge operations, which are applied consecutively
    """

    if not dropout and orig in cache:
        return cache[orig]

    if glossaries_regex and glossaries_regex.match(orig):
        cache[orig] = (orig,)
        return (orig,)

    if len(orig) == 1:
        return orig

    if version == (0, 1):
        word = list(orig) + ['</w>']
    elif version == (0, 2): # more consistent handling of word-final segments
        word = list(orig[:-1]) + [orig[-1] + '</w>']
    else:
        raise NotImplementedError

    while len(word) > 1:

        # get list of symbol pairs; optionally apply dropout
        pairs = [(bpe_codes[pair],i,pair) for (i,pair) in enumerate(zip(word, word[1:])) if (not dropout or random.random() > dropout) and pair in bpe_codes]

        if not pairs:
            break

        #get first merge operation in list of BPE codes
        bigram = min(pairs)[2]

        # find start position of all pairs that we want to merge
        positions = [i for (rank,i,pair) in pairs if pair == bigram]

        i = 0
        new_word = []
        bigram = ''.join(bigram)
        for j in positions:
            # merges are invalid if they start before current position. This can happen if there are overlapping pairs: (x x x -> xx x)
            if j < i:
                continue
            new_word.extend(word[i:j]) # all symbols before merged pair
            new_word.append(bigram) # merged pair
            i = j+2 # continue after merged pair
        new_word.extend(word[i:]) # add all symbols until end of word
        word = new_word

    # don't print end-of-word symbols
    if word[-1] == '</w>':
        word = word[:-1]
    elif word[-1].endswith('</w>'):
        word[-1] = word[-1][:-4]

    word = tuple(word)
    if vocab:
        word = check_vocab_and_split(word, bpe_codes_reverse, vocab, separator)

    cache[orig] = word
    return word

def recursive_split(segment, bpe_codes, vocab, separator, final=False):
    """Recursively split segment into smaller units (by reversing BPE merges)
    until all units are either in-vocabulary, or cannot be split futher."""

    try:
        if final:
            left, right = bpe_codes[segment + '</w>']
            right = right[:-4]
        else:
            left, right = bpe_codes[segment]
    except:
        #sys.stderr.write('cannot split {0} further.\n'.format(segment))
        yield segment
        return

    if left + separator in vocab:
        yield left
    else:
        for item in recursive_split(left, bpe_codes, vocab, separator, False):
            yield item

    if (final and right in vocab) or (not final and right + separator in vocab):
        yield right
    else:
        for item in recursive_split(right, bpe_codes, vocab, separator, final):
            yield item

def check_vocab_and_split(orig, bpe_codes, vocab, separator):
    """Check for each segment in word if it is in-vocabulary,
    and segment OOV segments into smaller units by reversing the BPE merge operations"""

    out = []

    for segment in orig[:-1]:
        if segment + separator in vocab:
            out.append(segment)
        else:
            #sys.stderr.write('OOV: {0}\n'.format(segment))
            for item in recursive_split(segment, bpe_codes, vocab, separator, False):
                out.append(item)

    segment = orig[-1]
    if segment in vocab:
        out.append(segment)
    else:
        #sys.stderr.write('OOV: {0}\n'.format(segment))
        for item in recursive_split(segment, bpe_codes, vocab, separator, True):
            out.append(item)

    return out


def read_vocabulary(vocab_file, threshold):
    """read vocabulary file produced by get_vocab.py, and filter according to frequency threshold.
    """

    vocabulary = set()

    for line in vocab_file:
        word, freq = line.strip('\r\n ').split(' ')
        freq = int(freq)
        if threshold == None or freq >= threshold:
            vocabulary.add(word)

    return vocabulary

def isolate_glossary(word, glossary):
    """
    Isolate a glossary present inside a word.

    Returns a list of subwords. In which all 'glossary' glossaries are isolated

    For example, if 'USA' is the glossary and '1934USABUSA' the word, the return value is:
        ['1934', 'USA', 'B', 'USA']
    """
    # regex equivalent of (if word == glossary or glossary not in word)
    if re.match('^'+glossary+'$', word) or not re.search(glossary, word):
        return [word]
    else:
        segments = re.split(r'({})'.format(glossary), word)
        segments, ending = segments[:-1], segments[-1]
        segments = list(filter(None, segments)) # Remove empty strings in regex group.
        return segments + [ending.strip('\r\n ')] if ending != '' else segments

