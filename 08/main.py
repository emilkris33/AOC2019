
import numpy as np
import matplotlib.pyplot as plt

image = []

def task1():
    input_file = open("input.txt")
    layer = []
    row = []
    for char in input_file.readline().strip():
        row.append(int(char))
        if len(row) == 25:
            layer.append(row)
            row = []
        if len(layer) == 6:
            image.append(layer)
            layer = []

    fewest_zeroes = 9999
    result = None
    for layer in image:
        n_zeros = sum([ sum([n == 0 for n in row]) for row in layer])
        if n_zeros < fewest_zeroes:
            fewest_zeroes = n_zeros
            n_ones = sum([ sum([n == 1 for n in row]) for row in layer])
            n_twos = sum([ sum([n == 2 for n in row]) for row in layer])
            result = n_ones * n_twos
    return result




def task2():
    img = np.zeros([6, 25])
    for i in range(25):
        for j in range(6):
            for k in range(len(image)):
                if image[k][j][i] == 0:
                    break
                elif image[k][j][i] == 1:
                    img[j,i] = 1
                    break

    plt.imshow(img)
    plt.show()

if __name__ == '__main__':
    print(task1())
    print(task2())