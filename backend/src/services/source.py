from sqlalchemy import select
from fastapi import HTTPException
from src.models import SequenceStudy,ObservationTrace
from src.utils.serialize import row
from .validation import validate_traces
from .audit import record

def create_study(db,data,actor):
 if db.scalar(select(SequenceStudy).where(SequenceStudy.name==data.name)):raise HTTPException(409,'研究名已存在')
 try:validate_traces(data.symbols,[t.model_dump() for t in data.traces])
 except ValueError as error:raise HTTPException(422,str(error))
 study=SequenceStudy(**data.model_dump(exclude={'traces'}));db.add(study);db.flush()
 for trace in data.traces:db.add(ObservationTrace(study_id=study.id,**trace.model_dump()))
 db.commit();record(db,actor,'study.imported',{'study_id':study.id,'traces':len(data.traces)});return row(study)

def edit_trace(db,id,data,actor):
 trace=db.get(ObservationTrace,id)
 if not trace:raise HTTPException(404,'轨迹不存在')
 study=db.get(SequenceStudy,trace.study_id)
 try:validate_traces(study.symbols,[dict(row(trace),tokens=data.tokens)])
 except ValueError as error:raise HTTPException(422,str(error))
 trace.tokens=data.tokens;db.commit();record(db,actor,'trace.revised',{'trace_id':id});return row(trace)
