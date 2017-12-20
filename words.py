"""
Sort words in subtitles file based on TF-IDF.

Words that are less common in other movies subtitles
and more frequent in specified file come first.

Words frequency in other subtitles is based on

https://github.com/hermitdave/FrequencyWords/

Usage:

    make en_full.txt
    python words.py data/<srt-file-name> > <out-file-name>
"""

import argparse
from collections import Counter
import os
import string
import sys
from urllib.parse import quote


FREQUENCY_FILE = 'en_full.txt'


WORD_TEMPLATE = """
## {word}
    {sentence}
[Google Translate](https://translate.google.com/#en/ru/{sentence_encoded})
[Wordnik](http://wordnik.com/words/{word})
"""


def get_word_str(word, sentence, sentence_encoded):
    return WORD_TEMPLATE.format(word=word, sentence=sentence, sentence_encoded=sentence_encoded)


def strip_punctuation(line):
    return line.translate(
        str.maketrans(string.punctuation, ' ' * len(string.punctuation))).translate(
        str.maketrans('0123456789', ' ' * 10))


def main(args):

    # get frequency words count
    document_frequency = {}
    if not os.path.exists(FREQUENCY_FILE):
        print("make en_full.txt (see Makefile)")
        sys.exit()
    with open(FREQUENCY_FILE) as f:
        for line in f:
            w, count = line.split()
            document_frequency[w] = int(count)
    
    # get words example
    examples = {}
    with open(args.input) as f:
        example = ''
        for line in f:
            if not line.strip():
                if example:
                    for w in strip_punctuation(example).split():
                        if len(examples.get(w.lower(), '')) < len(example.strip()):
                            examples[w.lower()] = example.strip().replace('\n', ' ')
                example = ''
            line_no_punctuation = strip_punctuation(line).strip()
            if line_no_punctuation:
                example += line

    # count of words in subtitles file
    counter = Counter()
    with open(args.input) as f:
        for line in f:
            content = line.translate(
                str.maketrans(string.punctuation, ' ' * len(string.punctuation))).translate(
                str.maketrans('0123456789', ' ' * 10)).lower()
            counter.update(content.split())

    tfidf = Counter()
    for w in counter:
        tfidf.update({w: counter[w] / document_frequency.get(w, 1)})

    # output to stdout
    # tfidf
    if args.sort == 't':
        for w in tfidf.most_common():
            print(get_word_str(w[0], examples[w[0]], quote(examples[w[0]])))
    # count
    else:
        for w in counter.most_common():
            print("{} {}".format(w[0], counter[w[0]]))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Specify subtitles file")
        sys.exit()

    parser = argparse.ArgumentParser(
        description='Sort words form subtitles files based on TFIDF or count.')
    parser.add_argument(
        '-s', '--sort',
        help='specify sort based on tfidf (t) or count (c)',
        default='t',
        choices=['t', 'tfidf', 'c', 'count'])
    parser.add_argument(
        '-i', '--input', help='input file name', required=True)
    args = parser.parse_args()
    main(args)
