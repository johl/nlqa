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
$ python nlqa.py --question="Was ist die Hauptstadt von Angola?" --language=de
$ Luanda
$ python nlqa.py --question="What is Estonia's national currency?" --language=en
$ Euro
```
