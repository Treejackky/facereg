import f_main
import cv2
import json
import uuid
import time
import argparse
import imutils
import webbrowser
import f_main
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import string
import os
import sys
import requests
from ttkthemes import ThemedStyle 


recognizer = f_main.rec()


def update_image():
    ret, frame = cam.read()
    frame = imutils.resize(frame, width=400)
    res = recognizer.recognize_face(frame)
    if not res["names"] or res["names"][0] is None:
        res["names"] = ["unknown"]
    frame = f_main.bounding_box(frame, res["faces"], res["names"])
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=im)
    image_label.config(image=img)
    image_label.image = img
    root.after(1, update_image)


def register_user():
    name = name_entry.get()
    surname = surname_entry.get()
    if name and surname:
        # Generate a unique ID for the person
        random_num = "{:02d}".format(random.randint(0, 99))  # random 2 digit number
        random_char = ''.join(random.choice(string.ascii_letters) for _ in range(2))  # random 2 letters
        person_id = name + random_num + random_char
        # Send the person's data to the server
        url = "http://localhost:3000/v1/register"
        body = {
            "id": person_id,
            "name": name,
            "surname": surname,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%d/%m/%Y")
        }
        res = requests.post(url, json=body)
        # Save the person's data
        if res.status_code == 200:
            # Save the images
            for i in range(10):
                if cam.isOpened():  # Check if the camera is opened
                    ret, frame = cam.read()
                    cv2.imwrite(f'images/{person_id}_{i}.jpg', frame)
                    time.sleep(0.5)  # delay between pictures

            # Open the file in read mode
            try:
                with open('data.json', 'r') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            # Add the new user's data to the list
            data.append(body)

            # Write the updated data back to the file
            try:
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                print("Error while writing to the file: ", e)

            messagebox.showinfo("สถานะการลงทะเบียน", "ลงทะเบียนสำเร็จ")

        else:
            messagebox.showerror("สถานะการลงทะเบียน", "ลงทะเบียนไม่สำเร็จ")


def open_camera():
    global cam
    cam = cv2.VideoCapture(0)
    update_image()



root = Tk()
root.title("ลงทะเบียนใบหน้า")

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
header_label = ttk.Label(frame_header, text="ลงทะเบียนพนักงานใหม่", style="TLabel")
header_label.grid(row=0, column=0, padx=20, pady=10)

frame_content = ttk.Frame(root, style="TFrame", padding="10 10 10 10")
frame_content.place(relx=0.5, rely=0.5, anchor="center")

# btn_checkin = ttk.Button(frame_content, text="Check_in", style="TButton")
# btn_checkin.grid(row=1, column=0, padx=20, pady=10, sticky='e')

# btn_checkout = ttk.Button(frame_content, text="Check_out", style="TButton")
# btn_checkout.grid(row=1, column=1, padx=20, pady=10, sticky='e')

# btn_register = ttk.Button(frame_content, text="Register User", style="TButton")
# btn_register.grid(row=1, column=2, padx=20, pady=10, sticky='e')

# btn_admin = ttk.Button(frame_content, text="Print", style="TButton")
# btn_admin.grid(row=1, column=3, padx=20, pady=10, sticky='e')

# btn_back = ttk.Button(frame_content, text="Back",  command= open_main,  style="TButton")
# btn_back.grid(row=1, column=0, padx=20, pady=10, sticky='e')



image_label = ttk.Label(frame_content, style="TLabel")
image_label.grid(row=3, column=2, padx=10, pady=10, sticky=W, columnspan=4)

name_label = ttk.Label(frame_content, text="ชื่อ:", style="TLabel")
name_label.grid(row=4, column=2, padx=10, pady=10, sticky=W)

name_entry = ttk.Entry(frame_content, width=30)
name_entry.grid(row=4, column=3, padx=10, pady=10)

surname_label = ttk.Label(frame_content, text="นามสกุล:", style="TLabel")
surname_label.grid(row=5, column=2, padx=10, pady=10, sticky=W)

surname_entry = ttk.Entry(frame_content, width=30)
surname_entry.grid(row=5, column=3, padx=10, pady=10)

register_button = ttk.Button(frame_content, text="ลงทะเบียน", command=register_user, style="TButton")
register_button.grid(row=6, column=2, columnspan=2, pady=10)

btn_exit = ttk.Button(frame_content, text="ย้อนกลับ", command=root.quit, style="TButton")
btn_exit.grid(row=6, column=4, columnspan=2, pady=10)

 
open_camera()

root.mainloop()
