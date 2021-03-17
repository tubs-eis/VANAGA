import config as cf  # General Parameters for a GA
import numpy as np  # use numpy due to array structure, code simplicity and performance
import random as rn
import threading
import csv
from population_nano import create_starting_population
from tournament_selection_nano import tournament_individual_selection
from crossover_nano import breed_by_crossover
from mutation_nano import randomly_mutate_population
from hardware_synthesis import *    # has all the functions to implement the synthesis
from switching_simulation import *  # has all the functions to start the power simulations
from get_area_nano import *         # gets all the areas of the nano controller
from get_power_nano import *        # gets all the powers of the nano controller
from pareto_selection_nano import *

# local track of the area
cell_area_results = []           # Track the total cell area progress, also the fitness
func_rtc_inst_area_results = []  # Track function instructions area progress
nano_ctrl_area_results = []      # Track control instructions area
nano_dp_area_results = []        # Track dp instructions area
# global cache tracking to save run time
cache_ISE = []   # Track all the synthesised ISE to save run time
cache_cell_area = []
cache_func_area = []
cache_ctrl_area = []
cache_dp_area = []
# global track
cell_area_over_gen = []       # Track the cell area (best fitness) progress over the generations
func_rtc_area_over_gen = []   # Track the func rtc  area (best fitness) progress over the generations
nano_ctrl_area_over_gen = []  # Track the control inst area (best fitness) progress over the generations
nano_dp_area_over_gen = []    # Track the dp inst area (best fitness) progress over the generations
# local track of the power
cell_logic_power_results = []        # Track the total cell logic power progress (best fitness) progress over the generations
cell_memory_power_results = []       # Track the total cell memory power progress (best fitness) progress over the generations
total_memory_power_results = []      # Track the total memory power progress, also fitness (best fitness) progress over the generations
func_rtc_inst_power_results = []     # Track function instructions power progress (best fitness) progress over the generations
nano_ctrl_power_results = []         # Track control instructions power (best fitness) progress over the generations
nano_dp_power_results = []           # Track dp instructions power (best fitness) progress over the generations
nano_imem_inst_power_results = []    # Track instruction memory power (best fitness) progress over the generations
nano_dmem_inst_power_results = []    # Track data memory power (best fitness) progress over the generations
best_fitness_metric_ISE = []  # Track the power of a ISE best fitness (best fitness) progress over the generations
# global cache tracking to save run time
cache_cell_logic_power = []
cache_cell_memory_power = []
cache_total_memory_power = []
cache_func_power = []
cache_ctrl_power = []
cache_dp_power = []
cache_imem_power = []
cache_dmem_power = []
# global track
cell_logic_power_over_gen = []        # Track the cell logic power (best fitness) progress over the generations
cell_memory_power_over_gen = []       # Track the cell memory power (best fitness) progress over the generations
total_memory_power_over_gen = []      # Track the total memory power (best fitness) progress over the generations
func_rtc_power_over_gen = []          # Track the func rtc power (best fitness) progress over the generations
nano_ctrl_power_over_gen = []         # Track the control inst power (best fitness) progress over the generations
nano_dp_power_over_gen = []           # Track the dp inst power (best fitness) progress over the generations
nano_imem_inst_over_gen = []          # Track the imem inst power (best fitness) progress over the generations
nano_dmem_inst_over_gen = []          # Track the dmem inst power (best fitness) progress over the generations
best_fitness_metric_ISE_over_gen = []  # Track the ISE of cell power (best fitness) progress over the generations

# reference chromosome
# reference_ISE = [['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001']]
# reference_ISE = [['0010', '0111', '1001', '0011', '0100', '1110', '1111', '0110', '1100', '1010']]

# Initialize starting population
# population = create_starting_population(cf.population_size - 1, cf.chromosome_length) # use with reference chromosome
# population = np.vstack((np.array(reference_ISE), population))
population = create_starting_population(cf.population_size, cf.chromosome_length)

# Transform population and scores to use append to ISE power results
population = list(population)

# Overwrite make file to synthesise the memory and then the logic
make_file_logic_to_memory_overwrite()
make_all_cmd()
make_file_memory_to_logic_overwrite()

