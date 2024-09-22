
import asyncio

from langchain.prompts import PromptTemplate
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains import LLMChain, StuffDocumentsChain
from langchain.agents import AgentExecutor, create_react_agent

from aichat.agents.memory import AssistrChatMemory
from aichat.agents.tools import get_tools
from aichat.agents.llm import get_llm
from aichat.prompts.prompt import sahayak_system_prompt, SUMMARIZE_PROMPT

class AssistrConversationChain:

    def __init__(self, converstaion_id, max_tokens=4096, temp:float=0.7):
        self.callbacks = [AsyncIteratorCallbackHandler()]
        self.callback_manager = None
        self.llm = get_llm(temp=temp, max_tokens=max_tokens)
        
        tools = get_tools()
        self.llm = self.llm.bind(functions=tools)

        self.memory = AssistrChatMemory(
            conversation_id=converstaion_id,
        )
        self.conversation_agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=sahayak_system_prompt,
        )
        self.agent_executor = AgentExecutor(
            agent=self.conversation_agent,
            tools=self.tools,
            verbose=True,
            memory=self.memory,
        )
        self.existing_summary = None

    def summarize_docs(self, docs):
        prompt = PromptTemplate(template=SUMMARIZE_PROMPT)
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        stuff_chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_variable_name="text"
        )
        summary = stuff_chain.run(docs)
        summary = f"Here is the summary of your uploaded Document:\n{summary}"
        self.memory.chat_memory.add_ai_message(summary)
        return summary
    
    def get_response(self, message: str):
        return self.agent_executor.invoke({"input": message})
    
    async def aget_response(self, message: str):
        response = await self.agent_executor.ainvoke({"input": message})
        return response

    def get_conversation_summary(self):
        summary = self.memory.get_conversation_summary(self.llm)
        # generate title using summary
        title = self.llm(f"make a title for this summary `{summary}`")
        return title, summary
    