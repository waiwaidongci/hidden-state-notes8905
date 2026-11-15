import math
from .hmm import infer_sequence,ImpossibleSequence
from .validation import validate_traces,validate_states
from .fingerprint import fingerprint

def analyze(profile,traces):
 if not 1<=len(traces)<=30:raise ValueError('单次须选择1..30条轨迹')
 validate_traces(profile['symbols'],traces);parameters=profile['parameters'];validate_states(profile['states'],len(parameters['pi']));lookup={symbol:i for i,symbol in enumerate(profile['symbols'])};results=[]
 for trace in sorted(traces,key=lambda t:t['reference']):
  try:inferred=infer_sequence([lookup[s] for s in trace['tokens']],parameters['pi'],parameters['transition'],parameters['emission'])
  except ImpossibleSequence as error:raise ImpossibleSequence(f'{trace["reference"]}：{error}') from error
  results.append({'id':trace['id'],'reference':trace['reference'],'tokens':trace['tokens'],**inferred})
 return {'profile':profile,'states':profile['states'],'symbols':profile['symbols'],'trace_count':len(results),'token_count':sum(len(r['tokens']) for r in results),'total_log_likelihood':math.fsum(r['log_likelihood'] for r in results),'illegal_marginal_paths':sum(not r['marginal_path_is_legal'] for r in results),'traces':results,'fingerprint':fingerprint(profile,traces),'interpretation':'Fixed HMM parameters, no EM or fitting. Marginal argmax can violate legal transitions; Viterbi is the full joint MAP path. States are model labels, not equipment-fault facts or online alarms.'}
