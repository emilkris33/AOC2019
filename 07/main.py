import itertools
from copy import copy
from typing import final


class Computer:
    def __init__(self, program):
        self.memory = copy(program)
        self.pointer = 0
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
            case 99:
                self.running = False
            case _:
                raise Exception(f"Unknown opcode {op_code}")

def get_max_signal(inp, depth, phase_options):
    max_signal = 0
    for a in phase_options:
        A = Computer(program)
        A.input(a)
        A.input(inp)
        output = A.run()
        if depth > 1:
            new_phase_options = copy(phase_options)
            new_phase_options.remove(a)
            output = get_max_signal(output, depth-1, new_phase_options)
        if output > max_signal:
            max_signal = output
    return max_signal

def task1():
    global program
    input_file = open("input.txt")
    program = [int(n) for n in input_file.readline().split(",")]

    return get_max_signal(0, 5, [n for n in range(5)])

def task2():
    final_out = 0
    for a, b, c, d, e in itertools.permutations([5,6,7,8,9]):
        A = Computer(program)
        B = Computer(program)
        C = Computer(program)
        D = Computer(program)
        E = Computer(program)

        A.input(a)
        B.input(b)
        C.input(c)
        D.input(d)
        E.input(e)

        run_out = None
        A.input(0)
        while A.running:
            a_out = A.run()
            B.input(a_out)
            b_out = B.run()
            C.input(b_out)
            c_out = C.run()
            D.input(c_out)
            d_out = D.run()
            E.input(d_out)
            e_out = E.run()
            A.input(e_out)
            if e_out is not None:
                run_out = e_out

        if run_out > final_out:
            final_out = run_out

    return final_out

if __name__ == '__main__':
    print(task1())
    print(task2())