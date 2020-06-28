import hinter.ui.main
import tkinter
from dotenv import load_dotenv

load_dotenv('.env')


###

def NewFile():
    print("New File!")

###

hinter.ui.main.UI.root.mainloop()
