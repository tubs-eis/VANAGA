import numpy
import random
import config as cf  # General Parameters for a GA

# create population
# Set an initial population with a random order of the individuals(random instructions from 0 to 15)
# 2D array, 1D represents each individual for the population
# 2D represents one individual (possible instruction set encode) for the population

# Define the bitlength and maximal instruction number

max_instructions = (2**cf.bitlength) - 1

def create_starting_population(individuals, chromosome_length):
    """This function will create a starting population with random individuals containing a possible
       instruction set coding for the nanocontroller. The instructions are from 0000 to 1111"""

    # Set an initial population
    population = []
    # individuals
    for i in range(individuals):
        row = []
        # create 10 random instruction between 0000 and 1111 to form an individual
        instruction = 0
        while instruction < chromosome_length:
            random_int = random.randint(0, max_instructions)
            random_binary_instruction = numpy.binary_repr(random_int, width=cf.bitlength)
            if random_binary_instruction not in row:
                row.append(random_binary_instruction)
                instruction += 1

        # convert to numpy array and shuffle the instructions
        row = numpy.array(row)
        # numpy.random.shuffle(row)
        population.append(row)

    # converting to numpy array
    population = numpy.array(population)
    return population


