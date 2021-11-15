from __future__ import annotations
import numpy as np

MAX_X = 1
MIN_X = 0
MAX_Y = 1
MIN_Y = 0
DT_STORE = 1


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
        self.__recordingFilm = {'position': np.array([]),
                                'velocity': np.array([])}

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def vx(self):
        return self.velocity[0]

    @property
    def vy(self):
        return self.velocity[1]

    @vx.setter
    def vx(self, new_vx):
        self.velocity[0] = new_vx

    @vy.setter
    def vy(self, new_vy):
        self.velocity[1] = new_vy

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

    def singleRecord(self):
        """
        Record current state only. One record will be add to recordingFilm.
        :return:
        """
        np.append(self.recordingFilm['position'], round(self.position, 1))
        np.append(self.recordingFilm['velocity'], self.velocity)

    def update(self, dt):
        """
        Update particle according to velocity and position. Will Record
        particle state at the and if record flag set to True.
        :return:
        """
        update_pos = self.position + self.velocity * dt

        if self.record:
            for discrete_dt in np.linspace(0, dt, dt.astype(int)):
                self.position = self.position + self.velocity * discrete_dt
                self.singleRecord()

            self.position = update_pos

    def min_dt_wall(self):
        """
        returns the minimum dt before meeting any wall
        """
        values = []
        if self.velocity[0] < 0:
            values.append(
                (self.position[0] - self.r) / abs(self.velocity[0]))
        else:
            values.append((1 - self.position[0] - self.r) / self.velocity[0])

        if self.velocity[1] < 0:
            values.append(
                (self.position[1] - self.r) / abs(self.velocity[1]))
        else:
            values.append((1 - self.position[1] - self.r) / self.velocity[1])
        return min(values)

    def dt_to_collision_between(self, other: ParticleNp):

        dl = self.position - other.position
        dv = self.velocity - other.velocity
        s = np.dot(dv, dl)
        dl_squared = np.power(np.linalg.norm(dl), 2)
        dv_squared = np.power(np.linalg.norm(dv), 2)
        gama = s ** 2 - dv_squared * (dl_squared - self.r - other.r)

        if gama > 0 and s < 0:
            return - (s + np.sqrt(gama)) / dv_squared
        return np.inf


class MinEnergyError(ArithmeticError):
    pass
