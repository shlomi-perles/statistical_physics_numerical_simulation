class Particle:
    MIN_ENERGY = 0
    INIT_ENERGY = 10

    def __init__(self, particleID):
        self.__id = particleID
        self.__energy = Particle.INIT_ENERGY

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
        self.__energy = energy


class MinEnergyError(ArithmeticError):
    pass
