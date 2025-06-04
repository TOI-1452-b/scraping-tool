import scrapy
import json
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from scraper.services.selector_service import SelectorService

load_dotenv()

path_to_results = os.getenv('path_to_results')

class MyscraperSpider(scrapy.Spider):
    name = "myScraper"
    custom_settings = {
        'CONCURRENT_REQUESTS': 8,  
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
        'DOWNLOAD_DELAY': 2,        
        'COOKIES_ENABLED': False,   
        'RETRY_TIMES': 0,          
    }

    def __init__(self, *args, **kwargs):
        super(MyscraperSpider, self).__init__(*args, **kwargs)
        self.selector_service = SelectorService()
        self.allowed_domains = self._get_allowed_domains()

    def _get_allowed_domains(self):
        with open(path_to_results, 'r') as f:
            data = json.load(f)
            domains = set()
            for item in data:
                parsed_uri = urlparse(item['link'])
                domain = parsed_uri.netloc
                if domain:
                    domains.add(domain)
        return list(domains)

    def start_requests(self):
        try:
            with open(path_to_results, 'r') as f:
                data = json.load(f)
                
            for item in data:
                url = item['link']
                
                
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    errback=self.errback_httpbin,
                    dont_filter=True
                )
                
        except Exception as e:
            self.logger.error(f'Error reading URLs: {e}')

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

    def errback_httpbin(self, failure):
        # Log different types of failures
        if failure.check(TimeoutError):
            self.logger.error(f'TimeoutError on {failure.request.url}')
        elif failure.check(ConnectionRefusedError):
            self.logger.error(f'ConnectionRefusedError on {failure.request.url}')
        else:
            self.logger.error(f'Other error on {failure.request.url}: {failure.value}')

    def get_links(self):
        with open(path_to_results, 'r') as f:
            data = json.load(f)
            return [item['link'] for item in data]
