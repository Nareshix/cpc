
## Table of Contents
- [Usage](#usage)
- [Installation](#installation)
- [Uninstall](#uninstall)


### note
Tested only on Debian 12 (GNOME 43.9). Requires `wl-copy`  to be installed. 
## Usage

cpc <file_or_directory> [--exclude <file/folder>, --tree <dir>]

- Copies file content if input is a file.

- Copies all files recursively (subfolders as well) if input is a directory

- can exclude a file or a folder (--exclude <file> or --exclude <folder>)

- Errors if input is neither file nor directory.

- --tree dir to just  copy the tree structure that you would usually get after running `tree`

The text file content then gets saved to ur clipboard (can use ```ctrl + v``` to start pasting)


## Installation

### Wget 
```bash
wget https://raw.githubusercontent.com/nareshix/cpc/main/cpc.sh -O ~/.local/bin/cpc && chmod +x ~/.local/bin/cpc
```
### or

### Curl 
```bash
curl -fSL https://raw.githubusercontent.com/nareshix/cpc/main/cpc.sh -o ~/.local/bin/cpc && chmod +x ~/.local/bin/cpc
```

Make sure `~/.local/bin` is in your `PATH`.


## Uninstall
run 
```bash
rm ~/.local/bin/cpc
```
