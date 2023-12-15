import json
from datetime import datetime
from typing import Dict, Type, Optional

from langchain.tools.base import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from aichat.models import DynamicForm

class CreateDynamicFormInput(BaseModel):
    form_title:str = Field(description="The title of the form")
    form_fields: Dict[str, str] = Field(description="The field in the form along with example inputs that are possible")

class CreateDynamicFormResponse(BaseModel):
    form_id: str = Field(description="The ID of the form")
    form_title: str = Field(description="The title of the form")
    form_fields_json: str = Field(description="The field format in JSON formatted string")

class CreateDynamicForm(BaseTool):
    name = "CreateForm"
    description = "used to create custom forms for requesting data or information from the user"
    args_schema: Type[BaseModel] = CreateDynamicFormInput

    def _run(self, form_title: str, form_fields: Dict[str, str], run_manager: Optional[CallbackManagerForToolRun] = None):
        try:
            json_fields = json.dumps(form_fields)
            form_id = f"{form_title}_{str(datetime.utcnow())}"
            dynamic_form = DynamicForm(form_id=form_id, form_title=form_title, form_data=json_fields)
            dynamic_form.save()
            return CreateDynamicFormResponse(form_id=form_id, form_title=form_title, form_fields_json=form_fields)
        except Exception as ex:
            return f"Error occured, the form format provided is not valid JSON"
        
class SubmitDynamicFormInput(BaseModel):
    form_id: str = Field("The ID of the form")
    form_field_values: Dict[str, str] = Field(description="The values next to their corresponding fields")
    
class SubmitDynamicForm(BaseTool):
    name = "SubmitForm"
    description = "use when need to submit filled forms"
    args_schema: Type[BaseModel] = SubmitDynamicFormInput
    
    def _run(self, form_id, form_field_values: Dict[str, str], run_manager: Optional[CallbackManagerForToolRun] = None):
        try:
            dyn_form = DynamicForm.objects.get(form_id=form_id)
            dyn_form.form_data = form_field_values
            dyn_form.save()
            return "Successfully saved Form"
        except DynamicForm.DoesNotExist:
            return f"The Form with ID {form_id} DOES NOT EXIST"