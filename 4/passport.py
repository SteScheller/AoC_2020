import string
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

def check_passport_fields(
        passport: Dict[str, str],
        required_fields: List[str]) -> bool:
    return all([field in passport for field in required_fields])

def check_passport_valid(passport: Dict[str, str]) -> bool:
    valid = True
    try:
        byr = int(passport['byr']) if len(passport['byr']) == 4 else None
        if not((byr >= 1920) and (byr <= 2002)): valid = False;
        iyr = int(passport['iyr']) if len(passport['iyr']) == 4 else None
        if not((iyr >= 2010) and (iyr <= 2020)): valid = False;
        eyr = int(passport['eyr']) if len(passport['eyr']) == 4 else None
        if not((eyr >= 2020) and (eyr <= 2030)): valid = False;
        hgt_unit = passport['hgt'].lstrip(string.digits)
        if not (hgt_unit in {'cm', 'in'}): valid = False;
        else:
            hgt_value = int(passport['hgt'].rstrip(hgt_unit)) #rstrip doesn't check order of chars!
            if (hgt_unit == 'cm') and \
                    not ((hgt_value >= 150) and (hgt_value <= 193)):
                valid = False
            if (hgt_unit == 'in') and \
                    not ((hgt_value >= 59) and (hgt_value <= 76)):
                valid = False
        hcl = passport['hcl']
        if (not hcl.startswith('#')) or (len(hcl) != 7): valid = False;
        elif not all(
                [c in set(string.digits+'abcdef') for c in hcl[1:]]):
            valid = False
        if not (passport['ecl'] in \
                {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}):
            valid = False
        pid = int(passport['pid']) if len(passport['pid']) == 9 else None
        if pid is None: valid = False;
    except (ValueError, KeyError):
        valid = False

    return valid

if __name__ == '__main__':
    passports = parse_input('input.txt')
    passports_with_required_fields = [passport for passport in passports \
        if check_passport_fields(
            passport, ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']) ]
    print('Number of passports with required fields: {}'.format(
        len(passports_with_required_fields) ) )
    valid_passports = [passport for passport in passports_with_required_fields \
        if check_passport_valid(passport)]
    print('Number of valid passports: {}'.format(len(valid_passports)))
