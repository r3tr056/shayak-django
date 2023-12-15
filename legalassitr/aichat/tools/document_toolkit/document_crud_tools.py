
from datetime import datetime
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun
)

from doc_store.models import AIIntermediateDoc

class CreateDocumentInput(BaseModel):
    document_title: str = Field(description="The title of the document")
    document_content: str = Field(description="The content of the document")

class CreateDocumentTool(BaseTool):
    name = "create_document"
    description = "used to create a document or send document to user"
    args_schema: Type[BaseModel] = CreateDocumentInput

    def _run(self, document_title: str, document_content: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        if not document_title or not document_content:
            return Exception("Missing Document Title or Document content")
        timestamp = datetime.utcnow()
        simple_id = f'{document_title}_{str(timestamp)}'
        new_document = AIIntermediateDoc(
            simple_id=simple_id,
            title=document_title, doc_content=document_content)
        new_document.save()

        return f"Document with ID {simple_id} created successfully"
    
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None):
        raise NotImplementedError("CreateDocumentTool does not support async")

class DeleteDocumentInput(BaseModel):
    document_id: str = Field(description="The ID of the document to delete")

class DeleteDocumentTool(BaseTool):
    name = "delete_document"
    description = "used to delete a previously created document"
    args_schema: Type[BaseModel] = DeleteDocumentInput

    def _run(self, document_id:str, run_manager: Optional[CallbackManagerForToolRun] = None):
        try:
            doc = AIIntermediateDoc.objects.get(simple_id=document_id)
            doc.delete()
            return f"Document with ID {document_id} deleted."
        except AIIntermediateDoc.DoesNotExist:
            return f"Document with ID {document_id} DOES NOT EXIST"


class EditDocumentInput(BaseModel):
    document_id: str = Field(description="The ID of the document to edit")
    target_content: str = Field(description="The part to edit or replace with new text")
    edit_content: str = Field(description="The new content to put in place of the old content")

class EditDocumentTool(BaseTool):
    name = "edit_document"
    description = "used to edit a document, replace a part of the content with new content"
    args_schema: Type[BaseModel] = EditDocumentInput

    def _run(self, document_id: str, target_content: str, edit_content: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        try:
            document = AIIntermediateDoc.objects.get(simple_id=document_id)
            old_content = document.content
            new_content = old_content.replace(target_content, edit_content)
            document.content = new_content
            document.save()
            return "Successfully replaced with string"
        except AIIntermediateDoc.DoesNotExist:
            return f"Document with document id {document_id} DOES NOT EXIST"
    

