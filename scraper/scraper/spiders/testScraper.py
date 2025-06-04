import scrapy
from scraper.services.selector_service import SelectorService


class TestscraperSpider(scrapy.Spider):
    name = "testScraper"
    allowed_domains = ["vita-gesundheit.de"]
    start_urls = ["https://vita-gesundheit.de/leistungen/"]

    def __init__(self, *args, **kwargs):
        self.selector_service = SelectorService()
        super().__init__(*args, **kwargs)
        

    def parse(self, response):
        title = self.selector_service.get_title(response)
        body = self.selector_service.get_body_content(response)
        articles = self.selector_service.get_articles(response)
        blog_posts = self.selector_service.get_blog_posts(response) 
        list_items = self.selector_service.get_list_items(response)
        yield {
           'title' : title,
           'body' : body,
           'articles' : articles,
           'blog_posts' : blog_posts,
           'list_items' : list_items
        }
    
