from database import Library
import aiatools
from saveVar import save_var, restore_var

import sys
import argparse

parser = argparse.ArgumentParser(description='Data analysis tools for edit stream data.')
parser.add_argument('-d', '-u', '--userFiles', help='Path to userFiles input folder')
parser.add_argument('-f', '--file', help='Saved pickle file from which to restore data')
parser.add_argument('-e', '--empty', action='store_true',
                    help='Initialize with an empty database, useful for testing the environment')

args = parser.parse_args()

# Main function
if __name__ == '__main__':

    if sys.version_info.major < 3:
        print("Requires Python 3.")
        exit(1)

    base_dir = '../data/userFiles-YPP/userFiles'  # overwritten by command line option

    if args.userFiles:
        base_dir = args.userFiles

    a = None

    if args.file:
        """Load from previously saved pickle file"""
        a = Library.from_raw_file(args.file)
    elif args.empty:
        """Don't load anything! Init an empty library."""
        a = Library([])
    else:
        """Load from a raw userFiles directory"""
        a = Library.from_dir(base_dir)

    if a is not None:
        print("Imported all projects into variable a.")
