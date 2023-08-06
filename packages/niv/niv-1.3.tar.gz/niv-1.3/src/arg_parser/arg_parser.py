"""
Parser class for Arguments when you start NIV
"""

import argparse
import os
from src import pathname_validitor as pv
from src.niv_logger.niv_logger import NivLogger
from src.yaml_parser.yaml_parser import get_yaml


class ArgParser:
    """
    A class for parsing the console arguments

    Methods
    -------
    set_args():
        Adds the needed arguments to the ArgumentParser class
    """
    config = get_yaml(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config.yaml')

    # logging.basicConfig(filename='logs/arg_parser.log', level=logging.DEBUG)
    logger = NivLogger
    # Dictionary for argument choices
    ICONS = [1, 2, 3]
    DETAIL = [0, 1, 2, 3]

    def __init__(self, args):
        self.args = args
        self.parser = argparse.ArgumentParser
        self.set_args()

    def set_args(self):
        """
        Adds the needed arguments to the ArgumentParser class

        :return: Argument strings converted to objects and assigned as attributes of the namespace
        """
        parser = argparse.ArgumentParser(prog="niv",
                                         description="Creates a visualization of your network infrastructure",
                                         add_help=False)

        parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')

        parser.add_argument('-v', '--version', action='version', version='0.3',
                            help="Show program's version number and exit")

        parser.add_argument('-s', '--save', type=self.save_to_path,
                            nargs=1, metavar='SAVE_PATH',
                            help='Save .svg, .png, .jpg or .pdf file to a given path (DEFAULT: .svg)')

        parser.add_argument('-l', '--load', type=self.is_path_to_yaml_file,
                            nargs=1, metavar='LOAD_PATH',
                            help='Create visualization with a given .yaml file', )

        parser.add_argument('-d', '--detail', type=int, nargs='?', metavar='INT',
                            default=self.config.get('default').get('std_details'), choices=self.DETAIL,
                            help='The level of detail you want to use for the visualization; 1: least detail, '
                                 '2: medium detail, 3: most detail (DEFAULT: 0)')

        parser.add_argument('-vv', '--verbose', action='store_true',
                            help='Increase verbosity of console messages')

        # print(parser.parse_args("-g".split()))
        # If no argument given, print help
        if len(self.args) == 0:
            print('You didnt specify any arguments, here is some help:\n')
            parser.print_help()

        # Checks if the arguments are compatible with each other, else raise Exception
        if self.check_args_compatibility():
            self.parser = parser.parse_args(self.args)
            self.logger.log_debug("Arguments are compatible.")
            return
        raise ValueError("Arguments are not compatible.")

    def get_load(self):
        """
        :return: returns data from argument load
        """
        # For the case when no argument is given
        if len(self.args) < 1:
            return None
        # access load argument, workaround for program start
        for i, arg in enumerate(self.args):
            if arg in ("-l", "--load"):
                file_name = self.args[i + 1]
                return file_name
        raise OSError("Can\'t access file_name.")

    def get_parser(self):
        """
        :return: returns set parser from set_parser()
        """
        return self.parser

    def get_save_path(self):
        """
        :return: returns save path
        """
        return self.parser.save

    def get_verbose(self):
        """
        :return: return verbose value
        """
        return self.parser.verbose

    def get_detail_level(self):
        """
        :return: return detail level
        """
        return self.parser.detail

    @staticmethod
    def is_path_to_yaml_file(file_path):
        """
        Checks if file path is valid and file is a .yaml file

        :param file_path: path to file
        :return: path of file or raise error
        """
        # call lstrip() to remove all whitespaces in front of the path
        file_path = file_path.lstrip()
        if os.path.isfile(file_path):
            file_name = file_path.split('/')[-1]
            file_type = file_name.split('.')[-1]
            if file_type == "yaml":
                return file_path
            raise TypeError(f'"{file_name}" is not a .yaml.')
        raise OSError(f'"{file_path}" is not a valid file path or file doesn\'t exist.')

    def create_filename(self):
        """
        generate name from input file and return it
        :return: generated filename
        """
        file_name = ""
        # default_name = self.config["DEFAULT"]["std_out"]
        file_format = self.config.get('default').get('std_type')

        # if default_name == "_":
        # access load argument, workaround for program start
        for i, arg in enumerate(self.args):
            if arg in ("-l", "--load"):
                file_name = self.args[i + 1]
                break
        if file_name == "":
            raise OSError("Can\'t access file_name.")
        file_name = file_name.split('/')[-1].split('.')[0]
        file_name = f"{file_name}{file_format}"
        return file_name

        # return default_name + file_format

    def save_to_path(self, path):
        """
        Checks if the path is a file path or a directory path
        and check for validity

        :param path: path to where the file should be saved
        :return: path to file or raise error
        """
        # check if path is valid and (creatable or exists)
        if pv.is_path_exists_or_creatable(path):
            # if path is directory, create filename
            if os.path.isdir(path):
                if path == ".":
                    path = path + "/"
                return path + self.create_filename()

            # if path leads to a file
            if os.path.isfile(path):
                # if file is in the directory, raise error
                if pv.is_file_not_in_directory(path):
                    raise FileExistsError(f"{path} already exists")
                # if file format isnt pdf, png, svg or jpg, raise error
                if not pv.check_file_format(path):
                    raise TypeError('Wrong Fileformat, use ".svg", ".png", ".pdf" or ".jpg"')

            # otherwise return path
            return path
        raise OSError(f"{path} is not a valid path")

    def check_args_compatibility(self):
        """
        Checks if the given arguments are compatible with each other

        :return: true, if arguments are compatible. false, if not
        """
        # Set variable to True if argument is given
        load = "--load" in self.args or "-l" in self.args
        version = "--version" in self.args or "-v" in self.args
        hlp = "--help" in self.args or "-h" in self.args

        # If no arguments are given
        if len(self.args) == 0:
            return True

        # If only help or version are given
        if len(self.args) == 1 and (version or hlp):
            return True

        # If load is an argument
        if load:
            return True
        raise ValueError("To use NIV you need load as an argument :)")
