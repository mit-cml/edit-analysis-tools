# Analysis Tools for Edit Operations Data

## Interactive Environment
Recommended environment is [IPython](https://github.com/ipython/ipython), version 6 or above. 
```bash
$ ipython -i main.py
```
Also works equally well with ```$ python3 -i```.
*Requires Python 3* (which is included in IPython >=6). 

## Usage
```bash
$ python3 main.py -h
usage: main.py [-h] [-u USERFILES]

Data analysis tools for edit stream data.

optional arguments:
  -h, --help            show this help message and exit
  -u USERFILES, --userFiles USERFILES
                        path to userFiles input folder
```
The `-u USERFILES` argument will overwrite the hard-coded default directory from which to read in userFiles data.

## Data Structures
Snapshot:
* contents - state of the project, basically raw import from the collection server
* flags - metadata added during processing. Starts empty at import.
* date - date/time the snapshot was received by the server. Copied from contents during import.

## Modules
### main
Provides command line interface, loads data into memory, and presents interactive analysis environment. 

### dataImportJson
Imports raw data from a userFiles directory. Entry point is generally ```import_all_projects(folder)``` which will 
return all projects organized in a hierarchy of user/project/snapshots. This is the default behavior when running main.

This module:
* combines snapshots from all screens in a project into a single snapshot stream 
* copies the received date/time out of the snapshot contents into the top-level structure field ```date```

## Development
Recommend using [JetBrains PyCharm](https://www.jetbrains.com/pycharm/). Configuration files are included. 

Code style is [PEP-8](https://www.python.org/dev/peps/pep-0008/). 
