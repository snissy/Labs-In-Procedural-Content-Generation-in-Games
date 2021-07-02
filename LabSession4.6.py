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
import math as mt
from tqdm import tqdm


def okAccess(value, maxValue):
    return min(maxValue, max(value, 0))


def getDiamondSquareData(seed, iterations, roughness):
    iterations = min(iterations, 10)
    length = int(mt.pow(2, iterations) + 1)
    lastIndex = length - 1
    data = np.zeros((length, length))

    data[0, 0] = seed*rd.random()
    data[0, lastIndex] = seed*rd.random()
    data[lastIndex, 0] = seed*rd.random()
    data[lastIndex, lastIndex] = seed*rd.random()
    stepIndex = length - 1
    subStepIndex = stepIndex // 2

    for ITER in tqdm(range(iterations)):

        sideSquare = int(mt.pow(2, ITER))
        rFactor = roughness / (ITER + 1)

        # Create diamond step
        for i in range(sideSquare):
            i = i * stepIndex
            for j in range(sideSquare):
                j = j * stepIndex

                vertx00 = data[i][j]
                vertx01 = data[i][j + stepIndex]

                vertx10 = data[i + stepIndex][j]
                vertx11 = data[i + stepIndex][j + stepIndex]
                data[i + subStepIndex][j + subStepIndex] = (vertx00 + vertx01 + vertx10 + vertx11) / 4 + rd.random() * rFactor

        # Square step

        nSquareIterRange = int(mt.ceil(length / subStepIndex))

        start = 1

        for i in range(nSquareIterRange):

            startPos = start * subStepIndex
            y = i * subStepIndex

            for j in range(startPos, lastIndex+1, stepIndex):
                x = j

                vertexCord = ((y - subStepIndex, x),
                              (y, x + subStepIndex),
                              (y + subStepIndex, x),
                              (y, x - subStepIndex))

                vertexData = (data[okAccess(cord[0], lastIndex)][okAccess(cord[1], lastIndex)] for cord in vertexCord)

                squareValue = (sum(vertexData)/4) + rd.random() * rFactor
                data[y][x] = squareValue

            start = (start + 1) % 2

        stepIndex = subStepIndex
        subStepIndex = stepIndex // 2

    plt.imshow(data)
    plt.show()
    return data


if __name__ == '__main__':
    test = getDiamondSquareData(10, 12, 20)

    plt.imshow(test)
    plt.show()
