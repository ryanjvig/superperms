"""

Create an instance of the symmetric traveling salesman problem in TSPLIB format
representing the minimal superpermutation problem on n symbols.

Writes the resulting TSPLIB file to [n].tsp

Command format: python3 make_tsp.py [n]

"""

import sys
from itertools import permutations

if len(sys.argv) != 2:
    print('Invalid number of arguments.')
    sys.exit(1)

### Constants/Parameters ###

n = int(sys.argv[1])

tsp_buffer = 3*n + 1
ordered = tuple(range(n))
perms = list(permutations(range(n)))

n_perms = len(perms)
two_n_perms = n_perms * 2

INF = (tsp_buffer + n) * n_perms
INF_STR = str(INF)

### ATSP Construction ###

def atsp_distance(p: tuple, q: tuple) -> int:
    """Asymmetric TSP weight."""
    if q == ordered:
        return 0

    for i in range(n+1):
        if p[i:] == q[:n-i]:
            return i
    return INF

def make_atsp() -> list[int]:
    """Generate ATSP problem representing the minimal superpermutation problem on n symbols."""
    res = []
    for perm_p in perms:
        res.append([atsp_distance(perm_p, perm_q) for perm_q in perms])
    return res

atsp = make_atsp()

### ATSP to Symmetric TSP (Jonker-Volgenant) Transformation ###

def tsp_distance(i: int, j: int) -> int:
    """Symmetric TSP weight."""
    if i == j:
        return 0

    res = atsp[i][j] + tsp_buffer
    return res

def tsp_distance_str(i: int, j: int) -> str:
    """Symmetric TSP weight formatted as a string."""
    res = str(tsp_distance(i, j))
    return res

def make_tsp() -> list[str]:
    """Generate (string-formatted) TSP problem from ATSP problem."""
    res = []
    for i in range(n_perms):
        res.append([INF_STR] * (n_perms - i - 1) + [tsp_distance_str(i, j) for j in range(n_perms)])

    for i in range(n_perms - 1, 0, -1):
        res.append([INF_STR] * i)
    return res

tsp = make_tsp()

### Output ###

def write_tsp() -> None:
    """Write TSP problem to file in TSPLIB format."""
    with open(f'{n}.tsp', 'w', encoding='utf-8') as file:
        file.write(
            f'NAME : minsuperperm{n}\n'
            'TYPE : TSP\n'
            f'DIMENSION : {two_n_perms}\n'
            'EDGE_WEIGHT_TYPE : EXPLICIT\n'
            'EDGE_WEIGHT_FORMAT : UPPER_ROW\n'
            'NODE_COORD_TYPE : NO_COORDS\n'
            'DISPLAY_DATA_TYPE : NO_DISPLAY\n'
            'EDGE_WEIGHT_SECTION :\n'
        )
        for row in tsp:
            line = ' '.join(row) + '\n'
            file.write(line)

write_tsp()
