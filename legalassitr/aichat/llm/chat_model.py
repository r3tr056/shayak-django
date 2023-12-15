from typing import Dict, Any, List, Optional, Union, Tuple, Callable
from pydantic import Field

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult
from langchain.chat_models.base import BaseChatModel

class LegalAssitrChatModel(BaseChatModel):
    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {"custom_api_key": "CUSTOMCHAT_API_KEY"}
    
    @property
    def lc_serializable(self) -> bool:
        return True
    
    client: Any
    temp: float = 0.7
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    custom_api_key: Optional[str] = None
    request_timeout: Optional[Union[float, Tuple[float, float]]] = None
    max_retries: int = 6
    streaming: bool = False
    max_tokens: Optional[int] = None

    def _create_retry_decorator(self) -> Callable[[Any], Any]:
        pass

    def completion_with_retry(self, **kwargs):
        pass

    def _combile_llm_outputs(self, llm_outputs):
        pass

    def _stream(self, messages, stop, run_mananger, **kwargs):
        pass

    def _generate(self, messages: List[BaseMessage], stop: List[str] | None = None, run_manager: CallbackManagerForLLMRun | None = None, **kwargs: Any) -> ChatResult:
        pass

    def _create_message_dicts(self, messages: List[BaseMessage], stop: Optional[List[str]]):
        pass

    def _create_chat_model(self, response):
        pass

    async def _astream(self, messages, stop, run_manager, **kwargs):
        pass