# define Event to later use the wait method to secure that all the threads are done in order to start a new one
wait1 = threading.Event()
wait2 = threading.Event()
wait3 = threading.Event()
wait4 = threading.Event()
wait5 = threading.Event()
individual = 0
# Synthesise Simulate all the individual of the starting population using the power as fitness
for parallel_execution in range(int(len(population)/cf.parallel_threads)):

    for folder in range(cf.parallel_threads):
        population[individual] = list(population[individual])
        # Track all the simulated ISE to not synthesise the same twice
        cache_ISE.append(population[individual])
        # Track the simulated ISE
        best_fitness_metric_ISE.append(population[individual])
        # overwrite nano_pkg_vhdl to get the new Instruction Set Encode
        nano_pkg_vhdl_overwrite(population[individual], folder)
        # overwrite nanodefs_h to get the new Instruction Set Encode
        nanodefs_h_overwrite(population[individual], folder)
        individual += 1

    # implement the area synthesis and switching simulation
    thread1 = threading.Thread(target=make_all_cmd)
    thread1.start()
    thread1.join()
    wait1.set()
    wait1.wait()
    thread2 = threading.Thread(target=assembler_execution_rom_image)
    thread2.start()
    thread2.join()
    wait2.set()
    wait2.wait()
    thread3 = threading.Thread(target=assembler_execution_imem_image)
    thread3.start()
    thread3.join()
    wait3.set()
    wait3.wait()
    thread4 = threading.Thread(target=make_all_net)
    thread4.start()
    thread4.join()
    wait4.set()
    wait4.wait()
    thread5 = threading.Thread(target=make_all_pwr)
    thread5.start()
    thread5.join()
    wait5.set()
    wait5.wait()

    # get all the areas and power of the nanocontroller from each log folder
    for folder in range(cf.parallel_threads):
        # get area
        cell_area = get_cell_area(folder)
        func_rtc_inst_area = get_func_rtc_inst_area(folder)
        nano_ctrl_instr_area = get_nano_ctrl_instr_area(folder)
        nano_dp_inst_area = get_nano_dp_inst_area(folder)
        # Add each areas to the track progress arrays
        cell_area_results.append(cell_area)
        func_rtc_inst_area_results.append(func_rtc_inst_area)
        nano_ctrl_area_results.append(nano_ctrl_instr_area)
        nano_dp_area_results.append(nano_dp_inst_area)
        # Add to the caches
        cache_cell_area.append(cell_area)
        cache_func_area.append(func_rtc_inst_area)
        cache_ctrl_area.append(nano_ctrl_instr_area)
        cache_dp_area.append(nano_dp_inst_area)
        # get power
        cell_logic_power = get_cell_logic_power(folder)
        cell_memory_power = get_cell_memory_power(folder)
        total_memory_power = get_total_memory_power(folder)
        func_rtc_inst_power = get_func_rtc_inst_power(folder)
        nano_ctrl_instr_power = get_nano_ctrl_instr_power(folder)
        nano_dp_inst_power = get_nano_dp_inst_power(folder)
        nano_imem_inst_power = get_nano_imem_inst_power(folder)
        nano_dmem_inst_power = get_nano_dmem_inst_power(folder)
        # Add each power to the track progress arrays
        cell_logic_power_results.append(cell_logic_power)
        cell_memory_power_results.append(cell_memory_power)
        total_memory_power_results.append(total_memory_power)
        func_rtc_inst_power_results.append(func_rtc_inst_power)
        nano_ctrl_power_results.append(nano_ctrl_instr_power)
        nano_dp_power_results.append(nano_dp_inst_power)
        nano_imem_inst_power_results.append(nano_imem_inst_power)
        nano_dmem_inst_power_results.append(nano_dmem_inst_power)
        # Add to the caches
        cache_cell_logic_power.append(cell_logic_power)
        cache_cell_memory_power.append(cell_memory_power)
        cache_total_memory_power.append(total_memory_power)
        cache_func_power.append(func_rtc_inst_power)
        cache_ctrl_power.append(nano_ctrl_instr_power)
        cache_dp_power.append(nano_dp_inst_power)
        cache_imem_power.append(nano_imem_inst_power)
        cache_dmem_power.append(nano_dmem_inst_power)

