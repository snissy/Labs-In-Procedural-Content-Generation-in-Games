import random as rd
from matplotlib import pyplot as plt
import numpy as np
import math as mt
from tqdm import tqdm
from multiprocessing import Pool


def searchSpace(n, start, end, freq):
    yRange = np.linspace(start, end, n)
    xRange = np.linspace(start, end, n)

    data = np.zeros((n, n))

    for yi, y in enumerate(yRange):
        for xi, x in enumerate(xRange):
            data[yi][xi] = np.exp(y + x) * np.power(np.sin(y * freq), 2) * np.power(np.cos(x * freq), 2)

    return data


def generateRandomGenome(n):
    nPoints = int((n * n) * 0.1)
    genome = np.zeros(nPoints*4)

    for p in range(nPoints):
        p = p*4
        xS = rd.random()
        yS = rd.random()
        o = rd.random()
        ln = rd.random()
        genome[p] = xS
        genome[p+1] = yS
        genome[p+2] = o
        genome[p+3] = ln

    return genome


def genomeToPhenotype(genome):
    outPut = np.ones((n, n))

    outPut[:, 0] = 0
    outPut[:, n - 1] = 0
    outPut[0, :] = 0
    outPut[n - 1, :] = 0

    lenGene = len(genome) // 4

    for gi in range(lenGene):
        g = gi * 4

        xS = min(int(genome[g] * n + 1), (n - 5))
        yS = min(int(genome[g+1] * n + 1), (n - 5))
        o = 1 if genome[g + 2] > 0 else 0
        ln = min(int((genome[g + 3] * 5)), 4)

        for l in range(ln):
            y = yS + (l * o)
            x = xS + (l * (1 - o))
            outPut[y, x] -= 1

    return outPut


def evaluateGenome(data):
    error = 0
    for y in range(1, n - 1):
        for x in range(1, n - 1):

            if data[y, x] == 0:
                cnt = 0
                cnt += 1 - data[y + 1, x]
                cnt += 1 - data[y - 1, x]
                cnt += 1 - data[y, x + 1]
                cnt += 1 - data[y, x - 1]
                if cnt != 2:
                    if cnt == 0:
                        error += 100
                    else:
                        error += 20

            elif data[y, x] < 0:
                error += 500
    return error


def featureGenonome(data):

    result = data.copy()

    for y in range(1, n - 1):
        for x in range(1, n - 1):

            if data[y, x] == 0:
                cnt = 0
                cnt += 1 - data[y + 1, x]
                cnt += 1 - data[y - 1, x]
                cnt += 1 - data[y, x + 1]
                cnt += 1 - data[y, x - 1]
                if cnt != 2:
                    if cnt == 0:
                        result[y, x] = 4
                    else:
                        result[y, x] = 2

    return result


def getRandomValue(value, factor, rFactor):

    return max(value + rd.gauss(0, 1/factor)*rFactor, 0)


def addMutation(genome, rFactor):

    for gi in range(len(genome)//4):
        g = gi * 4
        genome[g] = getRandomValue(genome[g], 15, rFactor)  # xS
        genome[g + 1] = getRandomValue(genome[g + 1], 15, rFactor)  # yS
        #genome[g + 2] = getRandomValue(genome[g + 2], 10, rFactor)  # o
        #genome[g + 3] = getRandomValue(genome[g + 3], 4, rFactor)  # ln


def test(n):

    pass


if __name__ == '__main__':

    """
    1.  Initialise the population of μ+λ individuals. The individuals could be randomly generated, or include some 
    individuals that were hand-designed or the result of previous evolutionary runs.
    
    2.  Shuffle the population (permute it randomly). This phase is optional but helps in escaping loss-of-gradient 
    situations.
    
    3.  Evaluate all individuals with the evaluation function, or some combination of several evaluation functions, so 
    that each individual is assigned a single numeric value indicating its fitness.
    
    4.  Sort the population in order of ascending fitness.
    
    5.  Remove the λ worst individuals. 6.  Replace the λ removed individuals with copies of the μ remaining 
    individuals. The newly made copies are called the offspring. Ifμ=λ, each individual in the elite is copied once; 
    otherwise, it could be copied fewer or more times.
    
    7.  Mutate the λ offspring, i.e. perturb them randomly. The most suitable mutation operator depends on the 
    representation and to some extent on the fitness land-scape.  If  the  representation  is  a  vector  of  real  
    numbers,  an  effective  mutation operator isGaussian mutation: add random numbers drawn from a Gaussian 
    distribution with a small standard deviation to all numbers in the vector.
    
    8.  If the population contains an individual of sufficient quality, or the maximum number of generations is reached,
     stop. Otherwise, go to step 2 (i.e. start the next generation).
    
    """

    n = 25

    my = 100
    lmd = 50

    nIter = 1000

    population = [[generateRandomGenome(n), None] for i in range(my + lmd)]

    for ITER in range(nIter):

        rd.shuffle(population)

        for i in range(len(population)):
            population[i][1] = evaluateGenome(genomeToPhenotype(population[i][0]))

        population.sort(key=lambda x: x[1])

        for pi in range(my, lmd+my):
            population[pi][0] = population[pi-my][0].copy()

        for p in population[3:]:
            addMutation(p[0], max((1/(0.05*ITER+1)), 0.012))

        print("ITER - {}, Current best {}".format(ITER, population[0][1]))
        plt.plot(ITER, population[0][1], "ro")

    plt.show()

    plt.imshow(featureGenonome(genomeToPhenotype(population[0][0])))
    plt.show()