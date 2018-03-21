import json
import os
import operator
from subprocess import call
from statistics import stdev, mean
from datetime import datetime

def GetNameOfJSON():
    categoryToFilesDict = {}
    categoryToFilesDict["article"] = []
    categoryToFilesDict["race"] = []
    for filename in os.listdir("."):
        if filename.endswith(".json") and not filename.startswith("Analysis"):
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

def LoadAndGetJSONS(jfiles, DeleteUnloadableFiles=True):
    jsons = []
    for filename in jfiles:
        try:
            with open(filename) as json_data:
                jsons = jsons + json.load(json_data)
        except json.decoder.JSONDecodeError:
            print(filename + ": unable to load")
            if DeleteUnloadableFiles:
                call(["rm", filename])
    return jsons

def RememoveDepulicateArticle(jsons):
    pass

def GetStandardDeviation(jsons):
    polarity_float_arr = []
    subjectivity_float_arr = []
    for jdata in jsons:
        polarity_float_arr.append(jdata["polarity"])
        subjectivity_float_arr.append(jdata["subjectivity"])
    return (
           (stdev(polarity_float_arr), mean(polarity_float_arr)),
           (stdev(subjectivity_float_arr), mean(subjectivity_float_arr))
    )

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

def MakeJSONAnalysisFile(jsons, filename):
    filename = filename+"_"+str(datetime.now()).split(" ")[0]+".json"
    with open(filename, 'w') as jfile:
        jfile.write("[\n")
        for jdata in jsons:
            ## TODO Find out why std_subjectivity does not write to file
            ## print(jdata["std_mode_subjectivity"])
            print(json.dump(jdata, jfile))
            jfile.write(",\n")
        #json.dump(jsons[-1], jfile)
        jfile.write("\n]")


def MakeAnalysisJSONArray():
    '''
    For each newsoutlet, five most positve keywords, and five
    least favorite keywords. Print the amount of positve negative articles
    in general, and the positive to negative with rave politics
    '''
    CategoryDict = GetNameOfJSON()
    reference_data = {
      "avgpolarity": 0.0,
      "avgsubjectivity": 0.0,
      "category": "",
      "length": 0,
      "negativekeywords": [],
      "std_mode_polarity": (),
      "std_mode_subjectivity": (),
      "positivekeywords": [],
    }
    jsons_category = []
    for category in CategoryDict.keys():
        jsons = LoadAndGetJSONS(CategoryDict[category])
        avgsentiment = GetAveragePolarityOrSubjectivity(jsons)
        avgsubjectivity = GetAveragePolarityOrSubjectivity(jsons, "subjectivity")
        keywords = GetPolarityOfKeyword(jsons)
        std_data = GetStandardDeviation(jsons)

        datadict = dict(reference_data)
        datadict["category"] = category
        datadict["avgpolarity"] = avgsentiment
        datadict["avgsubjectivity"] = avgsubjectivity
        datadict["length"] = len(jsons)
        datadict["std_mode_polarity"] = std_data[0]
        datadict["std_mode_subjectivity"] = std_data[1]
        datadict["negativekeywords"] = keywords[:15]
        datadict["positivekeywords"] = keywords[len(keywords)-15:]
        jsons_category.append(datadict)

        print(category, "Articles: ", len(jsons))
        print(category, "Average Polarity ", avgsentiment)
        print(category, "Average Subjectivity", avgsubjectivity)
        print(category, "Average standard deviation", avgsubjectivity)
        print(category, "Standard Deviation and mode Polarity", std_data[0])
        print(category, "Standard Deviation and mode Subjectity", std_data[1])
        print(category, "Top Fifteen Positive Keywords ", keywords[len(keywords)-15:])
        print(category, "Top Five Negative Keywords ", keywords[:15])


    return jsons_category

if __name__ == "__main__":
    MakeJSONAnalysisFile(MakeAnalysisJSONArray(), "AnalysisReport")
