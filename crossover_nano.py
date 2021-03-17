import random


# create children with the single point crossover method
def breed_by_crossover(parent_1, parent_2):
    """This function will breed 1 child for the next generation
    using uniform crossover. The parents of the child with the
    best fitness value were previously selected in the tournament.
    The parent1 will be then set a the new child to check that the
    no parent1 (child) has no duplicates"""

    # Uniform crossover probability
    uniform_crossover_rate = 1.0

    breeder_1 = parent_1
    breeder_2 = parent_2

    # Get length of chromosome
    chromosome_length = len(parent_1)
    # check that the instructions do not repeat in the parent
    for instruction in range(chromosome_length):

        # Swap the instructions between the parents if the crossover rate meets the condition
        if random.random() < uniform_crossover_rate:
            if breeder_2[instruction] in breeder_1 or breeder_1[instruction] in breeder_2:
                continue
            else:
                breeder_1[instruction], breeder_2[instruction] = breeder_2[instruction], breeder_1[instruction]

    child_1 = breeder_1
    return child_1


def check_for_duplicates(child_with_duplicates):
    """This function checks if the child has duplicates,
    which means if an instruction encode repeats in the chromosome"""
    if len(child_with_duplicates) == len(set(child_with_duplicates)):
        return False
    else:
        return True

