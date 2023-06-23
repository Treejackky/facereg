import requests
from fpdf import FPDF
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from ttkthemes import ThemedStyle 

def fetch_and_create_pdf():
    name = name_combobox.get()
    date = date_entry.get_date()

    response = requests.get('http://localhost:3000/v1/get')
    data = response.json()

    pdf = FPDF('L')

    pdf.add_page()

    pdf.set_font("Arial", size = 12)

    users = data['users']

    headers = ['date', 'name', 'check_in', 'check_out']
    for idx, header in enumerate(headers):
        pdf.cell(60, 10, txt=f"{header}", ln=False, align='C')

    pdf.ln(10)

    for user in users:
        if (name and user['name'] == name) or (date and user['date'] == str(date)) or (name == "ทั้งหมด"):
            for header in headers:
                pdf.cell(60, 10, txt=f"{user[header]}", ln=False, align='C')
            pdf.ln(10)

    pdf.output(f"{name or date}_data.pdf")





   



def fetch_data():
    response = requests.get('http://localhost:3000/v1/get')  
    data = response.json()

    users = data['users']
    names = {user['name'] for user in users}
    name_combobox['values'] = list(names)

    names = list(names)
    names.append("ทั้งหมด")
    name_combobox['values'] = names

    for i in tree.get_children():
        tree.delete(i)

    for user in users:
        tree.insert('', 'end', values=(user['date'], user['name'], user['check_in'], user['check_out']))



root = Tk()

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
style.set_theme("arc")# Set the theme# You can replace "arc" with your preferred theme



name_label = Label(root, text='Name:')
name_label.grid(row=0, column=0, padx=(50, 0), pady=(50, 0))  # Add some padding
name_combobox = ttk.Combobox(root, width=50)  # Set width
name_combobox.grid(row=0, column=1, padx=(0, 50), pady=(50, 0))  # Add some padding

date_label = Label(root, text='Date:')
date_label.grid(row=1, column=0, padx=(50, 0))  # Add some padding
date_entry = DateEntry(root, width=50)  # Set width
date_entry.grid(row=1, column=1, padx=(0, 50))  # Add some padding

button = ttk.Button(root, text='สร้าง pdf ', command=fetch_and_create_pdf)  # Use ttk.Button for better style
button.grid(row=2, column=0, columnspan=2, pady=(20, 0))  # Add some padding

fetch_data_button = ttk.Button(root, text='เรียกดูข้อมูล', command= fetch_data)  # Use ttk.Button for better style
fetch_data_button.grid(row=3, column=0, columnspan=2, pady=(20, 0))  # Add some padding

btn_exit = ttk.Button( text="ย้อนกลับ", command=root.quit, style="TButton")
btn_exit.grid(row=6, column=4, columnspan=2, pady=10)

tree = ttk.Treeview(root, columns=('date', 'name', 'check_in', 'check_out'), show='headings')

tree.heading('date', text='Date')
tree.heading('name', text='Name')
tree.heading('check_in', text='Check-in')
tree.heading('check_out', text='Check-out')
tree.grid(row=4, column=0, columnspan=2, padx=(50, 50), pady=(20, 50))  # Add some padding
fetch_data()
root.mainloop()