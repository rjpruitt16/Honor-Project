from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from ArticleScrapyv2.items import NewsArticleItem
import logging

class NYTArticleSpider(CrawlSpider):
    name = "NYT_article"
    allowed_domains = ["nytimes.com"]
    start_urls = [
        "https://www.nytimes.com/"
    ]

    rules = (
       Rule(LinkExtractor(allow=(r"2018")), callback="parse_item", follow=True),
    )

    xpath_dict = {
        'articles' : '//article',
        'title' : 'div[@class="story-body"]/a/div[@class="story-meta"]/h2/text()',
        'url'   : 'div[@class="story-body"]/a/@href'
    }

    def parse_item(self, response):
        self.log("Scraping: " + response.url)

        articles = response.xpath(self.xpath_dict["articles"])

        for article in articles:
            item = NewsArticleItem()
            item["title"] = article.xpath(self.xpath_dict["title"]).extract_first()
            item["url"] = article.xpath(self.xpath_dict["url"]).extract_first()

            yield item

class CNNArticleSpider(CrawlSpider):
    name = "CNN_article"
    allowed_domains = ["cnn.com"]
    start_urls = [
        "https://www.cnn.com/",
    ]

    rules = (
       Rule(LinkExtractor(allow=(r"2018")), callback="parse_item", follow=True),
    )

    xpath_dict = {
        'articles' : '//article',
        'title' : 'div/div[@class="cd__content"]/h3/a/span/text()',
        'url'   : 'div/div[@class="cd__content"]/h3/a'
    }

    def parse_item(self, response):
        self.log("Scraping: " + response.url)

        articles = response.xpath(self.xpath_dict["articles"])

        for article in articles:
            item = NewsArticleItem()
            item["title"] = article.xpath(self.xpath_dict["title"]).extract_first()
            item["url"] = article.xpath(self.xpath_dict["url"]).extract_first()

            yield item

class NPRArticleSpider(CrawlSpider):
    ## TODO update xpath. Not Scraping properly
    name = "NPR_article"
    allowed_domains = ["npr.org"]
    start_urls = [
        "https://www.npr.org/",
    ]

    rules = (
       Rule(LinkExtractor(allow=(r"news")), callback="parse_item", follow=True),
    )

    xpath_dict = {
        'articles' : '//article',
        'title' : 'div[@class="item-info"]/h2/a/text()',
        'url'   : 'div[@class="item-info"]/h2/a/@href'
    }

    def parse_item(self, response):
        self.log("Scraping: " + response.url)

        articles = response.xpath(self.xpath_dict["articles"])

        for article in articles:
            item = NewsArticleItem()
            item["title"] = article.xpath(self.xpath_dict["title"]).extract_first()
            item["url"] = article.xpath(self.xpath_dict["url"]).extract_first()

            yield item

class TheRootSpider(CrawlSpider):
    name = "Root_article"
    allowed_domains = ["theroot.com"]
    start_urls = [
        "https://www.theroot.com/",
    ]

    rules = (
       Rule(LinkExtractor(allow=(r"-")), callback="parse_item", follow=True),
    )

    xpath_dict = {
        'articles' : '//article',
        'url'   : "header/h1/a/@href"
    }

    def parse_item(self, response):
        self.log("Scraping: " + response.url)

        articles = response.xpath(self.xpath_dict["articles"])
        logging.log(logging.INFO, "Article:: \n" + str(articles))

        for article in articles:
            item = NewsArticleItem()
            try:
              item["url"] = article.xpath(self.xpath_dict["url"]).extract_first()
              logging.log(logging.INFO, "Linked scraped: \n" + str(item["url"]))
              title = item["url"].split(".com")[-1]
              item["title"] = title[:len(title)-10]
            except AttributeError:
              print("Root Spider failed to scrape item")
            yield item
