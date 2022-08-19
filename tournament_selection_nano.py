## Copyright (c) 2022 Chair for Chip Design for Embedded Computing,
##                    Technische Universitaet Braunschweig, Germany
##                    www.tu-braunschweig.de/en/eis
##
## Use of this source code is governed by an MIT-style
## license that can be found in the LICENSE file or at
## https://opensource.org/licenses/MIT.


import random as rn
import numpy
import config as cf

# breeding (selection) with tournament selection
def tournament_individual_selection(population, scores):
    """This function will select the individuals with the for the next generation
    using the tournament selection method. 2 Individuals will be picked at random.
    The one with the highest fitness score will win and get selected."""
    # Get population size
    population_size = len(scores)

    # Pick differents individuals for the tournament at random from the population
    contender_1 = rn.randint(0, population_size-1)
    contender_2 = rn.randint(0, population_size-1)

    # Pick two different individuals
    while contender_1 == contender_2:
        contender_2 = rn.randint(0, population_size - 1)

    # Get fitness for each
    contender_1_fitness = scores[contender_1]
    contender_2_fitness = scores[contender_2]

    # Identify individual with the best fitness
    # Fighter1 will win if the scores are equal
    if cf.tracked_fitness == 'min_metric':
        if contender_1_fitness <= contender_2_fitness:
            winner = contender_1
        else:
            winner = contender_2
    elif cf.tracked_fitness == 'max_metric':
        if contender_1_fitness >= contender_2_fitness:
            winner = contender_1
        else:
            winner = contender_2

    # Return the chromosome of the winner
    return population[winner, :]

