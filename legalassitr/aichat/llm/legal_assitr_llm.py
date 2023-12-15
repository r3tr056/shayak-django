from  typing import *

import os
import requests

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.openai import OpenAI

API_URL = "https://api-inference.huggingface.co/models/TinyPixel/Llama-2-7B-bf16-sharded"

class LegalAssitrLLM(LLM):

    model_name = "legalassitr"
    model_type = "custom"

    hf_model_id = "legalassitr-13b"
    hf_api_token = "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"

    # model arguments
    # Total probablity mass of tokens to consider at each step
    top_p = 0.1
    top_k = 40
    # The max number of tokens to generate in the completion
    max_tokens = 2000
    # 
    n_threads = 4
    n_predict = 256
    temp = 0.7
    repeat_last_n = 64
    repeat_penalty = 1.18

    model_api_instance = None

    # For the Inference server
    request_timemout = None
    

    @property
    def _llm_type(self):
        return self.model_type
    
    def _identifying_params(self) -> Mapping[str, Any]:
        return {}

    def _get_model_default_parameters(self):
        default_params = {
            "n_predict": self.n_predict,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "n_threads": self.n_threads,
            "temp": self.temp,
            "repeat_last_n": self.repeat_last_n,
            "repeat_penalty": self.repeat_penalty,
        }

        if self.max_tokens is not None:
            default_params["max_tokens"] = self.max_tokens
        if self.request_tiemout is not None:
            default_params["request_timeout"] = self.request_timeout

        return default_params
    
    def _stream(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any):
        params = {**self._invocation_params, **kwargs, "stream": True}
        self.get_sub_prompts(params)
    
    def _call(self, prompt, stop, run_manager, **kwargs):
        if stop is not None:
            raise ValueError("stop kwargs are not permitted")
        try:
            headers = {"Authorization": f"Bearer {self.hf_api_token}"}
            response = requests.post(API_URL, headers=headers, json=prompt)
            return response.json()
        except Exception as e:
            print(e)
    