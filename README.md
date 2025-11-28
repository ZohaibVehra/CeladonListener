# CeladonListener
A script to get notifications from Celadon discord server for sale pings and automatically respond as needed
Meant to run on a VM and will communicate to external PC.


# Requirements
pip install pyautogui
pip install python-dotenv
pip install pyperclip
pip install psutil
pip install pywin32
pip install flask
pip install requests


# env file set up
D1_NEWPOST=%coordinates of the bottom left corner of the latest discord post, slightly below and left of the icon%  example -> D1_NEWPOST=14.8,42.01
DISCORD_EXE= your_path_to_discord/Update.exe
DISCORD_ARGS=--processStart Discord.exe
SEVERICON=server icon coordinates