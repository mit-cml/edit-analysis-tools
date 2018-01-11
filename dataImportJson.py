"""
    Imports raw data from snapshot server into python environment.
    The input file structure from the snapshot server looks like this:
        userFiles/                              <-- hard-coded name of the base folder
            user/                               <-- username (usually a code name)
                projectName#projectID/          <-- project folder (named after the projects name AND ID number)
                    screenID_ScreenName/        <-- Screen (there is always 'nnn_Screen1', could be more with any name)
                        snapshot_2017-08-10T17:43:26.764Z.json
                                                ^-- Any number of snapshots, named after their date/time

    Conventions:
    "folder" suffix refers to actual directory on-disk. Is a full path.
    "base" is the folder containing all the user folders.
    "user" is a directory in the base containing projects.
    "project" is a directory in a user folder that contains snapshots, separated by screens.
    "snapshot" is a single captured frame of the project, containing the entire app state at that moment

    The output of this is is a collection of users, which is a collection of projects, which is a list of snapshots.

    Snapshot data structure is a dictionary:
    {
        'contents'  : dictionary, actual contents from the snapshot server
        'flags'     : dictionary, flags referring to signals found and other metadata
        'date'      : string, date/time for indexing. There is also a date in 'contents'.
    }

    Authors:
    Diane Zhou <dianezhou96@gmail.com>
    Mark Sherman <shermanm@mit.edu>
    Coding style: PEP8
    python version >= 3.6
"""

import os
import json


# list of users to always ignore in data processing
# used for test data, researcher accounts, etc
ignore_users = []
# it will be populated from this file, if it exists:
ignore_users_file = 'ignore_users'

# list of files to always ignore
ignore_files = ['.DS_Store']


# reads a file as lines, and takes the first token from that file
# allows for comments to be on any line in the file after white space.
# used for configuration files, not snapshot data.
# Example: ignore_users is read in with this to establish a list of users whose data should be ignored.
def read_file_lines(filename):
    if os.path.isfile(filename):
        with open(filename) as a_file:
            data_lines = [line.split()[0] for line in a_file.readlines()]
        return data_lines
    else:
        return []


# if there is an ignore_users file, read it in and populate the ignore list.
# ignore_users will take the first token on each line as a username.
ignore_users.extend(read_file_lines(ignore_users_file))


def list_dir(folder):
    return [f for f in os.listdir(folder) if f not in ignore_files]


# True if given entity in a folder is itself a folder, not a file.
def is_folder(folder, entity):
    return os.path.isdir(os.path.join(folder, entity))


def get_all_user_names_in(base_folder):
    """gets a list of all the users in the base folder"""
    base_path = os.path.abspath(base_folder)
    return [user for user in list_dir(base_path) if is_folder(base_folder, user)]


def get_all_user_folders_in(base_folder):
    """gets the list of all users in a base folder, returning list of the full paths to each user's folder"""
    base_path = os.path.abspath(base_folder)
    return [os.path.join(base_path, user) for user in get_all_user_names_in(base_folder)]


def get_projects_of_user(user_folder):
    """gets the list of all projects in a user, returning list of full paths to each project"""
    return [os.path.join(user_folder, folder) for folder in list_dir(user_folder)]


def get_all_projects_in(base_folder, filter_procedure=lambda x: True):
    """Returns list of all projects for all users in a base folder. Is a list of folder paths.
        filter_procedure can be used to run a test on each project folder, where True includes that project."""
    all_projects = []
    for user in get_all_user_folders_in(base_folder):
        project_folders = [os.path.join(user, folder) for folder in list_dir(user)]
        for project in project_folders:
            if filter_procedure(project):
                all_projects.append(project)

    return all_projects


def make_empty_snapshot():
    """Returns an empty snapshot structure."""
    return dict(contents={}, flags={}, date="No date set. Look in 'contents'")


def import_project(project_folder):
    """Imports all screens of a given project and returns a date-sorted list of snapshots"""
    snapshots = []
    screens = [s for s in list_dir(project_folder) if s not in ignore_files]

    for screen_name in screens:

        screen = os.path.join(project_folder, screen_name)

        if not os.path.isdir(screen):
            continue

        for filename in list_dir(screen):
            if filename in ignore_files:
                continue
            snapshot = make_empty_snapshot()
            snapshot['contents'] = convert_json_to_dict(filename, screen)
            snapshot['date'] = snapshot['contents']['sendDate']
            snapshots.append(snapshot)

    snapshots.sort(key=lambda x: x['date'])
    return snapshots


def import_users_projects(user_folder):
    """Imports all projects from a specific user folder, returning a list of the projects."""
    return [import_project(p) for p in get_projects_of_user(user_folder)]


def import_all_projects(base_folder):
    """Imports all projects from all users, hierarchically organized [user[project...], user[...]]"""
    return [import_users_projects(u) for u in get_all_user_folders_in(base_folder)]


# convert json file to Python dictionary
def convert_json_to_dict(filename, folder):
    file = os.path.join(folder, filename)
    with open(file) as afile:
        data = json.load(afile)
    return data
