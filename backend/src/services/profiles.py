from sqlalchemy import select
from fastapi import HTTPException
from src.models import SequenceStudy,ModelProfile
from src.utils.serialize import row
from .parameters import normalize_parameters
from .validation import validate_states
from .audit import record

def create_profile(db,data,actor):
 study=db.get(SequenceStudy,data.study_id)
 if not study:raise HTTPException(404,'研究不存在')
 if db.scalar(select(ModelProfile).where(ModelProfile.name==data.name)):raise HTTPException(409,'模型版本名已存在')
 try:
  normalized=normalize_parameters(data.pi,data.transition,data.emission);validate_states(data.states,len(normalized['pi']))
  if len(normalized['emission'][0])!=len(study.symbols):raise ValueError('发射列须匹配研究声明观测码')
 except ValueError as error:raise HTTPException(422,str(error))
 profile=ModelProfile(study_id=study.id,name=data.name,version=data.version,states=data.states,symbols=study.symbols,parameters=normalized,normalization_max_delta=normalized['max_normalization_delta'],created_by=actor);db.add(profile);db.commit();record(db,actor,'profile.frozen',{'profile_id':profile.id,'normalization_delta':profile.normalization_max_delta});return row(profile)
