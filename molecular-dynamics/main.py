from particles.particleNp import ParticleNp
import numpy as np
import cProfile

import matplotlib.pyplot as plt

PARTICLE_IDX = 0
OTHER_OBJ_IDX = 1
DT_IDX = 2
# CLASH_ITERATIONS = int(10e7)
CLASH_ITERATIONS = int(10e6)
START_RADIUS = 15
END_RADIUS = 23

CURRENT_TIME = 0
NEXT_DT = 1


def main():
    for radius in range(START_RADIUS, END_RADIUS + 1):
        radius = radius / 100

        cluster = init_particles(radius)

        for particle in cluster:
            particle.record = True

        iteration = 0

        while iteration < CLASH_ITERATIONS:
            update_cluster(cluster, get_closest_event(cluster))
            iteration += 1
            if iteration % int(10e3) == 0:
                print('\r' + f'{iteration}', end="")

        np.save(f'results\\radius_{radius}.npy', np.array(cluster))
        print(f'\ncurrent radius:{radius} have been finished running')


def init_particles(radius):
    a = ParticleNp(0, (0.25, 0.25), (0.21, 0.12), r=radius)
    b = ParticleNp(1, (0.25, 0.75), (0.71, 0.18), r=radius)
    c = ParticleNp(2, (0.75, 0.25), (-0.23, -0.79), r=radius)
    d = ParticleNp(3, (0.75, 0.75), (0.78, 0.34583), r=radius)

    return [a, b, c, d]


def get_closest_event(cluster):
    """
    :param cluster:
    :return:
    """
    closest_event = [None, None, np.inf]
    # Here we update the closest dt event: [particle, clash obj, dt]
    for i, particle in enumerate(cluster):
        closest_event = get_wall_event(closest_event, particle)

        for other_particle in range(i + 1, len(cluster)):
            closest_event = get_particle_event(closest_event, particle,
                                               cluster[other_particle])
    return closest_event


def get_particle_event(closest_event, particle, other_particle):
    dt = particle.dt_to_collision_between(other_particle)

    if dt < closest_event[DT_IDX]:
        closest_event = [particle, other_particle, dt]
    return closest_event


def get_wall_event(closest_event, particle):
    dt, vertical_wall = particle.min_dt_wall()
    if dt < closest_event[DT_IDX]:
        closest_event = [particle, vertical_wall, dt]
    return closest_event


def update_cluster(cluster, event):
    global NEXT_DT
    global CURRENT_TIME

    next_time = CURRENT_TIME + event[DT_IDX]

    while CURRENT_TIME < next_time:
        if next_time > NEXT_DT:
            for particle in cluster:
                particle.update(NEXT_DT - CURRENT_TIME)
                particle.singleRecord()
            CURRENT_TIME = NEXT_DT
            NEXT_DT += 1
        else:
            for particle in cluster:
                particle.update(next_time - CURRENT_TIME)
            CURRENT_TIME = next_time

    if isinstance(event[OTHER_OBJ_IDX], ParticleNp):
        particles_clash_update(event[PARTICLE_IDX], event[OTHER_OBJ_IDX])
        return

    wall_clash_update(event[PARTICLE_IDX], event[OTHER_OBJ_IDX])


def particles_clash_update(particle: ParticleNp, other: ParticleNp):
    dl = particle.position - other.position
    dv = particle.velocity - other.velocity
    dl_normed = np.linalg.norm(dl)

    slope = dl / dl_normed
    s_v = np.dot(dv, slope)
    vadd = slope * s_v

    particle.velocity = particle.velocity - vadd
    other.velocity = other.velocity + vadd


def wall_clash_update(clash_particle: ParticleNp, vertical_wall):
    if vertical_wall:  # if clash vertical wall
        clash_particle.velocity[0] = -  clash_particle.velocity[0]
        return

    clash_particle.velocity[1] = -  clash_particle.velocity[1]


if __name__ == "__main__":
    main()
# cProfile.run('main()')
