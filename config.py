## Copyright (c) 2022 Chair for Chip Design for Embedded Computing,
##                    Technische Universitaet Braunschweig, Germany
##                    www.tu-braunschweig.de/en/eis
##
## Use of this source code is governed by an MIT-style
## license that can be found in the LICENSE file or at
## https://opensource.org/licenses/MIT.


# General Parameters from one- and two-objective Genetic Algorithm
bitlength = 4
chromosome_length = 10
population_size = 150
maximum_generation = 10000
mutation_rate = 0.85
parallel_threads = 10

# implement one objective or NSGA-II optimization
objectives = 'NSGA-II'  # one_objective or NSGA-II

# define tracked fitness in genetic optimization
tracked_fitness = 'max_metric'  # min_metric or max_metric

# use in one objective optimization
best_individuals_number = 2  # Choose percentage of elitism population
metric = 'area'  # area, power or mix

# use in NSGA-II optimization
min_population_size = population_size
max_population_size = population_size
