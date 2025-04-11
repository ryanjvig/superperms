"""

Translate a symmetric TSP tour representing a solution to the minimal superpermutation problem
on n symbols to the solution's corresponding superpermutation. Designed for compatibility
with .sol files produced by the Concorde TSP solver.

Writes the resulting minimal superpermutation to min_superperm_[n].txt

Command format: python3 make_superperm.py [n] [solution file]

"""

import sys
from itertools import permutations

if len(sys.argv) != 3:
    print('Invalid number of arguments.')
    sys.exit(1)

### Constants/Parameters ###

n = int(sys.argv[1])
solution_filename = sys.argv[2]

perms = list(permutations(range(1, n+1)))
perm_strings = [''.join(map(str, perm)) for perm in perms]

n_perms = len(perms)

### Superpermutation Construction ###

def get_tsp_tour() -> list[int]:
    """Read TSP tour from solution file."""
    res = []
    with open(solution_filename, 'r', encoding='utf-8') as file:
        tour_raw = file.read()
        tour_flat = tour_raw.replace('\n', ' ')
        tour_array = tour_flat.split(' ')
        tour_array_parsed = tour_array[1:-1]
        res = [int(node) for node in tour_array_parsed]
    return res

tsp_tour = get_tsp_tour()

def get_atsp_tour() -> list[int]:
    """Map TSP tour to tour for original ATSP problem."""
    res = [0] * n_perms
    for i in range(n_perms):
        res[i] = tsp_tour[i*2]
    return res

atsp_tour = get_atsp_tour()

def overlap(p: str, q: str) -> int:
    """Compute overlap length between suffix of p and prefix of q."""
    for i in range(n, 0, -1):
        if p[-i:] == q[:i]:
            return i
    return 0

def get_superperm() -> str:
    """Construct superpermutation from sequence of permutations."""
    perm_seq = [perm_strings[i] for i in atsp_tour]
    res = perm_seq[0]
    for i in range(1, n_perms):
        start = overlap(perm_seq[i-1], perm_seq[i])
        res += perm_seq[i][start:]
    return res

superperm = get_superperm()

### Output ###

def write_superperm() -> None:
    """Write superpermutation to text file."""
    with open(f'min_superperm_{n}.txt', 'w', encoding='utf-8') as file:
        file.write(superperm + '\n')
    print(f'Superpermutation length: {len(superperm)}')

write_superperm()
