#### Epidemic Simulator ####

An epidemic simulator to assist research with contagions such as COVID-19.

Group 4: Majed Almazrouei, Justin Becker, Dylan Conway, Kyle Diodati, and Nicholas Fay.

Date created: 02/26/2020

CIS 422 Software Methodologies, Project 2.

### Installation ###

First, unzip the program directory deadzone422 into your preferred location. Second, use the terminal to execute the command pip3 install matplotlib.

To start the program, open up terminal or command prompt on your local machine and direct the terminal to the directory that contains the Epidemic Simulator program. Run simulation.py with  python3 and add any parameters needed for your simulation. This will look like the following:
	python3 ./simulation.py

More information on the operation of the program is provided in User_Documentation.pdf and Programmer_Documentation.pdf.

### Directory description ###

legend:
    "->" is a directory
    "--" is a file

-> root: root directory, contains the main Python file, README, and directories for configuration and Python modules.
    -- .gitignore
    -- README.txt
    -- deadzone2.py
    -> config: This directory holds the configuration files for cities and planes.
        -- cities.tsv
        -- planes.tsv
    -> lib: This directory holds the separate Python modules.
        -- argparserModule.py
        -- cityModule.py
        -- parserModule.py
        -- personModule.py
        -- statisticsModule.py
        -- vesselModule.py
        -- graph.py
        -- infoCollector.py
