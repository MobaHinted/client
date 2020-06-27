import hinter.ui.mainScreen
import tkinter

from dotenv import load_dotenv

load_dotenv('.env')

text = tkinter.Label(hinter.ui.mainScreen.app.root, text='test')
text.pack()

hinter.ui.mainScreen.app.root.mainloop()
