from wildgram import wildgram
import Levenshtein as lev
import re
errorMessage = "documents needs to be a list of dictionaries in the form {text: 'text'}"

def isTheSameWord(word1, word2, threshold=0.75):
    test=word1.lower()
    test2 = word2.lower()
    if test == test2:
        return True
    if len(test) <= 3:
        return False
    if len(test2) <= 3:
        return False
    if test[0] != test2[0]:
        return False
    test, test2 = normalizeWords(test, test2)
    if lev.ratio(test, test2) < threshold:
        return False
    return True

def normalizeWords(test, test2):
    if len(test) > len(test2)*2:
        return test, test2
    if len(test)*2 < len(test2):
        return test, test2
    if len(test) < len(test2):
        return test, test2[:len(test)]
    return test[:len(test2)], test2

def stripWord(word):
    ret = word.lower()
    for sb in ["ing$", "ness$", "tion$", "sion$"]:
        ret = re.sub(sb, "", ret)
    return ret

def getTokenLists(textarray):
    if not isinstance(textarray, list):
        raise Exception(errorMessage)
    ret = []
    for i in range(len(textarray)):
        app = []
        try:
            text = textarray[i]["text"]
        except:
            raise Exception(errorMessage)
        tokens = wildgram(text)
        docID = i
        if "docID" in textarray[i]:
            docID = textarray[i]["docID"]
        for tok in tokens:
            tok["docID"] = docID
            app.append(tok)
        ret.append(app)
    return ret


def getPhrases(tokenlists):
    frequency = {}
    for i in range(len(tokenlists)):
        tokens = tokenlists[i]
        for token in tokens:
            if token["tokenType"] == "noise":
                continue
            if token["tokenType"] != "token":
                if token["tokenType"] not in frequency:
                    frequency[token["tokenType"]] = []
                frequency[token["tokenType"]].append(token)
                continue
            if token["token"] not in frequency:
                frequency[token["token"]] = []
            frequency[token["token"]].append(token)

    phrases = sorted(frequency.items(), key=lambda item: len(item[1]), reverse=True)
    return phrases

def groupPhrasesBySimilarity(phrases, threshold=0.75):
    newdata = []

    while len(phrases) != 0:
        print("Unique keywords left...", len(phrases))
        key = phrases.pop(0)
        group = {"phrases": [key[0]], "tokens": key[1]}
        found = False
        indexes = []
        for i in range(len(phrases)):
            if isTheSameWord(key[0], phrases[i][0], threshold):
                group["phrases"].append(phrases[i][0])
                group["tokens"] = group["tokens"] + phrases[i][1]
                continue
            indexes.append(i)
        dat = []
        for index in indexes:
            dat.append(phrases[index])
        phrases = dat
        newdata.append(group)

    return newdata


def synopsis(documents, threshold=0.75):
    if not isinstance(documents, list):
        raise Exception(errorMessage)
    tokenlists = getTokenLists(documents)
    phrases = getPhrases(tokenlists)
    keywords = groupPhrasesBySimilarity(phrases, threshold)
    return keywords

# topics in the form {token:" ", unit: " ", value: " ", frequency: 1}
def topicfinder(doc, topics, threshold=0.75):
    tokens = wildgram(doc["text"])
    topics = sorted(topics, key=lambda x: x["frequency"], reverse=True)
    ret = []
    for token in tokens:
        bestScore = 0
        bestMatch = ""
        token["topic"] = {}
        for topic in topics:
            if token["tokenType"] != "token":
                break
            if isTheSameWord(token["token"],topic["token"], threshold):
                token["topic"] = topic
                break
        ret.append(token)
    return ret
