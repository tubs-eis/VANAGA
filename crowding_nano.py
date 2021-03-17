import numpy as np
import random as rn


def calculate_crowding(scores):
    """Crowding is based on a vector for each individual. All scores
    are normalised between low and high. For any score, all
    solutions are sorted in order low to high. Crowding for chromosome
    x for that score is the difference between the next highest and
    next lowest score. Total crowding value sums all crowding for all
    scores"""

    population_size = len(scores[:, 0])
    number_of_scores = len(scores[0, :])

    # create crowding matrix of population (row) and score (column)
    crowding_matrix = np.zeros((population_size, number_of_scores))

    # normalise scores (ptp is max-min)
    normed_scores = (scores - scores.min(0)) / scores.ptp(0)
    # calculate crowding distance for each score in turn
    for col in range(number_of_scores):
        crowding = np.zeros(population_size)

        # Sort each score (to calculate crowding between adjacent scores)
        sorted_scores = np.sort(normed_scores[:, col])
        sorted_scores_index = np.argsort(normed_scores[:, col])

        # Calculate crowding distance for each individual
        end_point = 1
        crowding[1:population_size-1] = sorted_scores[2:population_size] - sorted_scores[0:population_size - 2]
        # No optimal solution is know, therefore open ends to keep optimization flow
        crowding[0] = sorted_scores[1] - end_point
        crowding[population_size - 1] = end_point - sorted_scores[population_size - 2]

        # resort to original order (two steps)
        re_sort_order = np.argsort(sorted_scores_index)
        sorted_crowding = crowding[re_sort_order]
        # Record crowding distances
        crowding_matrix[:, col] = sorted_crowding

    # Sum crowding distances of each score
    crowding_distances = np.sum(crowding_matrix, axis=1)
    return crowding_distances


def reduce_by_crowding(scores, number_to_select):
    """This function selects a number of solutions based on tournament
    of crowding distances. Two members of the population are picked at
    random. The one with the higher crowding distance is always picked"""

    population_ids = np.arange(scores.shape[0])
    crowding_distances = calculate_crowding(scores)
    picked_population_ids = np.zeros(number_to_select)
    picked_scores = np.zeros((number_to_select, len(scores[0, :])))

    for i in range(number_to_select):

        population_size = len(population_ids)
        fighter1id = rn.randint(0, population_size - 1)
        fighter2id = rn.randint(0, population_size - 1)

        # If fighter 1 is better
        if crowding_distances[fighter1id] >= crowding_distances[fighter2id]:
            # add solution to picked solutions array
            picked_population_ids[i] = population_ids[fighter1id]
            # Add score to be picked scores array
            picked_scores[i, :] = scores[fighter1id, :]
            # remove selected solution from available solutions
            population_ids = np.delete(population_ids, fighter1id, axis=0)
            scores = np.delete(scores, fighter1id, axis=0)
            crowding_distances = np.delete(crowding_distances, fighter1id, axis=0)

        else:
            # add lost fighter solution to picked solutions array
            picked_population_ids[i] = population_ids[fighter2id]
            # Add score to be picked scores array
            picked_scores[i, :] = scores[fighter2id, :]
            # remove selected solution from available solutions
            population_ids = np.delete(population_ids, fighter2id, axis=0)
            scores = np.delete(scores, fighter2id, axis=0)
            crowding_distances = np.delete(crowding_distances, fighter2id, axis=0)

        # Convert to integer
    picked_population_ids = np.asarray(picked_population_ids, dtype=int)

    return picked_population_ids
