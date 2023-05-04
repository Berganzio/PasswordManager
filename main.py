from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
from psw_characters import letters, symbols, numbers
import pyperclip
import json
FONT = ('Source Code Pro', 10, 'bold')
ENTRY_FONT = ('Source Code Pro', 10, 'normal')

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generator():
    entry_psw.delete(0, END)
    correct_psw = False
    while not correct_psw:
        new_letters = [choice(letters) for _ in range(randint(1, 5))]
        new_symbols = [choice(symbols) for _ in range(randint(1, 5))]
        new_numbers = [choice(numbers) for _ in range(randint(1, 5))]
        password = new_numbers + new_letters + new_symbols
        shuffle(password)

        if 8 <= len(password) <= 15:
            clean_psw = "".join(password)   # easiest way to convert a list into a string
            correct_psw = True
            entry_psw.insert(END, string=f"{clean_psw}")
            pyperclip.copy(clean_psw)

# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search():
    website = entry_web.get()
    try:
        with open('data.json', mode='r') as f:
            data = json.load(f)
            messagebox.showinfo(title=f"{website}", message=f"password: {data[website]['password']}\n"
                                                            f"email: {data[website]['email']}")
            pyperclip.copy(data[website]['password'])
    except KeyError:
        messagebox.showerror(title='invalid input', message=f'{website} not present in database.')
    except FileNotFoundError:
        messagebox.showerror(title='invalid input', message='No database Found')


# ---------------------------- SAVE PASSWORD ------------------------------- #

def store_data():
    website = entry_web.get()
    email = entry_email.get()
    psw = entry_psw.get()

    json_dict = {
        website: {
            "email": email,
            "password": psw
        }
    }

    if len(website) == 0 or len(psw) == 0:
        messagebox.showerror(title='WARNING', message="EMPTY FIELDS")
    else:
        try:
            with open('data.json', mode='r') as f:
                # reading old data
                data = json.load(f)
        except FileNotFoundError:
            with open('data.json', mode='w') as f:
                json.dump(json_dict, f, indent=4)
        else:
            # updating old data with new data
            data.update(json_dict)
            with open('data.json', mode='w') as f:
                # saving updated data
                json.dump(data, f, indent=4)
        finally:
            entry_web.delete(0, END)
            entry_psw.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

screen = Tk()
screen.title('Password Manager')
screen.config(pady=5, padx=5, bg='#FFF5E4')

canvas = Canvas(width=200, height=200, bg='#FFF5E4', highlightthickness=0)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

web_label = Label(text='Website', font=FONT, bg='#FFF5E4')
web_label.grid(column=0, row=1)

email_user_label = Label(text='Email/Username', font=FONT, bg='#FFF5E4')
email_user_label.grid(column=0, row=2)

psw_label = Label(text='Password', font=FONT, bg='#FFF5E4')
psw_label.grid(column=0, row=3)

generate_button = Button(text='Generate Password', font=FONT, command=generator)
generate_button.grid(column=2, row=3)

search_button = Button(text='Search', width=15, font=FONT, command=search)
search_button.grid(column=2, row=1)

entry_web = Entry(width=34, font=ENTRY_FONT)
entry_web.focus()
entry_web.insert(END, string="")
entry_web.grid(column=1, row=1)

entry_email = Entry(width=34, font=ENTRY_FONT)
entry_email.insert(END, string="andreamusic.bergantin@gmail.com")
entry_email.grid(column=1, row=2)

entry_psw = Entry(width=33, justify='center', font=ENTRY_FONT)
entry_psw.grid(column=1, row=3)

add_button = Button(text='ADD', width=46, font=FONT, command=store_data)
add_button.grid(column=1, row=4, columnspan=2)


screen.mainloop()