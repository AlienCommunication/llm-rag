import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def process(self, text):
        # Tokenize
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and non-alphabetic tokens
        processed_tokens = [token for token in tokens if token.isalpha() and token not in self.stop_words]
        
        return ' '.join(processed_tokens)