from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from ArticleScrapyv2.items import NewsArticleItem

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
