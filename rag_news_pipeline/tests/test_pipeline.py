import unittest
from unittest.mock import patch, MagicMock
from src.scraper import NewsScraper
from src.processor import TextProcessor
from src.embedder import TextEmbedder
from src.retriever import Retriever
from src.generator import Generator
from src.main import RAGPipeline

class TestRAGPipeline(unittest.TestCase):

    def setUp(self):
        self.urls = ['https://example.com']
        self.pipeline = RAGPipeline(self.urls)

    @patch('src.scraper.requests.get')
    def test_scraper(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = '<html><body><article><h2>Test Title</h2><p>Test Summary</p></article></body></html>'
        mock_get.return_value = mock_response

        news = self.pipeline.scraper.scrape()
        self.assertEqual(len(news), 1)
        self.assertEqual(news[0]['title'], 'Test Title')
        self.assertEqual(news[0]['summary'], 'Test Summary')

    def test_processor(self):
        text = "This is a test sentence with some stop words."
        processed = self.pipeline.processor.process(text)
        self.assertEqual(processed, "test sentence stop words")

    @patch('src.embedder.SentenceTransformer')
    def test_embedder(self, mock_transformer):
        mock_transformer.return_value.encode.return_value = [[1.0, 2.0, 3.0]]
        embeddings = self.pipeline.embedder.embed(["test sentence"])
        self.assertEqual(embeddings.tolist(), [[1.0, 2.0, 3.0]])

    def test_retriever(self):
        self.pipeline.retriever.add_documents([{'title': 'Test'}], [[1.0, 2.0, 3.0]])
        results = self.pipeline.retriever.retrieve([1.0, 2.0, 3.0])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Test')

    @patch('src.generator.pipeline')
    def test_generator(self, mock_pipeline):
        mock_pipeline.return_value.return_value = [{'generated_text': 'Generated answer'}]
        result = self.pipeline.generator.generate("Test prompt")
        self.assertEqual(result, 'Generated answer')

    @patch.object(RAGPipeline, 'update_news')
    @patch.object(RAGPipeline, 'query')
    def test_pipeline_integration(self, mock_query, mock_update_news):
        mock_query.return_value = "Test answer"
        self.pipeline.update_news()
        result = self.pipeline.query("Test question")
        mock_update_news.assert_called_once()
        mock_query.assert_called_once_with("Test question")
        self.assertEqual(result, "Test answer")

if __name__ == '__main__':
    unittest.main()