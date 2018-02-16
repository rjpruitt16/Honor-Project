import json
import os
import operator

def GetNameOfJSON():
    NewsToFilesDict = {}
    for filename in os.listdir("."):
        if filename.endswith(".json"):
            if filename.split("_")[0] not in NewsToFilesDict.keys():
                NewsToFilesDict[filename.split("_")[0]] = [filename]
            else:
                NewsToFilesDict[filename.split("_")[0]].append(filename)
    return NewsToFilesDict

def ScoreKeywordPolarity(keywordDict, jdata):
    for word in jdata["keywords"]:
        if word not in keywordDict.keys():
            keywordDict[word] = 0
        if jdata["polarity"] < -.3:
            print("negative article")
            keywordDict[word] = keywordDict[word] - 1
        elif jdata["polarity"] > .3:
            keywordDict[word] = keywordDict[word] + 1

def LoadAndGetJSONS(jfiles):
    jsons = []
    for filename in jfiles:
        try:
            with open(filename) as json_data:
                jsons = jsons + json.load(json_data)
        except json.decoder.JSONDecodeError:
            print(filename + ": unable to load")
    return jsons

def GetPolarityOfKeyword(jsons):
    keywordDict = {}
    for jdata in jsons:
        ScoreKeywordPolarity(keywordDict, jdata)
    return sorted(keywordDict.items(), key=operator.itemgetter(1))

def GetPositveOrNegativeArticles(jsons, positive=True):
    articles = []
    for jdata in jsons:
        if positive:
            if jdata["polarity"] < 0:
                articles.append(jdata)
        else:
            if jdata["polarity"] > 0:
                articles.append(jdata)
    return articles

def GetAveragePolarity(jsons, sentiment="polarity"):
    total = 0
    for jdata in jsons:
        total+=jdata[sentiment]
    return total/len(jsons)

def PrintAnalysis():
    '''
    For each newsoutlet, five most positve keywords, and five
    least favorite keywords. Print the amount of positve negative articles
    in general, and the positive to negative with rave politics
    '''
    NewsToFilesDict = GetNameOfJSON()
    for key in NewsToFilesDict.keys():
        jsons = LoadAndGetJSONS(NewsToFilesDict[key])
        print(key, " Total Article: ", len(jsons))
        print(key, " Average Polarity: ", GetAveragePolarity(jsons))
        print(key, " Average Subjectivity: ", GetAveragePolarity(jsons, "subjectivity"))
        keywords = GetPolarityOfKeyword(jsons)
        print(key, " Top 5 positive words: ", str(keywords[:5]))
        print(key, " Top 5 negative words: ", str(keywords[len(keywords)-5:]))

if __name__ ==  "__main__":
    PrintAnalysis()
