import json
import os
import operator

def GetNameOfJSON():
    categoryToFilesDict = {}
    categoryToFilesDict["article"] = []
    categoryToFilesDict["race"] = []
    for filename in os.listdir("."):
        if filename.endswith(".json"):
            if filename.split("_")[0] not in categoryToFilesDict.keys():
                categoryToFilesDict[filename.split("_")[0]] = [filename]
            if filename.split("_")[1] == "article":
                categoryToFilesDict["article"].append(filename)
            if filename.split("_")[1] == "race":
                categoryToFilesDict["race"].append(filename)
            categoryToFilesDict[filename.split("_")[0]].append(filename)
    return categoryToFilesDict

def ScoreKeywordPolarity(keywordDict, jdata):
        for word in jdata["keywords"]:
            if word not in keywordDict.keys():
                keywordDict[word] = 0
            if jdata["polarity"] < -.3:
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

def GetAveragePolarityOrSubjectivity(jsons, key="polarity"):
    average = 0
    for jdata in jsons:
        average+=jdata[key]
    return average/len(jsons)

def PrintAnalysis():
    '''
    For each newsoutlet, five most positve keywords, and five
    least favorite keywords. Print the amount of positve negative articles
    in general, and the positive to negative with rave politics
    '''
    CategoryDict = GetNameOfJSON()
    for category in CategoryDict.keys():
        jsons = LoadAndGetJSONS(CategoryDict[category])
        print(category, "Articles: ", len(jsons))
        print(category, "Average Polarity ", GetAveragePolarityOrSubjectivity(jsons))
        print(category, "Average Subjectivity", GetAveragePolarityOrSubjectivity(jsons, "subjectivity"))
        keywords = GetPolarityOfKeyword(jsons)
        print(category, "Top Five Positive Keywords ", keywords[len(keywords)-5:])
        print(category, "Top Five Negative Keywords ", keywords[:5])


if __name__ ==  "__main__":
    PrintAnalysis()
