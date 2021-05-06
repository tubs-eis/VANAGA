# VANAGA: Tool for Instruction-Set Encoding Optimization in Embedded Processors

VANAGA is an open-source tool, which optimizes the instruction-set encoding in embedded processors using a one- and multi-objective (NSGA-II) Genetic Algorithm (GA).

## Table of contents

[Getting started](#Getting-started)

- [Installation](#Installation)
- [Configuring VANAGA](#Configuring-VANAGA)
- [Running VANAGA](#Running-VANAGA)
- [Recommendations](#Recommendations)

[Contributors](#Contributors)
[License](#License)

## Getting started

The following overview should outline the configuration of the VANAGA open source tool in order to adapt to a specific application.

### Installation

Clone the repository

```bash
git clone https://github.com/tubs-eis/VANAGA
```

### Configuring VANAGA

The following presented files and functions have to be edited accordingly for your own application. Here, an overview of the contents and recommendations are given.

1. Open the `config.py` and choose the desired optimization objectives, as well as the desired fitness to be tracked. Finally, adapt the genaral parameter of the genetic algorithm to your application.

2. The `switching_simulation.py` file contains the `make_file_logic_to_memory_overwrite()`, `make_all_cmd()` and `make_file_memory_to_logic_overwrite()` functions. They are used to modify Makefiles of an external tool flow, which automatically executes logic synthesis in order to generate, e.g., silicon area values. The `make_all_cmd()` function executes the external tool flow using the subprocess.Popen() method. This allows a configurable number of processes to be executed in parallel.

3. Open the `hardware_synthesis.py` file and edit the `nano_pkg_vhdl_overwrite()` function. This function modifies the binary encoded instruction-set encoding, written in a VHDL package, using regular expressions. Later, the file is read by the external tool flow to generate, e.g., silicon area results. The same has to be done in the `switching_simulation.py` file, which uses the `nanodefs_h_overwrite()` function to overwrite the instruction-set encoding in the SystemC testbench headers (if required) in order to simulate the switching activity of an application.

4. Open the `switching_activity.py` file and edit the `assembler_execution_imem_image()`, `assembler_execution_rom_image()`, `make_all_net()` and `make_all_pwr()`. All of these functions allow a parallel execution of a switching simulation. Adapt all these functions to your application accordingly.

5. Finally, edit the `get_area_nano.py` and `get_power_nano.py` files. Here, a variety of functions is defined, which reads in the generated silicon area and power consumption results from the generated report files of the external tool flow. This is also done using regular expressions. Furthermore, remember to edit the tracking arrays which are used to track the desired metrics locally (GA generations loop) and globally (over generations).

### Running VANAGA

Once all the abovementioned configurations have been adapted to your application, run VANAGA using:

```bash
python3 main_nano.py
```

### Recommendations

- With litte effort, the algorithm can be extended for the optimization of more than two objects, i.e., add a new column to the scores array containing the fitness values of the 3rd objective.

- The algorithm tracks the percentage of repeated Instruction-Set Encodings (ISE) at the end of the genetic process. A function can be built, which checks if an ISE has already been synthesised and simulated. If this is the case, remove it from the population and create a new individual (new ISE) until the new population has non-repeated individuals. This will expand the search space of the application.

## Contributors

- Guillermo Payá Vayá (Technische Universität Braunschweig)
- Moritz Weißbrich (Technische Universität Braunschweig)
- Javier Andrés Moreno Medina (Leibniz Universität Hannover)

## License

This open-source project is distributed under the MIT license.
