import os
import json
import pickle
from pprint import pprint


# list of users to always ignore in data processing
# used for test data, researcher accounts, etc
ignore_users = []
# it will be populated from this file, if it exists:
ignore_users_file = 'ignore_users_msp'


# reads a file as lines, and takes the first token from that file
# allows for comments to be on any line in the file after white space.
# used for configuration files, not snapshot data.
# Example: ignore_users is read in with this to establish a list of users whose data should be ignored.
def readFileLines(filename):
	if os.path.isfile(filename):
		with open(filename) as afile:
			datalines = [line.split()[0] for line in afile.readlines()]
		return datalines
	else:
		return []


# if there is an ignore_users file, read it in and populate the ignore list.
# ignore_users will take the first token on each line as a username.
ignore_users.extend(readFileLines(ignore_users_file))


# Find all users in the database, store as variable users
def isUserDir(basefolder, udir):
	return os.path.isdir(os.path.join(basefolder, udir))


# gets the list of all users in a folder
# Users do have absolute path included.
def getAllUsersIn(folder):
	userFiles = os.path.abspath(folder)
	return [os.path.join(userFiles, user) for user in os.listdir(userFiles) if isUserDir(folder, user) if
			user not in ignore_users]


# walk through all the users and all of their projects
def filterAllProjectsIn(folder, filterProc=lambda x: True):
	"""Returns list of all projects that match that satisfied filterProc.
		filterProc: isTemperatureActivity, isDebuggingActivity"""
	value = []
	for user in getAllUsersIn(folder):
		dirs_in_user = [os.path.join(user, repo) for repo in os.listdir(user)]
		for repo in dirs_in_user:
			if filterProc(repo):
				value.append(repo)

	return value

# make pickle file for all Json files in repo, sorted by time
def makePickles(repo):

	snapshots = []
	screen_names = os.listdir(repo)

	# screens = [os.path.join(repo, screen_name) for screen_name in screen_names]

	for screen_name in screen_names:

		screen = os.path.join(repo, screen_name)

		if not os.path.isdir(screen):
			continue

		for filename in os.listdir(screen):
			if filename == '.DS_Store':
				continue
			snapshot = convertJson2dict(filename, screen)
			# snapshot["screen"] = screen_name
			snapshots.append(snapshot)

	snapshots.sort(key = lambda x: x['sendDate'])
	pickle.dump(snapshots, open(repo + '/' + os.path.basename(repo) + '.p', 'wb'))



# This global variable holds files that caused problems 
# during json.load in convertJson2pickle
problem_files = []


# convert json file to Python dictionary
def convertJson2dict(filename, folder):
	file = os.path.join(folder, filename)
	with open(file) as afile:
		data = json.load(afile)
	return data

# Main function
if __name__ == '__main__':

	repos = filterAllProjectsIn('/Users/mark/data-local/userFiles-YPP/userFiles')

	for repo in repos:
		if os.path.isdir(repo):
			makePickles(repo)

	if len(problem_files) == 0:
		print('OK')
	else:
		print('Problem Files:')
		pprint(problem_files)

