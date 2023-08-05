Topic Finder works in a three part process.

To install:
```python
pip3 install topicfinder
```

1. tokenizing the document set. This applies the default wildgram analysis to tokenize
the document set. documents must be in the structure below, a list of dictionaries.
docID is optional as a parameter (if not included, the id is the index in the array).


```python
from topicfinder import getTokenLists
ret = getTokenLists([{"text": "boo", "docID": "1"}])
```

2. sorting the entire tokenset by the unique tokens and their frequencies.

```python
from topicfinder import getTokenLists, getPhrases
ret = getPhrases(getTokenLists([{"text": "boo", "docID": "1"}]))
```

3. grouping the phrases by similarity, with some lemmatization and fuzzy matching. It considers any word or lemmatized word less than 3 letters impossible to group. You can also set a threshold similarity (1.0 is an exact match). Default is (for now) 0.75. If you have a custom tokenType (e.g. not "token" or "noise") generated from wildgram it will group the tokens on that. For example, with default settings
in synopsis it automatically deals with grouping numbers together and negations.


```python
from topicfinder import getTokenLists, getPhrases, groupPhrasesBySimilarity
ret = groupPhrasesBySimilarity(getPhrases(getTokenLists([{"text": "boo", "docID": "1"}])))

ret = groupPhrasesBySimilarity(getPhrases(getTokenLists([{"text": "boo", "docID": "1"}])),threshold=0.8)

## ret is a sorted list (descending order) of the following style of dictionaries
## {"phrases": [#list of phrases#], "tokens": [##list of unique tokens from the documents]}
## descending order by the size of the tokens array
```
you can also just call:
```python
from topicfinder import synopsis
ret = synopsis([{"text": "boo", "docID": "1"}], threshold=0.8)

```
this will do steps 1-3 in one go. I split it up because with medical things, sometimes
you need to run and store the data off given the size of the dataset or do a map reduce situation
or be extra careful about PHI.

For anyone worrying about PHI -- aint none of this connected to the internet. It's
all local baby. You can check the code if you need to also.

Future work will include
1. being able to apply a annotation normalization function (e.g. a set of synonyms rolling up)
2. making some default normalization functions (E.g. querying UMLS, etc.)
---- note that this might need to be connected to the internet to work.
3. dealing with acronyms and short words better
4. dealing with numbers and time durations better
