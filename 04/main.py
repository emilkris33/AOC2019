options = []

def does_not_decrease(digits):
    for j in range(len(digits) - 1):
        if int(digits[j]) > int(digits[j + 1]):
            return False
    return True

def task1():
    for i in range(235741,706948):
        digits = str(i)
        for j in range(len(digits)-1):
            if digits[j] == digits[j+1]:
                break
        else:
            continue

        if not does_not_decrease(digits):
            continue

        options.append(i)
    return len(options)

def has_double(digits):
    last_pair = None
    for j in range(len(digits) - 1):
        if digits[j] == last_pair:
            continue
        if digits[j] == digits[j + 1]:
            last_pair = digits[j]
            if j + 2 == len(digits) or digits[j + 1] != digits[j + 2]:
                return True
    return False

def task2():
    options_2 = []

    for i in options:
        digits = str(i)
        if not has_double(digits):
            continue

        options_2.append(i)
    return len(options_2)


if __name__ == '__main__':
    print(task1())
    print(task2())