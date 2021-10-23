from particleCluster import ParticleCluster
from particle import Particle
import random

TWO_SOLIDS_ITERATION = int(1e5)


def main():
    twoEinsteinSolids()


def twoEinsteinSolids():
    solidA = ParticleCluster(size=100, energy=300)
    solidB = ParticleCluster(size=100, energy=0)

    solidA.distributeEnergy()

    solidAEnergy, solidBEnergy = [], []
    #TODO: 1,2,3

    for _ in range(TWO_SOLIDS_ITERATION):
        particleA = random.choice(solidA)
        particleB = random.choice(solidB)
        particleA, particleB = swapRandom(particleA, particleB)

        if particleA.energy > Particle.MIN_ENERGY:
            particleA.energy -= 1
            particleB.energy += 1
        solidAEnergy.append()



def swapRandom(a, b):
    return (a, b) if random.getrandbits(1) else (b, a)


if __name__ == "__main__":
    main()
