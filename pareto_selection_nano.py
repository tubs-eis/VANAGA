import numpy as np
import config as cf
from crowding_nano import reduce_by_crowding


def identify_pareto(scores, population_ids):
    """Identifies a single Pareto front, and returns the
    population IDs of the selected solutions"""

    population_size = scores.shape[0]
    # Create a starting list of items on the Pareto front
    # All items start off as being labelled as on the Pareto front
    pareto_front = np.ones(population_size, dtype=bool)
    if cf.tracked_fitness == 'min_metric':
        # Loop through each item. This will then be compared with all other items
        for i in range(population_size):
            # Loop though all other items
            for j in range(population_size):
                # Check if our 'j' point is dominated by out 'i' point
                if all(scores[j] <= scores[i]):
                    if any(scores[j] < scores[i]):
                        # i dominates j. Label 'j' point as not on the Pareto front
                        pareto_front[i] = 0
                        # Stop further comparisons with 'i' (no more comparisons needed)
                        break

    elif cf.tracked_fitness == 'max_metric':
        # Loop through each item. This will then be compared with all other items
        for i in range(population_size):
            # Loop though all other items
            for j in range(population_size):
                # Check if our 'i' point is dominated by out 'j' point
                if all(scores[j] >= scores[i]):
                    if any(scores[j] > scores[i]):
                        # j dominates i. Label 'i' point as not on the Pareto front
                        pareto_front[i] = 0
                        # Stop further comparisons with 'i' (no more comparisons needed)
                        break

    # Returns ids of scenarios on pareto front
    return population_ids[pareto_front]


def build_pareto_population(population, scores, min_population_size, max_population_size):
    """As necessary repeats Pareto front selection to build a population
    within defined size limits. It will reduce a Pareto front by applying
    crowding selection as necessary"""
    unselected_population_ids = np.arange(population.shape[0])
    all_population_ids = np.arange(population.shape[0])
    pareto_front = []
    while len(pareto_front) < min_population_size:
        temp_pareto_front = identify_pareto(scores[unselected_population_ids, :], unselected_population_ids)
        # Check size of total Pareto front
        # If larger than max size reduce new Pareto front by crowding
        combined_pareto_size = len(pareto_front) + len(temp_pareto_front)
        if combined_pareto_size > max_population_size:
            number_to_select = len(temp_pareto_front) - (combined_pareto_size - max_population_size)
            selected_individuals = reduce_by_crowding(scores[temp_pareto_front], number_to_select)
            temp_pareto_front = temp_pareto_front[selected_individuals]

        # Add latest Pareto front to full Pareto front
        pareto_front = np.hstack((pareto_front, temp_pareto_front))
        # Update unselected population ID by using sets to find IDs in all ids that are not in the selected front
        unselected_set = set(all_population_ids) - set(pareto_front)
        unselected_population_ids = np.array(list(unselected_set))

    population = population[pareto_front.astype(int)]
    scores = scores[pareto_front.astype(int)]
    return population, scores
