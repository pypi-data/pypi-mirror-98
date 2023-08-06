import unittest

from kolibri.stopwords import get_stop_words
from kolibri.tokenizer import RegexpTokenizer, WordTokenizer, CharTokenizer, SentenceTokenizer

text_original = "The quick brown fox jumps over the lazy dog"
tokenized_words = ['The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog']
tokenized_no_stopwords = ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog']
tokenized_chars = ['th', 'e ', 'qu', 'ic', 'k ', 'br', 'ow', 'n ', 'fo', 'x ', 'ju', 'mp', 's ', 'ov', 'er', ' t', 'he',
                   ' l', 'az', 'y ', 'do', 'g']

en_stopwords = get_stop_words('en')
fr_stopwords = get_stop_words('fr')


def areEqual(arr1, arr2):
    # Linearly compare elements
    for i in range(0, len(arr1) - 1):
        if (arr1[i] != arr2[i]):
            return False
    return True


class TestKolibriTokeniers(unittest.TestCase):

    def test_regex_tokenizer(self):
        tokenizer = RegexpTokenizer()
        tokenized = tokenizer.tokenize(text_original)
        assert len(tokenized_words) == len(tokenized)
        assert areEqual(tokenized, tokenized_words)

    def test_word_tokenizer(self):
        tokenizer = WordTokenizer({'filter-stopwords': False})
        tokenized = tokenizer.tokenize(text_original)
        assert len(tokenized_words) == len(tokenized)
        assert areEqual(tokenized, tokenized_words)

    def test_word_tokenizer_lower(self):
        tokenizer = WordTokenizer({'do_lower_case': True})
        self.assertListEqual(
            tokenizer.tokenize(u" \tHeLLo!how  \n Are yoU?  "),
            ["hello",  "how", "are", "you"])
        self.assertListEqual(tokenizer.tokenize(u"H\u00E9llo"), ["hello"])

    def test_word_tokenizer_white_space(self):
        tokenizer = WordTokenizer({'do_lower_case': True, "whitespace": True})
        self.assertListEqual(
            tokenizer.tokenize(u" \tHeLLo!how  \n Are yoU?  "),
            ["hello", "!", "how", "are", "you", "?"])
        self.assertListEqual(tokenizer.tokenize(u"H\u00E9llo"), ["hello"])

    def test_word_tokenizer_stopwords(self):
        tokenizer = WordTokenizer({'filter-stopwords': True})
        tokenized = tokenizer.tokenize(text_original)
        assert tokenizer.stopwords == set(en_stopwords)
        assert len(tokenized_no_stopwords) == len(tokenized)
        assert areEqual(tokenized, tokenized_no_stopwords)
        tokenizer = WordTokenizer({'filter-stopwords': True, 'language': 'fr'})
        assert tokenizer.stopwords == set(fr_stopwords)

    def test_char_tokenizer(self):
        tokenizer = CharTokenizer({'ngram': 2})
        tokenized = tokenizer.tokenize(text_original)
        assert len(tokenized_chars) == len(tokenized_chars)
        assert areEqual(tokenized, tokenized_chars)

    def test_sentence_tokenizer(self):
        text = "This is a text with 3 sentences that should be splitted. This is the second sentence in this text. What about a third sentence also?"
        tokenizer = SentenceTokenizer()
        sentences = tokenizer.tokenize(text)

        assert len(sentences) == 3
        assert sentences[0] == "This is a text with 3 sentences that should be splitted."
        assert sentences[1] == "This is the second sentence in this text."
        assert sentences[2] == "What about a third sentence also?"

    def test_custom_stopwords(self):
        custom_sw = ['sw1', 'ws2', 'sw3', 'sw4']

        tokenizer = WordTokenizer({'filter-stopwords': True, "custom-stopwords": custom_sw})

        assert tokenizer.stopwords == set(custom_sw)

    def test_add_to_stopwords(self):
        custom_sw = ['sw1', 'ws2', 'sw3', 'sw4', 'a', 'about', 'above']

        tokenizer = WordTokenizer({'filter-stopwords': True, "add-to-stopwords": custom_sw})
        custom_sw_unique = ['sw1', 'ws2', 'sw3', 'sw4']
        custom_sw_unique.extend(en_stopwords)
        assert tokenizer.stopwords == set(custom_sw_unique)

    def test_remove_from_stopwords(self):

        custom_sw = ['a', 'about', 'above', 'sw4']
        en_stopwords_local = en_stopwords.copy()
        tokenizer = WordTokenizer({'filter-stopwords': True, "remove-from-stopwords": custom_sw})
        for sw in custom_sw:
            if sw in en_stopwords_local:
                en_stopwords_local.remove(sw)

        assert tokenizer.stopwords == set(en_stopwords_local)
