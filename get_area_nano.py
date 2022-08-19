## Copyright (c) 2022 Chair for Chip Design for Embedded Computing,
##                    Technische Universitaet Braunschweig, Germany
##                    www.tu-braunschweig.de/en/eis
##
## Use of this source code is governed by an MIT-style
## license that can be found in the LICENSE file or at
## https://opensource.org/licenses/MIT.


import re

def get_cell_area(folder):
    """This function will get the cell area of the simulated Instruction Set encode
    of the instruction decoder for the nanocontroller"""

    with open(r"../meh-microcontroller/nano/syn_sdc_netsim/log" + str(folder+1) + "/nano_logic.area", "rt") as area_nano:
        list_of_lines = area_nano.readlines()

        # look for pattern nano_ctrl_inst to get the area value
        pattern = re.compile('nano_logic')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                area_cell = line[34:41]

    return area_cell


def get_func_rtc_inst_area(folder):
    """This function will get the func rtc instruction area of the simulated Instruction Set encode
    of the instruction decoder for the nanocontroller"""

    with open(r"../meh-microcontroller/nano/syn_sdc_netsim/log" + str(folder+1) + "/nano_logic.area", "rt") as area_nano:
        list_of_lines = area_nano.readlines()

        # look for pattern nano_ctrl_inst to get the area value
        pattern = re.compile('func_rtc_inst')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                area_func = line[35:41]

    return area_func


def get_nano_ctrl_instr_area(folder):
    """This function will get the nano control instruction area of the simulated Instruction Set 
    encode of the instruction decoder for the nanocontroller"""

    with open(r"../meh-microcontroller/nano/syn_sdc_netsim/log" + str(folder+1) + "/nano_logic.area", "rt") as area_nano:
        list_of_lines = area_nano.readlines()

        # look for pattern nano_ctrl_inst to get the area value
        pattern = re.compile('nano_ctrl_inst')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                area_ctrl_inst = line[35:41]

    return area_ctrl_inst


def get_nano_dp_inst_area(folder):
    """This function will get the nano dp instruction area of the simulated Instruction Set encode
    of the instruction decoder for the nanocontroller"""

    with open(r"../meh-microcontroller/nano/syn_sdc_netsim/log" + str(folder+1) + "/nano_logic.area", "rt") as area_nano:
        list_of_lines = area_nano.readlines()

        # look for pattern nano_ctrl_inst to get the area value
        pattern = re.compile('nano_dp_inst')
        for line in list_of_lines:
            match = re.search(pattern, line)
            if match:
                area_dp_inst = line[35:41]

    return area_dp_inst


