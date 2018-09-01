import tkinter as tk
#from tkinter import *
import subprocess

grey = '#708090'

def raise_frame(frame):
    frame.tkraise()

def libre_window():
        subprocess.call(['libreoffice'])

def obd_hud():
        subprocess.call(['python3'] + ['hud3.py'])

def raspi_config():
        subprocess.call(['sudo'] + ['raspi-config'])

def yes_option():
        subprocess.call(['shutdown'] + ['now'])
        #subprocess.call(['sudo'] + ['shutdown'] + ['now']) #need sudo?

menu = tk.Tk()

f1 = tk.Frame(menu)
f2 = tk.Frame(menu)
b_height = 4
b_width = 8
screen_width = menu.winfo_screenwidth()
screen_height = menu.winfo_screenheight()
screen_resolution = str(screen_width)+'x'+str(screen_height)
menu.configure(background= grey)
menu.geometry(screen_resolution)
menu.geometry('800x480') #raspberry pi 7" touch screen emulation 
menu.resizable(0, 0)
menu.title("My simple GUI")

for frame in (f1, f2):
    frame.grid(row=0, column=0, sticky='nsew')
    frame.configure(background=grey)

tk.Label(f1, text='Main Menu', bg = grey).pack(padx=100, pady=20, side='left')
tk.Button(f1, text = 'OBD HUD', command = obd_hud, height = b_height, width = b_width, highlightbackground = grey).pack(padx=5, pady=20, side='left')
tk.Button(f1, text = 'Libre Office', command = libre_window, height = b_height, width = b_width, highlightbackground = grey).pack(padx=5, pady=20, side='left')
tk.Button(f1, text = 'Raspi\nConfig', command = raspi_config, height = b_height, width = b_width, highlightbackground = grey).pack(padx=5, pady=20, side='left')
tk.Button(f1, text = 'Close', command = menu.quit, height = b_height, width = b_width, highlightbackground = grey).pack(padx=5, pady=20, side='left')
tk.Button(f1, text='Power Off\n The Pi', command=lambda:raise_frame(f2), height = b_height, width = b_width, highlightbackground = grey).pack(padx=5, pady=20, side='left')


tk.Label(f2, text='Please Confirm that Action', bg = grey).pack()
tk.Button(f2, text = 'Yes\nI\'m Sure\nPower Off', command = yes_option, bg = 'red',activebackground='red', height = b_height, width = b_width, highlightbackground = grey).pack()
tk.Button(f2, text='NO\nGo Back to\nMain Menu', command=lambda:raise_frame(f1), height = b_height, width = b_width, highlightbackground = grey).pack()

raise_frame(f1)
menu.mainloop()
