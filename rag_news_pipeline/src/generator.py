from transformers import pipeline

class Generator:
    def __init__(self):
        self.generator = pipeline('text-generation', model='gpt2')

    def generate(self, prompt, max_length=100):
        return self.generator(prompt, max_length=max_length, num_return_sequences=1)[0]['generated_text']