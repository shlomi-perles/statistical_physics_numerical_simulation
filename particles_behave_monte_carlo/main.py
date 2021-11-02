from particleCluster import ParticleCluster
from particle import Particle
import random
import matplotlib.pyplot as plt
import numpy as np

TWO_SOLIDS_ITERATION = int(1e5)
METROPOLIS_ITERATION = int(1e7)
T = 2.5


def main():
    twoEinsteinSolids()
    metropolis()


def twoEinsteinSolids():
    solidA = ParticleCluster(size=100, energy=300)
    solidB = ParticleCluster(size=100, energy=0)
    solid = ParticleCluster(size=0, energy=0)
    solid += solidA
    solid += solidB

    solidAEnergy, solidBEnergy = [], []

    for _ in range(TWO_SOLIDS_ITERATION):
        particleA = random.choice(solid)
        particleB = random.choice(solid)
        particleA, particleB = swapRandom(particleA, particleB)

        if particleA.energy > Particle.MIN_ENERGY:
            particleA.energy -= 1
            particleB.energy += 1

        solidAEnergy.append(solidA.clusterEnergy)
        solidBEnergy.append(solidB.clusterEnergy)

    twoSolidsPlotter(solidAEnergy, solidBEnergy)


def metropolis():
    solid = ParticleCluster(size=100, energy=0)
    totalEnergy = []
    q1_hist = [0] * int(10 * T)
    list_of_hist = []

    for i in range(METROPOLIS_ITERATION):
        particle = random.choice(solid)
        result = random.choice([1, -1])
        record_energy(totalEnergy, solid, q1_hist)

        if result == -1:
            if particle.energy <= Particle.MIN_ENERGY:
                # record_energy(totalEnergy, solid, q1_hist)
                continue
            particle.energy += result
        else:
            p = random.random()
            if p > np.exp(-1 / T):
                # record_energy(totalEnergy, solid, q1_hist)
                continue

            particle.energy += result

        if i in {int(2e6), int(4e6), int(6e6), int(8e6)}:
            list_of_hist.append(single_hist(solid))

    list_of_hist.append(single_hist(solid))

    keys = ["2e6", "4e6", "6e6", "8e6", "1e7"]
    plotMetropolis(totalEnergy, q1_hist, dict(zip(keys, list_of_hist)))


# --------------------------- plot ---------------------------------

def twoSolidsPlotter(solidA, solidB):
    markerSize = 0.1
    fig, (ax1, ax2) = plt.subplots(2)
    iterations = [x for x in range(TWO_SOLIDS_ITERATION)]

    ax1.scatter(iterations, solidA, s=markerSize, label=r'$q_A$')
    ax2.scatter(iterations, solidB, s=markerSize, label=r'$q_B$')

    ax1.grid()
    ax2.grid()

    ax1.set_title("solid A")
    ax2.set_title("solid B")

    ax1.set_xlabel("Iteration")
    ax2.set_xlabel("Iteration")

    ax1.set_ylabel("Solid Energy [a.u.]")
    ax2.set_ylabel("Solid Energy [a.u.]")

    ax1.axhspan(149, 151, color='red')
    ax2.axhspan(149, 151, color='red')

    xlim_space = TWO_SOLIDS_ITERATION // 100
    ax1.set_xlim([-xlim_space, TWO_SOLIDS_ITERATION + xlim_space])
    ax2.set_xlim([-xlim_space, TWO_SOLIDS_ITERATION + xlim_space])

    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)

    ax1.legend(markerscale=10)
    ax2.legend(markerscale=10)

    fig.tight_layout()
    plt.show()


def plotMetropolis(totalEnergy, q_hist, hist_dict):
    plotTotalEnergy(totalEnergy)
    plotHistogram(hist_dict,
                  "Distribution of energy quantums in different iterations",
                  "Ratio in the solid",
                  list(range(16)), xlabel="Energy quantums")
    plotSingleParticleHist(q_hist)


def plotTotalEnergy(totalEnergy):
    fig, ax = plt.subplots()
    ax.scatter(np.arange(0, METROPOLIS_ITERATION, 1), totalEnergy,
                s=0.1, label=r'$q_tot$')
    ax.set_title(r'$q_tot\/\/VS\/\/Iterations$')
    ax.set_xlabel("Iteration")
    ax.set_ylabel(r'$q_tot$')
    ax.grid()
    ax.legend(markerscale=10)
    plt.show()


def plotSingleParticleHist(q_hist):
    fig, ax = plt.subplots()
    langs = list(range(int(T * 8)))
    ax.bar(langs, q_hist[0:20])
    ax.grid()

    ax.set_title(r'$Iterations\/\/VS\/\/q_1\/\/energy\/\/quantums$')

    ax.set_xlabel(r'$q_1\/\/energy\/\/quantums$')
    ax.set_ylabel(r'$Iteration\/\/(Normalized)$')
    plt.show()


def plotHistogram(data, title, ylabel, xticks, xlabel=None, colors=None,
                  total_width=0.8, single_width=1, legend=True):
    """
      Use example:
        plotHistogram({
        "a": [1, 2, 3, 2, 1],
        "b": [2, 3, 4, 3, 1],
        "c": [3, 2, 1, 4, 2],
        "d": [5, 9, 2, 1, 8],
        "e": [1, 3, 2, 2, 3],
        "f": [4, 3, 1, 1, 4],
    }, "title", "ylabel", ['group1', 'group2', 'group3',
                                     'group4', 'group5'])

    First group will be: [1,2,3,5,1,4] (first value in each list)
    """

    fig, ax = plt.subplots()
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    n_bars = len(data)
    bar_width = total_width / n_bars
    bars = []

    for i, (name, values) in enumerate(data.items()):

        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width,
                         color=colors[i % len(colors)])
        bars.append(bar[0])

    if legend:
        ax.legend(bars, data.keys())

    ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_title(title)
    # ax.set_xticklabels([0] + xticks)
    plt.show()


# --------------------------- tools --------------------------------

def swapRandom(a, b):
    return (a, b) if random.getrandbits(1) else (b, a)


def record_energy(solid_energy, solid, q1_hist):
    solid_energy.append(solid.clusterEnergy)
    if solid[0].energy < int(T * 10):
        q1_hist[solid[0].energy] += 1 / METROPOLIS_ITERATION


def single_hist(solid):
    hist = [0] * 16
    for particle in solid.particles:
        if particle.energy < 16:
            hist[particle.energy] += 1 / len(solid)
    return hist


if __name__ == "__main__":
    main()

