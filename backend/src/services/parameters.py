import numpy as np
ROW_SUM_TOLERANCE=1e-8

def normalize_parameters(pi,transition,emission):
 raw={'pi':pi,'transition':transition,'emission':emission}
 def numbers(value):
  if isinstance(value,(list,tuple)):return all(numbers(v) for v in value)
  return type(value) is not bool
 if not all(numbers(v) for v in raw.values()):raise ValueError('概率不能是bool')
 p=np.asarray(pi,dtype=float);A=np.asarray(transition,dtype=float);B=np.asarray(emission,dtype=float);K=len(p) if p.ndim==1 else 0
 if not 2<=K<=5 or A.shape!=(K,K) or B.ndim!=2 or B.shape[0]!=K or not 2<=B.shape[1]<=6:raise ValueError('需要2..5状态、2..6码且π/A/B维度匹配')
 if any(not np.isfinite(a).all() or (a<0).any() or (a>1).any() for a in [p,A,B]):raise ValueError('π/A/B须有限且非负≤1')
 logs=[]
 def norm(row,field,index):
  total=float(row.sum());delta=total-1
  if total<=0 or abs(delta)>ROW_SUM_TOLERANCE:raise ValueError(f'{field}[{index}]行和{total}不在1±1e-8')
  logs.append({'field':field,'row':index,'original_sum':total,'delta_from_one':delta,'renormalized':total!=1.0});return row/total
 pn=norm(p,'pi',0);An=np.vstack([norm(row,'transition',i) for i,row in enumerate(A)]);Bn=np.vstack([norm(row,'emission',i) for i,row in enumerate(B)])
 return {'pi':pn.tolist(),'transition':An.tolist(),'emission':Bn.tolist(),'raw':{'pi':p.tolist(),'transition':A.tolist(),'emission':B.tolist()},'normalization':logs,'sum_tolerance':ROW_SUM_TOLERANCE,'max_normalization_delta':max(abs(l['delta_from_one']) for l in logs),'zero_policy':'Exact zeros retained; no epsilon floors; only row-sum tolerance renormalization.'}
