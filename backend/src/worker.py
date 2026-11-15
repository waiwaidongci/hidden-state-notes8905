import json
from pathlib import Path
from celery import Celery
from src.config.database import SessionLocal
from src.config.settings import REDIS_URL,ARTIFACT_DIR
from src.models import InferenceRun
from src.services.analysis import analyze
from src.services.audit import record
app=Celery('hidden_state_notes',broker=REDIS_URL,backend=REDIS_URL)
app.conf.update(task_track_started=True,worker_prefetch_multiplier=1,task_acks_late=True)
@app.task(name='hmm.analyze',soft_time_limit=120,time_limit=150)
def analyze_run(id):
 with SessionLocal() as db:
  run=db.get(InferenceRun,id)
  if not run or run.status=='completed':return
  run.status='running';db.commit()
  try:
   result=analyze(run.profile_snapshot,run.trace_snapshot)
   Path(ARTIFACT_DIR).mkdir(parents=True,exist_ok=True);Path(ARTIFACT_DIR,f'hmm-{id}.json').write_text(json.dumps(result,ensure_ascii=False,allow_nan=False));run.result=result;run.total_log_likelihood=result['total_log_likelihood'];run.status='completed';run.error=None;db.commit();record(db,'worker','run.completed',{'run_id':id,'trace_count':result['trace_count']})
  except Exception as error:
   db.rollback();run=db.get(InferenceRun,id);run.status='failed';run.error=str(error)[:1000];db.commit();record(db,'worker','run.failed',{'run_id':id,'error':run.error})
