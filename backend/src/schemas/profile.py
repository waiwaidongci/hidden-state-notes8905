from pydantic import BaseModel,Field,ConfigDict
from typing import Annotated
Probability=Annotated[float,Field(ge=0,le=1,strict=True,allow_inf_nan=False)]
class ProfileInput(BaseModel):
 model_config=ConfigDict(allow_inf_nan=False,str_strip_whitespace=True)
 study_id:int=Field(gt=0,strict=True)
 name:str=Field(min_length=2,max_length=180)
 version:str=Field(min_length=1,max_length=80)
 states:list[str]=Field(min_length=2,max_length=5)
 pi:list[Probability]=Field(min_length=2,max_length=5)
 transition:list[list[Probability]]=Field(min_length=2,max_length=5)
 emission:list[list[Probability]]=Field(min_length=2,max_length=5)
