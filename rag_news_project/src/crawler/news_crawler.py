import requests
from bs4 import BeautifulSoup
import datetime

class NewsCrawler:
    def __init__(self, sources):
        self.sources = sources

    def crawl(self):
        articles = []
        for source in self.sources:
            articles.extend(self._crawl_source(source))
        return articles

    def _crawl_source(self, source):
        response = requests.get(source['url'])
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []

        for article in soup.find_all(source['article_tag'], class_=source['article_class']):
            title = article.find(source['title_tag']).text.strip()
            link = article.find('a')['href']
            if not link.startswith('http'):
                link = source['base_url'] + link
            
            content = self._get_article_content(link, source['content_tag'], source['content_class'])
            
            articles.append({
                'title': title,
                'content': content,
                'url': link,
                'source': source['name'],
                'crawled_at': datetime.datetime.now().isoformat()
            })

        return articles

    def _get_article_content(self, url, content_tag, content_class):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find(content_tag, class_=content_class)
        return content.text.strip() if content else ""