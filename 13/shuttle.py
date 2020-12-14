#!/usr/bin/env python3

import math
import numpy as np
from typing import List, Tuple, Union

def parse_input(file_path: str) -> Tuple[int, List[Union[int, str]]]:
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
    shortest_cycle = sorted(list(offsets.keys()))[0]
    longest_cycle = sorted(list(offsets.keys()))[-1]
    cycles = sorted(list(offsets.keys()))
    match = False
    pivot = (lower_bound // longest_cycle) * longest_cycle
    inc = np.lcm(shortest_cycle, longest_cycle)
    inc = np.lcm(cycles[-2], cycles[-1])
    #l = [max((id_ - offsets[id_]), 1) for id_ in offsets]
    #inc = np.lcm.reduce(l)
    print(longest_cycle, inc)
    while match is False:
        t = pivot - offsets[longest_cycle]
        match = True
        for line in offsets:
            if (t + offsets[line]) % line > 0:
                match = False
                pivot += inc
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
    t = find_subsequent_departure_t(ids, lower_bound=0)
    print(f'The earliest timestamp satisfying subsequent departures is {t}.')


    assert(t == 1068781)
    print('\nReal input:')
    t, ids = parse_input('input.txt')
    t = find_subsequent_departure_t(ids, lower_bound=100000000000000)
    print(f'The earliest timestamp satisfying subsequent departures is {t}.')