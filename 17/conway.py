import itertools
from typing import Tuple

import numpy as np
from scipy.ndimage import convolve

def parse_input(file_path: str) -> np.array:
    with open(file_path) as f:
        lines = [l.strip() for l in f.readlines()]
    x, y, z =  len(lines), len(lines[0]), 1
    slice_ = np.zeros((z, y, x), dtype=np.int32)
    for i, j in itertools.product(range(x), range(y)):
        slice_[0][j][i] = 1 if lines[j][i] == '#' else 0
    return slice_

def simulate_cycle_3D(old_cube: np.array) -> np.array:
    kernel = np.ones((3, 3, 3), np.int32)
    kernel[1, 1, 1] = 0

    old_cube = np.pad(
        old_cube, ((1, 1), (1, 1), (1, 1)), mode='constant', constant_values=0)
    new_cube = convolve(old_cube, kernel, mode='constant')

    sz, sy, sx = new_cube.shape
    for z, y, x in itertools.product(range(sz), range(sy), range(sx)):
        if old_cube[z, y, x] == 1:
            if (2 <= new_cube[z, y, x] <= 3): new_cube[z, y, x] = 1;
            else: new_cube[z, y, x] = 0;
        if old_cube[z, y, x] == 0:
            if new_cube[z, y, x] == 3: new_cube[z, y, x] = 1;
            else: new_cube[z, y, x] = 0;

    return new_cube

def simulate_cycle_4D(old_cube: np.array) -> np.array:
    kernel = np.ones((3, 3, 3, 3), np.int32)
    kernel[1, 1, 1, 1] = 0

    old_cube = np.pad(
        old_cube, ((1, 1), (1, 1), (1, 1), (1, 1)),
        mode='constant', constant_values=0)
    new_cube = convolve(old_cube, kernel, mode='constant')

    sw, sz, sy, sx = new_cube.shape
    for w, z, y, x in itertools.product(
            range(sw), range(sz), range(sy), range(sx)):
        if old_cube[w, z, y, x] == 1:
            if (2 <= new_cube[w, z, y, x] <= 3): new_cube[w, z, y, x] = 1;
            else: new_cube[w, z, y, x] = 0;
        if old_cube[w, z, y, x] == 0:
            if new_cube[w, z, y, x] == 3: new_cube[w, z, y, x] = 1;
            else: new_cube[w, z, y, x] = 0;

    return new_cube

if __name__ == '__main__':
    initial = parse_input('input.txt')
    cube = initial
    for t in range(6):
        cube = simulate_cycle_3D(cube)
    print(f'{np.sum(cube)} cubes are active after {t+1} cycles in 3D.')
    cube = initial.reshape([1] + list(initial.shape))
    for t in range(6):
        cube = simulate_cycle_4D(cube)
    print(f'{np.sum(cube)} cubes are active after {t+1} cycles in 4D.')