# convert to numpy array
    for i in range(len(population)):
        population[i] = np.array(population[i])
    population = np.array(population)

scores = []
# Choose desired fitness for one objective optimization
if cf.objectives == 'one_objective':
    # COMBINATION OF AREA AND POWER FITNESS
    # mix fitness function using a combination of area and power
    if cf.metric == 'mix':
        scores_mix = []
        for i in range(len(total_memory_power_results)):
            mix_fitness = (float(total_memory_power_results[i]) * 1000000) + float(cell_area_results[i])
            scores_mix.append(mix_fitness)
        scores = scores_mix
    # TOTAL POWER IS FITNESS
    elif cf.metric == 'power':
        scores = total_memory_power_results
    # TOTAL LOGIC AREA IS FITNESS
    elif cf.metric == 'area':
        scores = cell_area_results

    # depending on desired fitness metric choose min or max values traction
    index_variable = 0
    if cf.tracked_fitness == 'min_metric':
        index_variable = scores.index(min(scores))
    elif cf.tracked_fitness == 'max_metric':
        index_variable = scores.index(max(scores))
    # Add the areas, powers and ISE of the first population to the overall trackers tracked with the desired fitness
    if cf.metric == 'mix' or 'power':
        cell_area_over_gen.append(cell_area_results[index_variable])
    elif cf.metric == 'area':
        if cf.tracked_fitness == 'min_metric':
            cell_area_over_gen.append(min(scores))
        elif cf.tracked_fitness == 'max_metric':
            cell_area_over_gen.append(max(scores))
    func_rtc_area_over_gen.append(func_rtc_inst_area_results[index_variable])
    nano_ctrl_area_over_gen.append(nano_ctrl_area_results[index_variable])
    nano_dp_area_over_gen.append(nano_dp_area_results[index_variable])
    # Add the min power and ISE of the initializing population to the overall trackers
    best_fitness_metric_ISE_over_gen.append(population[index_variable])
    cell_logic_power_over_gen.append(cell_logic_power_results[index_variable])
    cell_memory_power_over_gen.append(cell_memory_power_results[index_variable])
    if cf.metric == 'mix' or 'area':
        total_memory_power_over_gen.append(total_memory_power_results[index_variable])  # use if area is fitness or mix
    elif cf.metric == 'power':
        if cf.tracked_fitness == 'min_metric':
            total_memory_power_over_gen.append(min(scores))  # use if power is fitness, choose min or max
        elif cf.tracked_fitness == 'max_metric':
            total_memory_power_over_gen.append(max(scores))
    func_rtc_power_over_gen.append(func_rtc_inst_power_results[index_variable])
    nano_ctrl_power_over_gen.append(nano_ctrl_power_results[index_variable])
    nano_dp_power_over_gen.append(nano_dp_power_results[index_variable])
    nano_imem_inst_over_gen.append(nano_imem_inst_power_results[index_variable])
    nano_dmem_inst_over_gen.append(nano_dmem_inst_power_results[index_variable])
    # clear scores mix
    scores_mix = []

# 2-objective optimization with NSGA-II algorithm
elif cf.objectives == 'NSGA-II':
    # convert to float, values in scores are read and added from the source files as strings
    for i in range(len(cell_area_results)):
        cell_area_results[i] = float(cell_area_results[i])
        total_memory_power_results[i] = float(total_memory_power_results[i])

    # stack column wise the scores, i.e., Row1=[Area, Power]
    scores = np.column_stack((np.array(cell_area_results), np.array(total_memory_power_results)))

# clear the area result arrays to use in the generations loop
cell_area_results = []
func_rtc_inst_area_results = []
nano_ctrl_area_results = []
nano_dp_area_results = []

# clear the power result arrays to use in the generations loop
best_fitness_metric_ISE = []
cell_logic_power_results = []
cell_memory_power_results = []
total_memory_power_results = []
func_rtc_inst_power_results = []
nano_ctrl_power_results = []
nano_dp_power_results = []
nano_imem_inst_power_results = []
nano_dmem_inst_power_results = []

