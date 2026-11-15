from fastapi import HTTPException
from src.models import InterpretationNote
from src.utils.csv_export import csv_response
from src.services.audit import record

def export_note(db,id,actor):
 note=db.get(InterpretationNote,id)
 if not note:raise HTTPException(404,'说明不存在')
 if note.status!='approved':raise HTTPException(409,'仅批准说明可导出')
 r=note.result_snapshot;rows=[]
 for trace in r['traces']:
  for t,token in enumerate(trace['tokens']):rows.append([note.name,r['profile']['name'],r['profile']['version'],r['fingerprint'],trace['reference'],t+1,token,r['states'][trace['viterbi_path'][t]],r['states'][trace['marginal_path'][t]],str(trace['posterior'][t]),trace['log_likelihood'],trace['viterbi_log_joint'],trace['marginal_path_is_legal'],note.interpretation,note.next_step,note.review_note])
 record(db,actor,'note.exported',{'note_id':id});return csv_response(f'hmm-note-{id}.csv',rows,['核对说明','固定模型','版本','指纹','轨迹','步号','观测码','Viterbi联合MAP','单点最高态','边际后验向量','序列logL','Viterbi联合logP','边际路径合法','人工解释','下一步','审核意见'])
