from particles.particleNp import ParticleNp
import numpy as np

import matplotlib.pyplot as plt


def plot_velocity(cluster, velocityType):
    velostring = {"vx": "V_x", "vy": "V_y", "velocity": "V_{abs}"}
    global NORMAL
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for particle in cluster:
        ax.plot(np.linspace(0, 2, 100),
                particle.recordingFilm[velocityType] / NORMAL,
                label=f"particle {particle.id}")

    ax.grid()
    ax.set_xlabel(fr'${format(velostring[velocityType])}\/[a.u.]$')
    ax.set_ylabel("Probability")

    fig.tight_layout()
    plt.legend()
    plt.show()


def plot_heat_map(particle):
    global NORMAL
    fig, ax = plt.subplots()
    img = ax.imshow(
        particle.recordingFilm['position'] / NORMAL, extent=[0, 1, 0, 1])
    plt.colorbar(img, ax=ax)
    ax.set_title("Position incidence of particle")
    ax.set_xlabel("X [a.u.]")
    ax.set_ylabel("Y [a.u.]")
    plt.show()


def plot_all_velocities(clusters, velocityType):

    global NORMAL
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    radius = 0.1
    for cluster in clusters:
        ax.plot(np.linspace(-2, 2, 200),
                cluster[0].recordingFilm[velocityType] /
                cluster[0].recordingFilm['norm'],
                label=f"Radius {radius}")
        radius += 0.01

    ax.grid()
    ax.set_xlabel(fr'$V_x\/[a.u.]$')
    ax.set_ylabel("Probability")

    fig.tight_layout()
    plt.legend()
    plt.show()


cluster = np.load(f'results\\radius_0.15.npy', allow_pickle=True)
NORMAL = np.sum(cluster[0].recordingFilm['position'])
plot_heat_map(cluster[0])
# plot_velocity(cluster, "vx")
# plot_velocity(cluster, "vy")
plot_velocity(cluster, "velocity")

# all_radiuses = []
# radius = 0.1
# for _ in range(14):
#     all_radiuses = np.load(f'results\\radius_{radius}.npy', allow_pickle=True)
#     radius += 0.01
#
# for cluster in all_radiuses:
#     cluster[0].recordingFilm['norm'] = np.sum(
#         cluster[0].recordingFilm['position'])
