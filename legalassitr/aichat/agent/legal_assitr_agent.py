
from pathlib import Path
from typing import Any, List, Tuple, Union

from langchain.chains import RetrievalQA
from langchain.embeddings.llamacpp import LlamaCppEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain.agents import AgentExecutor, BaseMultiActionAgent, Tool
from langchain.schema import AgentAction, AgentFinish
from langchain.utilities.serpapi import SerpAPIWrapper

from aichat.tools.document_toolkit import DocumentToolkit
from aichat.tools.dynamic_forms import CreateDynamicForm, SubmitDynamicForm
from aichat.tools.research_tool import ResearchTool
from aichat.tools.summarization_tool import SummarizationTool

document_tools = DocumentToolkit().get_tools()
form_tools = [CreateDynamicForm(), SubmitDynamicForm()]
research_tool = [ResearchTool()]
summarization_tool = [SummarizationTool()]

tools = document_tools + form_tools + research_tool + summarization_tool

class LegalAssitrAgent(BaseMultiActionAgent):
    search = SerpAPIWrapper()

    def setup(self):
        self.vector_db = Chroma()

    @property
    def input_keys(self):
        return ["input"]
    
    def plan(self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any) -> Union[List[AgentAction], AgentFinish]:
        return AgentAction(tool='online_research', tool_input=kwargs["input"], log="")

    async def aplan(self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any) -> Union[AgentAction, AgentFinish]:
        """ Given input, decided what to do. 
        Args:
            intermediate_steps: Steps the LLM has taken to date, along with observations
            **kwargs: User inputs
        Returns:
            Action specifying what tool to use.
        """
        return AgentAction(tool='Search', tool_input=kwargs["input"], log="")


