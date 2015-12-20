# tktk.py
# Python 2.7.6

"""
A simple form that prompts for name and prints it back
"""

import Tkinter as tk # use "tkinter" for python 3.x

# All widgets belong to a parent which is defined first
root = tk.Tk()

root.wm_title("Entry form")

# Widgets are 2 types
# Input widgets - Entry, Text, Button, Radiobutton, Checkbutton
# Output widgets - Label, PhotoImage/ BitmapImage, Listbox, Menu
# With event bindings, some widgets play dual role

# Define a label widget within parent widget
label = tk.Label(root, text="What is your name?")

# Define a entry widget within parent widget
entry = tk.Entry(root)

# Define the output label, the text variable is binded with submit button
display = tk.Label(root)

# Binding method based on button click
def buttonClick():
	msg = "Hello " + entry.get() + "!!"
	display.config(text=msg)

# Define the  submit button
button = tk.Button(root, text="Submit", command=buttonClick)


# How the widgets are displayed is determined by geometry managers
# There are 3 types of geometry managers
# 1. pack - used to fill parent by widgets as TOP, BOTTOM etc.
# 2. grid - widget in row and column positions
# 3. place - custom window layouts

label.grid(row=0, column=0)
entry.grid(row=0, column=1)
button.grid(row=0, column=3)
display.grid(row=1, column=0)

# Break out of current execution environment and run from main frame
root.mainloop()