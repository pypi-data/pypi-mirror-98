import collections
import re
import tensorflow as tf
from kolibri.tokenizer.tokenizer import Tokenizer
from kolibri.tokenizer import WordTokenizer
#ToDo Consider removing
def validate_case_matches_checkpoint(do_lower_case, init_checkpoint):
  """Checks whether the casing config is consistent with the checkpoint name."""

  # The casing has to be passed in by the user and there is no explicit check
  # as to whether it matches the checkpoint. The casing information probably
  # should have been stored in the bert_config.json file, but it's not, so
  # we have to heuristically detect it to validate.

  if not init_checkpoint:
    return

  m = re.match("^.*?([A-Za-z0-9_-]+)/bert_model.ckpt", init_checkpoint)
  if m is None:
    return

  model_name = m.group(1)

  lower_models = [
    "uncased_L-24_H-1024_A-16", "uncased_L-12_H-768_A-12",
    "multilingual_L-12_H-768_A-12", "chinese_L-12_H-768_A-12"
  ]

  cased_models = [
    "cased_L-12_H-768_A-12", "cased_L-24_H-1024_A-16",
    "multi_cased_L-12_H-768_A-12"
  ]

  is_bad_config = False
  if model_name in lower_models and not do_lower_case:
    is_bad_config = True
    actual_flag = "False"
    case_name = "lowercased"
    opposite_flag = "True"

  if model_name in cased_models and do_lower_case:
    is_bad_config = True
    actual_flag = "True"
    case_name = "cased"
    opposite_flag = "False"

  if is_bad_config:
    raise ValueError(
      "You passed in `--do_lower_case=%s` with `--init_checkpoint=%s`. "
      "However, `%s` seems to be a %s model, so you "
      "should pass in `--do_lower_case=%s` so that the fine-tuning matches "
      "how the model was pre-training. If this error is wrong, please "
      "just comment out this check." % (actual_flag, init_checkpoint,
                                        model_name, case_name, opposite_flag))


def load_vocab(vocab_file):
  """Loads a vocabulary file into a dictionary."""
  vocab = collections.OrderedDict()
  index = 0
  with tf.io.gfile.GFile(vocab_file, "r") as reader:
    while True:
      token = reader.readline()
      if not token:
        break
      token = token.strip()
      vocab[token] = index
      index += 1
  return vocab


def convert_by_vocab(vocab, items):
  """Converts a sequence of [tokens|ids] using the vocab."""
  output = []
  for item in items:
    output.append(vocab[item])
  return output


def convert_tokens_to_ids(vocab, tokens):
  return convert_by_vocab(vocab, tokens)


def convert_ids_to_tokens(inv_vocab, ids):
  return convert_by_vocab(inv_vocab, ids)


class FullTokenizer(Tokenizer):
  """Runs end-to-end tokenziation."""

  def __init__(self, vocab_file, do_lower_case=True):
    self.vocab = load_vocab(vocab_file)
    self.inv_vocab = {v: k for k, v in self.vocab.items()}
    self.basic_tokenizer = WordTokenizer({'do_lower_case':do_lower_case})
    self.wordpiece_tokenizer = WordpieceTokenizer({'vocabulary':self.vocab})

  def tokenize(self, text):
    split_tokens = []
    for token in self.basic_tokenizer.tokenize(text):
      for sub_token in self.wordpiece_tokenizer.tokenize(token):
        split_tokens.append(sub_token)

    return split_tokens

  def convert_tokens_to_ids(self, tokens):
    return convert_by_vocab(self.vocab, tokens)

  def convert_ids_to_tokens(self, ids):
    return convert_by_vocab(self.inv_vocab, ids)

class WordpieceTokenizer(Tokenizer):
  """Runs WordPiece tokenziation."""
  name = "wordpiece_tokenizer"
  defaults = {
    'whitespace': True,
    'max_input_chars_per_word':200,
    'unk_token': "[UNK]",
    'vocabulary': None
  }

  def __init__(self, config={}):
    self.defaults.update(super(WordpieceTokenizer, self).defaults)
    super().__init__(config)
    self.vocab = self.component_config['vocabulary']
    self.unk_token = self.component_config['unk_token']
    self.max_input_chars_per_word = self.component_config['max_input_chars_per_word']
    self.whitespace_tokenizer=WordTokenizer(self.component_config)

  def tokenize(self, text):
    """Tokenizes a piece of text into its word pieces.

    This uses a greedy longest-match-first algorithm to perform tokenization
    using the given vocabulary.

    For example:
      input = "unaffable"
      output = ["un", "##aff", "##able"]

    Args:
      text: A single token or whitespace separated tokens. This should have
        already been passed through `BasicTokenizer.

    Returns:
      A list of wordpiece tokens.
    """

    output_tokens = []
    for token in self.whitespace_tokenizer.tokenize(text):
      chars = list(token)
      if len(chars) > self.max_input_chars_per_word:
        output_tokens.append(self.unk_token)
        continue

      is_bad = False
      start = 0
      sub_tokens = []
      while start < len(chars):
        end = len(chars)
        cur_substr = None
        while start < end:
          substr = "".join(chars[start:end])
          if start > 0:
            substr = "##" + substr
          if substr in self.vocab:
            cur_substr = substr
            break
          end -= 1
        if cur_substr is None:
          is_bad = True
          break
        sub_tokens.append(cur_substr)
        start = end

      if is_bad:
        output_tokens.append(self.unk_token)
      else:
        output_tokens.extend(sub_tokens)
    return output_tokens

