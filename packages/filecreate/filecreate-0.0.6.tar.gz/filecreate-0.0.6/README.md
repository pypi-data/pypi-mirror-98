# FileCreate
[![PyPI](https://img.shields.io/pypi/v/FileCreate)](https://pypi.org/project/winregmgr/)

Provides functionality for creating a new empty file with unique name.

The file_mask parameter may contain a sequence of hash marks '#' which will be substituted by a unique sequence number 
starting from 001. 

## Install:

```bash  
$ pip install FileCreate
```  

## Usage Samples:

```Python
from filecreate import FileCreate

# Create file using mask
with FileCreate('test####.txt') as file:    # if test0001.txt does not exist - creates it
    file.writelines()                       # working with file descriptor as usual

# Get available file name without creating an actual file
filename = FileCreate.get_filename('Folder', 'test###.txt')

```

