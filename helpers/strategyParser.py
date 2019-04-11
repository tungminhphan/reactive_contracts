# Tung Phan
# February 18, 2019
# Reactive Contract Example
import numpy as np
from itertools import groupby

filename = 'three_islands'
strategy_filename = filename + '.strat'
raw_strat = open(strategy_filename).read()
lines = raw_strat.split('State ')[1:]
strategy = dict()
for line in lines:
    state = line[:line.find('w')-1]
    strategy[state] = dict()
    succ = set(line[line.find('successors : ')+len('successors : '):].replace(' ','').strip('\n').split(','))
    strategy[state]['successors'] = succ

    state_data = line[line.find('<')+1:line.find('>\n')].replace(' ', '')
    data_array = state_data.split(',')
    for k, g in groupby(data_array, lambda data: data[0:data.find(':')] if not '@' in data else data[0:data.find('@')]):
        val = 0
        g =  list(g)
        if '@' in g[0]:
            for bit in g:
                power = int(bit.split('@')[-1][0])
                digit = int(bit.split('@')[-1][-1])
                val += digit * 2 **power
        else:
            val = int(g[0][-1])
        strategy[state][k] = val

np.save(filename+'.npy', strategy)
