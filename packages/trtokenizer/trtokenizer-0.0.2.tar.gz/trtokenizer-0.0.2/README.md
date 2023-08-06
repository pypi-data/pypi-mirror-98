# TrTokenizer 🇹🇷

[![Python](https://img.shields.io/pypi/pyversions/tensorflow.svg?style=plastic)](https://badge.fury.io/py/trtokenizer)
[![PyPI](https://badge.fury.io/py/tensorflow.svg)](https://badge.fury.io/py/trtokenizer)

TrTokenizer is a complete solution for Turkish sentence and word tokenization with extensively-covering language
conventions. If you think that Natural language models always need robust, fast, and accurate tokenizers, be sure that you are at the
the right place now. Sentence tokenization approach uses non-prefix keyword given in 'tr_non_suffixes' file. This file can be expanded if
required, for developer convenience lines start with # symbol are evaluated as comments.
Designed regular expressions are pre-compiled to speed-up the performance.

## Install

```sh
pip install trtokenizer
```

## Usage

```sh
from TrTokenizer import SentenceTokenize, WordTokenize

sentence_tokenizer_object = SentenceTokenize()  # during object creation regexes are compiled only at once

sentence_tokenizer_object.tokenize(<given paragraph as string>)

word_tokenizer_object = WordTokenize()  # # during object creation regexes are compiled only at once

word_tokenizer_object.tokenize(<given sentence as string>)

```

## To-do

- Usage examples (Done)
- Cython C-API for performance (Done, build/tr_tokenizer.c)
- Release platform specific shared dynamic libraries (Done, build/tr_tokenizer.cpython-38-x86_64-linux-gnu.so, only for
  Debian Linux with gcc compiler)
- Limitations
- Prepare a simple guide for contribution

## Resources

* [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/)
* [Bogazici University CMPE-561](https://www.cmpe.boun.edu.tr/tr/courses/cmpe561)