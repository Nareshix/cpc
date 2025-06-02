# Cpc
A simple script to copy the contents of a file to the clipboard using `wl-copy` on Wayland

## Note
Tested only on Debian 12 (GNOME 43.9). Requires `wl-copy`  to be installed.

## Installation

### 1. Wget 
```bash
wget https://raw.githubusercontent.com/nareshix/cpc/main/cpc.sh -O ~/.local/bin/cpc && chmod +x ~/.local/bin/cpc
```

### 2. Curl 
```bash
curl -fSL https://raw.githubusercontent.com/nareshix/cpc/main/cpc.sh -o ~/.local/bin/cpc && chmod +x ~/.local/bin/cpc
```


Make sure `~/.local/bin` is in your `PATH`.

## Usage

```bash
cpc <filename>
```

Copies the contents of `<filename>` to your clipboard and prints the content.

Example:

`notes.txt` contains
```
hello
there
my
name is
Naresh
and naresh is awesome
```
Running
```bash
cpc notes.txt
```
outputs:
```
Copied:

hello
there
my
name is
Naresh
and naresh is awesome
```
and is also saved to ur clipboard (can use ```ctrl + v``` to start pasting)
