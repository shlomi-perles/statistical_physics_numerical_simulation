from __future__ import annotations
import numpy as np
import math

MAX_X = 1
MIN_X = 0
MAX_Y = 1
MIN_Y = 0
DT_STORE = 1
MAX_VELOCITY = 2
VELOCITY_NUM = 200
VELOCITY_STEPS = MAX_VELOCITY * 2 / VELOCITY_NUM


def round_value(value):
    return math.floor(value / VELOCITY_STEPS) * VELOCITY_STEPS


def velocity_index(value):
    return int(round(round_value(value), 2) / VELOCITY_STEPS)


class ParticleNp:
    MIN_ENERGY = 0
    INIT_ENERGY = 0
    DEFAULT_RADIUS = 0.15

    def __init__(self, particleID, position, velocity,
                 r=DEFAULT_RADIUS, energy=INIT_ENERGY):

        self.__id = particleID
        self.__energy = energy
        self.__position = np.array(position)
        self.__velocity = np.array(velocity)
        self.__r = r

        # Set to true if you want to record particles velocity and
        # position at each update. Records located at recordingFilm.
        self.__record = False
        self.__recordingFilm = {'position': [[0] * 10 for _ in range(10)],
                                'velocity': [0] * (VELOCITY_NUM // 2),
                                'vx': [0] * VELOCITY_NUM,
                                'vy': [0] * VELOCITY_NUM}

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
        Update position
        :param position:
        """
        self.__position = position

    @velocity.setter
    def velocity(self, velocity):
        self.__velocity = np.array(velocity)

    @r.setter
    def r(self, r):
        self.__r = r

    @record.setter
    def record(self, needToRecord):
        self.__record = needToRecord

    @recordingFilm.setter
    def recordingFilm(self, film):
        self.__recordingFilm = film

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
            otherRadius = particle.r
            particle = particle.position

        return np.linalg.norm(
            particle - self.position) - self.r - otherRadius

    def velocityTo(self, particle):
        """
        Relative velocity between two particles
        :param particle: particle
        :return: Relative velocity
        """
        return np.linalg.norm(particle.velocity - self.velocity)

    def min_dt_wall(self):
        """
        returns the minimum dt before meeting any wall
        """
        vertical_wall = True
        if self.velocity[0] < 0:
            dt = (self.position[0] - self.r) / (- self.velocity[0])
        else:
            dt = (1 - self.position[0] - self.r) / self.velocity[0]

        if self.velocity[1] < 0:
            temp_dt = (self.position[1] - self.r) / -self.velocity[1]
            temp_vertical_wall = False
        else:
            temp_dt = (1 - self.position[1] - self.r) / self.velocity[1]
            temp_vertical_wall = False

        if temp_dt < dt:
            dt = temp_dt
            vertical_wall = temp_vertical_wall

        return dt, vertical_wall

    def dt_to_collision_between(self, other: ParticleNp):
        dl = self.position - other.position
        dv = self.velocity - other.velocity
        s = np.dot(dv, dl)
        dl_squared = np.dot(dl, dl)
        dv_squared = np.dot(dv, dv)
        gama = s ** 2 - dv_squared * (dl_squared - 4 * self.r ** 2)

        if gama > 0 > s:
            return - (s + gama ** 0.5) / dv_squared
        return np.inf

    def singleRecord(self):
        """
        Record current state only. One record will be add to recordingFilm.
        :return:
        """
        round_pos = np.floor(self.position * 10)
        x = 9 if round_pos[0] == 10. else int(round_pos[0])
        y = 9 if round_pos[1] == 10. else int(round_pos[1])

        self.recordingFilm['position'][x][y] += 1
        a = velocity_index(np.linalg.norm(self.velocity))
        self.recordingFilm['velocity'][
            velocity_index(np.linalg.norm(self.velocity))] += 1

        self.recordingFilm['vx'][
            velocity_index(self.velocity[0] + MAX_VELOCITY)] += 1

        self.recordingFilm['vy'][
            velocity_index(self.velocity[1] + MAX_VELOCITY)] += 1

    def update(self, dt):
        """
        Update particle according to velocity and position. Will Record
        particle state at the and if record flag set to True.
        :return:
        """
        update_pos = self.position + self.velocity * dt

        if self.record:
            for discrete_dt in np.linspace(1, dt, dt.astype(int)):
                self.position = self.position + self.velocity * discrete_dt
                self.singleRecord()

        self.position = update_pos
        self.singleRecord()


class MinEnergyError(ArithmeticError):
    pass
