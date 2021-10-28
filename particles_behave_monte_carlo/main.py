from particles_behave_monte_carlo.particleCluster import ParticleCluster
from particles_behave_monte_carlo.particle import Particle
import random
import matplotlib.pyplot as plt
import numpy as np
import functools


TWO_SOLIDS_ITERATION = int(1e5)
METROPOLIS_ITERATION = int(1e7)
T = 2.5


def main():
    twoEinsteinSolids()


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


def twoSolidsPlotter(solidA, solidB):
    markerSize = 0.1
    fig, (ax1, ax2) = plt.subplots(2)
    iterations = [x for x in range(TWO_SOLIDS_ITERATION)]

    ax1.scatter(iterations, solidA, s=markerSize)
    ax2.scatter(iterations, solidB, s=markerSize)

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

    xlim_space = TWO_SOLIDS_ITERATION//100
    ax1.set_xlim([-xlim_space, TWO_SOLIDS_ITERATION+xlim_space])
    ax2.set_xlim([-xlim_space, TWO_SOLIDS_ITERATION+xlim_space])

    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)

    fig.tight_layout()
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
    ax.set_xticklabels([0] + xticks)
    plt.show()


def swapRandom(a, b):
    return (a, b) if random.getrandbits(1) else (b, a)


def metropolis():

    solid = ParticleCluster(size=100, energy=0)
    solid_energy = []
    q1_hist = [0 for i in range(int(10 * T))]
    list_of_hist = []
    for i in range(METROPOLIS_ITERATION):
        particle = random.choice(solid)
        result = random.choice([1, -1])
        if result == -1:
            if not particle.energy:
                continue
            particle.energy += result
        else:
            p = random.random()
            if p > np.exp(-1/T):
                continue

            particle.energy += result

        solid_energy.append(solid.clusterEnergy)
        if solid[0].energy < int(T * 10):
            q1_hist[solid[0].energy] += 1 / METROPOLIS_ITERATION

        if i in [int(2e6), int(4e6), int(6e6), int(8e6), int(1e7) - 1]:
            list_of_hist.append(single_hist(solid))
    # TODO here is the attempt to plot the first histogram, its not clear to me why we have more than 5 groups
    keys = list(range(len(list_of_hist)))
    dictionary = dict(zip(keys, list_of_hist))
    plotHistogram(dictionary, "distribution of energy quantums in different moments", "rate in the solid",
                  ["2e6", "4e6", "6e6", "8e6", "1e7"])
    # TODO this is the attempt to create the second histogram. just need to make a simple bars plot
    # keys = list(range(len(q1_hist)))
    # values = [[i] for i in q1_hist]
    # dictionary = dict(zip(keys, values))
    f(q1_hist)
    # a = []
    # for i in range(int(T * 10)):
    #     if i in [0,5,10,15,20,24]:
    #         a.append(str(i))
    #     else:
    #         a.append("")
    # plotHistogram(dictionary, "Number of iterations of q(1) in every energy level",
    #               "rate from all iterations", a)


def f(q_hist):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    langs = list(range(int(T * 10)))
    ax.bar(langs, q_hist)
    fig.tight_layout()
    plt.show()


def single_hist(solid):
    hist = [0 for i in range(int(T * 10))]
    for particle in solid.particles:
        if particle.energy < int(T * 10):
            hist[particle.energy] += 1 / len(solid)
    return hist



if __name__ == "__main__":

    # main()
    metropolis()
