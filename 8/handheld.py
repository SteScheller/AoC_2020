import copy
from typing import List, Tuple, Any

class VirtualMachine:
    def __init__(self):
        self._acc = 0
        self._pc = 0

        self.commands = {
            'nop' : (self._nop_op, [int], []),
            'acc' : (self._acc_op, [int], []),
            'jmp' : (self._jmp_op, [int], [])
        }

    def _nop_op(self, _: int) -> None:
        self._pc += 1

    def _acc_op(self, value: int) -> None:
        self._acc += value
        self._pc += 1

    def _jmp_op(self, value: int) -> None:
        self._pc += value

    def execute_instruction(self, command: str, *args: Tuple[str]) -> Any:
        cmd, arg_types, ret_types = self.commands[command]
        ret_values = cmd(*[arg_types[i](a) for i, a in enumerate(args)])
        if ret_values is not None:
            ret_values = [ret_types[i](r) for i, r in enumerate(ret_values)]
        return ret_values

    def execute_program(
            self,
            p: List[Tuple[str, List[str]]],
            reset: bool=True,
            break_on_loop: bool=False) -> Any:
        if reset:
            self._acc = 0
            self._pc = 0
        if break_on_loop:
            executed_commands = set()

        while self._pc < len(p):
            ret_values = self.execute_instruction(
                p[self._pc][0], *(p[self._pc][1]) )
            if break_on_loop:
                if not self._pc in executed_commands: executed_commands.add(self._pc);
                else: return (1, self._pc, self._acc, ret_values);

        return (0, self._pc, self._acc, ret_values)

def parse_input(file_path:str) -> List[Tuple[str, List[str]]]:
    with open(file_path) as f:
        lines = f.readlines()
    program = [(l.split()[0], l.split()[1:]) for l in lines]
    return program

if __name__ == '__main__':
    p_orig = parse_input('input.txt')
    vm = VirtualMachine()
    for i in range(len(p_orig)):
        p_modified = copy.deepcopy(p_orig)
        if p_modified[i][0] == 'nop': p_modified[i] = ('jmp', p_modified[i][1]);
        elif p_modified[i][0] == 'jmp': p_modified[i] = ('nop', p_modified[i][1]);
        ret_value = vm.execute_program(p_modified, break_on_loop=True)
        print('Program terminated with code {0} : pc={1}, acc={2}, values={3}'.format(*ret_value))
        if ret_value[0] == 0: break;
