from __future__ import annotations
import numpy as np


MAX_X = 1
MIN_X = 0
MAX_Y = 1
MIN_Y = 0


class ParticleNp:
    MIN_ENERGY = 0
    INIT_ENERGY = 0
    DEFAULT_RADIUS = 0.15

    def __init__(self, particleID, position, velocity,
                 r=DEFAULT_RADIUS, energy=INIT_ENERGY):
        self.__id = particleID
        self.__energy = energy
        self.__position = np.array(position)
        self.__velocity = np.array(velocity)  # הפכתי גם את זה למערך
        self.__r = r

        # Set to true if you want to record particles velocity and
        # position at each update. Records located at recordingFilm.
        self.__record = False
        self.__recordingFilm = {'position': np.array([]),
                                'velocity': np.array([])}

    @property
    def id(self):
        return self.__id

    @property
    def energy(self):
        return self.__energy

    @property
    def position(self):
        return self.__position

    @property
    def velocity(self):
        return self.__velocity

    @property
    def r(self):
        return self.__r

    @property
    def record(self):
        return self.__record

    @property
    def recordingFilm(self):
        return self.__recordingFilm

    @energy.setter
    def energy(self, energy):
        if energy < ParticleNp.MIN_ENERGY:
            raise MinEnergyError(
                f"Energy cant be less than {ParticleNp.MIN_ENERGY}")
        prevEnergy = self.__energy
        self.__energy = energy

    @position.setter
    def position(self, position):
        """
        Update position and if clash with a wall - negate the corrct
        velocity.
        :param position:
        :return:
        """
        if position[0] > MAX_X or position[0] < MIN_X:
            self.velocity[0] = -self.velocity[0]

        if position[1] > MAX_Y or position[1] < MIN_Y:
            self.velocity[1] = -self.velocity[1]

        self.__position = position

    @velocity.setter
    def velocity(self, velocity):
        self.__velocity = np.array(velocity)

    @r.setter
    def r(self, r):
        self.__r = r

    @record.setter
    def record(self, needToRecord):
        self.record = needToRecord

    @recordingFilm.setter
    def recordingFilm(self, film):
        self.recordingFilm = film

    def distanceTo(self, particle):
        """
        Distance to other particle or a wall. Can get ParticleNp
        or [x,y] np array. *CALCULATE CONSIDER RADIUS!*
        :param particle: ParticleNp or [x,y] np array representing single
        point.
        :return: Distance to other particle or a wall.
        """
        otherRadius = 0
        if isinstance(particle, ParticleNp):
            otherRadius = particle.r  # החלפתי כאן בין השורות
            particle = particle.position

        return np.linalg.norm(particle - self.position) - self.r - otherRadius

    def velocityTo(self, particle):
        """
        Relative velocity between two particles
        :param particle: particle
        :return: Relative velocity
        """
        return np.linalg.norm(particle.velocity - self.velocity)

    def singleRecord(self):
        """
        Record current state only. One record will be add to recordingFilm.
        :return:
        """
        np.append(self.recordingFilm['position'], self.position)
        np.append(self.recordingFilm['velocity'], self.velocity)

    def update(self):
        """
        Update particle according to velocity and position. Will Record
        particle state at the and if record flag set to True.
        :return:
        """

        if self.record:
            self.singleRecord()

    def min_dt_wall(self):
        """
        returns the minimum dt before meeting any wall
        """
        values = []
        if self.velocity[0] < 0:
            values.append((self.position[0] - self.r) / abs(self.velocity[0]))
        else:
            values.append((1 - self.position[0] - self.r) / self.velocity[0])

        if self.velocity[1] < 0:
            values.append((self.position[1] - self.r) / abs(self.velocity[1]))
        else:
            values.append((1 - self.position[1] - self.r) / self.velocity[1])
        return min(values)

    def dt_to_collision_between(self, other : ParticleNp):

        dl = self.position - other.position
        dv = self.velocity - other.velocity
        s = np.dot(dv, dl)
        dl_squared = np.power(np.linalg.norm(dl), 2)
        dv_squared = np.power(np.linalg.norm(dv), 2)
        gama = s**2 - dv_squared * (dl_squared - self.r - other.r)

        if gama > 0 and s < 0:
            return - (s + np.sqrt(gama)) / dv_squared
        return np.inf





class MinEnergyError(ArithmeticError):
    pass
