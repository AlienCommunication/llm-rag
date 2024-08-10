import requests
from bs4 import BeautifulSoup
import datetime

class NewsScraper:
    def __init__(self, urls):
        self.urls = urls

    def scrape(self):
        news_articles = []
        for url in self.urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # This is a simplified scraping logic. You'll need to adjust it based on each website's structure
            articles = soup.find_all('article')
            for article in articles:
                title = article.find('h2').text.strip() if article.find('h2') else ''
                summary = article.find('p').text.strip() if article.find('p') else ''
                link = article.find('a')['href'] if article.find('a') else ''
                date = datetime.datetime.now().isoformat()  # Use actual published date if available

                news_articles.append({
                    'title': title,
                    'summary': summary,
                    'link': link,
                    'date': date,
                    'source': url
                })

        return news_articles