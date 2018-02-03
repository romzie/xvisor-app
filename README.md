# xvisor-app
**xvisor** parser for CSUG project

## Execution

`python3 xvisor.py` runs the comparator and loads the config from the `config.ini` file
Option `-y` does not ask if you want to overwrite the csv file if it already exists.

`python3 visualization.py` generates the heatmap under a default name `heatmap.jpg`

`python3 PIL_image_reader.py <image_path>` reads the image and generates the .h file containing the pixels

## Configuration Sections
The parser is configurable using the `config.ini` file.
### [FORMAT]
Concerns **xvisor** output.
- `prefix_addr` is the string that annonces the address where the fault was injected. It should end with "0x".
- `prefix_cycle` is the string that annonces the cycle when the fault was injected.
- `prefix_result` is the string that annonces the program output or the program state at the end of the maximum time. It is expected to see a blank space after the prefix.
- `deadlock_tag` is the token defined for deadlocks
- `error_msg` is the token present in every and only errors
### [TEST_FILE]
This file contains the real output of **xvisor**.
### [REF_FILE]
This file contains the expected output of the program tested through **xvisor**.
### [CSV_FILE]
File where the results of parsing will be stored.
- `delimiter` is the CSV delimiter
- `_tag` tokens that define situations that can be encountered in **xvisor** output
### [VISUAL]
Configuration of `visualization.py` script.
- `no_data_tag` is the tag when no fault has been injected at a particular (address, cycle) couple

## Adding tags
Add them in the `[CSV_FILE]` section of `config.ini`.
Implement the behavior of parsing by adding an `elif` statement in `xvisor.py`.
For the visualization, add a color in the `[VISUAL]` section of `config.ini` AND you must add both tag and color in the `__init__` function of `visualization.py` in the arrays respectively named `self.tags` and `self.cmap`. Refer to the tags already present for example.

## Example
Two files have been added to give an example of what could contain xvisor output and what could be an expected output for the program state with the files `example_xvisor_output` and `example_expected_program_output`
