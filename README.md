# INSE6130
This repository will hold code as part of the INSE6130 project.

Vulnerability reproduction and testing team :
- Burak 
- Ajmain Alam 
- Abdelrahman Ragab 
- Philippe Mangeard 

Security application development team : 
- Adivardhan Maheshwari 
- Kazi Farhat Lamisa
- Melvin
- Xin

# Steps to setup the environment

To add repository and install python3.8
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8
sudo apt install python3.8-venv
```
Create virtual environment
```
python3.8 -m venv myenv
```
Activate virtual environment
```
source ./myenv/bin/activate
```
Install the requirements inside virtual environment
```
python3.8 -m pip install -r requirements.txt 
```
Use this if you are developing and have added dependencies
```
python3.8 -m pip freeze > requirements.txt
```
Run the application
```
python3.8 main.py
```
If error with qt platform crashing,
> sudo apt-get install qt5-default

Note:
These steps are written based on the assumption that many older ubuntu versions have python3.6 installed and we need the script to run on python3.8. If your machine already has python3.8 as the default version, you can skip python3.8 installation and using python3 instead of python3.8 when creating env, or pip install or running script.

# Fix scripts:
1. Each file is written for a particular CVE. The file has 2 functions: check() and fix(). 
2. check() returns True if the docker is vulnerable to that CVE otherwise False. It also returns the logs when the script has ran.
3. fix() returns True if the fix was successful without any errors otherwise it returns False. It also returns the logs when the script has ran.

# Demo
https://user-images.githubusercontent.com/48666834/232841572-d03bab0d-9bc6-48e1-ba96-6d3c8222a506.mp4




# -PyQT5_GUI_app
