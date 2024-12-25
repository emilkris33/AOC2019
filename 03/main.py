
def task1():
    input_file = open("input.txt")
    wires = []
    for line in input_file.readlines():
        wires.append([n for n in line.strip().split(',')])

    global wire_points
    wire_points = [{}, {}]
    for i, wire in enumerate(wires):
        X = 0
        Y = 0
        steps = 0
        for section in wire:
            direction = section[0]
            distance = int(section[1:])
            for _ in range(distance):
                steps += 1
                match direction:
                    case 'U':
                        Y += 1
                    case 'D':
                        Y -= 1
                    case 'L':
                        X -= 1
                    case 'R':
                        X += 1
                if (X, Y) not in wire_points[i]:
                    wire_points[i][(X, Y)] = steps
    global intersections
    intersections = list(set(wire_points[0]) & set(wire_points[1]))

    output = 999999999
    for intersection in intersections:
        distance = abs(intersection[0]) + abs(intersection[1])
        if distance < output:
            output = distance
    return output

def task2():
    global intersections
    global wire_points

    output = 999999999
    for intersection in intersections:
        distance = wire_points[0][intersection] + wire_points[1][intersection]
        if distance < output:
            output = distance
    return output

if __name__ == '__main__':
    print(task1())
    print(task2())