from particles.particleNp import ParticleNp, MinEnergyError
import random
import numpy as np


class ParticleClusterNp(np.ndarray):
    DEFAULT_CLUSTER_ENERGY = 0

    def __new__(cls, particlesIterate, energy=DEFAULT_CLUSTER_ENERGY):
        if isinstance(particlesIterate, int):
            particles = np.vectorize(ParticleNp)(
                np.arange(particlesIterate)).view(cls)
            particles.clusterEnergy = energy
            return particles

        if isinstance(particlesIterate, np.ndarray):
            particlesIterate.energy = energy
            return particlesIterate

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.clusterEnergy = getattr(obj, 'clusterEnergy',
                                     ParticleClusterNp.DEFAULT_CLUSTER_ENERGY)

    @property
    def clusterEnergy(self):
        return self.clusterEnergy

    @clusterEnergy.setter
    def clusterEnergy(self, newEnergy):
        if newEnergy < ParticleNp.MIN_ENERGY:
            raise MinEnergyError(
                f"Cluster energy must be at least {ParticleNp.MIN_ENERGY}")
        self.__clusterEnergy = \
            newEnergy


class EnergyPerParticleError(ArithmeticError):
    pass
