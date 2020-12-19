#!/usr/bin/env python3

import re
import string
import itertools
from typing import List

def parse_input(file_path: str) -> List[str]:
    with open(file_path) as f:
        lines = f.readlines()
    rules = dict()
    messages = list()
    for l in lines:
        if l[0] in string.digits:
            num, rule = l.split(':')
            rules[int(num)] = rule.strip()
        elif l[0] in 'ab':
            messages.append(l.strip())

    return rules, messages

def check_rule(rules: ..., num_rule: int, message: str) -> bool:
    def assemble_rule(rule: str, num_rule: int):
        options = list()
        for option in rule.split('|'):
            word = ''
            elements = re.findall(r'([\d]+|[a-b]+)', option)
            if str(num_rule) in elements:
                group_name = itertools.cycle(['first', 'second'])
                wrap = lambda x: f'(?P<{next(group_name)}_{num_rule}>{x})+'
                elements = [elem for elem in elements if elem != str(num_rule)]
            else:
                wrap = lambda x: x
            for elem in elements:
                if elem.isnumeric():
                    num = int(elem)
                    word += wrap(assemble_rule(rules[num], num))
                else:
                    word += elem
            options.append(word)
        return (f'({"|".join(options)})' if len(options) > 1
                else f'{options[0]}')

    rule = assemble_rule(rules[num_rule], num_rule)
    m = re.fullmatch(rule, message)
    if m:
        groups = m.groupdict()
        if ('first_11' in groups) and ('second_11' in groups):
            if len(groups['first_11'] or []) != len(groups['second_11'] or []):
                m = None

    return not(m is None)

if __name__ == '__main__':
    rules, messages = parse_input('input_one.txt')
    checks = [check_rule(rules, 0, m) for m in messages]
    print(('The number of messages that matches rule 0 of the first input is '
        f'{sum(checks)}'))
    rules, messages = parse_input('input_two.txt')
    checks = [check_rule(rules, 0, m) for m in messages]
    print(('The number of messages that matches rule 0 of the second input is '
        f'{sum(checks)}'))

