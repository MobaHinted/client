import os

os.system('pyinstaller --onefile -p=.\\venv\\Lib\\site-packages -i .\\assets\\logo.ico main.py')
os.system('copy .\\dist\\main.exe .\\MobaHinted.exe /a')
os.system('rmdir /s /q .\\build\\, .\\dist\\')
os.system('del /f /q .\\main.spec')
