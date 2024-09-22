import os
from typing import Dict
from django.conf import settings

from langchain.callbacks.manager import CallbackManager
from langchain_google_genai import ChatGoogleGenerativeAI
from aichat.agents.callback import LegalAssistrAgentCallbackHandler


DEFAULT_CALLBACK_MANAGER = CallbackManager([LegalAssistrAgentCallbackHandler()])

def get_llm(max_tokens=1024, temp:float=0.7, callbacks=None, callback_manager=DEFAULT_CALLBACK_MANAGER):
    llm = ChatGoogleGenerativeAI(temperature=temp, max_output_tokens=max_tokens, model="gemini-pro", callbacks=callbacks, callback_manager=callback_manager)
