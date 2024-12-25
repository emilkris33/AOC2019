masses = []

def task1():
    input_file = open("input.txt")
    for line in input_file.readlines():
        masses.append(int(line))

    output = 0
    for mass in masses:
        output += int(mass/3) - 2
    return output


def calc_fuel(mass):
    value = int(mass/3) - 2
    if value <= 0:
        return 0
    return value + calc_fuel(value)


def task2():
    output = 0
    for mass in masses:
        output += calc_fuel(mass)
    return output

if __name__ == '__main__':
    print(task1())
    print(task2())