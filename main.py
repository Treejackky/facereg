from tkinter import *
from tkinter import ttk
import os
import f_main
from datetime import datetime
from ttkthemes import ThemedStyle 
 


def opne_reg():
    os.system('python g_register.py')

def open_print():
    os.system('python g_print.py')

def open_work():
    os.system('python g_go_work.py')

# instacio recognizer
recognizer = f_main.rec()



root = Tk()
root.title("ระบบสแกนใบหน้าลงเวลางาน")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.attributes('-fullscreen', True)

# Center the window
window_width = 900
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.attributes('-fullscreen', True)

style = ThemedStyle(root) # Use ThemedStyle
style.set_theme("arc")# Set the theme
style.configure("TFrame")
style.configure("TButton", foreground="#000", font=("Arial", 14))
style.configure("TLabel", foreground="#000", font=("Arial", 18))

frame_header = ttk.Frame(root, style="TFrame", padding="10 10 10 10")
frame_header.place(relx=0.5, rely=0.1, anchor="center")

current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
header_label = ttk.Label(frame_header, text="ระบบสแกนใบหน้าลงเวลางาน\nวันที่และเวลา: {}".format(current_datetime), style="TLabel")
header_label.pack()

frame_content = ttk.Frame(root, style="TFrame", padding="10 10 10 10")
frame_content.place(relx=0.5, rely=0.5, anchor="center")

btn_checkin = ttk.Button(frame_content, text="ลงเวลางาน", command= open_work, style="TButton")
btn_checkin.grid(row=0, column=0, padx=20, pady=10, sticky='e')

btn_checkout = ttk.Button(frame_content, text="ลงทะเบียน", command= opne_reg, style="TButton")
btn_checkout.grid(row=0, column=1, padx=20, pady=10, sticky='e')

btn_admin = ttk.Button(frame_content, text="รายงานลงเวลา", command= open_print, style="TButton")
btn_admin.grid(row=0, column=3, padx=20, pady=10, sticky='e')

btn_exit = ttk.Button(frame_content, text="ออก", command=root.quit, style="TButton")
btn_exit.grid(row=0, column=4, padx=20, pady=10, sticky='e')

root.mainloop()


