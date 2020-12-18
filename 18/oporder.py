#!/usr/bin/env python3

import re
from functools import reduce
from operator import add, mul
from typing import List

def parse_input(file_path: str) -> List[str]:
    with open(file_path) as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

def compute_expression(expr: str, precedence: bool=False) -> int:
    def eval_parentheses(term: str):
        numbers = [int(i) for i in re.findall(r'[\d]+', term)]
        ops = [add if op == '+' else mul
                for op in re.findall(r'(\+|\*)', term)]
        f = lambda a, b: ops.pop(0)(a, b)
        return reduce(f, numbers)

    def add_parentheses(expr: str) -> str:
        m = re.search(r'[\d]+ \+ [\d]+', expr)
        if m: expr = expr.replace(m.group(0), f'({m.group(0)})');
        return expr

    expr = f'({expr})'
    m = True
    while m:
        m = re.search(r'[\d \+\*]*(\([\d \+\*]+\))[\d \+\*]*', expr)
        if m:
            term = m.group(1)
            if precedence and (('*' in term) and ('+' in term)):
                term = add_parentheses(term)
                expr = expr.replace(m.group(1), term)
                continue
            value = eval_parentheses(term)
            expr = expr.replace(m.group(1), str(value))

    return int(expr)

if __name__ == '__main__':
    expressions = parse_input('input.txt')
    results = [compute_expression(e) for e in expressions]
    print(f'The sum of the results is {sum(results)}.')
    results = [compute_expression(e, True) for e in expressions]
    print(('The sum of the results with different precedence levels is '
        f'{sum(results)}.'))

