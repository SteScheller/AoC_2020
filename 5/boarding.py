import functools
from typing import List

def compute_seat_id(s: str) -> int:
    return int(s.strip().replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2)

def find_seat(ids: List[int], max_id: int=1023) -> int:
    total_sum = sum([i for i in range(max_id + 1)])
    min_sum = sum([i for i in range(min(ids))])
    max_sum = sum([i for i in range(max(ids) + 1, max_id + 1)])
    return total_sum - min_sum - max_sum - sum(ids)

if __name__ == '__main__':
    with open('input.txt') as f:
        seats = f.readlines()
    ids = [compute_seat_id(s) for s in seats]
    print('Highest seat ID: {}'.format(max(ids)))
    print('My seat ID: {}'.format(find_seat(ids)))
