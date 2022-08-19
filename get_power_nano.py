## Copyright (c) 2022 Chair for Chip Design for Embedded Computing,
##                    Technische Universitaet Braunschweig, Germany
##                    www.tu-braunschweig.de/en/eis
##
## Use of this source code is governed by an MIT-style
## license that can be found in the LICENSE file or at
## https://opensource.org/licenses/MIT.


import re


def get_cell_logic_power(folder):
    """This function will get the cell logic power of the simulated Instruction Set encode
    of the instruction decoder for the nanocontroller"""

    with open(r"../meh-microcontroller/nano/pwr/reports" + str(folder+1) + "/nano_logic/summary_power.report", "rt") as power_nano:
        list_of_lines = power_nano.readlines()

        # look for pattern Total Power to get the logic power value
        pattern = re.compile('Total Power')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                power_logic_cell = line[25:35]
                # transform string to float
                power_logic_cell = float(power_logic_cell)
                # multiply to maintain unit in micro Watt (uW)
                # power_logic_cell = power_logic_cell * 1e06

    return '{:.8f}'.format(power_logic_cell)


def get_nano_ctrl_instr_power(folder):
    """This function will get the nano control instruction power of the simulated Instruction Set
    encode of the instruction decoder for the nanocontroller"""

    with open(r"../meh-microcontroller/nano/pwr/reports" + str(folder+1) + "/nano_logic/hierarchy_power.report", "rt") as power_nano:
        list_of_lines = power_nano.readlines()

        # look for pattern nano_ctrl_inst to get the ctrl power value
        pattern = re.compile('nano_ctrl_inst')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                power_ctrl_inst = line[66:73]
                # transform string to float
                power_ctrl_inst = float(power_ctrl_inst)
                # multiply to maintain unit in micro Watt (uW)
                power_ctrl_inst = power_ctrl_inst * 0.1

    return '{:.8f}'.format(power_ctrl_inst)


def get_nano_dp_inst_power(folder):
    """This function will get the nano data path instruction power of the simulated Instruction Set
    encode of the instruction decoder for the nanocontroller"""

    with open(r"../meh-microcontroller/nano/pwr/reports" + str(folder+1) + "/nano_logic/hierarchy_power.report", "rt") as power_nano:
        list_of_lines = power_nano.readlines()

        # look for pattern nano_dp_inst to get the dp power value
        pattern = re.compile('nano_dp_inst')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                power_dp_inst = line[66:73]
                # transform string to float
                power_dp_inst = float(power_dp_inst)
                # multiply to maintain unit in micro Watt (uW)
                power_dp_inst = power_dp_inst * 0.1

    return '{:.8f}'.format(power_dp_inst)


def get_func_rtc_inst_power(folder):
    """This function will get the func real time clock instruction power of the simulated
    Instruction Set encode of the instruction decoder for the nanocontroller"""

    with open(r"../meh-microcontroller/nano/pwr/reports" + str(folder+1) + "/nano_logic/hierarchy_power.report", "rt") as power_nano:
        list_of_lines = power_nano.readlines()

        # look for pattern func_rtc__inst to get the rtc power value
        pattern = re.compile('func_rtc_inst')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                power_func = line[66:73]
                # transform string to float
                power_func = float(power_func)
                # multiply to maintain unit in micro Watt (uW)
                power_func = power_func * 0.1

    return '{:.8f}'.format(power_func)


def get_cell_memory_power(folder):
    """This function will get the nano memory power of the nanocontroller"""

    with open(r"../meh-microcontroller/nano/pwr/reports" + str(folder+1) + "/nano_memory/summary_power.report", "rt") as power_nano:
        list_of_lines = power_nano.readlines()

        # look for pattern Total Power to get the memory power value
        pattern = re.compile('Total Power')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                power_memory_cell = line[25:35]
                # transform string to float
                power_memory_cell = float(power_memory_cell)
                # multiply to maintain unit in micro Watt (uW)
                power_memory_cell = power_memory_cell * 10

    return '{:.8f}'.format(power_memory_cell)


def get_nano_imem_inst_power(folder):
    """This function will get the instruction memory power of the nanocontroller"""

    with open(r"../meh-microcontroller/nano/pwr/reports" + str(folder+1) + "/nano_memory/hierarchy_power.report", "rt") as power_nano:
        list_of_lines = power_nano.readlines()

        # look for pattern nano_imem_inst to get the imem power value
        pattern = re.compile('nano_imem_inst')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                # increase the line number, due that the power info is in the next line
                next_line = list_of_lines.index(line) + 1
                power_imem_inst = list_of_lines[next_line][66:73]
                # transform string to float
                power_imem_inst = float(power_imem_inst)
                # multiply to maintain unit in micro Watt (uW)
                power_imem_inst = power_imem_inst * 10

    return '{:.8f}'.format(power_imem_inst)


def get_nano_dmem_inst_power(folder):
    """This function will get the data memory power of the nanocontroller"""

    with open(r"../meh-microcontroller/nano/pwr/reports" + str(folder+1) + "/nano_memory/hierarchy_power.report", "rt") as power_nano:
        list_of_lines = power_nano.readlines()

        # look for pattern nano_dmem_inst to get the dmem power value
        pattern = re.compile('nano_dmem_inst')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                # increase the line number, due that the power info is in the next line
                next_line = list_of_lines.index(line) + 1
                power_dmem_inst = list_of_lines[next_line][66:73]
                # transform string to float
                power_dmem_inst = float(power_dmem_inst)
                # multiply to maintain unit in micro Watt (uW)
                # power_dmem_inst = power_dmem_inst * 1e06

    return '{:.8f}'.format(power_dmem_inst)


def get_total_memory_power(folder):
    """This function will get the total memory power of the nanocontroller"""

    power_logic_cell = float(get_cell_logic_power(folder))
    power_memory_cell = float(get_cell_memory_power(folder))
    total_memory_power = power_memory_cell + power_logic_cell
    #total_memory_power = total_memory_power * 1e-05

    return str('{:.8f}'.format(total_memory_power))

