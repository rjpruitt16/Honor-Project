import json
import os

def getNameOfJSON():
    jsons = []
    for filename in os.listdir("."):
        if filename.endswith(".json") or filename.endswith(".jl"):
            jsons.append(filename)
    return jsons

def loadJSON(jsons):
    for filename in jsons:
        with open(filename) as json_data:
            data = json.load(json_data)
            print(data)


if __name__ ==  "__main__":
    jsons = getNameOfJSON()
    print(jsons)
    loadJSON([jsons[1]])
