from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pandas as pd
import pyperclip


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
               't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)


def save():
    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showerror(title="Error", message="Please don't leave any spaces!")
    else:
        try:
            data = pd.read_csv('password_manager_data.csv', index_col=0)
            new_df = pd.DataFrame({'Website': [website], 'Email': [email], 'Password': [password]})
            new_data = pd.concat([data, new_df], ignore_index=True)
            new_data.to_csv('password_manager_data.csv')
        except:
            df = pd.DataFrame(columns=['Website', 'Email', 'Password'])
            df.to_csv('password_manager_data.csv')
            save()
        pyperclip.copy(password)
        website_entry.delete(0, END)
        password_entry.delete(0, END)

def search():
    website_search = website_entry.get().lower()
    if len(website_search) == 0:
        messagebox.showerror(title="Error", message="Please don't leave empty space!")
    else:
        try:
            data = pd.read_csv('password_manager_data.csv', index_col='Website')
            data.columns.str.match("Unnamed")
            data = data.loc[:, ~data.columns.str.match("Unnamed")]
            email_search = data.loc[website_search]['Email']
            password_search = data.loc[website_search]['Password']
            messagebox.showinfo(title=website_search, message=f"Email: {email_search} \nPassword: {password_search}")
            pyperclip.copy(password_search)
        except KeyError:
            messagebox.showerror(title='Oops', message=f"Sorry, website '{website_search}' doesn't exist.\nTry again.")
        except:
            messagebox.showerror(title='Oops', message=f"Sorry, data file is empty or file doesn't exist.")


# Canvas, Label, Button, Entry
window = Tk()
window.title("Password manager")
window.config(padx=25, pady=40)

imageFile = PhotoImage(file="lock.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(120, 100, image=imageFile)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=34)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "yourmail@gmail.com")

password_entry = Entry(width=34)
password_entry.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate password", width=14, command=generate_password)
generate_button.grid(row=3, column=2)

add_button = Button(text='Add', width=44, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text='Search', width=14, command=search)
search_button.grid(row=1, column=2)

window.mainloop()


