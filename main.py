import random
from tkinter import *
from tkinter import messagebox
import string
import secrets
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_entry.delete(0, END)

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""

    for i in range(random.randint(10, 15)):
        password += "".join(secrets.choice(characters))

    password_entry.insert(0, string=password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_to_file():
    web = website_entry.get()
    email = username_entry.get()
    password = password_entry.get()
    new_data = {
        web: {
            "email": email,
            "password": password,
        }
    }

    if len(web) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please do not leave any fields empty.")

    else:
        try:
            with open("password.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            with open("password.json", "w") as file:
                json.dump(new_data, file, indent=4)

        else:
            data.update(new_data)
            with open("password.json", "w") as file:
                json.dump(data, file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search_password():
    web = website_entry.get()
    try:
        with open("password.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="You haven't stored any passwords yet.")

    else:
        if web in data:
            email = data[web]["email"]
            password = data[web]["password"]
            messagebox.showinfo(title=web, message=f"Email: {email}\nPassword: {password}")
        else:
            (messagebox.showerror(title="Oops", message=f"No password found for \"{web}\"."))


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(height=200, width=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Website
website_label = Label(text="Website:", font=("Arial", 10))
website_label.grid(column=0, row=1)
website_entry = Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()

#  Email/Username
username_label = Label(text="Email/Username:", font=("Arial", 10))
username_label.grid(column=0, row=2)
username_entry = Entry(width=53)
username_entry.grid(column=1, row=2, columnspan=2)
username_entry.insert(0, "example@email.com")

# Password
password_label = Label(text="Password:", font=("Arial", 10))
password_label.grid(column=0, row=3)
password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate Password", font=("Arial", 10), highlightthickness=0, command=generate_password)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add", font=("Arial", 10), highlightthickness=0, command=add_to_file)
add_button.grid(column=1, row=4, columnspan=2)
add_button.config(width=40)
search_button = Button(text="Search", font=("Arial", 10), highlightthickness=0, command=search_password)
search_button.grid(column=2, row=1)
search_button.config(width=15)

window.mainloop()
