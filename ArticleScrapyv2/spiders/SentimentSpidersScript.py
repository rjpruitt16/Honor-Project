#!/usr/bin/python3
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl("NYT_race_politic")
process.crawl("NYT_article")
process.crawl("NPR_race_politic")
process.crawl("NPR_article")
process.crawl("Root_article")
print('~~~~~~~~~~~~ Processing is going to be started ~~~~~~~~~~')
process.start()
print('~~~~~~~~~~~~ Processing ended ~~~~~~~~~~')
process.stop()
