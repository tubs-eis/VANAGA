import config as cf  # General Parameters for a GA
import numpy
import subprocess  # for make all
import re  # for file overwrite

# from population_nano import create_starting_population
# from fitness_nano import calculate_fitness


def make_file_logic_to_memory_overwrite():
    """This function will edit the make file located in syn_sdc_netsim
    to simulate the nano logic and nano memory of the nanocontroller. It
    changes the word logic to memory"""

    with open(r"../meh-microcontroller/nano/syn_sdc_netsim/Makefile", "rt") as makefile_old:
        list_of_lines = makefile_old.readlines()

    pattern = re.compile('logic')
    with open(r"../meh-microcontroller/nano/syn_sdc_netsim/Makefile", "wt") as nanodefs_new:
        for line in list_of_lines:
            # search if the pattern is in the line
            match = re.search(pattern, line)
            # print(match)
            if match:
                # overwrite the line with the word memory instead of logic
                new_line = re.sub(pattern, 'memory', line)
                nanodefs_new.write(new_line)
            else:
                nanodefs_new.write(line)


def make_file_memory_to_logic_overwrite():
    """This function will edit the make file located in syn_sdc_netsim
    to simulate the nano logic and nano memory of the nanocontroller. It
    changes the word memory to logic"""

    with open(r"../meh-microcontroller/nano/syn_sdc_netsim/Makefile", "rt") as makefile_old:
        list_of_lines = makefile_old.readlines()

    pattern = re.compile('memory')
    with open(r"../meh-microcontroller/nano/syn_sdc_netsim/Makefile", "wt") as nanodefs_new:
        for line in list_of_lines:
            # search if the pattern is in the line
            match = re.search(pattern, line)
            # print(match)
            if match:
                # overwrite the line with the word memory instead of logic
                new_line = re.sub(pattern, 'logic', line)
                nanodefs_new.write(new_line)
            else:
                nanodefs_new.write(line)


def nanodefs_h_overwrite(population, folder):
    """This function will edit nanodef.h to change the instruction set encode for the Operations(OP)"""

    # convert population in binary to int as the instruction are in nanodefs.h as int
    population_int = []
    for instruction in population:
        instruction_int = int(instruction, 2)
        population_int.append(instruction_int)

    # ISE = Instruction Set Encode
    possible_ISE = population_int
    possible_ISE = numpy.array(possible_ISE)

    # Operations
    ops = ['OP_LDI', 'OP_CMPI', 'OP_LIS', 'OP_LISL', 'OP_DBNE', 'OP_BNE', 'OP_CST', 'OP_CSTL', 'OP_ST', 'OP_SLEEP']

    # read the lines of nanodefs.h
    with open(r"../meh-microcontroller/nano/config" + str(folder+1) + "/nanodefs.h", "rt") as nanodefs_old:
        list_of_lines = nanodefs_old.readlines()

    # search for the line with the Operations(OP), look for a pattern to change the ISE of the OPs
    i = 0
    j = 0
    pattern = re.compile(r'OP_.*$')
    with open(r"../meh-microcontroller/nano/config" + str(folder+1) + "/nanodefs.h", "wt") as nanodefs_new:
        for line in list_of_lines:
            # search if the pattern is in the line
            match = re.search(pattern, line)
            # print(match)
            if match:
                # overwrite the line with the new instruction set encode
                new_line = re.sub(pattern, '{:<9}'.format(ops[i]) + '{:>2}'.format(possible_ISE[j]), line)
                nanodefs_new.write(new_line)
                i += 1
                j += 1
            else:
                nanodefs_new.write(line)


def checkSubset(list1, list2):
    """This function will check if an ISE has already been simulated"""

    exist = False
    for i in list2:
        if i == list1:
            index_repeated_ise = list2.index(i)
            exist = True
            break

    return index_repeated_ise, exist


def check_for_repetetions(ISE):
    """This function will check how many ISE have been repeatedly simulated"""
    non_repeat = len(set(map(tuple, ISE)))
    print('Unique number of instructions', non_repeat)
    repeat = len(ISE)

    return (((repeat - non_repeat)/repeat) * 100)


def make_all_cmd():
    """This function will execute the command 'make all' to run the power
    simulation after the nanodefs.h c_file has been overwritten."""

    global parallel_threads
    # store the processes to wait for each process to finish
    processes = []
    for i in range(cf.parallel_threads):
        cmds = subprocess.Popen(['make', 'all', 'SYN_SUFFIX=' + str(i+1)], cwd='../meh-microcontroller/nano/syn_sdc_netsim')
        processes.append(cmds)
    # wait for each thread to finish in order to start a new loop without delay
    for proc in processes:
        proc.wait()


def assembler_execution_imem_image():
    """This function will execute the assembler command to load all the net list"""

    global parallel_threads
    # store the processes to wait for each process to finish
    # processes = []
    for i in range(cf.parallel_threads):
        subprocess.run(['./axasm', '-p', 'nano' + str(i+1), '-c', '-o', '../sim' + str(i+1) + '/systemc/include/imem_image.h', '../sw/rtc.asm'],
                           cwd='../meh-microcontroller/nano/asm')
        # processes.append(cmds)
    # wait for each thread to finish in order to start a new loop without delay
    # for proc in processes:
        # proc.wait()

def assembler_execution_rom_image():
    """This function will execute the assembler command to load all the net list"""

    global parallel_threads
    # store the processes to wait for each process to finish
    # processes = []
    for i in range(cf.parallel_threads):
        subprocess.run(['./axasm', '-p', 'nano' + str(i+1), '-l', '-o', '../pkg_sim' + str(i+1) + '/nano_rom_image.vhdl', '../sw/rtc.asm'],
                           cwd='../meh-microcontroller/nano/asm')
        # processes.append(cmds)
    # wait for each thread to finish in order to start a new loop without delay
    # for proc in processes:
        # proc.wait()
        
        
def make_all_net():
    """This function will execute the command 'make all-net' to run the switching
    simulation after the nanodefs.h c file has been overwritten for the net lists. It will be implemented
    once a population, new population, is created"""

    global parallel_threads
    # store the processes to wait for each process to finish
    processes = []
    for i in range(cf.parallel_threads):
        cmds = subprocess.Popen(['make', 'all-net', 'SYN_SUFFIX=' + str(i+1)], cwd='../meh-microcontroller/nano/sim' + str(i+1))
        processes.append(cmds)
    # wait for each thread to finish in order to start a new loop without delay
    for proc in processes:
        proc.wait()


def make_all_pwr():
    """This function will execute the command 'make all' to run the switching
    simulation after the net list has been executed. It will create the result files
    where the instruction and data memory power is located"""

    global parallel_threads
    # store the processes to wait for each process to finish
    processes = []
    for i in range(cf.parallel_threads):
        cmds = subprocess.Popen(['make', 'all', 'SYN_SUFFIX=' + str(i+1)], cwd='../meh-microcontroller/nano/pwr')
        processes.append(cmds)
    # wait for each thread to finish in order to start a new loop without delay
    for proc in processes:
        proc.wait()

