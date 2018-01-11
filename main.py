from database import Library

import sys
import argparse

parser = argparse.ArgumentParser(description='Data analysis tools for edit stream data.')
parser.add_argument('-u', '--userFiles', help='path to userFiles input folder')
parser.add_argument('-f', '--file', help='saved pickle file from which to restore data')

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
        a = Library.from_file(args.file)
    else:
        """Load from a raw userFiles directory"""
        a = Library.from_dir(base_dir)

    if a is not None:
        print("Imported all projects into variable a.")
