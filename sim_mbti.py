import itertools
from collections import defaultdict

questions_dims = [
    ['S-J', 'Se-P', 'I-J', 'F-J'],       # Q1
    ['P',   'Fi',   'Si',  'S-T'],       # Q2
    ['Fi-J','T-J',  'F',   'P'],         # Q3
    ['S',   'N',    'N',   'S'],         # Q4
    ['F',   'T-J',  'Te-P','F'],         # Q5
    ['T',   'F',    'N-P', 'E-P'],       # Q6
    ['T',   'N-P',  'F',   'S-P'],       # Q7
    ['N',   'S',    'N',   'S'],         # Q8
    ['E-F', 'E-T',  'I-T', 'I-F'],       # Q9
    ['I-F', 'F-J',  'T-P', 'E-P'],       # Q10
    ['N-P', 'I',    'E',   'J'],         # Q11
    ['J',   'P',    'I',   'E'],         # Q12
]

TENDENCY = set('einasfjtp')

def opt_votes(dim):
    votes = defaultdict(float)
    if '/' in dim:
        for d in dim.split('/'):
            if d in votes or d in 'EIFNTJPS':
                votes[d] += 1
    elif '-' in dim:
        parts = dim.split('-')
        prefix, suffix = parts[0], parts[1]
        if len(prefix) == 1:
            votes[prefix] += 1
        else:
            votes[prefix[0]] += 1
            if prefix[1].lower() in TENDENCY:
                votes[prefix[1].upper()] += 0.5
        if suffix in votes or suffix in 'EIFNTJPS':
            votes[suffix] += 1
    else:
        votes[dim] += 1
    return dict(votes)

# Precompute
opt_vote_cache = {}
for qi, opts in enumerate(questions_dims):
    for oi, dim in enumerate(opts):
        opt_vote_cache[(qi, oi)] = opt_votes(dim)

dims_list = ['E','I','N','S','F','T','J','P']
results = {}

# Precompute halves
first_half = []
for combo in itertools.product(range(4), repeat=6):
    v = {d: 0.0 for d in dims_list}
    for qi, oi in enumerate(combo):
        for d, val in opt_vote_cache[(qi, oi)].items():
            if d in v:
                v[d] += val
    first_half.append(v)

second_half = []
for combo in itertools.product(range(4), repeat=6):
    v = {d: 0.0 for d in dims_list}
    for qi, oi in enumerate(combo):
        for d, val in opt_vote_cache[(qi+6, oi)].items():
            if d in v:
                v[d] += val
    second_half.append(v)

for fv in first_half:
    for sv in second_half:
        e = fv['E']+sv['E']; i = fv['I']+sv['I']
        n = fv['N']+sv['N']; s = fv['S']+sv['S']
        f = fv['F']+sv['F']; t = fv['T']+sv['T']
        j = fv['J']+sv['J']; p = fv['P']+sv['P']
        t4 = ('E' if e>=i else 'I') + ('N' if n>=s else 'S') + ('F' if f>=t else 'T') + ('J' if j>=p else 'P')
        results[t4] = results.get(t4, 0) + 1

total = 4**12
for k in sorted(results):
    pct = results[k]/total*100
    print(f'{k}: {results[k]:>8}  {pct:5.2f}%')
print(f'Total: {total}')
print()

# Dimension totals
print('=== 维度总票数 ===')
dim_totals = {d: 0.0 for d in dims_list}
for opts in questions_dims:
    for opt in opts:
        for d, val in opt_votes(opt).items():
            if d in dim_totals:
                dim_totals[d] += val
for d in dims_list:
    print(f'  {d}: {dim_totals[d]:.1f}')