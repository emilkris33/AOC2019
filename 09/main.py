import itertools
from copy import copy
from typing import final


class Computer:
    def __init__(self, program):
        self.memory = dict(zip(range(len(program)),program))
        self.pointer = 0
        self.relative_base = 0
        self.running = True
        self.input_buffer = []
        self.output_buffer = []

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
                self.memory[out_idx] = self.memory[in1_idx] + self.memory[in2_idx]
                self.pointer += 4
            case 2:
                in1_idx, in2_idx, out_idx = self.get_parameters(3, parameter_modes, 3)
                self.memory[out_idx] = self.memory[in1_idx] * self.memory[in2_idx]
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

    A = Computer(program)
    A.input(1)
    output = A.run()
    return output

def task2():
    A = Computer(program)
    A.input(2)
    output = A.run()
    return output

if __name__ == '__main__':
    print(task1())
    print(task2())