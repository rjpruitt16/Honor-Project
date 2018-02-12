# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem, CloseSpider
from newspaper import Article
from textblob import TextBlob
import json
import logging
from datetime import datetime

class Articlescrapyv2Pipeline(object):
    def process_item(self, item, spider):
        return item

class DropNullItemPipeline(object):
    def process_item(self, item, spider):
        if not item["url"] or not item["title"]:
            raise DropItem("Null item exception")
        return item

class NewspaperTextExtractionPipeline(object):
    def process_item(self, item, spider):
        article = Article(item["url"])
        article.download()
        article.parse()
        article.nlp()
        item["text"] = article.text
        item["keywords"] = article.keywords
        logging.log(logging.INFO, "Item text:: \n" + item["text"] + "\n Item keyword:: \n" + str(item["keywords"]))
        return item

class SentimentPipeline(object):
    def process_item(self, item, spider):
        blob = TextBlob(item["text"])
        item["polarity"] = blob.sentiment.polarity
        item["subjectivity"] = blob.sentiment.subjectivity
        return item

class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.path = "Data/"
        self.filename = spider.name+"_"+str(datetime.now()).split(" ")[0]+".json"
        self.jfile = open(self.path+self.filename, 'w')
        self.lines = []
        self.jfile.write("[\n")

    def close_spider(self, spider):
        for line in self.lines[:len(self.lines)-1]:
            self.jfile.write(line + ",\n")
        self.jfile.write(self.lines[-1]+ "\n")
        self.jfile.write("]")
        self.jfile.close()

    def process_item(self, item, spider):
        self.lines.append(json.dumps(dict(item)))
        return item
