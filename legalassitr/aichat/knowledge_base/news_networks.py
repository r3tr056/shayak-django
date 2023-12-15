
from langchain.prompts import ChatPromptTemplate
from langchain.embeddings.llamacpp import LlamaCppEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.vectorstores.chroma import Chroma
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.document_loaders import AsyncHtmlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.chains import create_extraction_chain_pydantic

DEFAULT_LAW_WEBSITES = [
    "https://www.livelaw.in/",
    "https://timesofindia.indiatimes.com/",
    "https://www.indiatoday.in/law-today"
]

class NewsSchema(BaseModel):
    article_title: str = Field(description="The title of the new article")
    article_summary: str = Field(description="The summary of the news article")

def load_web(network):
    web_loader = AsyncHtmlLoader(network)
    return web_loader.load()

async def load_news(news_networks=DEFAULT_LAW_WEBSITES):
    web_loader = AsyncHtmlLoader(news_networks)
    docs = web_loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs = await bs_transformer.atransform_documents(docs, tags_to_extract=["span"])

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = splitter.split_documents(docs)

    embeddings = LlamaCppEmbeddings()
    vector_store = await Chroma.afrom_documents(documents=documents, embedding=embeddings, persist_directory="./news_knowledge_base")
    vector_store.persist()
    vector_store = None

async def search(self, query: str):
    docs = await self.vector_store.asimilarity_search(query=query)
    return docs[0].page_content
    
async def search_by_vector(self, embedding_vector: str):
    docs = await self.vector_store.asimilarity_search_by_vector(embedding_vector)
    return docs[0].page_content
    
