# xvisor-app
**xvisor** parser for CSUG project

## Execution

`python3 xvisor.py` runs the comparator and loads the config from the `config.ini` file

`python3 visualization.py` generates the heatmap under a default name `heatmap.jpg`

`python3 PIL_image_reader.py <image_path>` reads the image and generates the .h file containing the pixels

## Configuration Sections
The parser is configurable using the `config.ini` file.
### [FORMAT]
Concerns **xvisor** output.
- `xvisor_order` is the ouput format 
- `x_delimiter` is the separator between the output informations
- `id` is the identifier of the output value of the program 
- `deadlock_tag` is the token defined for deadlocks
- `error_msg` is the token present in every and only errors
### [TEST_FILE]
This file contains the real output of **xvisor**.
### [REF_FILE]
This file contains the expected output of **xvisor**.
### [CSV_FILE]
File where the results of parsing will be stored.
- `delimiter` is the CSV delimiter
- `_tag` tokens that define situations that can be encountered in **xvisor** output
