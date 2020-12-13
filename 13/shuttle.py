#!/usr/bin/env python3

import math
from typing import List, Tuple, Union

from scipy.optimize import minimize_scalar

def parse_input(file_path: str) -> Tuple[int, List[int]]:
    with open(file_path) as f:
        lines = f.readlines()
    t = int(lines[0][:-1])
    ids = [int(id) if id != 'x' else id for id in lines[1][:-1].split(',') ]
    return t, ids

def find_subsequent_departure_t(
        ids: List[Union[int, str]],
        limits: Tuple[int, int]=(0, math.inf) ) -> int:
    target = [(id, i) for i, id in enumerate(ids) if id != 'x']
    def loss(t: float):
        nonlocal target
        d = [((t + i) % id)**2 for id, i in target]
        return sum(d)

    res = minimize_scalar(
            loss,
            method='bounded',
            #bounds=(1.0e6, 1.1e6),
            #bounds=(1068780, 1068782),
            bounds=(1068480, 1069000),
            options={
                'maxiter' : 1e6 }
            )

    print(res)
    return res.x

if __name__ == '__main__':
    t, ids = parse_input('input_test.txt')
    departing_order = sorted(
        [id for id in ids if id != 'x'],
        key=lambda x: (math.ceil(t / x) * x) % t)
    first = departing_order[0]
    print(f'The ID of the earliest bus we can take is {first}.')
    print(f'We have to wait {math.ceil(t / first) * first - t} minutes.')
    t = find_subsequent_departure_t(ids)
    print(f'The earliest timestamp satisfying subsequent departures is {t}.')
    print([round(t + i) % id for i, id in enumerate(ids) if id != 'x'])


