# coding=utf-8
# Copyright 2018 The Google AI Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Lint as: python2, python3
# coding=utf-8
"""Tokenization classes."""

import unicodedata
from kolibri.tokenizer.bert_tokenizer import load_vocab, convert_by_vocab, WordTokenizer, WordpieceTokenizer
import six
import tensorflow as tf
from six.moves import range

SPIECE_UNDERLINE = u"▁".encode("utf-8")


def encode_pieces(sp_model, text, return_unicode=True, sample=False):
    """turn sentences into word pieces."""


    if not sample:
        pieces = sp_model.EncodeAsPieces(text)
    else:
        pieces = sp_model.SampleEncodeAsPieces(text, 64, 0.1)
    new_pieces = []
    for piece in pieces:
        if isinstance(piece, bytes):
            piece= six.ensure_text(piece, "utf-8", "ignore")

        if len(piece) > 1 and piece[-1] == "," and piece[-2].isdigit():
            cur_pieces = sp_model.EncodeAsPieces(
                six.ensure_binary(piece[:-1]).replace(SPIECE_UNDERLINE, b""))
            if piece[0] != SPIECE_UNDERLINE and cur_pieces[0][0] == SPIECE_UNDERLINE:
                if len(cur_pieces[0]) == 1:
                    cur_pieces = cur_pieces[1:]
                else:
                    cur_pieces[0] = cur_pieces[0][1:]
            cur_pieces.append(piece[-1])
            new_pieces.extend(cur_pieces)
        else:
            new_pieces.append(piece)

    return new_pieces


def encode_ids(sp_model, text, sample=False):
    pieces = encode_pieces(sp_model, text, return_unicode=False, sample=sample)
    ids = [sp_model.PieceToId(piece) for piece in pieces]
    return ids


def whitespace_tokenize(text):
    """Runs basic whitespace cleaning and splitting on a piece of text."""
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens


class FullTokenizer(object):
    """Runs end-to-end tokenziation."""

    def __init__(self, vocab_file, do_lower_case=True, spm_model_file=None):
        self.vocab = None
        self.sp_model = None
        if spm_model_file:
            import sentencepiece as spm

            self.sp_model = spm.SentencePieceProcessor()
            tf.compat.v1.logging.info("loading sentence piece model")
            self.sp_model.Load(spm_model_file)
            # Note(mingdachen): For the purpose of consisent API, we are
            # generating a vocabulary for the sentence piece tokenizer.
            self.vocab = {self.sp_model.IdToPiece(i): i for i
                          in range(self.sp_model.GetPieceSize())}
        else:
            self.vocab = load_vocab(vocab_file)
            self.basic_tokenizer = WordTokenizer({'do_lower_case':do_lower_case})
            self.wordpiece_tokenizer = WordpieceTokenizer({'vocabulary':self.vocab})
        self.inv_vocab = {v: k for k, v in self.vocab.items()}

    @classmethod
    def from_scratch(cls, vocab_file, do_lower_case, spm_model_file):
        return FullTokenizer(vocab_file, do_lower_case, spm_model_file)

    @classmethod
    def from_hub_module(cls, hub_module, spm_model_file):
        """Get the vocab file and casing info from the Hub module."""
        import tensorflow_hub as hub
        with tf.Graph().as_default():
            albert_module = hub.Module(hub_module)
            tokenization_info = albert_module(signature="tokenization_info",
                                              as_dict=True)
            with tf.Session() as sess:
                vocab_file, do_lower_case = sess.run(
                    [tokenization_info["vocab_file"],
                     tokenization_info["do_lower_case"]])
        return FullTokenizer(
            vocab_file=vocab_file, do_lower_case=do_lower_case,
            spm_model_file=spm_model_file)

    def tokenize(self, text):
        if self.sp_model:
            split_tokens = encode_pieces(self.sp_model, text, return_unicode=False)
        else:
            split_tokens = []
            for token in self.basic_tokenizer.tokenize(text):
                for sub_token in self.wordpiece_tokenizer.tokenize(token):
                    split_tokens.append(sub_token)

        return split_tokens

    def convert_tokens_to_ids(self, tokens):
        if self.sp_model:
            tf.compat.v1.logging.info("using sentence piece tokenzier.")
            return [self.sp_model.PieceToId(token) for token in tokens]
        else:
            return convert_by_vocab(self.vocab, tokens)

    def convert_ids_to_tokens(self, ids):
        if self.sp_model:
            tf.compat.v1.logging.info("using sentence piece tokenzier.")
            return [self.sp_model.IdToPiece(id_) for id_ in ids]
        else:
            return convert_by_vocab(self.inv_vocab, ids)



