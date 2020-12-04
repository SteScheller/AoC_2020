import string
import re
from typing import List, Dict, Set, Any

def parse_input(file_path: str) -> List[Dict[str, str]]:
    with open(file_path) as f:
        text = f.read()
    blocks = text.split('\n\n')
    list_of_dictionaries = list()
    for b in blocks:
        d = dict()
        lines = b.splitlines()
        for l in lines:
            items = l.strip().split(' ')
            for item in items:
                k, v = item.split(':')
                d[k] = v
        list_of_dictionaries.append(d)
    return list_of_dictionaries

def check_passport_fields(passport: Dict[str, str], required_fields: List[str]) -> bool:
    return all([field in passport for field in required_fields])

def check_passport_valid(passport: Dict[str, str]) -> bool:
    valid = True
    try:
        if not(1920 <= int(passport['byr']) <= 2002): valid = False;
        if not(2010 <= int(passport['iyr']) <= 2020): valid = False;
        if not(2020 <= int(passport['eyr']) <= 2030): valid = False;
        hgt_v, hgt_u = re.fullmatch(r'([0-9]+)(cm|in)', passport['hgt']).group(1, 2)
        if not (hgt_u in {'cm', 'in'}): valid = False;
        if (hgt_u == 'cm') and not ((150 <= int(hgt_v) <= 193)): valid = False;
        if (hgt_u == 'in') and not ((59 <= int(hgt_v) <= 76)): valid = False;
        if re.fullmatch(r'#[0-9a-f]{6}', passport['hcl']) is None: valid = False;
        if not (passport['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}): valid = False;
        if re.fullmatch(r'[0-9]{9}', passport['pid']) is None: valid = False;
    except (TypeError, AttributeError):
        valid = False
    return valid

if __name__ == '__main__':
    pp = parse_input('input.txt')
    pp_r = [p for p in pp  if check_passport_fields(
        p, ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']) ]
    print('Number of passports with required fields: {}'.format(len(pp_r)))
    pp_v = [p for p in pp_r if check_passport_valid(p)]
    print('Number of valid passports: {}'.format(len(pp_v)))
