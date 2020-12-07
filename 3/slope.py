import itertools
import functools
import operator
from typing import Tuple

import numpy as np

def parse_input(file_path: str) -> np.array:
    with open(file_path) as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]
    h, w = len(lines), len(lines[0])
    slope = np.zeros((h, w), dtype=np.int32)
    for x, y in itertools.product(range(w), range(h)):
        slope[y][x] = 1 if lines[y][x] == '#' else 0
    return slope

def count_trees(
        slope: np.array,
        v: Tuple[int, int],
        p0: Tuple[int, int] = (0, 0)) -> int:
    p = np.array(p0)
    v = np.array(v)
    trees = 0
    while p[1] < slope.shape[0]:
        trees += slope[p[1]][p[0] % slope.shape[1]]
        p += v
    return trees

if __name__ == '__main__':
    slope = parse_input('input.txt')
    print('Number of encountered trees: {}'.format(count_trees(slope, (3,1))))
    tree_counts = [count_trees(slope, v) for v in \
        [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)] ]
    print('Product of encountered trees with different trajectories: {}'.format(
        int(functools.reduce(lambda x,y: float(x*y), tree_counts)) ) )