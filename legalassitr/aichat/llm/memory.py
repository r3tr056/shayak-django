
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory, ChatMessageHistory

class LegalAssitrMemory:
    memory = ConversationBufferMemory()

    def add_user_message(self, content):
        self.memory.add_user_message(content)