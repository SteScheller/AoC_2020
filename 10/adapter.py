#!/usr/bin/env python3

from copy import copy
import itertools
import functools
import operator
from typing import List, Dict

def parse_input(file_path: str) -> List[int]:
    with open(file_path) as f:
        numbers = [int(l) for l in f.readlines()]
    return numbers

def compute_differences(adapters: List[int]) -> Dict[int, int]:
    differences = dict()
    adapters.sort()
    for i in range(len(adapters) - 1):
        diff = adapters[i+1] - adapters[i]
        differences[diff] = differences.setdefault(diff, 0) + 1
    return differences

def count_arrangements(adapters: List[int]) -> int:
    sub_lists = list()
    remains = sorted(copy(adapters))
    while len(remains) > 0:
        idx = 0
        while idx < (len(remains) - 1):
            if (remains[idx + 1] - remains[idx]) == 3: break;
            else: idx += 1;
        sub_lists.append(remains[:idx+1])
        remains = remains[idx+1:]

    factors = list()
    for n_l, l in enumerate(sub_lists):
        if n_l == 0: lower, l, upper = 0, l[0:-1], l[-1];
        else: lower, l, upper = l[0], l[1:-1], l[-1];
        num_combinations = 0
        for count in range(0, len(l) + 1):
            for combi in itertools.combinations(l, count):
                if (len(combi) == 0) and ((upper - lower) > 3): continue;
                if (count > 1):
                    if (min(combi) - lower) > 3: continue;
                    if (upper - max(combi)) > 3: continue;
                    differences = \
                        [combi[i+1] - combi[i] for i in range(len(combi) - 1)]
                    if max(differences) > 3: continue;
                num_combinations += 1;
        factors.append(num_combinations)

    return functools.reduce(operator.mul, factors)

if __name__ == '__main__':
    adapters = parse_input('input.txt')
    differences = compute_differences([0] + adapters + [max(adapters) + 3])
    print(('The product of 1-jolt and 3-jolt differences is '
        f'{differences[1] * differences[3]}.'))
    print(f'There are {count_arrangements(adapters)} working arrangements.')

