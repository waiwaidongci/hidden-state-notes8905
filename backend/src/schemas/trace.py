from pydantic import BaseModel,Field,ConfigDict
class TraceInput(BaseModel):
 model_config=ConfigDict(str_strip_whitespace=True)
 reference:str=Field(min_length=1,max_length=100)
 tokens:list[str]=Field(min_length=1,max_length=200)
class TracePatch(BaseModel):
 tokens:list[str]=Field(min_length=1,max_length=200)
