from dataImportJson import import_all_projects, get_all_user_names_in, get_all_projects_in

import sys
import argparse
from pprint import pprint

parser = argparse.ArgumentParser(description='Data analysis tools for edit stream data.')
parser.add_argument('-u', '--userFiles', help='path to userFiles input folder')
args = parser.parse_args()

# Main function
if __name__ == '__main__':

    if sys.version_info.major < 3:
        print("Requires Python 3.")
        exit(1)

    base_dir = '../data/userFiles-YPP/userFiles'  # overwritten by command line option

    if args.userFiles:
        base_dir = args.userFiles

    users = get_all_user_names_in(base_dir)
    projects = get_all_projects_in(base_dir)

    print("Using " + base_dir)
    print("Found " + str(len(projects)) + " total projects.")
    print("Found " + str(len(users)) + " users:")
    pprint(users)

    a = import_all_projects(base_dir)

    print("Imported all projects into variable a.")
