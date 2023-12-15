from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from aichat.llm.legal_assitr_llm import LegalAssitrLLM

llm = LegalAssitrLLM()

def setup_cache():
    set_llm_cache(InMemoryCache())

