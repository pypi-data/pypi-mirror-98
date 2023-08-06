import os
import tempfile
from kolibri.tokenizer import bert_tokenizer as tokenization
import six


import unittest


class TokenizationTest(unittest.TestCase):

  def test_full_tokenizer(self):
    vocab_tokens = [
        "[UNK]", "[CLS]", "[SEP]", "want", "##want", "##ed", "wa", "un", "runn",
        "##ing", ","
    ]
    with tempfile.NamedTemporaryFile(delete=False) as vocab_writer:
      if six.PY2:
        vocab_writer.write("".join([x + "\n" for x in vocab_tokens]))
      else:
        vocab_writer.write("".join(
            [x + "\n" for x in vocab_tokens]).encode("utf-8"))

      vocab_file = vocab_writer.name

    tokenizer = tokenization.FullTokenizer(vocab_file)
    os.unlink(vocab_file)

    tokens = tokenizer.tokenize(u"UNwant\u00E9d,running")
    self.assertListEqual(tokens, ["un", "##want", "##ed", ",", "runn", "##ing"])

    self.assertListEqual(
        tokenizer.convert_tokens_to_ids(tokens), [7, 4, 5, 10, 8, 9])

  def test_chinese(self):
    tokenizer = tokenization.WordTokenizer({'whitespace':True})

    self.assertListEqual(
        tokenizer.tokenize(u"ah\u535A\u63A8zz"),
        [u"ah", u"\u535A", u"\u63A8", u"zz"])

  def test_wordpiece_tokenizer(self):
    vocab_tokens = [
        "[UNK]", "[CLS]", "[SEP]", "want", "##want", "##ed", "wa", "un", "runn",
        "##ing"
    ]

    vocab = {}
    for (i, token) in enumerate(vocab_tokens):
      vocab[token] = i
    tokenizer = tokenization.WordpieceTokenizer({'vocabulary':vocab})

    self.assertListEqual(tokenizer.tokenize(""), [])

    self.assertListEqual(
        tokenizer.tokenize("unwanted running"),
        ["un", "##want", "##ed", "runn", "##ing"])

    self.assertListEqual(
        tokenizer.tokenize("unwantedX running"), ["[UNK]", "runn", "##ing"])

  def test_convert_tokens_to_ids(self):
    vocab_tokens = [
        "[UNK]", "[CLS]", "[SEP]", "want", "##want", "##ed", "wa", "un", "runn",
        "##ing"
    ]

    vocab = {}
    for (i, token) in enumerate(vocab_tokens):
      vocab[token] = i

    self.assertListEqual(
        tokenization.convert_tokens_to_ids(
            vocab, ["un", "##want", "##ed", "runn", "##ing"]), [7, 4, 5, 8, 9])

