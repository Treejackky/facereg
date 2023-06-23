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
    
    # เรียกใช้ฟังก์ชัน check_time() เพื่อตรวจสอบเวลาตามชื่อที่แสดง
    # check_time(res["names"][0])
    
    root.after(1, update_image)

def check():
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
    check_time(res["names"][0])

def check_time(name):
    if name != "unknown":
        # ตรวจสอบเวลาของบุคคลที่มีชื่อตรงกับที่ระบบสแกนหน้าตรวจจับ
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%Y")
        # spilt name with _ and get the first name
        name = name.split("_")[0]
        # Send the person's data to the server
        url = "http://localhost:3000/v1/check_time"
        body = {
            "name": name,
            "time": current_time,
            "date": current_date,
        }
        res = requests.post(url, json=body)

        # Save the person's data
        if res.status_code == 200:
            # Save the image
            if cam.isOpened():  # Check if the camera is opened
                ret, frame = cam.read()
                cv2.imwrite(f'images/{current_date}_{name}.jpg', frame)
                time.sleep(0.5)  # delay between pictures

            # Open the file in read mode
            try:
                with open('time.json', 'r') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            # Add the new user's data to the list
            data.append(body)

            # Write the updated data back to the file
            try:
                with open('time.json', 'w') as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                print("Error while writing to the file: ", e)

            messagebox.showinfo("สถานะการลงเวลางาน", "ลงเวลางานสำเร็จ")
        else:
            messagebox.showerror("สถานะการลงเวลางาน", "ลงเวลางานไม่สำเร็จ")


def open_camera():
    global cam
    cam = cv2.VideoCapture(0)
    update_image()

 


root = Tk()
root.title("ลงเวลาเข้าทำงาน")

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
header_label = ttk.Label(frame_header, text="ลงเวลาทำงาน",  style="TLabel")
header_label.grid(row=0, column=0, padx=20, pady=10)

frame_content = ttk.Frame(root, style="TFrame", padding="10 10 10 10")
frame_content.place(relx=0.5, rely=0.5, anchor="center")

image_label = ttk.Label(frame_content, style="TLabel")
image_label.grid(row=3, column=2, padx=10, pady=10, sticky=W, columnspan=4)

register_button = ttk.Button(frame_content, text="ลงเวลางาน", command= check ,style="TButton")
register_button.grid(row=6, column=2, columnspan=2, pady=10)

btn_exit = ttk.Button(frame_content, text="ย้อนกลับ", command=root.quit, style="TButton")
btn_exit.grid(row=6, column=4, columnspan=2, pady=10)
 
open_camera()

root.mainloop()