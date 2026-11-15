from pydantic import BaseModel,Field
from typing import Annotated
TraceId=Annotated[int,Field(gt=0,strict=True)]
class RunInput(BaseModel):
 study_id:int=Field(gt=0,strict=True)
 profile_id:int=Field(gt=0,strict=True)
 name:str=Field(min_length=2,max_length=180)
 trace_ids:list[TraceId]=Field(min_length=1,max_length=30)
