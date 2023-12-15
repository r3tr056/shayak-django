import os

from typing import Type, List, Optional

from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import LlamaCppEmbeddings
from langchain.retrievers.web_research import WebResearchRetriever
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.utilities.google_search import GoogleSearchAPIWrapper
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.tools.base import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field

os.environ["GOOGLE_CSE_ID"] = "36ef5fe3e496545da"
os.environ["GOOGLE_API_KEY"] = "AIzaSyAcXABfzBoXUULOhl73HAt8ikhwlNIEHd0"


class ResearchToolInput(BaseModel):
    reference_document_title: str = Field(description="The document being referred to")
    topic: str = Field(description="The topic of the research")
    subtopics: List[str] = Field(description="Possible subtopics or other subideas")
    query: str = Field(description="The main question, doubt or the query.")

class ResearchTool(BaseTool):
    name = "online_research"
    description = "useful for researching or finding answers to doubts, questions and legal news on the internet"
    args_schema: Type[BaseModel] = ResearchToolInput

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.embedding_model = LlamaCppEmbeddings()
        self.vectorstore = Chroma(self.embeddings_model.embed_query, persist_directory="./chroma_research")
        self.search = GoogleSearchAPIWrapper()
        self.web_search_retriver = WebResearchRetriever.from_llm(
            vectorstore=self.vectorstore,
            llm=self.llm,
            search=self.search,
            num_search_results=int(kwargs.get('max_search_results', 10)),
        )

    def _run(self, reference_document_title: str, topic: str, subtopics: List[str], query: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
            self.llm,
            retriever=self.web_search_retriver,
        )
        search_str = f'For {topic} within the subtopics {", ".join(subtopics)}  search for : {query}'
        result = qa_chain({"question": search_str})
        return result
