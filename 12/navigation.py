#!/usr/bin/env python3

import re
import math
from typing import List, Tuple

def parse_input(file_path: str) -> List[Tuple[str, int]]:
    with open(file_path) as f:
        lines = f.readlines()
    instructions = list()
    for l in lines:
        m = re.fullmatch(r'(N|S|E|W|L|R|F)([\d]+)\n', l)
        instructions.append((m.group(1), int(m.group(2))))
    return instructions

class Ferry:
    def __init__(self):
        self.pos = (0, 0)
        self.wp = (10, 1)
        self.angle = 0

    def rotate(self, angle: int) -> None:
        self.angle += angle
        if self.angle < 0:  self.angle = -1 * (abs(self.angle) % 360);
        else: self.angle %= 360

    def forward(self, distance: int) -> None:
        x = round(math.cos(self.angle / 180 * math.pi) * distance)
        y = round(math.sin(self.angle / 180 * math.pi) * distance)
        self.pos = self.pos[0] + x, self.pos[1] + y

    def move(self, inst: Tuple[str, int]) -> None:
        action, value = inst
        if action == 'N': self.pos = (self.pos[0], self.pos[1] + value);
        elif action == 'S': self.pos = (self.pos[0], self.pos[1] - value);
        elif action == 'E': self.pos = (self.pos[0] + value, self.pos[1]);
        elif action == 'W': self.pos = (self.pos[0] - value, self.pos[1]);
        elif action == 'L': self.rotate(value);
        elif action == 'R': self.rotate(-1 * value);
        elif action == 'F': self.forward(value);

    def rotate_waypoint(self, angle: int) -> None:
        d = math.sqrt(self.wp[0]**2 + self.wp[1]**2)
        angle += math.atan2(self.wp[1], self.wp[0]) / math.pi * 180
        if angle < 0:  angle = -1 * (abs(angle) % 360);
        else: angle %= 360
        self.wp = (
            round(math.cos(angle / 180 * math.pi) * d),
            round(math.sin(angle / 180 * math.pi) * d) )

    def forward_waypoint(self, distance: int) -> None:
        self.pos = (
                self.pos[0] + distance * self.wp[0],
                self.pos[1] + distance * self.wp[1] )

    def move_waypoint(self, inst: Tuple[str, int]) -> None:
        action, value = inst
        if action == 'N': self.wp = (self.wp[0], self.wp[1] + value);
        elif action == 'S': self.wp = (self.wp[0], self.wp[1] - value);
        elif action == 'E': self.wp = (self.wp[0] + value, self.wp[1]);
        elif action == 'W': self.wp = (self.wp[0] - value, self.wp[1]);
        elif action == 'L': self.rotate_waypoint(value);
        elif action == 'R': self.rotate_waypoint(-1 * value);
        elif action == 'F': self.forward_waypoint(value);

    def get_position(self) -> None:
        return self.pos

    def get_waypoint(self) -> None:
        return self.wp

if __name__ == '__main__':
    instructions = parse_input('input.txt')
    ferry = Ferry()
    for inst in instructions:
        ferry.move(inst)
    pos = ferry.get_position()
    print(('The ferry\'s Manhatten distance from its starting positions is '
        f'{abs(pos[0]) + abs(pos[1])}.'))
    ferry = Ferry()
    for inst in instructions:
        ferry.move_waypoint(inst)
    pos = ferry.get_position()
    print(('The ferry\'s Manhatten distance from its starting positions is '
        f'{abs(pos[0]) + abs(pos[1])} when using the waypoint method.'))

