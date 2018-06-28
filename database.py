from dataImportJson import *
from saveVar import *
from dataIntegrity import *
from pprint import pprint
from datetime import datetime, timedelta
from io import StringIO
from sessions import divide_sessions
from sessions import print_session_summary as sessions_print_session_summary

import pkg_resources
import aiatools

print_errors = True

if not pkg_resources.get_distribution("aiatools").version.startswith('p3-'):
    raise ImportWarning("aiatools does not appear to be from the Python3 branch.")


class Library:
    """Hierarchical database of users and their projects, suitable for data inquiry."""

    def __init__(self, array):
        """Initializes a library with array as its data."""
        self.raw = array
        self.users_list = [User(u) for u in array]
        self.users = {u.user_name: u for u in self.users_list}

        names = list(self.user_names())
        for name in names:
            if names.count(name) > 1:
                raise Warning("User " + name + " found more than once in Library.")

    @classmethod
    def from_dir(cls, directory):
        """Imports data from a database directory."""
        users = get_all_user_names_in(directory)
        projects = get_all_projects_in(directory)

        print("Using " + directory)
        print("Found " + str(len(projects)) + " total projects.")
        print("Found " + str(len(users)) + " users:")
        pprint(users)
        print("Importing...")
        return cls(import_all_projects(directory))

    @classmethod
    def from_raw_file(cls, file):
        """Initializes a library with restored data from a pickle file."""
        return restore_var(file)

    def save(self, file):
        """Saves this library to a file on disk, under the given file name."""
        save_var(self, file)

    def user_names(self):
        return self.users.keys()

    def all_projects(self):
        """Returns all projects in this library as a single list, irrespective of users."""
        projects = []
        for u in self.users_list:
            projects.extend(u.projects_list)
        return projects

    def divide_sessions(self, idle_time=timedelta(hours=2)):
        for p in self.all_projects():
            p.divide_sessions(idle_time)

    def print_session_summary(self, idle_time=None):
        """
        Prints out a summary table of all the individual sessions in the given library.

        If the idle_time parameter is specified, it will re-segment all the sessions with the given time,
        overwriting the previous session data.

        :param idle_time: Timeout
        :type idle_time: timedelta
        :return:
        """
        sessions_print_session_summary(self, idle_time)

    def get_project(self, name):
        """
        Gets projects by matching the project's name, irrespective of which user owns it.
        :param name: name to match
        :return: list of projects
        """
        return [p for p in self.all_projects() if p.project_name == name]

    def __getitem__(self, item):
        return self.users[item]


class User:
    """Container representing a single user, which is a collection of projects."""

    def __init__(self, array):
        self.projects_list = [Project(p) for p in array]
        self.user_name = self.projects_list[0].user_name
        self.projects = {p.project_name: p for p in self.projects_list}
        self.project_ids = {p.project_id: p for p in self.projects_list}

        if len(self.projects_list) == 1:
            self.only_one_project = True
            self.the_project = self.projects_list[0]
        else:
            self.only_one_project = False

    def length(self):
        return len(self.projects_list)


class Project:
    """Container class representing a single project, which is a collection of snapshots, and some metadata."""

    def __init__(self, array):
        self.snapshots = []
        dropped_snapshots = 0
        for s in array:
            snap = Snapshot(s)
            if snap.init:
                self.snapshots.append(snap)
            else:
                dropped_snapshots += 1

        self.user_name = self.snapshots[0].user_name
        self.project_name = self.snapshots[0].project_name
        self.project_id = self.snapshots[0].project_id

        if dropped_snapshots > 0:
            print("Dropped " + str(dropped_snapshots) + " snapshots from " + self.user_name + "/" + self.project_name)

        self.last = self.snapshots[-1]

        """Generate time deltas"""
        # All snapshots now initialize with deltas initialized to 0

        for i in range(1, len(self.snapshots)):
            self.snapshots[i].delta = self.snapshots[i].date - self.snapshots[i-1].date
            if self.snapshots[i].receive_date:
                self.snapshots[i].receive_date_delta = self.snapshots[i].receive_date - \
                                                       self.snapshots[i - 1].receive_date
                self.snapshots[i].send_date_delta = self.snapshots[i].send_date - self.snapshots[i - 1].send_date

        self.sessions = None
        self.session_count = None
        self.divide_sessions()

    def divide_sessions(self, idle_time=timedelta(hours=2)):
        """Separate into sessions"""
        self.sessions = divide_sessions(self.snapshots, idle_time)
        self.session_count = len(self.sessions)

    def length(self):
        return len(self.snapshots)


class Snapshot:
    """A project's state at a single moment in time."""

    def __init__(self, dictionary):
        self.init = False

        try:
            check_blocks_corruption(dictionary['contents']['blocks'])
            check_all_fields_present(dictionary)

            self.raw = dictionary
            self.send_date = datetime.strptime(self.raw['contents']['sendDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
            if 'receiveDate' in self.raw['contents']:
                self.receive_date = datetime.strptime(self.raw['contents']['receiveDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                self.receive_date = None
            self.date = self.send_date
            self.user_name = self.raw['contents']['userName']
            self.project_name = self.raw['contents']['projectName']
            self.project_id = self.raw['contents']['projectId']
            if '_' in self.raw['contents']['screenName']:
                self.screen_name = self.raw['contents']['screenName'].split('_')[1]
            else:
                self.screen_name = self.raw['contents']['screenName']
            self.screen_id = self.raw['contents']['screenName']
            self.session_id = self.raw['contents']['sessionId']

            # print(self.user_name + " " + self.project_name)
            form = adapt_form_for_aiatools(self.raw['contents']['form'])
            blocks = StringIO(self.raw['contents']['blocks'])
            self.screen = aiatools.Screen(form=form, blocks=blocks)

            self.delta = self.receive_date_delta = self.send_date_delta = timedelta(0)
            self.init = True

        except DataIntegrityException as err:
            if print_errors:
                print(err.message)
                # print("Dump of bad snapshot: ")
                # pprint(err.snapshot_contents)
            pass


def adapt_form_for_aiatools(form):
    return StringIO('\n' + '$JSON\n' + form)



