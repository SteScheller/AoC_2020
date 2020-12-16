import re
import functools
import operator
import itertools
from typing import List, Tuple, Dict

def parse_input(file_path: str
        ) -> Tuple[Dict[str, List[range]], List[int], List[List[int]]]:
    with open(file_path) as f:
        lines = f.readlines()
    rules = dict()
    mine = list()
    nearby = list()
    for i, l in enumerate(lines):
        if re.match(r'your ticket:', l):
            mine = [int(n) for n in lines[i+1].strip().split(',')]
            continue
        if re.match(r'nearby tickets:', l):
            for ll in lines[i+1:]:
                nearby.append([int(n) for n in ll.strip().split(',')])
            continue
        m = re.match(r'([a-z ]+): ([\d]+-[\d]+) or ([\d]+-[\d]+)', l)
        if m:
            field, range1, range2 = m.groups()
            ranges = list()
            for r in (range1, range2):
                lb, ub = [int(n) for n in r.split('-')]
                ranges.append(range(lb, ub+1))
            rules[field] = ranges
    return rules, mine, nearby

def find_invalid_values(
        rules: Tuple[Dict[str, List[range]]], ticket: List[int]) -> List[int]:
    invalid_values = list()
    for val in ticket:
        valid = False
        for r in rules:
            if (val in rules[r][0]) or (val in rules[r][1]):
                valid = True
                break
        if not valid: invalid_values.append(val);
    return invalid_values

def determine_field_order(
        rules: Tuple[Dict[str, List[range]]], tickets: List[List[int]]
        ) -> Dict[str, int]:
    field_order = dict()
    indices = [i for i in range(len(tickets[0]))]
    for p in itertools.permutations(indices, len(indices)):
        for i, r in enumerate(rules):
            field_order[r] = p[i]
        valid = True
        for r, t in itertools.product(rules, tickets):
            if not ((t[field_order[r]] in rules[r][0]) or
                    (t[field_order[r]] in rules[r][1])):
                valid = False
                break
        if valid: break;
        else: field_order = dict()
    return field_order

if __name__ == '__main__':
    rules, mine, nearby = parse_input('input.txt')
    invalid_values = list()
    valid_tickets = list()
    for n in nearby:
        values = find_invalid_values(rules, n)
        if values: invalid_values += values;
        else: valid_tickets.append(n)
    print(f'The ticket scanning error rate is {sum(invalid_values)}.')
    field_order = determine_field_order(rules, valid_tickets)
    print(field_order)
    l = [mine[field_order[r]] for r in rules if r.startswith('departure')]
    print(l)
    multiplied = functools.reduce(
        operator.mul,
        [mine[field_order[r]] for r in rules if r.startswith('departure')])
    print('The result of multiplying all fields in my ticket that start with '
        f'"departure" is {multiplied}')

