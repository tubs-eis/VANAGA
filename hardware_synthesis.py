import numpy
import subprocess # for make allfolder
import re # for nano pkg overwrite
import config as cf  # General Parameters for a GA

# from population_nano import create_starting_population
# from fitness_nano import calculate_fitness

def nano_pkg_vhdl_overwrite(population, folder):
    """This function will edit nano.pkg.vhdl to change the instruction set encode for the Operations(OP)"""

    # ISE = Instruction Set Encode
    possible_ISE = population
    possible_ISE = numpy.array(possible_ISE)

    # read the lines of nano_pkg.vhdl
    with open(r"../meh-microcontroller/nano/rtl" + str(folder+1) + "/nano.pkg.vhdl", "rt") as nano_pkg_old:
        list_of_lines = nano_pkg_old.readlines()

    # search for the line with the Operations(OP), look for a pattern to change the ISE of the OPs
    pattern = re.compile(r':= "(.*?)";')
    j = 0
    with open(r"../meh-microcontroller/nano/rtl" + str(folder+1) + "/nano.pkg.vhdl", "wt") as nano_pkg_new:
        for line in list_of_lines:

            # search if the pattern is in the line
            match = re.search(pattern, line)
            # print(match)
            if match:
                # overwrite the line with the new instruction set encode
                new_line = re.sub(pattern, ':= "' + possible_ISE[j] + '";', line)
                nano_pkg_new.write(new_line)
                j += 1
            else:
                nano_pkg_new.write(line)


def checkSubset(list1, list2):
    """This function will check if an ISE has already been synthesised and return 
    the index of the position where the already synthesised ISE is located"""

    index_repeated_ise = 0
    exist = False
    for i in list2:
        if i == list1:
            index_repeated_ise = list2.index(i)
            exist = True
            break
    return index_repeated_ise, exist


def make_all_command():
    """This function will exectute the command 'make all SYN_SUFFIX=i' to run the hardware
    synthesis after the nano_pkg.vhdl file has been overwritten. It will be implemented
    once a population, new population, is created"""
    # store the processes to wait for each process to finish
    processes = []
    for i in range(cf.parallel_threads):
        cmds = subprocess.Popen(['make', 'all', 'SYN_SUFFIX=' + str(i+1)], cwd='../meh-microcontroller/nano/syn_sdc')
        processes.append(cmds)
    # wait for each thread to finish in order to start a new loop without delay
    for proc in processes:
        proc.wait()
    


