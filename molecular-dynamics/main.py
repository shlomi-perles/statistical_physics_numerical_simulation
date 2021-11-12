from particles.particleNp import ParticleNp
from particles.particleClusterNp import ParticleClusterNp
import numpy as np

def main():
    #  initialization

    a = ParticleNp(1, (0.25, 0.25), (0.21, 0.12))
    b = ParticleNp(2, (0.25, 0.75), (0.71, 0.18))
    c = ParticleNp(3, (0.75, 0.25), (-0.23, -0.79))
    d = ParticleNp(4, (0.75, 0.75), (0.78, 0.34583))
    # TODO for this moment I refrain from intializing a cluster, feel free to change it
    cluster = [a, b, c, d]
    while(True):
        dt = calculate_minimum_dt_to_collision(cluster)
        update_cluster(cluster, dt)


def calculate_minimum_dt_to_collision(cluster: list[ParticleNp]):
    # TODO: this function currently just calculatinf the dt, bot not returning the type of collison
    #       and not the particles which taking part in the collision
    values = []
    for i in range(3):
        for j in range(i+1, 4):
            values.append(cluster[i].dt_to_collision_between(cluster[j]))
    for particle in cluster:
        values.append(particle.min_dt_wall())
    return min(values)


def update_cluster(cluster: list[ParticleNp], dt):
    for particle in cluster:
        # TODO update each particle according to the type of collision:
        #     if in wall- all the particles just updating to position vector + dt * velocity vector
        #     except for the one which collided that you already made his change in ParticleNp
        #     if collision between two particles: more complex update like showed in the pdf
        pass





if __name__ == "__main__":
    main()

