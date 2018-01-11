from dataImportJson import *
from saveVar import *
from pprint import pprint


class Library:
    """Hierarchical database of users and their projects, suitable for data inquiry."""

    def __init__(self, array):
        """Initializes a library with array as its data."""
        self.a = array

    @classmethod
    def from_dir(cls, directory):
        """Imports data from a database directory."""
        users = get_all_user_names_in(directory)
        projects = get_all_projects_in(directory)

        print("Using " + directory)
        print("Found " + str(len(projects)) + " total projects.")
        print("Found " + str(len(users)) + " users:")
        pprint(users)
        return cls(import_all_projects(directory))

    @classmethod
    def from_file(cls, file):
        """Initializes a library with restored data from a pickle file."""
        return cls(restore_var(file))

    def save(self, file):
        """Saves this library to a file on disk, under the given file name."""
        save_var(self.a, file)

