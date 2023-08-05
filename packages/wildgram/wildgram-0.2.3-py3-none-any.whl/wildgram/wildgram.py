import regex as re
import string
import os
import numpy as np

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
"you(\'?)re", "you(\'?)ve", "you(\'?)ll", "you(\'?)d", 'your', 'yours', 'yourself', 'yourselves',
'he', 'him', 'his', 'himself', 'she', "she(\'?)s", 'her', 'hers', 'herself', 'it',
"it(\'?)s", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',
'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very','can', 'just',
'should', "should(\'?)ve", 'now']

punc = "!|\"|\#|\$|\%|\&|\'|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~"

TOPICWORDS = [{"token": "no", "tokenType": "negation"},{"token": "negative", "tokenType": "negation"},
{"token": "not", "tokenType": "negation"},{"token": "nor", "tokenType": "negation"},
{"token": "ain(\'?)t", "tokenType": "negation"},{"token": "aren(\'?)t", "tokenType": "negation"},
{"token": "couldn(\'?)t", "tokenType": "negation"},{"token": "didn(\'?)t", "tokenType": "negation"},
{"token": "doesn(\'?)t", "tokenType": "negation"},{"token": "hadn(\'?)t", "tokenType": "negation"},
{"token": "hasn(\'?)t", "tokenType": "negation"},{"token": "haven(\'?)t", "tokenType": "negation"},
{"token": "isn(\'?)t", "tokenType": "negation"},{"token": "mightn(\'?)t", "tokenType": "negation"},
{"token": "mustn(\'?)t", "tokenType": "negation"},{"token": "needn(\'?)t", "tokenType": "negation"},
{"token": "shan(\'?)t", "tokenType": "negation"},{"token": "shouldn(\'?)t", "tokenType": "negation"},
{"token": "wasn(\'?)t", "tokenType": "negation"},{"token": "weren(\'?)t", "tokenType": "negation"},
{"token": "won(\'?)t", "tokenType": "negation"},{"token": "don(\'?)t", "tokenType": "negation"},
{"token": "wouldn(\'?)t", "tokenType": "negation"},{"token": "denies", "tokenType": "negation"},
{"token": "denied", "tokenType": "negation"},{"token": "\d+\.\d+", "tokenType": "numeric"},
{"token": "\d+", "tokenType": "numeric"},{"token": "one", "tokenType": "numeric"},
{"token": "two", "tokenType": "numeric"},{"token": "three", "tokenType": "numeric"},
{"token": "four", "tokenType": "numeric"},{"token": "will", "tokenType": "future"},
"reveal", "revealed","(\w("+punc+")?){1,2}\w"]

JOINERWORDS = ["of", "in", "to", "on","than","at"]

def pullOutJoiners(merged, text, joinerwords):
    if len(joinerwords) == 0:
        return []
    ret = []
    joiners = "|".join(["(\s|^)"+stop+"(\s|$)" for stop in joinerwords])
    for i in range(len(merged)):
        match = merged[i]
        start = 0
        end = len(text)
        if not re.search("("+joiners+")", text[match[0]:match[1]]):
            continue
        if i > 0:
            start = merged[i-1][0]
        if i < len(merged)-1:
            end = merged[i+1][1]
        if start != merged[i][0] and end != merged[i][1]:
            ret.append((start,end, 'token'))
    return ret

def pullOutNoise(pattern, text, leftovers):
    matches = [(match.start(), match.end(), "noise") for match in pattern.finditer(text.lower(),overlapped=True)]
    matches = sorted(matches, key=lambda x: (x[0], x[1]))
    prev = 0
    noise = []
    for i in range(len(matches)-1):
        if matches[i][1] < matches[i+1][0]:
            leftovers, noise = checkAndRemoveLeftovers(leftovers,matches[prev][0],matches[i][1],noise,"noise" )
            prev = i+1
    if prev < len(matches):
        leftovers, noise = checkAndRemoveLeftovers(leftovers,matches[prev][0],matches[-1][1],noise,"noise" )
    return noise, leftovers

def pullOutTokens(indexes):
    indexes = list(indexes)
    if len(indexes) == 0:
        return []
    indexes = sorted(indexes)
    prev = indexes[0]
    ret = []
    for i in range(len(indexes)-1):
        if indexes[i]+1 != indexes[i+1]:
            ret.append((prev,indexes[i]+1, "token"))
            prev = indexes[i+1]
    ret.append((prev, indexes[-1]+1,"token"))
    return ret

def pullOutTopics(topics, text, leftovers, noise):
    ret = []
    punc = [x for x in string.punctuation]
    for topic in topics:
        token = topic
        tokenType = "token"
        if isinstance(topic, dict):
            token = topic["token"]
            tokenType = topic["tokenType"]
        for match in re.finditer("(\s|^)"+token+"(\s|"+"|\\".join(punc)+"\s|$)", text.lower(),overlapped=True):
            prev = 0
            for top in re.finditer(token, text[match.start():match.end()].lower()):
                if top.start() != prev:
                    leftovers,noise =checkAndRemoveLeftovers(leftovers, prev+ match.start(), top.start()+match.start(), noise, "noise")
                leftovers,ret = checkAndRemoveLeftovers(leftovers, top.start() + match.start(), top.end()+match.start(), ret, tokenType)
                prev = top.end()
            if prev != (match.end()-match.start()):
                leftovers,noise =checkAndRemoveLeftovers(leftovers, prev+ match.start(), match.end(), noise, "noise")

    return ret, leftovers,noise

def checkAndRemoveLeftovers(leftovers, start, end, ret, tokenType):
    r = range(start, end)
    if len(leftovers.intersection(set(r))) == len(r):
        ret.append((start, end, tokenType))
    leftovers = leftovers.difference(r)
    return leftovers, ret


