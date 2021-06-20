"""
Lab Task

Implement the diamond-square method to generate terrain heightmaps.
Have your function take three parameters:

seed, which specifies the initial values at the corners;
iterations, which specifies the number of diamond-square iterations to perform; and
roughness, which specifies the magnitude of the random components added in the diamond and square steps.

"""
import random as rd
from matplotlib import pyplot as plt
import numpy as np


def diamondSquare(seed, iterations, roughness):
    if iterations == 0:
        return seed

    r_factor = iterations * roughness

    diamondPoint = np.sum(seed) / 4 + rd.random() * r_factor

    northPoint = np.average((seed[0][0], seed[0][1], diamondPoint)) + rd.random() * r_factor
    westPoint = np.average((seed[0][0], seed[1][0], diamondPoint)) + rd.random() * r_factor
    eastPoint = np.average((seed[0][1], seed[1][1], diamondPoint)) + rd.random() * r_factor
    southPoint = np.average((seed[1][0], seed[1][1], diamondPoint)) + rd.random() * r_factor

    seed00 = np.array([[seed[0][0], northPoint],
                       [eastPoint, diamondPoint]])

    seed01 = np.array([[northPoint, seed[0][1]],
                       [diamondPoint, eastPoint]])

    seed10 = np.array([[westPoint, diamondPoint],
                       [seed[1][0], southPoint]])

    seed11 = np.array([[diamondPoint, eastPoint],
                       [southPoint, seed[1][1]]])

    sq00 = diamondSquare(seed00, iterations - 1, roughness)
    sq01 = diamondSquare(seed01, iterations - 1, roughness)
    sq10 = diamondSquare(seed10, iterations - 1, roughness)
    sq11 = diamondSquare(seed11, iterations - 1, roughness)

    sideLength = len(sq00)

    data = np.zeros((2 * sideLength, 2 * sideLength))

    data[:sideLength, :sideLength] = sq00
    data[:sideLength, sideLength:] = sq01

    data[sideLength:, :sideLength] = sq10
    data[sideLength:, sideLength:] = sq11

    return data


def getDiamondSquareData(seed, iterations, roughness):
    seed = np.array([[seed, seed],
                     [seed, seed]])

    return diamondSquare(seed, iterations=iterations, roughness=roughness)


if __name__ == '__main__':
    test = getDiamondSquareData(23, 2, 0.05)

    plt.imshow(test)
    plt.show()
