import streamlit as st
from main import RAGPipeline

@st.cache_resource
def get_pipeline():
    urls = [
        'https://timesofindia.indiatimes.com',
        'https://www.thehindu.com',
        'https://www.indiatimes.com'
    ]
    return RAGPipeline(urls)

st.title("Indian News RAG Pipeline")

pipeline = get_pipeline()

if st.button("Update News"):
    with st.spinner("Updating news..."):
        pipeline.update_news()
    st.success("News updated successfully!")

question = st.text_input("Ask a question about recent Indian news:")

if question:
    with st.spinner("Generating answer..."):
        answer = pipeline.query(question)
    st.write("Answer:", answer)