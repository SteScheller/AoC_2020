#!/usr/bin/env python3

from typing import List, Tuple, Any

def parse_input(
        input_path: str) -> List[Tuple[Tuple[str, Tuple[int, int]], str]]:
    with open(input_path) as f:
        lines = f.readlines()
    parsed = list()
    for line in lines:
        policy, pw = line.split(':')
        count, symbol = policy.strip().split(' ')
        count = tuple([int(c) for c in count.split('-')])
        parsed.append(((symbol, count), pw.strip()))
    return parsed

def check_password_policy_total(
        policy: Tuple[str, Tuple[int, int]], pw: str) -> bool:
    count = pw.count(policy[0])
    return ((count >= policy[1][0]) and (count <= policy[1][1]))

def check_password_policy_positional(
        policy: Tuple[str, Tuple[int, int]], pw: str) -> bool:
    count = sum((
        pw[policy[1][0] - 1] == policy[0],
        pw[policy[1][1] - 1] == policy[0]))
    return (count == 1)

if __name__ == '__main__':
    policy_pw = parse_input('input.txt')
    print('Number of valid passwords with total count policy: {0}'.format(
        sum([check_password_policy_total(item[0], item[1]) \
            for item in policy_pw]) ) )
    print('Number of valid passwords with positional count policy: {0}'.format(
        sum([check_password_policy_positional(item[0], item[1]) \
            for item in policy_pw]) ) )

