#!/usr/bin/env python3

from typing import Set, List, Callable
import operator
import string

def parse_input(file_path: str) -> List[Set[str]]:
    with open('input.txt') as f:
        text = f.read()
    blocks = text.split('\n\n')
    return blocks

def build_sets(blocks: List[str], op: Callable=operator.or_) -> List[Set[str]]:
    sets = list()
    for b in blocks:
        s = set(string.ascii_letters)
        for l in b.splitlines():
            s = op(s, set(l))
        sets.append(s)
    return sets

if __name__ == '__main__':
    blocks = parse_input('input.txt')
    print('Sum of "any yes" in groups: {}'.format(
        sum([len(y) for y in build_sets(blocks, operator.or_)]) ) )
    print('Sum of "all yes" in groups: {}'.format(
        sum([len(y) for y in build_sets(blocks, operator.and_)]) ) )

