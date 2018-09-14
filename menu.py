import tkinter as tk
import subprocess

grey = '#708090'

def raise_frame(frame):
    frame.tkraise()

def navit_window():
        subprocess.call(['navit'])

def obd_hud():
        subprocess.call(['python3'] + ['hud.py'])

def backup_view():
        subprocess.call(['python3'] + ['backup_camera.py'])
        #subprocess.call(['sudo'] + ['raspi-config']) #raspberry pi only program for the test

def yes_option():
        subprocess.call(['shutdown'] + ['now']) #Linux only "shut it down, shut it down forever" - Mr Book
        #subprocess.call(['sudo'] + ['shutdown'] + ['now']) #need sudo? maybe?

menu = tk.Tk()

menu_frame1 = tk.Frame(menu) #menu page 1
menu_frame2 = tk.Frame(menu) #menu page 2
b_height = 4
b_width = 8
size = 18
screen_width = menu.winfo_screenwidth()
screen_height = menu.winfo_screenheight()
screen_resolution = str(screen_width)+'x'+str(screen_height)
menu.configure(background= grey)
#menu.geometry(screen_resolution) #full screen 
menu.geometry('1024x600') #raspberry pi 7" touch screen emulation 
menu.resizable(0, 0)
#menu.attributes("-fullscreen", True) #forces full screen uncomment later
menu.title("My simple GUI")

for frame in (menu_frame1, menu_frame2):
    frame.grid(row=0, column=0, sticky='nsew')
    frame.configure(background=grey)
#menu page 1
tk.Label(menu_frame1, text='Smarter Car\nMain Menu',font=("Tahoma",size), bg = grey).pack(padx=10, pady=20, side='left')
tk.Button(menu_frame1, text = 'OBD HUD', command = obd_hud, height = b_height,
          width = b_width, font=("Tahoma",size), highlightbackground = grey).pack(padx=5, pady=20, side='left')
tk.Button(menu_frame1, text = 'Navit\nGPS', command = navit_window, height = b_height,
          width = b_width, font=("Tahoma",size), highlightbackground = grey).pack(padx=5, pady=20, side='left')
tk.Button(menu_frame1, text = 'Backup\nCamera\nView', command = backup_view, height = b_height,
          width = b_width, font=("Tahoma",size), highlightbackground = grey).pack(padx=5, pady=20, side='left')
tk.Button(menu_frame1, text = 'Close', command = menu.quit, height = b_height,
          width = b_width, font=("Tahoma",size), highlightbackground = grey).pack(padx=5, pady=20, side='left') #doesn't work in idle but fine in python3 grrrr
tk.Button(menu_frame1, text='Power Off\n The Pi', command=lambda:raise_frame(menu_frame2), height = b_height,
          width = b_width, font=("Tahoma",size), highlightbackground = grey).pack(padx=5, pady=20, side='left')

#menu page 2
tk.Label(menu_frame2, text='Please Confirm that Action', bg = grey).pack()
tk.Button(menu_frame2, text = 'Yes\nI\'m Sure\nPower Off', command = yes_option, bg = 'red',activebackground='red',
          height = b_height, width = b_width, font=("Tahoma",size), highlightbackground = grey).pack()
tk.Button(menu_frame2, text='NO\nGo Back to\nMain Menu', command=lambda:raise_frame(menu_frame1),
          height = b_height, width = b_width, font=("Tahoma",size), highlightbackground = grey).pack()

raise_frame(menu_frame1) #display menu page 1
menu.mainloop()
