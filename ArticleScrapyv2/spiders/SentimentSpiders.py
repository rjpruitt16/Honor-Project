from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from ArticleScrapyv2.items import NewsArticleItem
from scrapy.crawler import CrawlerProcess

class NYTSentimentSpider(CrawlSpider):
    name = "NYT"
    allowed_domains = ["nytimes.com"]
    start_urls = [
        "https://www.nytimes.com/",
        "https://www.nytimes.com/section/politics",
        "https://www.nytimes.com/topic/subject/race-and-ethnicity"
    ]

    rules = (
       Rule(LinkExtractor(allow=r"politics"), callback="parse_item", follow=True),
       Rule(LinkExtractor(allow=r"race"), callback="parse_item", follow=True),
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

class CNNSentimentSpider(CrawlSpider):
    name = "CNN"
    allowed_domains = ["cnn.com"]
    start_urls = [
        "https://www.cnn.com/",
        "https://www.cnn.com/politics",
        "https://www.nytimes.com/topic/subject/race-and-ethnicity"
    ]

    rules = (
       Rule(LinkExtractor(allow=r"politics"), callback="parse_item", follow=True),
       Rule(LinkExtractor(allow=r"race"), callback="parse_item", follow=True),
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

class NPRSentimentSpider(CrawlSpider):
    name = "NPR"
    allowed_domains = ["npr.org"]
    start_urls = [
        "https://www.npr.org/",
        "https://www.npr.org/sections/politics/",
        "https://www.npr.org/sections/race/"
    ]

    rules = (
       Rule(LinkExtractor(allow=r"politics"), callback="parse_item", follow=True),
       Rule(LinkExtractor(allow=r"race"), callback="parse_item", follow=True),
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


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(NYTSentimentSpider)
process.start()
