
from typing import List

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools.base import BaseTool
from langchain_core.pydantic_v1 import root_validator

from .document_crud_tools import CreateDocumentTool, EditDocumentTool, DeleteDocumentTool

DOCUMENT_TOOLS = {
    tool_cls.__fields__["name"].default: tool_cls 
    for tool_cls in [
        CreateDocumentTool,
        EditDocumentTool,
        DeleteDocumentTool
    ]
}

class DocumentToolkit(BaseToolkit):
    """Tookit for creating, editing and deleting documents"""
    
    @root_validator
    def validate_tools(cls, values:dict) -> dict:
        selected_tools = values.get("selected_tools") or []
        for tool_name in selected_tools:
            if tool_name not in DOCUMENT_TOOLS:
                raise ValueError(f"Tile Tool of name {tool_name} not supported. Permitted tools : {list(DOCUMENT_TOOLS)}")
        return values
    
    def get_tools(self) -> List[BaseTool]:
        allowed_tools = DOCUMENT_TOOLS.keys()
        return allowed_tools



