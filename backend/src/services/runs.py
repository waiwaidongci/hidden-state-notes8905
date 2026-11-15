from sqlalchemy import select
from fastapi import HTTPException
from src.models import ModelProfile,ObservationTrace,InferenceRun
from src.utils.serialize import row
from .audit import record

def create_run(db,data,actor):
 profile=db.get(ModelProfile,data.profile_id)
 if not profile or profile.study_id!=data.study_id:raise HTTPException(422,'模型版本不属于该研究')
 ids=data.trace_ids
 if len(ids)!=len(set(ids)):raise HTTPException(422,'轨迹ID不能重复')
 traces=list(db.scalars(select(ObservationTrace).where(ObservationTrace.id.in_(ids),ObservationTrace.study_id==data.study_id).order_by(ObservationTrace.reference)))
 if len(traces)!=len(ids):raise HTTPException(422,'轨迹不属于该研究或不存在')
 if db.scalar(select(InferenceRun).where(InferenceRun.name==data.name)):raise HTTPException(409,'运行名已存在')
 run=InferenceRun(study_id=data.study_id,profile_id=profile.id,name=data.name,profile_snapshot=row(profile),trace_snapshot=[row(t) for t in traces],created_by=actor);db.add(run);db.commit()
 try:
  from src.worker import analyze_run
  analyze_run.delay(run.id)
 except Exception:
  run.status='failed';run.error='队列不可用，请稍后重建';db.commit();raise HTTPException(503,run.error)
 record(db,actor,'run.queued',{'run_id':run.id,'traces':len(traces)});return row(run)
