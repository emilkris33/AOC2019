from functools import lru_cache

orbits = {}

@lru_cache(maxsize=None)
def num_orbits(obj):
    if obj == 'COM':
        return 0
    result = len(orbits[obj])
    for o in orbits[obj]:
        result += num_orbits(o)
    return result

def task1():
    input_file = open("input.txt")
    for line in input_file.readlines():
        x, y = line.strip().split(')')
        if y not in orbits:
            orbits[y] = []
        orbits[y].append(x)

    result = 0
    for o in orbits:
        result += num_orbits(o)
    return result

distance = {}
def set_distance(obj, dist, distance_dict):
    distance_dict[obj] = dist
    if obj == 'COM':
        return
    for o in orbits[obj]:
        set_distance(o, dist+1, distance_dict)


def task2():
    santa_distance = {}
    set_distance('SAN', -1, santa_distance)
    you_distance = {}
    set_distance('YOU', -1, you_distance)

    common_points = list(set(santa_distance.keys()) & set(you_distance.keys()))
    result = 99999999999
    for p in common_points:
        dist = santa_distance[p] + you_distance[p]
        if dist < result:
            result = dist
    return result

if __name__ == '__main__':
    print(task1())
    print(task2())