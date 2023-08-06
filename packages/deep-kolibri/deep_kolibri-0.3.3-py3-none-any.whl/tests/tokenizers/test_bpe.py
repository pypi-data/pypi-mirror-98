#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from kolibri.data.text.corpus.file_stream import FileStream
from kolibri.model_trainer import ModelTrainer
from kolibri.config import ModelConfig
from kolibri.tokenizer import WordTokenizer
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)


from kolibri.tokenizer.bpe import BPE


class TestBPELearnMethod(unittest.TestCase):

    def test_learn_bpe(self):

        confg = {
            "output_file": os.path.join(currentdir,'data','bpe.out'),
            "num_symbols": 1000,
            'do_lower_case': True
            }

        confg['output-folder'] = '/Users/mohamedmentis/Documents/Mentis/Development/Python/Deep_kolibri/demos'

        data = FileStream("/Users/mohamedmentis/Dropbox/My Mac (MacBook-Pro.local)/Documents/Mentis/Development/Python/Deep_kolibri/tests/tokenizers/data/corpus.en", filetype='txt')
        data.prepare()

        confg['pipeline'] = ['sentence_tokenizer', 'word_tokenizer', 'subword_vocabulary']

        trainer = ModelTrainer(ModelConfig(confg))
        x_val, y_val = data.get_data()
        trainer.fit(x_val, y_val)


        outlines = open(os.path.join(currentdir,'data','bpe.out'))
        reflines = open(os.path.join(currentdir,'data','bpe.ref'))

        for line, line2 in zip(outlines, reflines):
            self.assertEqual(line, line2)

        outlines.close()
        reflines.close()

class TestApplyBPE(unittest.TestCase):

    def setUp(self):
        confg = {
            "output_file": os.path.join(currentdir,'data','bpe.out'),
            "num_symbols": 1000,
            'do_lower_case': True,
            "codes_file": os.path.join(currentdir,'data','bpe.ref')
            }

        self.bpe = BPE(config=confg)

        self.infile = open(os.path.join(currentdir,'data','corpus.en'), encoding='utf-8')
        self.reffile = open(os.path.join(currentdir,'data','corpus.bpe.ref.en'), encoding='utf-8')

    def tearDown(self):

        self.infile.close()
        self.reffile.close()

    def test_apply_bpe(self):
        word_tokenizer=WordTokenizer(config={'do_lower_case': False, 'whitespace': True, 'split_on_punctuation':False})
        X=self.infile.readlines()
        X_target=self.reffile.readlines()
        X=word_tokenizer.transform(X)
        X=self.bpe.transform(X)
        for i, x in enumerate(X):
            self.assertEqual(' '.join(x), X_target[i].strip())

if __name__ == '__main__':
    unittest.main()
