from copy import copy


class Computer:
    def __init__(self, program):
        self.memory = copy(program)
        self.pointer = 0
        self.running = True

    def run(self):
        while self.running:
            self.step()

    def step(self):
        op_code = self.memory[self.pointer]
        match op_code:
            case 1:
                in1_idx = self.memory[self.pointer + 1]
                in2_idx = self.memory[self.pointer + 2]
                out_idx = self.memory[self.pointer + 3]
                self.memory[out_idx] = self.memory[in1_idx] + self.memory[in2_idx]
                self.pointer += 4
            case 2:
                in1_idx = self.memory[self.pointer + 1]
                in2_idx = self.memory[self.pointer + 2]
                out_idx = self.memory[self.pointer + 3]
                self.memory[out_idx] = self.memory[in1_idx] * self.memory[in2_idx]
                self.pointer += 4
            case 99:
                self.running = False
            case _:
                raise Exception

def task1():
    global program
    input_file = open("input.txt")
    program = [int(n) for n in input_file.readline().split(",")]

    program[1] = 12
    program[2] = 2

    computer = Computer(program)
    computer.run()
    return computer.memory[0]

def task2():
    global program
    for noun in range(100):
        for verb in range(100):
            program[1] = noun
            program[2] = verb

            computer = Computer(program)
            computer.run()
            if computer.memory[0] == 19690720:
                return 100 * noun + verb

if __name__ == '__main__':
    print(task1())
    print(task2())