from particleCluster import ParticleCluster
from particle import Particle
import random
import matplotlib.pyplot as plt
import numpy as np

TWO_SOLIDS_ITERATION = int(1e5)


def main():
    twoEinsteinSolids()


def twoEinsteinSolids():
    solidA = ParticleCluster(size=100, energy=300)
    solidB = ParticleCluster(size=100, energy=0)

    solidAEnergy, solidBEnergy = [], []

    for _ in range(TWO_SOLIDS_ITERATION):
        particleA = random.choice(solidA)
        particleB = random.choice(solidB)
        particleA, particleB = swapRandom(particleA, particleB)

        if particleA.energy > Particle.MIN_ENERGY:
            particleA.energy -= 1
            particleB.energy += 1

        solidAEnergy.append(solidA.clusterEnergy)
        solidBEnergy.append(solidB.clusterEnergy)

    twoSolidsPlotter(solidAEnergy, solidBEnergy)


def twoSolidsPlotter(solidA, solidB):
    markerSize = 0.1
    fig, (ax1, ax2) = plt.subplots(2)
    iterations = [x for x in range(TWO_SOLIDS_ITERATION)]
    ax1.scatter(iterations, solidA, s=markerSize)
    ax2.scatter(iterations, solidB, s=markerSize)
    ax1.grid()
    ax2.grid()
    plt.show()


def swapRandom(a, b):
    return (a, b) if random.getrandbits(1) else (b, a)


if __name__ == "__main__":
    main()
