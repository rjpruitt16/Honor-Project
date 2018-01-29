# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from newspaper import Article
from textblob import TextBlob
import json
import logging

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
        logging.log(logging.INFO, "Item text:: \n" + item["text"] + "\n Item keyword:: \n" + item["keywords"])
        return item

class SentimentPipeline(object):
    def process_item(self, item, spider):
        blob = TextBlob(item["text"])
        item["sentiment"] = blob.sentiment.polarity
        logging.log(logging.INFO, "Item Sentiment:: \n" + item["sentiment"])
        return item

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('ArticleSamples.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        logging.log(logging.INFO, "Succesful write")
        return item
