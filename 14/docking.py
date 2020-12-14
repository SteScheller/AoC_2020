import re
from typing import List, Tuple, Dict, Any

def parse_input(file_path: str) -> List[Tuple[str, Dict[str, Any]]]:
    with open(file_path) as f:
        lines = f.readlines()

    init_sequence = list()
    for l in lines:
        m = re.match(r'(mask|mem)(\[[0-9]+\]|) = ([X01]{36}|[0-9]+)', l)
        cmd = m.group(1)
        if cmd == 'mask':
            mask = m.group(3)
            init_sequence.append((cmd, {'mask' : mask}))
        elif cmd == 'mem':
            address = int(m.group(2)[1:-1])
            value = int(m.group(3))
            init_sequence.append((cmd, {'addr' : address, 'val' : value}))
    return init_sequence

class DockingProgram:
    def __init__(self):
        self.mem = dict()

    def run_initialization(
            self,
            program: List[Tuple[str, Dict[str, Any]]]):
        mask = 36 * 'X'
        for cmd, data in program:
            if cmd == 'mask': mask = data['mask'];
            elif cmd == 'mem':
                value = data['val']
                value |= int(mask.replace('X', '0'), 2)
                value &= int(mask.replace('X', '1'), 2)
                self.mem[data['addr']] = value

    def _assemble_addresses(self, address: int, mask: str) -> List[int]:
        addresses = list()
        if 'X' in mask:
            pos = mask.find('X')
            addr_s = f'{address:036b}'
            addresses += self._assemble_addresses(
                int(addr_s[:pos] + '0' + addr_s[pos+1:], 2),
                mask.replace('X', '0', 1))
            addresses += self._assemble_addresses(
                address,
                mask.replace('X', '1', 1))
        else:
            address |= int(mask, 2)
            addresses.append(address)

        return addresses

    def run_initialization_v2(
            self,
            program: List[Tuple[str, Dict[str, Any]]]):
        mask = 36 * 'X'
        for cmd, data in program:
            if cmd == 'mask': mask = data['mask'];
            elif cmd == 'mem':
                value = data['val']
                addresses = self._assemble_addresses(data['addr'], mask)
                for addr in addresses:
                    self.mem[addr] = data['val']

    def get_memory(self) -> Dict[int, int]:
        return self.mem

    def reset_memory(self) -> None:
        self.mem = dict()

if __name__ == '__main__':
    init_sequence = parse_input('input.txt')
    p = DockingProgram()
    p.run_initialization(init_sequence)
    mem = p.get_memory()
    print('The sum of all memory values is {0}.'.format(
        sum([mem[key] for key in mem.keys()])) )
    p.reset_memory()
    p.run_initialization_v2(init_sequence)
    mem = p.get_memory()
    print(('The sum of all memory values with version 2 memory decoding is '
        f'{sum([mem[key] for key in mem.keys()])}.') )

