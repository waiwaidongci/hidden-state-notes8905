import numpy as np
from scipy.special import logsumexp
from .parameters import normalize_parameters
class ImpossibleSequence(ValueError):pass

def log_probabilities(a):
 a=np.asarray(a,dtype=float);out=np.full(a.shape,-np.inf);positive=a>0;out[positive]=np.log(a[positive]);return out

def json_logs(a):return [[float(v) if np.isfinite(v) else None for v in row] for row in a]

def infer_sequence(observations,pi,transition,emission):
 normalized=normalize_parameters(pi,transition,emission);p=np.asarray(normalized['pi']);A=np.asarray(normalized['transition']);B=np.asarray(normalized['emission']);obs=np.asarray(observations)
 if obs.ndim!=1 or not 1<=len(obs)<=200 or not np.issubdtype(obs.dtype,np.integer) or np.issubdtype(obs.dtype,np.bool_) or (obs<0).any() or (obs>=B.shape[1]).any():raise ValueError('观测须1..200个合法整数码索引')
 obs=obs.astype(int);K=len(p);T=len(obs);lp=log_probabilities(p);lA=log_probabilities(A);lB=log_probabilities(B);alpha=np.full((T,K),-np.inf);alpha[0]=lp+lB[:,obs[0]]
 if not np.isfinite(alpha[0]).any():raise ImpossibleSequence('不可能序列：第1码在固定模型下概率为0')
 for t in range(1,T):
  alpha[t]=logsumexp(alpha[t-1,:,None]+lA,axis=0)+lB[:,obs[t]]
  if not np.isfinite(alpha[t]).any():raise ImpossibleSequence(f'不可能序列：到第{t+1}码所有路径概率为0')
 likelihood=float(logsumexp(alpha[-1]));beta=np.zeros((T,K))
 for t in range(T-2,-1,-1):beta[t]=logsumexp(lA+lB[:,obs[t+1]][None,:]+beta[t+1][None,:],axis=1)
 posterior=np.exp(alpha+beta-likelihood);posterior/=posterior.sum(axis=1,keepdims=True);marginal=np.argmax(posterior,axis=1).astype(int).tolist()
 # Retain each state's best prefix. Exact log-score ties use lexicographic state-index paths.
 score=lp+lB[:,obs[0]];paths=[(j,) if np.isfinite(score[j]) else None for j in range(K)]
 for t in range(1,T):
  nextscore=np.full(K,-np.inf);nextpaths=[None]*K
  for j in range(K):
   candidates=score+lA[:,j]+lB[j,obs[t]];best=float(candidates.max())
   if not np.isfinite(best):continue
   tied=[i for i in range(K) if candidates[i]==best and paths[i] is not None];prior=min(tied,key=lambda i:paths[i]);nextscore[j]=best;nextpaths[j]=paths[prior]+(j,)
  score=nextscore;paths=nextpaths
 best=float(score.max());terminal=min((j for j in range(K) if score[j]==best),key=lambda j:paths[j]);viterbi=list(paths[terminal])
 def joint(path):
  value=lp[path[0]]+lB[path[0],obs[0]]
  for t in range(1,T):value+=lA[path[t-1],path[t]]+lB[path[t],obs[t]]
  return float(value)
 marginal_joint=joint(marginal)
 with np.errstate(under='ignore'):linear_probability=float(np.exp(likelihood))
 representable=linear_probability>0
 return {'log_likelihood':likelihood,'likelihood_if_representable':linear_probability if representable else None,'linear_likelihood_underflows':not representable,'posterior':posterior.tolist(),'marginal_path':marginal,'marginal_path_is_legal':bool(np.isfinite(marginal_joint)),'marginal_log_joint':marginal_joint if np.isfinite(marginal_joint) else None,'viterbi_path':viterbi,'viterbi_log_joint':best,'log_forward':json_logs(alpha),'log_backward':json_logs(beta),'null_log_meaning':'null in log arrays means exact zero probability (-infinity), not missing data','tie_rule':'Exact floating log-score ties choose lexicographically smallest full state-index path; marginal ties choose smallest state index.','normalization':normalized['normalization']}
