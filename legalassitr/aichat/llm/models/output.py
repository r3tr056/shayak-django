from typing import List, Optional

from langchain.pydantic_v1 import BaseModel, Field, validator
from langchain.output_parsers import CommaSeparatedListOutputParser

list_parser  = CommaSeparatedListOutputParser()
format_instructions = list_parser.get_format_instructions()

class Document(BaseModel):
    title: str = Field(description="the title of the document to generate")
    preamble: Optional[str] = Field(description="a brief introduction on the context and the purpose of the document to generate")
    parties: Optional[List[str]] = Field(description="list of the full names of the parties involved, addresses and other relevant details")
    background: Optional[str] = Field(description="background or recital that outlines the circumstances leading to the creation of the document. Includes reasons and considerations of the parties involved")
    operative_clause: Optional[str] = Field(description="main body of the document where the rights, obligations, and responsibilities of the parties are clearly outlined. Use numbered paragraph for clarity")
    consideration_clause