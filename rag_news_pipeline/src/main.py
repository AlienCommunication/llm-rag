from scraper import NewsScraper
from processor import TextProcessor
from embedder import TextEmbedder
from retriever import Retriever
from generator import Generator

class RAGPipeline:
    def __init__(self, urls):
        self.scraper = NewsScraper(urls)
        self.processor = TextProcessor()
        self.embedder = TextEmbedder()
        self.retriever = Retriever(384)  # 384 is the dimension for 'all-MiniLM-L6-v2'
        self.generator = Generator()

    def update_news(self):
        news = self.scraper.scrape()
        processed_news = [self.processor.process(article['title'] + ' ' + article['summary']) for article in news]
        embeddings = self.embedder.embed(processed_news)
        self.retriever.add_documents(news, embeddings)

    def query(self, question):
        question_embedding = self.embedder.embed([question])[0]
        relevant_docs = self.retriever.retrieve(question_embedding)
        context = "\n".join([doc['title'] + ': ' + doc['summary'] for doc in relevant_docs])
        prompt = f"Based on the following news:\n{context}\n\nAnswer the question: {question}"
        return self.generator.generate(prompt)

# Usage
urls = [
    'https://timesofindia.indiatimes.com',
    'https://www.thehindu.com',
    'https://www.indiatimes.com'
]

pipeline = RAGPipeline(urls)
pipeline.update_news()
result = pipeline.query("What are the latest developments in Indian politics?")
print(result)