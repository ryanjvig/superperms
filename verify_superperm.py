"""

Verify that a provided superpermutation on n symbols is complete.

Command format: python3 verify_superperm.py [n] [superpermutation file]

"""

import sys
from itertools import permutations

if len(sys.argv) != 3:
    print('Invalid number of arguments.')
    sys.exit(1)

### Constants/Parameters ###

n = int(sys.argv[1])
superperm_filename = sys.argv[2]

### Read Superpermutation

def read_superperm() -> str:
    """Read superpermutation from file."""
    res = ''
    with open(superperm_filename, 'r', encoding='utf-8') as file:
        res = file.readlines()[0]
    return res

superperm = read_superperm()

### Output ###

def print_result() -> None:
    """Print verification result of superpermutation."""
    perms = permutations(range(1, n+1))
    perm_strings = [''.join(map(str, perm)) for perm in perms]
    for perm in perm_strings:
        if perm not in superperm:
            print(f'Superpermutation not complete. Missing permutation: {perm}')
            return
    print(f'Superpermutation is complete for n={n}')

print_result()
