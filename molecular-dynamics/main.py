from particles.particleNp import ParticleNp
import numpy as np
import matplotlib.pyplot as plt

MAX_VELOCITY = 1.5811388300841898
PARTICLE_IDX = 0
OTHER_OBJ_IDX = 1
PARTICLE_DIST_IDX = 2
PARTICLE_V_IDX = 3
DT_IDX = 4
CLASH_ITERATIONS = int(10e7)
START_RADIUS = 10
END_RADIUS = 23


def main():
    walls = (np.array([1, 0]), np.array([0, 1]))

    for radius in range(START_RADIUS, END_RADIUS + 1):
        radius = radius / 100

        cluster = init_particles(radius)

        for particle in cluster:
            particle.record = True

        iteration = 0

        while iteration < CLASH_ITERATIONS:
            update_cluster(cluster, get_closest_event(cluster, walls))
            iteration += 1

        np.save(f'results\\radius_{radius}.npy', particle.recordingFilm)


def init_particles(radius):
    a = ParticleNp(1, (0.25, 0.25), (0.21, 0.12), r=radius)
    b = ParticleNp(2, (0.25, 0.75), (0.71, 0.18), r=radius)
    c = ParticleNp(3, (0.75, 0.25), (-0.23, -0.79), r=radius)
    d = ParticleNp(4, (0.75, 0.75), (0.78, 0.34583), r=radius)

    return np.array([a, b, c, d])


def get_closest_event(cluster: list[ParticleNp], walls: tuple):
    """
    walls positions:
                    [0,-1]
            [1,0]           [-1,0]
                    [0,1]
    :param cluster:
    :param walls:
    :return:
    """
    # Here we update the closest dt event: [particle, clash obj, dist,
    # velocity, dt]
    closest_event = [None, None, None, None, np.inf]

    for particle in cluster:
        for wall in walls:
            closest_event = get_wall_event(closest_event, particle, wall)

        for other_particle in range(particle.id, len(cluster)):
            closest_event = get_particle_event(closest_event, particle,
                                               cluster[other_particle])
    return closest_event


def get_particle_event(closest_event, particle, other_particle):
    velocity = particle.velocityTo(other_particle)

    if velocity < 0:
        return closest_event

    clash_dist = particle.distanceTo(other_particle)
    dt = clash_dist / velocity

    if dt < closest_event[DT_IDX]:
        closest_event = \
            [particle, other_particle, clash_dist, velocity, dt]
    return closest_event


def get_wall_event(closest_event, particle, wall):
    clash_obj = wall.copy()
    clash_dist = np.dot(particle.position, wall) - particle.r
    velocity = particle.velocity[wall[1]]
    dt = - clash_dist / velocity
    c = 123

    if dt < 0:
        clash_dist = 1 - clash_dist - particle.r
        dt = clash_dist / velocity
        clash_obj = - clash_obj

    if dt < closest_event[DT_IDX]:
        closest_event = \
            [particle, clash_obj, clash_dist, velocity, dt]

    return closest_event

def update_cluster(cluster: list[ParticleNp], event):
    for particle in cluster:
        particle.update(event[DT_IDX])

    if isinstance(event[OTHER_OBJ_IDX], ParticleNp):
        return

    wall_clash_update(event[PARTICLE_IDX], event[OTHER_OBJ_IDX])


def particles_clash_update(clash_particle: ParticleNp,
                           other_particle: ParticleNp):
    slope = (clash_particle.position - other_particle.position)


def wall_clash_update(clash_particle: ParticleNp, wall):
    if wall[0] != 0:  # if clash vertical wall
        clash_particle.vx = -  clash_particle.vx
        return

    clash_particle.vy = -  clash_particle.vy


def plot(cluster):
    fig = plt.figure(label=r'$Probability density function of particles '
                           r'velocity$')
    ax = fig.add_subplot(1, 1, 1)

    for particle in cluster:
        # TODO: change possible velocity to 200 values
        ax.plot(np.abs(particle['velocity']))

    ax.grid()
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Solid Energy [a.u.]")

    fig.tight_layout()
    plt.show()

# def calculate_minimum_dt_to_collision(cluster: list[ParticleNp]):
#     # TODO: this function currently just calculatinf the dt, bot not returning the type of collison
#     #       and not the particles which taking part in the collision
#     possibles_dt = []
#     for i in range(3):
#         for j in range(i + 1, 4):
#             possibles_dt.append(
#                 cluster[i].dt_to_collision_between(cluster[j]))
#     for particle in cluster:
#         possibles_dt.append(particle.min_dt_wall())
#     return min(possibles_dt)



if __name__ == "__main__":
    main()
