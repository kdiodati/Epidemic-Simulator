"""
03/08/2020

Group 4: Majed Almazrouei, Justin Becker, Dylan Conway, Kyle Diodati, Nicholas Fay

This module is in charge of collecting program run options (program parameters)
"""

import argparse
import os

#Global variables for the current working directory and root directories of both mac and windows.
MAC = "/Users/"
WINDOWS = "C:\\Users\\"
CWD = os.getcwd()

#Default file names
PLANES = "planes.tsv"
CITIES = "cities.tsv"

#globals to get the absolute file paths of the config files
#pre processes this information in order to quicken the speed of the program
def get_file_paths(file):
    """
    self, string (filename) -> string (absolute file path)
    This function is in charge of finding the absolute file paths for the two configuration files.
    This function iterates through the root directory of the users system to find the proper file paths 
    in case a file is misplaced. Iteration through os files was based off of response to the question @
    https://stackoverflow.com/questions/1124810/how-can-i-find-path-to-given-file
    """
    #get the root of the system
    root = os.path.abspath(os.sep)
    #variable for if the file was found
    file_found = False
    #variable for the absoute path of the file
    abs_path = None
    #if the root is for mac set the mac root to be the users directory
    if(root == "/"):
        root = MAC + CWD.split("/")[2] + '/'
    else:
        #otherwise set it to windows
        root = WINDOWS + CWD.split("\\")[2] + '\\'

    #while the file path is not found
    while(not file_found):
        #iterate through the directories and files of the root directory
        for root, dirs, files in os.walk(root):
            #iterate through all the file names
            for name in files:
                #if the name matches the file we are trying to find
                if(name == file):
                    #get the absolute path break out of the loop and return
                    abs_path = os.path.abspath(os.path.join(root, name))
                    file_found = True
    return abs_path

#------------------------------------------------------------------------------#
class argparser:

    def __init__(self):
        """
        self, None -> None
        This function has the purpose of initializing the argparser. 
        """
        self.R_0 = 2.5
        self.life_time = 14
        self.death_rate = .08
        self.daily_travel_percentage = 0.001
        self.cities_file = os.path.abspath("./config/cities.tsv")
        self.planes_file = os.path.abspath("./config/planes.tsv")

    def obtain_command_line_args(self):
        """
        None -> Namespace
        This function is in charge of collecting system parameters by user input via command line. 
        The system is looking for 8 possible input arguments:
            1) R_O: The average number of infected individuals per person with the contagion. (type: float)
            2) life_time: Life time is the incubation period of the contagion. (type: float)
            3) death_rate: Death rate is the percentage of the individuals that will die from the contagion. (type: float)
            4) infected_count: This is the number of initially infected individuals in the population. (type: positive integer)
            5) cities_file: Cities file is the absolute filepath to the cities configuration file. (type: string)
            6) planes_file: Planes file is the absolute file path to the planes configuration file. (type: string)
            7) sim_time: The time (in the number of days) that the program will run. (type: positive int)
            8) daily_travel_percentage: This the percentage of daily travel that occurs. (type: positive float)
        """
        #create argparser
        argparser = argparse.ArgumentParser()
        #add the fives necessary arguments arguments we want
        #none of these arguments are required, if they are not given, the hard coded variables at the tops of this module
        #will be suplimented into the system configuration options.
        argparser.add_argument('--R_0', nargs=1, required=False, help="This is the number of average people that will be infected by the contagion. Input type: Positve floating point value.")
        argparser.add_argument('--life_time', '--lt', nargs=1, required=False, help="This is the incubation period of the contagion. Input type: Positive floating point value.")
        argparser.add_argument('--death_rate', '--dr', nargs=1, required=False, help="This is the percentage of individuals that die from the contagion. Input type: Positive floating point value.")
        argparser.add_argument('--infected_count', '--ic', nargs=1, required=False, help="This is the number of indivudals that will start as infected in the overall population. Input type: Positive Integer.")
        argparser.add_argument('--cities_file', '--cf', nargs=1, required=False, help="This is the complete filepath to the cities configuration file. Input type: complete file path.")
        argparser.add_argument('--planes_file', '--pf', nargs=1, required=False, help="This is the complete filepath to the planes configuration file. Input type: complete file path.")
        argparser.add_argument('--sim_time', '--st', nargs=1, required=False, help="This is the number of days that the simulation should run until. Input type: Positive Integer.")
        argparser.add_argument('--daily_travel_percentage', '--dtp', nargs=1, required=False, help="This is the percentage of daily travel. Input type: Positive floating value.")

        #create the namespace
        program_options = argparser.parse_args()
        return program_options
            
    def argparse_helper(self, options):
        """
        Namespace -> Namespace
        This function adjusts the values of the program options.
        Since nargs is set to 1, each options value is a list of the args, so
        since we only have one argument we take the first index of that list.
        If the options were not specified default to hard set contagion configuration information.
        """
        #get the absolute paths for the cities and planes configuration file
        #if the planes file was not given via command line try to open the 
        #file in the local directory
        if(options.planes_file == None):
            try:
                planes_file = open(self.planes_file, "r")
                planes_file.close()
            #if the file cannot be opened find the file in the local machine
            except:
                #if the file does exist fine the location
                if(os.path.exists(PLANES)):
                    self.planes_file = get_file_paths(PLANES)
                else:
                    #if the file does not exist raise an error
                    os.system('cls' if os.name == 'nt' else 'clear')
                    raise Exception("ERROR: No configuration file for planes found. Please provide one using command line arguments or placing the default file (planes.tsv) in the config folder within the systems main directory.")

        #If no cities file was given via the command line.
        if(options.cities_file == None):
            #try to open the file in the default location
            try:
                cities_file = open(self.cities_file, "r")
                cities_file.close()
            except:
                #if the file cannot be opened check to see if the file exists
                if(os.path.exists(CITIES)):
                    #if the file exists find the file path
                    self.cities_file = get_file_paths(CITIES)
                else:
                    #if it does not exist raise an error
                    os.system('cls' if os.name == 'nt' else 'clear')
                    raise Exception("ERROR: No configuration file for cities found. Please provide one using command line arguments or placing the default file (cities.tsv) in the config folder within the systems main directory.")
        #create arg_dict based on hard coded atts at the top
        arg_dict = {"R_0": self.R_0, "life_time": self.life_time, "death_rate": self.death_rate, "cities_file": self.cities_file, "planes_file": self.planes_file, "sim_time": 25, "infected_count": 5, "daily_travel_percentage": self.daily_travel_percentage}
        #iterate through each field in the argparse
        #if any argument is empty replace it
        #if the argument is not empty grab the first item in the list of the argument
        #this is because the argparse will great a list for each argument
        for arg in vars(options):
            att_value = getattr(options, arg)
            att_value = arg_dict[arg] if att_value == None else att_value[0]
            setattr(options, arg, att_value)
        return options

    def collect_and_return_args(self):
        """
        None -> Namespace
        This function ties the two functions above together.
        This function has a major role of obtaining user arguments and ensuring they are given the 
        right arguments if none are provided.
        """
        #obtain the options for the program
        options = self.obtain_command_line_args()
        #adjust value types
        options = self.argparse_helper(options)
        return options
