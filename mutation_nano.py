## Copyright (c) 2022 Chair for Chip Design for Embedded Computing,
##                    Technische Universitaet Braunschweig, Germany
##                    www.tu-braunschweig.de/en/eis
##
## Use of this source code is governed by an MIT-style
## license that can be found in the LICENSE file or at
## https://opensource.org/licenses/MIT.


import numpy
import random
import config as cf  # General Parameters for a GA


# Mutate to expand the search space of the problem to optimize
# Using a cache (list of the non use instruction set code to implement the mutation)
# when mutate, a random instruction set that was not used will be selected from the cache
# to the individual

def randomly_mutate_population(population, chromosome_length, best_individuals_number):
    """This function will mutate a random instruction encode using the a cache that stores the
    non used instructions encode. When the instruction mutates, a new one is added from the cache randomly"""

    # max number of instructions
    max_instructions = (2**cf.bitlength) - 1

    # Set cache and convert to numpy array
    cache = cache_for_mutation(population, max_instructions + 1)
    cache = numpy.array(cache)

    # Get length of the population and cache
    population_size = len(population)
    # Apply random mutation
    for j in range(best_individuals_number, population_size):

        # create a value for each instruction and compare it with a mutation rate
        random_num = numpy.random.random()

        if random_num <= cf.mutation_rate:
            # print('Individual:', j)
            # print('Random value', random_num)
            # randomly select the instruction to mutate
            randomly_mutated_instruction = random.randint(0, chromosome_length - 1)
            # print('Randomly_mutated_instruction', randomly_mutated_instruction)
            # randomly select new instruction from row of cache
            new_instruction = cache[j][random.randint(0, len(cache[j]) - 1)]
            # print('New instruction', new_instruction)

            # Apply new value
            population[j][randomly_mutated_instruction] = new_instruction
            # print('New mutated value:', population[j][randomly_mutated_instruction])

    return population


def cache_for_mutation(population, num_instructions):
    """This function will create a cache, the size of the population,
    to store the non use instructions. Each row of the cache has length 6"""

    # Get size of population
    population_size = len(population)
    cache = []
    for k in range(population_size):
        row_cache = []
        for instructions in range(num_instructions):
            missing_instruction = numpy.binary_repr(instructions, width=cf.bitlength)
            if missing_instruction not in population[k]:
                row_cache.append(missing_instruction)

        row_cache = numpy.array(row_cache)
        cache.append(row_cache)

    cache = numpy.array(cache)
    return cache

