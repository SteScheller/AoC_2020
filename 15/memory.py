#!/usr/bin/env python3

from typing import Tuple

def parse_input(file_path: str, line_num: int=0) -> Tuple[int]:
    with open(file_path) as f:
        lines = f.readlines()
    numbers = [int(n) for n in lines[line_num].strip().split(',')]
    return numbers

def get_spoken_number(
        starting_numbers: Tuple[int, int, int], n: int=2020) -> int:
    mem = dict()
    for i, num in enumerate(starting_numbers):
        x = num
        if not i == len(starting_numbers) - 1: mem[num] = i
    last = starting_numbers[-1]
    for i in range(len(starting_numbers), n):
        if last in mem: x = (i-1) - mem[last];
        else: x = 0;
        mem[last] = i-1
        last = x
    return x

if __name__ == '__main__':
    numbers = parse_input('input.txt')
    for n in (2020, 30000000):
        print(f'The {n}th spoken number is {get_spoken_number(numbers, n)}.')

