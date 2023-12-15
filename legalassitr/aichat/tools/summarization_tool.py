
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from .base_tool import LegalTool

class SummarizationTool(LegalTool):
    def __init__(self):
        super().__init__()
        MAP_TEMPLATE = """
The following is a set of documents
{docs}
Based on this list of docs, please identify the main themes 
Helpful Answer:
"""
        map_prompt = PromptTemplate.from_template(MAP_TEMPLATE)
        map_chain = LLMChain(
            llm=self.llm,
            prompt=map_prompt
        )