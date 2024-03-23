from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_password():
	password_entry.delete(0, END)
	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

	password_letters = [choice(letters) for _ in range(randint(8, 10))]
	password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
	password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

	password_list = password_letters + password_symbols + password_numbers

	shuffle(password_list)

	password = "".join(password_list)
	password_entry.insert(0, string=f"{password}")
	pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
	website = website_entry.get()
	username = user_entry.get()
	password = password_entry.get()
	new_data = {
		website: {
			"username": username,
			"password": password,
		}
	}

	if website == "" or username == "" or password == "":
		messagebox.showinfo(title="Warning", message="Please fill in all fields")
	else:
		try:
			with open("data_file.json", "r") as data_file:
				# Reading old data
				data = json.load(data_file)
		except FileNotFoundError:
			with open("data_file.json", "w") as data_file:
				json.dump(new_data, data_file, indent=4)
		else:
			# Updating old data with new data
			data.update(new_data)
			with open("data_file.json", "w") as data_file:
				# Saving updated data
				json.dump(data, data_file, indent=4)
		finally:
			website_entry.delete(0, END)
			password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
	website = website_entry.get()
	try:
		with open("data_file.json") as data_file:
			data = json.load(data_file)
			messagebox.showinfo(title=f"{website}", message=f"Username: {data[website]["username"]}"
															f"\nPassword: {data[website]["password"]}")
	except FileNotFoundError:
		messagebox.showinfo(title=f"{website}", message=f"No data file found."
															f"\nPlease make sure you enter some data first")
	except KeyError:
		messagebox.showinfo(title=f"{website}", message=f"No records for this website.")

	else:
		website_entry.delete(0, END)
	finally:
		pyperclip.copy(data[website]["password"])





# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
program_graphic = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=program_graphic)
canvas.grid(column=1, row =0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=33)
website_entry.focus()
website_entry.insert(0,"")
website_entry.grid(column=1, row=1)

user_entry = Entry(width=52)
user_entry.insert(0, string="dummymail@gmail.com")
user_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=33)
password_entry.insert(0, string="")
password_entry.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add", width=44, command=save_data)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()