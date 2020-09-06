import os

os.system('pyinstaller --onefile main.py')
os.system('copy .\\dist\\main.exe .\\MobaHinted.exe /a')
os.system('del /f .\\build\\, .\\dist\\, .\\main.spec /Q')
