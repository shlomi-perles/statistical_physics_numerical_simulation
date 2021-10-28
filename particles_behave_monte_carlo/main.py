from particleCluster import ParticleCluster
from particle import Particle
import random
import matplotlib.pyplot as plt
import numpy as np

TWO_SOLIDS_ITERATION = int(1e5)


def main():
    twoEinsteinSolids()

def twoEinsteinSolids():
    solidA = ParticleCluster(size=100, energy=300)
    solidB = ParticleCluster(size=100, energy=0)

    solidAEnergy, solidBEnergy = [], []

    for _ in range(TWO_SOLIDS_ITERATION):
        particleA = random.choice(solidA)
        particleB = random.choice(solidB)
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

    xlim_space = TWO_SOLIDS_ITERATION//100
    ax1.set_xlim([-xlim_space, TWO_SOLIDS_ITERATION+xlim_space])
    ax2.set_xlim([-xlim_space, TWO_SOLIDS_ITERATION+xlim_space])

    ax1.set_ylim(ymin=0)
    ax2.set_ylim(ymin=0)

    fig.tight_layout()
    plt.show()


def plotHistogram(data, title, ylabel, xticks, xlabel=None, colors=None,
                  total_width=0.8, single_width=1, legend=True):
    """
      Use exemple:
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


if __name__ == "__main__":
    main()
