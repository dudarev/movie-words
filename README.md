Sort words in subtitles file based on [TFIDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) or count.

When sorting based on TFIDF, words that are less common in other movies subtitles
and more frequent in specified file come first.

Words frequency in other subtitles is based on

https://github.com/hermitdave/FrequencyWords/

Usage:

```
pip install -r requirements.txt
make en_full.txt
python words.py [-h] [-s {t,tfidf,c,count}] -i INPUT
```
