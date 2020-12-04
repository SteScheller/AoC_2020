#!/usr/bin/env python3

from typing import Tuple, List

def find_summands(
        s: int, numbers: List[int], num_summands: int=2) -> Tuple[int, int]:
    numbers.sort()
    for i, x in enumerate(numbers):
        if s == x and num_summands == 1:
            return x
        elif s - x > 0:
            summands = find_summands(s-x, numbers[:i]+numbers[i+1:], num_summands-1)
            if type(summands) == int: summands = [summands];
            if (summands is not None) and (len(summands)+1 == num_summands):
                return [x] + summands
        else: break;

if __name__ == '__main__':
    with open('input.txt') as f:
        numbers = [int(i) for i in f.readlines()]
    try:
        x, y = find_summands(2020, numbers, 2)
        print('{0} + {1} = {2} -> {0} * {1} = {3}'.format(x, y, x+y, x*y))
        x, y, z = find_summands(2020, numbers, 3)
        print('{0} + {1} + {2} = {3} -> {0} * {1} * {2} = {4}'.format(x, y, z, x+y+z, x*y*z))
    except ValueError:
        print('No matching summands found..')

