#!/usr/bin/env python3

import itertools
from copy import copy

import numpy as np
from scipy.ndimage import convolve

def parse_input(file_path: str) -> np.ma.masked_array:
    with open(file_path) as f:
        lines = f.readlines()
    seats = np.zeros((len(lines), len(lines[0][:-1])), np.int32)
    for i, l in enumerate(lines):
        for j, c in enumerate(l[:-1]):
            if c == '.': seats[i,j] = -1
            if c == '#': seats[i,j] = 1
    return np.ma.masked_values(seats, -1)

def simulate_people_adjacent(old: np.array) -> np.array:
    kernel = np.ones((3, 3), np.int32)
    kernel[1, 1] = 0
    new = convolve(np.clip(old, 0, None), kernel, mode='constant')
    shape = new.shape
    for row, col in itertools.product(range(shape[0]), range(shape[1])):
        if old.mask[row, col]: new[row, col] = -1;
        elif new[row, col] == 0: new[row, col] = 1;
        elif new[row, col] >= 4: new[row, col] = 0;
        else: new[row, col] = old[row, col]
    return np.ma.masked_values(new, -1)

def simulate_people_see(old: np.array) -> np.array:
    new = copy(old)
    shape = new.shape
    for row, col in itertools.product(range(shape[0]), range(shape[1])):
        if old.mask[row, col]:
            new[row, col] = -1
            continue
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, 1), (1, -1), (-1, -1) ]
        occ = 0
        for dir in directions:
            rr, cc = row + dir[0], col + dir[1]
            while (0 <= rr < old.shape[0]) and (0 <= cc < old.shape[1]):
                if old[rr, cc] == 1:
                    occ += 1
                    break
                if old[rr, cc] == 0: break;
                rr, cc = rr + dir[0], cc + dir[1]
        if occ == 0: new[row, col] = 1;
        elif occ >= 5: new[row, col] = 0;
        else: new[row, col] = old[row, col]
    return np.ma.masked_values(new, -1)

if __name__ == '__main__':
    seats = parse_input('input.txt')
    old = copy(seats)
    new = np.zeros_like(old)
    while not np.array_equal(new, old):
        old = new
        new = simulate_people_adjacent(old)
    print((f'{np.sum(new)} seats end up occupied if people only care about '
        'adjacent seats.'))
    old = copy(seats)
    new = np.zeros_like(old)
    while not np.array_equal(new, old):
        old = new
        new = simulate_people_see(old)
    print((f'{np.sum(new)} seats end up occupied if people only care about '
        'the next seats they see.'))

