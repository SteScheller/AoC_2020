#!/usr/bin/env python3

import math
import numpy as np
from typing import List, Tuple, Union

from scipy.optimize import minimize_scalar

def parse_input(file_path: str) -> Tuple[int, List[int]]:
    with open(file_path) as f:
        lines = f.readlines()
    t = int(lines[0].strip())
    ids = [int(id_) if id_ != 'x' else id_
        for id_ in lines[1].strip().split(',') ]
    return t, ids

def find_subsequent_departure_t(
        ids: List[Union[int, str]], lower_bound: int=0) -> int:
    offsets = dict()
    for i, id_ in enumerate(ids):
        if id_ != 'x':
            offsets[id_] = i
    longest_cycle = sorted(list(offsets.keys()))[-1]
    match = False
    pivot = (lower_bound // longest_cycle) * longest_cycle
    while match is False:
        t = pivot - offsets[longest_cycle]
        match = True
        for line in offsets:
            if (t + offsets[line]) % line > 0:
                match = False
                pivot += longest_cycle
                break
    return t

if __name__ == '__main__':
    t, ids = parse_input('input_test.txt')
    departing_order = sorted(
        [id_ for id_ in ids if id_ != 'x'],
        key=lambda x: (math.ceil(t / x) * x) % t)
    first = departing_order[0]
    print(f'The ID of the earliest bus we can take is {first}.')
    print(f'We have to wait {math.ceil(t / first) * first - t} minutes.')
    #t = find_subsequent_departure_t(ids, lower_bound=100000000000000)
    t = find_subsequent_departure_t(ids, lower_bound=1000)
    print(f'The earliest timestamp satisfying subsequent departures is {t}.')
