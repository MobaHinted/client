import subprocess

buildCommand = 'pyinstaller --onefile main.py'

process = subprocess.Popen(buildCommand.split(), stdout=subprocess.PIPE)
process.wait()

moveCommand = 'mv ./dist/main.exe ./main.exe'
process = subprocess.Popen(moveCommand.split(), stdout=subprocess.PIPE)
process.wait()

removeCommand = 'rm -rf ./build && rm -rf ./dist && rm -rf ./main.spec'

process = subprocess.Popen(removeCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print(output, error)
