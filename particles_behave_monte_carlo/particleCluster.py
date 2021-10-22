from particle import Particle, MinEnergyError
import random


def randomEnergyDistribute(clusterSize, clusterEnergy):
    energyList = [0] * clusterSize

    while clusterEnergy > 0:
        energyList[random.randint(0, clusterSize)] += 1
        clusterEnergy -= 1

    return energyList


class ParticleCluster:
    DEFAULT_CLUSTER_ENERGY = 0

    def __init__(self, size, energy=DEFAULT_CLUSTER_ENERGY):
        self.__particles = [Particle(index) for index in range(size)]
        self.__clusterEnergy = energy

    def __getitem__(self, index):
        return self.particles[index]

    def __len__(self):
        return len(self.particles)

    def __iadd__(self, other):
        if isinstance(other, list) or isinstance(other, ParticleCluster):
            self.particles.extend(other)
            for particle in other:
                self.clusterEnergy += particle.energy

        elif isinstance(other, Particle):
            self.particles.append(other)
            self.clusterEnergy += other.energy
        else:
            raise TypeError(f"unsupported operand type(s) for +: "
                            f"ParticleCluster and {type(other)}")
        return self

    @property
    def clusterEnergy(self):
        return self.__clusterEnergy

    @clusterEnergy.setter
    def clusterEnergy(self, newEnergy):
        if newEnergy < Particle.MIN_ENERGY:
            raise MinEnergyError(
                f"Cluster energy must be at least {Particle.MIN_ENERGY}")
        self.__clusterEnergy = newEnergy

    @property
    def particles(self):
        return self.__particles

    def distributeEnergy(self, distributeFunc=randomEnergyDistribute):
        """
        get list from distributeFunc of energy to distribute between
        particles
        :param distributeFunc: get cluster size and cluster energy and
        distribute by some function. Default distribute random energy
        """

        for particle, energy in zip(
                self, distributeFunc(len(self), self.clusterEnergy)):
            particle.energy = energy
