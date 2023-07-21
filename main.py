import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    num_letters = randint(8, 10)
    num_symbols = randint(2, 4)
    num_numbers = randint(2, 4)

    password_list = [choice(letters) for num in range(num_letters)]
    password_list += [choice(symbols) for num in range(num_symbols)]
    password_list += [choice(numbers) for num in range(num_numbers)]

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_entry():
    website = website_entry.get()
    username = user_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="", message="Invalid response. Please enter a valid website, username and "
                                                 "password to continue.")
    else:
        proceed = messagebox.askokcancel(title="",
                                         message=f"These are the details entered for {website}: \n\nUsername: {username} \n"
                                                 f"Password: {password} \n\n Would you like to save this?")

        new_entry = {
            website: {
                "email": username.lower(),
                "password": password,
            }}

        if proceed:
            try:
                with open("data.json", mode="r") as file:
                    data = json.load(file)
                    if website in data:
                        update= messagebox.askyesno(title="", message="There is already an entry saved for this website.\n Would you like to overwrite?")
                        if update:
                            data[website]["email"] = username
                            data[website]["password"] = password
                        else:
                            messagebox.showinfo(title="", message="The new information was not saved.")
                            return
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                with open("data.json", mode="w") as file:
                    json.dump(new_entry, file, indent=4)
            else:
                data.update(new_entry)
                with open("data.json", mode="w") as file:
                    json.dump(data, file, indent=4)

            website_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            messagebox.showinfo(title="", message="Your information has been saved.")

        else:
            messagebox.showinfo(title="", message="Please try again.")


# ---------------------------- SEARCH BUTTON FOR PASSWORDS ------------------------------- #
def password_finder():
    website = website_entry.get()
    website = website.lower()
    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showwarning(title="", message="Error: No data file found. Add data to create the file.")
    else:
        if website in data:
            messagebox.showinfo(title="",
                                message=f" For {website.title()}- \nEmail: {data[website]['email']} \n Password: {data[website]['password']}")
        else:
            messagebox.showwarning(title="", message="Error: There are no saved entries for this website yet.")


# ---------------------------- UI SETUP ------------------------------- #
# Window and Canvas Set-up
window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=50)

canvas = tk.Canvas(width=200, height=200)
pic = tk.PhotoImage(file="logo.png")
canvas.create_image(140, 100, image=pic)
canvas.grid(column=1, row=0)

# Text, Entries, & Buttons

##Website line
website_text = tk.Label(text="Website:")
website_text.grid(column=0, row=1)

website_entry = tk.Entry()
website_entry.grid(column=1, row=1)
website_entry.focus()

search_button = tk.Button(text="Search", command=password_finder)
search_button.grid(column=2, row=1, columnspan=2, sticky="ew")

##Username/Email line
user_text = tk.Label(text="Email/Username:")
user_text.grid(column=0, row=2)

user_entry = tk.Entry()
user_entry.grid(column=1, row=2, columnspan=2, sticky="ew")
# user_entry.insert(0, "yoyrfrequentemail@email.com")

##Password line
password_text = tk.Label(text="Password:")
password_text.grid(column=0, row=3)

password_entry = tk.Entry()
password_entry.grid(column=1, row=3, sticky="w")

generate_password = tk.Button(text="Generate Password", command=gen_password)
generate_password.grid(column=2, row=3, columnspan=2, sticky="ew")

# Add Button
add = tk.Button(text="Add", width=36, command=add_entry)
add.grid(column=1, row=4, columnspan=2, sticky="ew")

window.mainloop()
