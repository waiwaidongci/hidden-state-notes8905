def validate_symbols(symbols):
 if not 2<=len(symbols)<=6 or len(set(symbols))!=len(symbols) or any(not isinstance(s,str) or not s.strip() or len(s)>80 for s in symbols):raise ValueError('声明2..6个唯一非空观测码')

def validate_traces(symbols,traces):
 validate_symbols(symbols)
 if not 1<=len(traces)<=240 or len({t['reference'] for t in traces})!=len(traces):raise ValueError('研究需1..240条唯一轨迹')
 for trace in traces:
  if not 1<=len(trace['tokens'])<=200 or any(type(s) is not str or s not in symbols for s in trace['tokens']):raise ValueError('轨迹须1..200个已声明观测码')

def validate_states(states,K):
 if len(states)!=K or len(set(states))!=len(states) or any(not isinstance(s,str) or not s.strip() or len(s)>80 for s in states):raise ValueError('状态标签须与π维度相同且唯一非空')
