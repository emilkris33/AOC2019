import itertools
from copy import copy
from typing import final

import numpy as np


class Computer:
    def __init__(self, program):
        self.memory = dict(zip(range(len(program)),program))
        self.pointer = 0
        self.relative_base = 0
        self.running = True
        self.input_buffer = []
        self.output_buffer = []

    def read_memory(self, pos):
        if pos in self.memory:
            return self.memory[pos]
        return 0

    def run(self):
        while self.running:
            self.step()
            if len(self.output_buffer) > 0:
                return self.output_buffer.pop(0)

    def get_parameters(self, num_parameters, modes, output_parameter=None):
        modes = modes.zfill(num_parameters)
        parameters = []
        for i in range(1, num_parameters+1):
            if modes[-i] == '1':
                if i == output_parameter:
                    raise Exception("Immediate mode is invalid for output parameter")
                parameters.append(self.pointer + i)
            elif modes[-i] == '0':
                parameters.append(self.memory[self.pointer + i])
            elif modes[-i] == '2':
                parameters.append(self.relative_base + self.memory[self.pointer + i])
            else:
                raise Exception(f"Invalid Parameter mode {modes}")
        return parameters

    def input(self, value):
        self.input_buffer.append(value)

    def step(self):
        op_code = self.memory[self.pointer]
        parameter_modes = str(int(op_code / 100))
        op_code %= 100
        match op_code:
            case 1:
                in1_idx, in2_idx, out_idx = self.get_parameters(3, parameter_modes, 3)
                self.memory[out_idx] = self.read_memory(in1_idx) + self.read_memory(in2_idx)
                self.pointer += 4
            case 2:
                in1_idx, in2_idx, out_idx = self.get_parameters(3, parameter_modes, 3)
                self.memory[out_idx] = self.read_memory(in1_idx) * self.read_memory(in2_idx)
                self.pointer += 4
            case 3:
                out_idx = self.get_parameters(1, parameter_modes, 1)[0]
                if len(self.input_buffer) > 0:
                    self.memory[out_idx] = self.input_buffer.pop(0)
                else:
                    raise Exception("Missing input")
                self.pointer += 2
            case 4:
                in_idx = self.get_parameters(1, parameter_modes)[0]
                self.output_buffer.append(self.memory[in_idx])
                self.pointer += 2
            case 5:
                test_idx, jmp_idx = self.get_parameters(2, parameter_modes)
                if self.memory[test_idx] != 0:
                    self.pointer = self.memory[jmp_idx]
                else:
                    self.pointer += 3
            case 6:
                test_idx, jmp_idx = self.get_parameters(2, parameter_modes)
                if self.memory[test_idx] == 0:
                    self.pointer = self.memory[jmp_idx]
                else:
                    self.pointer += 3
            case 7:
                in1_idx, in2_idx, out_idx = self.get_parameters(3, parameter_modes, 3)
                if self.memory[in1_idx] < self.memory[in2_idx]:
                    self.memory[out_idx] = 1
                else:
                    self.memory[out_idx] = 0
                self.pointer += 4
            case 8:
                in1_idx, in2_idx, out_idx = self.get_parameters(3, parameter_modes, 3)
                if self.memory[in1_idx] == self.memory[in2_idx]:
                    self.memory[out_idx] = 1
                else:
                    self.memory[out_idx] = 0
                self.pointer += 4
            case 9:
                in_idx = self.get_parameters(1, parameter_modes)[0]
                self.relative_base += self.memory[in_idx]
                self.pointer += 2
            case 99:
                self.running = False
            case _:
                raise Exception(f"Unknown opcode {op_code}")

def task1():
    global program
    input_file = open("input.txt")
    program = [int(n) for n in input_file.readline().split(",")]

    size = 100
    grid = np.zeros([size, size])
    visited = np.zeros([size, size])
    pos = (int(size/2), int(size/2))
    direction = (-1, 0)

    robot = Computer(program)
    while True:
        robot.input(int(grid[pos]))
        color = robot.run()
        if color is None:
            break
        grid[pos] = color
        visited[pos] = 1
        turn = robot.run()
        if turn is None:
            break
        elif turn == 0:
            direction = (-direction[1], direction[0])
        elif turn == 1:
            direction = (direction[1], -direction[0])
        else:
            raise Exception
        pos = (pos[0] + direction[0], pos[1] + direction[1])
    return int(np.sum(visited))

def task2():
    size = 100
    grid = np.zeros([size, size])
    pos = (int(size / 2), int(size / 2))
    direction = (-1, 0)
    grid[pos] = 1

    robot = Computer(program)
    while True:
        robot.input(int(grid[pos]))
        color = robot.run()
        if color is None:
            break
        grid[pos] = color
        turn = robot.run()
        if turn is None:
            break
        elif turn == 0:
            direction = (-direction[1], direction[0])
        elif turn == 1:
            direction = (direction[1], -direction[0])
        else:
            raise Exception
        pos = (pos[0] + direction[0], pos[1] + direction[1])
    return 0

if __name__ == '__main__':
    print(task1())
    print(task2())