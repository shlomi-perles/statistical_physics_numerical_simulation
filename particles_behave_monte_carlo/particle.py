class Particle:
    MIN_ENERGY = 0
    INIT_ENERGY = 0

    def __init__(self, particleID, cluster=None):
        self.__id = particleID
        self.__energy = Particle.INIT_ENERGY
        self.__cluster = cluster

    @property
    def id(self):
        return self.__id

    @property
    def energy(self):
        return self.__energy

    @energy.setter
    def energy(self, energy):
        if energy < Particle.MIN_ENERGY:
            raise MinEnergyError(
                f"Energy cant be less than {Particle.MIN_ENERGY}")
        prevEnergy = self.__energy
        self.__energy = energy
        if self.__cluster:
            self.__cluster.clusterEnergy += self.energy - prevEnergy


class MinEnergyError(ArithmeticError):
    pass
