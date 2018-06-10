A prototype for a natural language question answering tool for Wikidata in Python.
Barely usable, but maybe promising.

Usage:
------
```
nlqa.py [-h] [--question QUESTION] [--language LANGUAGE]

arguments:
  -h, --help           show this help message and exit
  --question QUESTION  question to Wikidata
  --language LANGUAGE  language code of the question
```

Examples:
---------
```
$ python3 nlqa.py --question="Was ist die Hauptstadt von Angola?" --language=de
$ Luanda
$ python3 nlqa.py --question="What is Estonia's national currency?" --language=en
$ Euro
```

Installation:
-------------
Make sure you have the necessary libraries installed.

Run this:

```
$ pip3 install -r requirements.txt
```

Afterwards, install the language models for spaCy that you need.

For example, if you want to install English and German, run this:

```
$ python3 -m spacy download en
$ python3 -m spacy download de
```
