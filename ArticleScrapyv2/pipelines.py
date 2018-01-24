# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from newspaper import Article
from textblob import TextBlob

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
        return item

class SentimentPipeline(object):
    def process_item(self, item, spider):
        blob = TextBlob(item["text"])
        item["sentiment"] = blob.sentiment.polarity
        return item
