# File-Server
File-Server is exactly what it sounds - a file server. Created using python(3.x), it currently does not contain a GUI, though I have plans to add it soon.

## Pre-Requisites
This project uses Python 3.x and pip

Installing python and pip
### Debain based systems
```
apt install python3 python3-pip
pip3 install shutil
```
### Arch based systems
```
pacman -S python python-pip
pip3 install shutil
```
### SUSE Linux based systems
```
zypper install python3 python3-pip
pip3 install shutil
```
## Usage
* Important note : Please move into server folder before executing server.py
Two terminals are required - one to run client program and the other to run the server program

### To run server program
```
cd server
python3 server.py
```

### To run client program
```
cd client
python3 client.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
