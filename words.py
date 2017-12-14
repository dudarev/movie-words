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

from collections import Counter
import os
import string
import sys

import srt


FREQUENCY_FILE = 'en_full.txt'


def main(filename):

    # get frequency words count
    document_frequency = {}
    if not os.path.exists(FREQUENCY_FILE):
        print("make en_full.txt (see Makefile)")
        sys.exit()
    with open(FREQUENCY_FILE) as f:
        for line in f:
            w, count = line.split()
            document_frequency[w] = int(count)

    # count of words in subtitles file
    counter = Counter()
    with open(filename) as f:
        subtitles = srt.parse(f.read())
        for s in subtitles:
            content = s.content.translate(
                str.maketrans(string.punctuation, ' ' * len(string.punctuation))).translate(
                str.maketrans('0123456789', ' ' * 10)).lower()
            counter.update(content.split())

    tfidf = Counter()
    for w in counter:
        tfidf.update({w: counter[w] / document_frequency.get(w, 1)})

    # output to stdout
    for w in tfidf.most_common():
        print("{} {}".format(w[0], counter[w[0]]))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Specify subtitles file")
        sys.exit()
    filename = sys.argv[1]
    main(filename)