def figureOutRegex(stopwords, size=2):
    punc = [x for x in string.punctuation]
    regex = '[\s' + "|\\".join(punc)+ ']{'+ str(size)+',}|\n'
    stops = "|".join(["(\s|^)"+stop+"(\s|$)" for stop in stopwords])
    if len(stops) != 0:
        regex = stops+'|'+regex
    prog = re.compile("("+regex+")")
    return prog

def filterAndSort(matches):
    ret = {}
    for match in matches:
        if match[0] not in ret:
            ret[match[0]] = {}
        if match[1] not in ret[match[0]]:
            ret[match[0]][match[1]] = match[2]
            continue
        if match[2] == "token":
            continue
        ret[match[0]][match[1]] = match[2]
    res = []
    for key in ret:
        for k in ret[key]:
            res.append((key, k, ret[key][k]))

    return sorted(res,key=lambda x: (x[0], x[1]) )


def getNoiseProfileLine(tokens, i):
    if i == -1:
        return ""
    line = tokens[i]["token"]
    if line.find(":") != -1:
        line = line[line.find(":")+1:]
    done = False
    for j in range(i+1, len(tokens)):
        if not done and tokens[j]["tokenType"] != "noise":
            line = line + "<TOKEN>"
        if tokens[j]["tokenType"] == "noise":
            if done and "\n" not in tokens[j]["token"]:
                continue
            done = True
            line = line + tokens[j]["token"]
            if "\n" in tokens[j]["token"]:
                return line
    return line

def assignParents(tokens):
    commonorder = [";", "\. ", "\n",":\n", "\|", "-", ": "]

    order = [(":\n",["\n", "root"]), ("\n", [":\n", "root"]),
    ("\. ", ["\n", ":\n"]), (";", ["\. ", "\n",":\n"]), (": ", ["\n", "\. ", ";"]),
    (",", commonorder), ("-",commonorder), ("\|",commonorder),
    ("(\s|^)and(\s|^)", commonorder), ("(\s|^)or(\s|^)",commonorder),
    ("(\s|^)by(\s|^)", commonorder), ("(\s|^)in(\s|^)",commonorder),
    ("(\s|^)on(\s|^)", commonorder), ("(\s|^)was(\s|^)",commonorder),
    ("(\s|^)is(\s|^)", commonorder), ("(\s|^)but(\s|^)", commonorder)]

    lastKnown = {}
    lastKnownKeys = [ord[0] for ord in order] + ["root", "newLineAny"]
    for key in lastKnownKeys:
        lastKnown[key] = -1

    for i in range(len(tokens)):
        if tokens[i]["tokenType"] != "noise":
            prev = np.amax(np.array(list(lastKnown.values())))
            tokens[i]["parent"] = prev
            continue
        snip = tokens[i]["token"]
        done = False
        for ord in order:
            if re.search(ord[0], tokens[i]["token"].lower()):
                prev = np.amax(np.array(list([lastKnown[r] for r in ord[1]])))
                ## if its a plain new line, determining if it should return to root.
                if "\n" in snip and ":" not in snip:
                    line = getNoiseProfileLine(tokens, i)
                    line2 = getNoiseProfileLine(tokens, lastKnown["newLineAny"])
                    if line.strip() != line2.strip():
                        prev = -1
                if "\n" in snip:
                    lastKnown["newLineAny"] = i
                tokens[i]["parent"] = prev
                lastKnown[ord[0]] = i
                done = True
                break
        if done:
            continue
        prev = np.amax(np.array(list(lastKnown.values())))
        tokens[i]["parent"] = prev
    return tokens

def createRangesFromProg(prog, topics, text, joinerwords, noise=[],ranges=[],leftover=[]):
    newnoise, leftover = pullOutNoise(prog, text, leftover)
    topics, leftover, newnoise = pullOutTopics(topics, text, leftover, newnoise)
    tokens = pullOutTokens(leftover)
    merged = sorted(noise + tokens + topics + newnoise, key=lambda x: (x[0], x[1]))
    ranges = ranges + pullOutJoiners(merged, text, joinerwords) + tokens + topics
    noise = newnoise + noise
    return noise, ranges, leftover

def createToken(start, end, type, text, index):
    return {"startIndex": start, "endIndex":end, "token":text[start:end], "tokenType": type, "index": index}

def wildgram(text, stopwords=STOPWORDS, topicwords=TOPICWORDS, include1gram=True, joinerwords=JOINERWORDS, returnNoise=True, includeParent=True):
    # corner case for inappropriate input
    if not isinstance(text, str):
        raise Exception("What you just gave wildgram isn't a string, mate.")
    if not returnNoise and includeParent:
        raise Exception("Parent is based on noise index, you need to set returnNoise to True in order to have includeParent be True. Otherwise set both to False.")

    prog = figureOutRegex(stopwords)
    ranges = []
    noise = []
    leftover = set(range(len(text))) # what characters haven't been marked previously
    noise, ranges, leftover = createRangesFromProg(prog, topicwords, text, joinerwords, noise,ranges, leftover)

    if include1gram:
        prog1gram = figureOutRegex(stopwords, 1)
        noise, ranges, leftover = createRangesFromProg(prog1gram, [], text, joinerwords, noise,ranges, leftover)

    if returnNoise:
        ranges = ranges + noise

    ranges =filterAndSort(ranges)
    ret = []
    for r in ranges:
        app = createToken(r[0], r[1], r[2], text,len(ret))
        ret.append(app)

    if includeParent:
        ret = assignParents(ret)

    return ret
