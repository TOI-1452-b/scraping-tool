import scrapy

class SelectorService:

    def get_title(self, response):
        try:
            selector_priorities = {
                'h1::text': 3,
                'h1.title::text': 3,
                'h1.entry-title::text': 3,
                'h1.post-title::text': 3,
                'article h1::text': 3,
                'header h1::text': 3,
                'main h1::text': 3,
                'h2::text': 2,
                'h2.title::text': 2,
                'h2.entry-title::text': 2,
                'h2.post-title::text': 2,
                'article h2::text': 2,
                'header h2::text': 2,
                'h3::text': 1,
                'h3.title::text': 1,
                'h3.entry-title::text': 1,
                'h3.post-title::text': 1,
                'article h3::text': 1,
                'title::text': 2,
                '.title::text': 2,
                '#title::text': 2,
                '.post-title::text': 3,
                '.entry-title::text': 3,
                '.headline::text': 2,
                '.main-title::text': 2,  
                '.article-title::text': 3,
                '.blog-title::text': 2,
                '.page-title::text': 2,
                'header .title::text': 2,
                'main .title::text': 2,
            }

            content_by_priority = {}
            for selector, priority in selector_priorities.items():
                try:
                    content = response.css(selector).get()
                    if content:
                        if priority not in content_by_priority:
                            content_by_priority[priority] = []
                        content_by_priority[priority].append(content)
                except Exception as selector_error:
                    self.logger.warning(f'Error processing selector {selector}: {selector_error}')
                    continue

            if content_by_priority:
                for priority in sorted(content_by_priority.keys(), reverse=True):
                    if content_by_priority[priority]:
                        return content_by_priority[priority][0].strip()

            return None

        except Exception as e:
            self.logger.error(f'Error getting title: {e}')
            return None   


    def get_body_content(self, response):
        try:
            selector_priorities = {
                'article::text': 3,
                '.post-content::text': 3,
                '.entry-content::text': 3,
                '.content::text': 2,
                '.main-content::text': 2,
                '#content::text': 2,
                '.article-content::text': 3,
                '.post-body::text': 3,
                'main::text': 2,
                '.body::text': 1,
                'p::text': 1,
                '.container p::text': 2,
                'div[class*="content"]::text': 2,
                '.article-body::text': 3,
                '.blog-post::text': 3,
                '.page-content::text': 2,
                '.text-content::text': 2,
                '.rich-text::text': 2,
                '.story-content::text': 3,
                '.news-article::text': 3,
                '.post-text::text': 2,
                '.article-text::text': 3,
                '.main-article::text': 3,
                '.wysiwyg-content::text': 2,
                '.blog-content::text': 2,
                '.article-container::text': 3,
                '.post-container::text': 3,
                '.content-area::text': 2,
                '.content-body::text': 2,
                '.content-wrapper::text': 2,
                '.content-section::text': 2,
                '.article-section::text': 3,
                '.post-section::text': 3,
                '.text-wrapper::text': 2,
                '.content-inner::text': 2,
                '.article-inner::text': 3,
                '.post-inner::text': 3,
                'section[class*="content"]::text': 2,
                'div[class*="article"]::text': 2,
                'div[class*="post"]::text': 2,
                '.cms-content::text': 2,
                '.editor-content::text': 2
            }

            content_by_priority = {}
            for selector, priority in selector_priorities.items():
                try:
                    content = response.css(selector).getall()
                    if content:
                        if priority not in content_by_priority:
                            content_by_priority[priority] = []
                        content_by_priority[priority].extend(content)
                except Exception as selector_error:
                    self.logger.warning(f'Error processing selector {selector}: {selector_error}')
                    continue

            if content_by_priority:
                all_content = []
                for priority in sorted(content_by_priority.keys(), reverse=True):
                    all_content.extend(content_by_priority[priority])
                
                return ' '.join(all_content).strip()

            return None

        except Exception as e:
            self.logger.error(f'Error getting body: {e}')
            return None
        
    def get_articles(self, response):
        try:
            selector_priorities = {
                '.article-content::text': 3,     
                '.article-body::text': 3,        
                '.article-text::text': 3,        
                '.main-article::text': 2,        
                '.article-container::text': 2,   
                '.article-section::text': 2,     
                '.article-inner::text': 1,       
                '.news-article::text': 2,        
                '.story-content::text': 2,       
            }

            content_by_priority = {}
            for selector, priority in selector_priorities.items():
                try:
                    articles = response.css(selector).getall()
                    if articles:
                        if priority not in content_by_priority:
                            content_by_priority[priority] = []
                        content_by_priority[priority].extend(articles)
                except Exception as selector_error:
                    self.logger.warning(f'Error processing selector {selector}: {selector_error}')
                    continue

            if content_by_priority:
                for priority in sorted(content_by_priority.keys()):
                    if content_by_priority[priority]:
                        return content_by_priority[priority]

            return []

        except Exception as e:
            self.logger.error(f'Error getting articles: {e}')
            return None


    def get_blog_posts(self, response):
        try:
            selector_priorities = {
                '.post-content::text': 3,
                '.post-body::text': 3,
                '.blog-post::text': 3,
                '.post-text::text': 2,
                '.blog-content::text': 2,
                '.post-container::text': 3,
                '.post-section::text': 3,
                '.post-inner::text': 3,
                '.entry-content::text': 3,       
            }

            content_by_priority = {}
            for selector, priority in selector_priorities.items():
                try:
                    blog_posts = response.css(selector).getall()
                    if blog_posts:
                        if priority not in content_by_priority:
                            content_by_priority[priority] = []
                        content_by_priority[priority].extend(blog_posts)
                except Exception as selector_error:
                    self.logger.warning(f'Error processing selector {selector}: {selector_error}')
                    continue

            if content_by_priority:
                for priority in sorted(content_by_priority.keys()):
                    if content_by_priority[priority]:
                        return content_by_priority[priority]

            return []

        except Exception as e:
            self.logger.error(f'Error getting articles: {e}')
            return None
        
    def get_list_items(self, response):
        try:
            selector_priorities = {
                'ul::text': 3,               
                'ol::text': 3,               
                'li::text': 3,               
                'dl::text': 2,               
                'dt::text': 2,               
                'dd::text': 2,               
                '.list::text': 2,            
                '.list-item::text': 2,       
                '.menu-list::text': 1,       
                '.nav-list::text': 1,        
                'nav ul::text': 1,           
                '.item-list::text': 2,       
                '.bullet-list::text': 2,     
                '.numbered-list::text': 2,   
                'ul.list::text': 2,          
                'ol.list::text': 2,          
                '.list-group::text': 2,      
                '.list-group-item::text': 2, 
                'ul[class*="list"]::text': 2,
                'li[class*="item"]::text': 2,
                '.checklist::text': 2,       
                '.feature-list::text': 2,    
                '.menu-items::text': 1,      
                '.dropdown-list::text': 1    
            }

            content_by_priority = {}
            for selector, priority in selector_priorities.items():            
                try:
                    list_items = response.css(selector).getall()
                    if list_items:
                        if priority not in content_by_priority:
                            content_by_priority[priority] = []
                        content_by_priority[priority].extend(list_items)
                except Exception as selector_error:
                    self.logger.warning(f'Error processing selector {selector}: {selector_error}')
                    continue

            if content_by_priority:
                for priority in sorted(content_by_priority.keys(), reverse=True):
                    if content_by_priority[priority]:
                        return content_by_priority[priority]

            return None

        except Exception as e:
            self.logger.error(f'Error getting articles: {e}')
            return None
