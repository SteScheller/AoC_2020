import itertools
from typing import List

def parse_input(file_path: str) -> List[int]:
    with open(file_path) as f:
        numbers = [int(l) for l in f.readlines()]
    return numbers

def find_num(inp: List[int], length_preamble: int=25) -> int:
    for i, x in enumerate(inp[length_preamble:]):
        num_set = inp[i:(i + length_preamble)]
        if x not in [a + b for a, b in itertools.combinations(num_set, 2)]:
            return x

def find_summands(x: int, inp: List[int], min_range_length: int=2):
    for rl in range(min_range_length, len(inp) + 1):
        for i in range(len(inp) - rl):
            summands = inp[i:(i + rl)]
            if sum(summands) == x:
                return summands

if __name__ == '__main__':
    inp = parse_input('input.txt')
    x = find_num(inp)
    print(f'{x} is not the sum of two of 25 numbers before it.')
    summands = find_summands(x, inp)
    print(f'The contigous range {summands} sums up to: {sum(summands)}')
    print(('The sum of the smallest and largest number in this range is: '
        f'{min(summands) + max(summands)}'))
