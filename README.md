# Analysis Tools for Edit Operations Data

## Interactive Environment
Recommended environment is [IPython](https://github.com/ipython/ipython), version 6 or above. 
```bash
$ ipython -i main.py
```
To load from a previously saved state file (on disk as mystate.pickle), use below.
The double-dash tells ipython to send subsequent args to the script.
```bash
$ ipython -i main.py -- -f mystate
```
Also works equally well with ```$ python3 -i```.
You can use *pyenv* to set up default python to be python 3.
*Requires Python 3* (which is included in IPython >=6). 

## Usage
```bash
$ python main.py -h
usage: main.py [-h] [-u USERFILES] [-f FILE]

Data analysis tools for edit stream data.

optional arguments:
  -h, --help            show this help message and exit
  -u USERFILES, --userFiles USERFILES
                        path to userFiles input folder
  -f FILE, --file FILE  saved pickle file from which to restore data
```
The `-u USERFILES` argument will overwrite the hard-coded default directory from which to read in userFiles data.
The `-f FILE` argument will ignore the input folder and instead load a previously-saved database from the given file.

## Data Structures
Library (class):
* Class for holding, interrogating, and updating a database of collected data.
* A Library is a dictionary of users, indexed by their user name.
* A User is a dictionary of projects, indexed by the project name, in addition to the user's name.
* A Project is a list of snapshots, in time-order, in addition to some useful metadata.
* A Snapshot represents the state of a project (app) at a point in time:
  * A snapshot was created for every code or design change during development.
  * A Snapshot object contains many metadata fields, including a processed date as a python datetime object.
  * A Snapshot object also includes a Screen representation provided by AIATools for in-depth code analysis.

## Importing Data
### Ignoring users during import
In the working directory of this script, place a file named *ignore_users* which lists users (as codenames),
with one user per line. This is useful when you have users who are to be ignored from experimental data,
which may include research staff or participants who did not complete informed consent.
Any text after whitespace on a line will be ignored, so it can be used for comments.
### Ignoring certain files
In `dataImportJson.py` there is a list of strings `ignore_files`. All file names in there will be ignored.
The default is `'.DS_Store'` to prevent Mac OS metadata from being processed.


## Development
Recommend using [JetBrains PyCharm](https://www.jetbrains.com/pycharm/). Configuration files are included. 

Code style is [PEP-8](https://www.python.org/dev/peps/pep-0008/). 
