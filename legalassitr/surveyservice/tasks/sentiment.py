from textblob import TextBlob
from celery import shared_task

from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic
from aichat.llm.legal_assitr_llm import LegalAssitrLLM

from surveyservice.models import Feedback

schema = {
    "properties": {
        "sentiment": {"type": "string"},
        "rating": {"type": "integer", "enum": [1, 2, 3, 4, 5], "description":"The rating in terms of positiveness, higher the number more positive is the sentiment"},
    }
}

llm = LegalAssitrLLM(temp=0)
chain = create_tagging_chain(schema, llm)

@shared_task
def analyze_sentiment(content):
    output = chain.run(content)
    return output