import scrapy

def get_title(self, response):
    try:
        title = response.css('title').get()
        yield title
    except Exception as e:
        self.logger.error(f'Error getting title: {e}')
        
        