# Now the generations will be evaluated
for generation in range(cf.maximum_generation):
    # convert numpy array to list to use append and pop, later it will be converted backwards
    population = list(population)
    scores = list(scores)

    # Create an empty list for the new population
    new_population = []
    new_population = list(new_population)

    if cf.objectives == 'one_objective':
        # Choose an arbitrary number of best individuals for new population
        individual_best_score = 0
        index_best_score = 0
        for best_individual in range(cf.best_individuals_number):
            # get individual with the better fitness
            if cf.tracked_fitness == 'min_metric':
                individual_best_score = population[scores.index(min(scores))]
                index_best_score = scores.index(min(scores))
            elif cf.tracked_fitness == 'max_metric':
                individual_best_score = population[scores.index(max(scores))]
                index_best_score = scores.index(max(scores))
            # Add to the new population the individual with the best fitness
            new_population.append(individual_best_score)
            # pop the individual with best fitness from the population
            population.pop(index_best_score)
            # remove the value with best fitness in scores
            scores.pop(index_best_score)

    # convert to numpy array
    temp_population = np.array(population)
    scores = np.array(scores)

    # Create new population generating one children at a time
    for i in range(int(len(population))):

        if cf.objectives == 'one_objective':
            population = np.array(population)
            parent_1 = tournament_individual_selection(population, scores)
            parent_2 = tournament_individual_selection(population, scores)

        elif cf.objectives == 'NSGA-II':
            parent_1 = temp_population[rn.randint(0, cf.population_size - 1)]
            parent_2 = temp_population[rn.randint(0, cf.population_size - 1)]

        # Check if both parents are different, until then breed a new child
        # comparison = parent_1 == parent_2
        # equal = comparison.all()
        # while equal:
        #     if cf.objectives == 'one_objective':
        #         parent_2 = tournament_individual_selection(population, scores)
        #     elif cf.objectives == 'NSGA-II':
        #         parent_2 = temp_population[rn.randint(0, cf.population_size - 1)]
        #     comparison = parent_1 == parent_2
        #     equal = comparison.all()

        # Breed a new child and add it to the new population
        child_1 = breed_by_crossover(parent_1, parent_2)
        new_population.append(child_1)

    if cf.objectives == 'one_objective':
        # Replace the old population with the new one
        population = np.array(new_population)
        # Apply mutation
        population = randomly_mutate_population(population, cf.chromosome_length, cf.best_individuals_number)

    elif cf.objectives == 'NSGA-II':
        # Replace the old population with the new one
        new_population = np.array(new_population)
        # Apply mutation
        new_population = randomly_mutate_population(new_population, cf.chromosome_length, cf.best_individuals_number)
        # Perform elitism and new population mix to create new population
        population = np.vstack((population, np.array(new_population)))
        # check uniqueness of individuals in population
        population = np.unique(population, axis=0)
        # create new individuals until a unique population is created
        while len(population) < 2*cf.population_size:
            fill_population = create_starting_population(2*cf.population_size - len(population), cf.chromosome_length)
            population = np.vstack((population, np.array(fill_population)))
            population = np.unique(population, axis=0)

    # convert to list in order to use python methods not included in numpy arrays
    population = list(population)
    scores = list(scores)

    # define Event to later use the wait method to secure that all the threads are done in order to start a new one
    wait1 = threading.Event()
    wait2 = threading.Event()
    wait3 = threading.Event()
    wait4 = threading.Event()
    wait5 = threading.Event()
    individual = 0
    # Synthesise Simulate all the individual of the starting population using the power as fitness
    for parallel_execution in range(int(len(population)/cf.parallel_threads)):

        for folder in range(cf.parallel_threads):
            population[individual] = list(population[individual])
            # Track all the simulated ISE to not synthesise the same twice
            cache_ISE.append(population[individual])
            # Track the simulated ISE
            best_fitness_metric_ISE.append(population[individual])
            # overwrite nano_pkg_vhdl to get the new Instruction Set Encode
            nano_pkg_vhdl_overwrite(population[individual], folder)
            # overwrite nanodefs_h to get the new Instruction Set Encode
            nanodefs_h_overwrite(population[individual], folder)
            individual += 1

        # implement switching simulation
        thread1 = threading.Thread(target=make_all_cmd)
        thread1.start()
        thread1.join()
        wait1.set()
        wait1.wait()
        thread2 = threading.Thread(target=assembler_execution_imem_image)
        thread2.start()
        thread2.join()
        wait2.set()
        wait2.wait()
        thread3 = threading.Thread(target=assembler_execution_rom_image)
        thread3.start()
        thread3.join()
        wait3.set()
        wait3.wait()
        thread4 = threading.Thread(target=make_all_net)
        thread4.start()
        thread4.join()
        wait4.set()
        wait4.wait()
        thread5 = threading.Thread(target=make_all_pwr)
        thread5.start()
        thread5.join()
        wait5.set()
        wait5.wait()

        # get all the areas and power of the nanocontroller from each log folder
        for folder in range(cf.parallel_threads):
            # get area
            cell_area = get_cell_area(folder)
            func_rtc_inst_area = get_func_rtc_inst_area(folder)
            nano_ctrl_instr_area = get_nano_ctrl_instr_area(folder)
            nano_dp_inst_area = get_nano_dp_inst_area(folder)
            # Add each areas to the track progress arrays
            cell_area_results.append(cell_area)
            func_rtc_inst_area_results.append(func_rtc_inst_area)
            nano_ctrl_area_results.append(nano_ctrl_instr_area)
            nano_dp_area_results.append(nano_dp_inst_area)
            # Add to the caches
            cache_cell_area.append(cell_area)
            cache_func_area.append(func_rtc_inst_area)
            cache_ctrl_area.append(nano_ctrl_instr_area)
            cache_dp_area.append(nano_dp_inst_area)
            # get power
            cell_logic_power = get_cell_logic_power(folder)
            cell_memory_power = get_cell_memory_power(folder)
            total_memory_power = get_total_memory_power(folder)
            func_rtc_inst_power = get_func_rtc_inst_power(folder)
            nano_ctrl_instr_power = get_nano_ctrl_instr_power(folder)
            nano_dp_inst_power = get_nano_dp_inst_power(folder)
            nano_imem_inst_power = get_nano_imem_inst_power(folder)
            nano_dmem_inst_power = get_nano_dmem_inst_power(folder)
            # Add each power to the track progress arrays
            cell_logic_power_results.append(cell_logic_power)
            cell_memory_power_results.append(cell_memory_power)
            total_memory_power_results.append(total_memory_power)
            func_rtc_inst_power_results.append(func_rtc_inst_power)
            nano_ctrl_power_results.append(nano_ctrl_instr_power)
            nano_dp_power_results.append(nano_dp_inst_power)
            nano_imem_inst_power_results.append(nano_imem_inst_power)
            nano_dmem_inst_power_results.append(nano_dmem_inst_power)
            # Add to the caches
            cache_cell_logic_power.append(cell_logic_power)
            cache_cell_memory_power.append(cell_memory_power)
            cache_total_memory_power.append(total_memory_power)
            cache_func_power.append(func_rtc_inst_power)
            cache_ctrl_power.append(nano_ctrl_instr_power)
            cache_dp_power.append(nano_dp_inst_power)
            cache_imem_power.append(nano_imem_inst_power)
            cache_dmem_power.append(nano_dmem_inst_power)

    for i in range(len(population)):
        population[i] = np.array(population[i])
    population = np.array(population)

    # Choose desired fitness for one objective optimization
    if cf.objectives == 'one_objective':
        # COMBINATION OF AREA AND POWER FITNESS
        # mix fitness function using a combination of area and power
        if cf.metric == 'mix':
            scores_mix = []
            for i in range(len(total_memory_power_results)):
                mix_fitness = (float(total_memory_power_results[i]) * 1000000) + float(cell_area_results[i])
                scores_mix.append(mix_fitness)
            scores = scores_mix
        # TOTAL POWER IS FITNESS
        elif cf.metric == 'power':
            scores = total_memory_power_results
        # TOTAL LOGIC AREA IS FITNESS
        elif cf.metric == 'area':
            scores = cell_area_results

        # depending on desired fitness metric choose min or max values traction
        index_variable = 0
        if cf.tracked_fitness == 'min_metric':
            index_variable = scores.index(min(scores))
        elif cf.tracked_fitness == 'max_metric':
            index_variable = scores.index(max(scores))
            # Add the areas, powers and ISE of the first population to the overall trackers tracked with the desired fitness
        if cf.metric == 'mix' or 'power':
            cell_area_over_gen.append(cell_area_results[index_variable])
        elif cf.metric == 'area':
            if cf.tracked_fitness == 'min_metric':
                cell_area_over_gen.append(min(scores))
            elif cf.tracked_fitness == 'max_metric':
                cell_area_over_gen.append(max(scores))
        func_rtc_area_over_gen.append(func_rtc_inst_area_results[index_variable])
        nano_ctrl_area_over_gen.append(nano_ctrl_area_results[index_variable])
        nano_dp_area_over_gen.append(nano_dp_area_results[index_variable])
        # Add the min power and ISE of the initializing population to the overall trackers
        best_fitness_metric_ISE_over_gen.append(population[index_variable])
        cell_logic_power_over_gen.append(cell_logic_power_results[index_variable])
        cell_memory_power_over_gen.append(cell_memory_power_results[index_variable])
        if cf.metric == 'mix' or 'area':
            total_memory_power_over_gen.append(
                total_memory_power_results[index_variable])  # use if area is fitness or mix
        elif cf.metric == 'power':
            if cf.tracked_fitness == 'min_metric':
                total_memory_power_over_gen.append(min(scores))  # use if power is fitness, choose min or max
            elif cf.tracked_fitness == 'max_metric':
                total_memory_power_over_gen.append(max(scores))
        func_rtc_power_over_gen.append(func_rtc_inst_power_results[index_variable])
        nano_ctrl_power_over_gen.append(nano_ctrl_power_results[index_variable])
        nano_dp_power_over_gen.append(nano_dp_power_results[index_variable])
        nano_imem_inst_over_gen.append(nano_imem_inst_power_results[index_variable])
        nano_dmem_inst_over_gen.append(nano_dmem_inst_power_results[index_variable])
        # clear scores mix
        scores_mix = []

        gens = np.arange(1, generation + 2, 1)
        # write the total area and power results over each generation in a csv file
        with open(r'one_objective_results/results_total.csv', mode='w') as results_total_file:
            fieldnames = ['Generation', 'Area (in μm²)', 'Power (in μW)']
            writer = csv.DictWriter(results_total_file, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(gens)):
                writer.writerow({'Generation': gens[i], 'Area (in μm²)': cell_area_over_gen[i],
                                 'Power (in μW)': total_memory_power_over_gen[i]})

        # write the control area and power results over each generation in a csv file
        with open(r'one_objective_results/results_control.csv', mode='w') as results_control_file:
            fieldnames = ['Generation', 'Control Area (in μm²)', 'Control Power (in μW)']
            writer = csv.DictWriter(results_control_file, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(gens)):
                writer.writerow({'Generation': gens[i], 'Control Area (in μm²)': nano_ctrl_area_over_gen[i],
                                 'Control Power (in μW)': nano_ctrl_power_over_gen[i]})

        # write the data path and real time clock unit area over each generation in a csv file
        with open(r'one_objective_results/others_area.csv', mode='w') as others_area:
            fieldnames = ['Generation', 'DP Area (in μm²)', 'RTC Area (in μm²)']
            writer = csv.DictWriter(others_area, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(gens)):
                writer.writerow({'Generation': gens[i], 'DP Area (in μm²)': nano_dp_area_over_gen[i],
                                 'RTC Area (in μm²)': func_rtc_area_over_gen[i]})

        # write the memory cell, data path, real time clock, instruction and data memory power over each generation in a csv file
        with open(r'one_objective_results/others_power.csv', mode='w') as others_power:
            fieldnames = ['Generation', 'Cell Memory Power (in μW)', 'DP Power (in μW)', 'RTC Power (in μW)',
                          'IMEM Power (in μW)', 'DMEM Power (in μW)']
            writer = csv.DictWriter(others_power, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(gens)):
                writer.writerow({'Generation': gens[i],
                                 'Cell Memory Power (in μW)': cell_memory_power_over_gen[i],
                                 'DP Power (in μW)': nano_dp_power_over_gen[i],
                                 'RTC Power (in μW)': func_rtc_power_over_gen[i],
                                 'IMEM Power (in μW)': nano_imem_inst_over_gen[i],
                                 'DMEM Power (in μW)': nano_dmem_inst_over_gen[i]})

        # write the ise of the minimal or maximal power and area with a the desired metric as fitness
        with open(r'one_objective_results/ise_over_generations.csv', mode='w') as ise_metrics:
            if cf.tracked_fitness == 'min_metric':
                fieldnames = ['Generation', 'Instruction encoding for minimal metrics']
            elif cf.tracked_fitness == 'max_metric':
                fieldnames = ['Generation', 'Instruction encoding for maximal metrics']
            writer = csv.DictWriter(ise_metrics, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(gens)):
                if cf.tracked_fitness == 'min_metric':
                    writer.writerow({'Generation': gens[i],
                                     'Instruction encoding for minimal metrics': best_fitness_metric_ISE_over_gen[i]})
                elif cf.tracked_fitness == 'max_metric':
                    writer.writerow({'Generation': gens[i],
                                     'Instruction encoding for maximal metrics': best_fitness_metric_ISE_over_gen[i]})

    # 2-objective optimization with NSGA-II algorithm
    elif cf.objectives == 'NSGA-II':

        # convert to float, values in scores are read and added from the source files as strings
        for i in range(len(cell_area_results)):
            cell_area_results[i] = float(cell_area_results[i])
            total_memory_power_results[i] = float(total_memory_power_results[i])

        # stack column wise the scores, i.e., Row1=[Area, Power]
        scores = np.column_stack((np.array(cell_area_results), np.array(total_memory_power_results)))

        # build pareto points of a minimum desired size
        population, scores = build_pareto_population(population, scores, cf.min_population_size, cf.max_population_size)

        population_ids = np.arange(population.shape[0]).astype(int)
        # use pareto front as best individuals in NSGAII
        pareto_front = identify_pareto(scores, population_ids)
        population_pareto = population[pareto_front, :]
        scores_pareto = scores[pareto_front]

        # write the total area and power results over each generation in a csv file
        individual_num = np.arange(1, len(population) + 1, 1)
        with open(r'pareto_scatter_results/pareto_generation_' + str(generation + 1) + '.csv', mode='w') as pareto_results:
            fieldnames = ['Individual', 'Area (in μm²)', 'Power (in μW)', 'ISE']
            writer = csv.DictWriter(pareto_results, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(population)):
                writer.writerow({'Individual': individual_num[i], 'Area (in μm²)': scores[i][0],
                                 'Power (in μW)': scores[i][1], 'ISE': population[i]})

        # write the total area and power results over each generation in a csv file
        with open(r'pareto_front_results/pareto_front_' + str(generation + 1) + '.csv', mode='w') as pareto_front_results:
            fieldnames = ['Front Area (in μm²)', 'Front Power (in μW)', 'Pareto Front ISE']
            writer = csv.DictWriter(pareto_front_results, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(scores_pareto)):
                writer.writerow({'Front Area (in μm²)': scores_pareto[i][0], 'Front Power (in μW)': scores_pareto[i][1],
                                 'Pareto Front ISE': population_pareto[i]})

    # clear the power result arrays to use in the generations loop
    cell_area_results = []
    func_rtc_inst_area_results = []
    nano_ctrl_area_results = []
    nano_dp_area_results = []

    # clear the power result arrays to use in the generations loop
    best_fitness_metric_ISE = []
    cell_logic_power_results = []
    cell_memory_power_results = []
    total_memory_power_results = []
    func_rtc_inst_power_results = []
    nano_ctrl_power_results = []
    nano_dp_power_results = []
    nano_imem_inst_power_results = []
    nano_dmem_inst_power_results = []

    # convert to numpy array
    population = np.array(population)
    scores = np.array(scores)

print('Number of ISE simulated')
print(len(cache_ISE))
print('-' * 80)
repetitions = check_for_repetetions(cache_ISE)
print('Repetitions in %')
print(repetitions)
print('-' * 80)



