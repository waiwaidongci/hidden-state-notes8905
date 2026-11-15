from pydantic import BaseModel,Field,ConfigDict
from .trace import TraceInput
class StudyInput(BaseModel):
 model_config=ConfigDict(str_strip_whitespace=True)
 name:str=Field(min_length=2,max_length=150)
 filename:str=Field(min_length=2,max_length=180)
 description:str=Field(default='',max_length=3000)
 symbols:list[str]=Field(min_length=2,max_length=6)
 traces:list[TraceInput]=Field(min_length=1,max_length=240)
