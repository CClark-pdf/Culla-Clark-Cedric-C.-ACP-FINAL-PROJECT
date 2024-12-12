import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------------------------------------------------DATABASE SETUP----------------------------------------------------------
conn = sqlite3.connect("leastahan.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    checked BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")
conn.commit()

# ---------------------------------------------------------CREATION OF THE MAIN WINDOW----------------------------------------------------------
root = tk.Tk()
root.title('Leastahan')
root.geometry("1080x500")
root.config(bg='dodgerblue3')
root.resizable(0, 0)
root.frame1 = tk.Frame(root, bg="dodgerblue3")
root.frame1.place(relwidth=0.75, relheight=0.35, relx=0.12, rely=0.34, anchor='nw')

# ---------------------------------------------------------PLACEHOLDERS--------------------------------------------------------------------------
items = []
current_user_id = None
current_username = None
View_Window = None

Label1 = tk.Label(root, text='Leastahan', font=('Berlin Sans FB', 20))
Label1.config(bg='dodgerblue3')
Label1.place(relx=0.42, rely=0.25, anchor='nw')

# -----------------------------------------------------------ENTRY BOX AND LABELS-----------------------------------------------------------------
entryBox_Add = tk.Entry(root)
entryBox_Add.config(bg='azure1', fg='black')
entryBox_Add.place(width=200, relx=0.31, rely=0.59, anchor='nw')
Label_Add = tk.Label(root, text='Add', font=('Franklin Gothic Heavy', 10), anchor='w')
Label_Add.config(bg='dodgerblue3')
Label_Add.place(width=200, relx=0.31, rely=0.53, anchor='nw')

entryBox_name = tk.Entry(root)
entryBox_name.config(bg='azure1', fg='black')
entryBox_name.place(width=200, relx=0.51, rely=0.47, anchor='nw')
Label_name = tk.Label(root, text='Name', font=('Franklin Gothic Heavy', 10), anchor='w')
Label_name.config(bg='dodgerblue3')
Label_name.place(width=200, relx=0.51, rely=0.42, anchor='nw')

entryBox_ID = tk.Entry(root)
entryBox_ID.config(bg='azure1', fg='black')
entryBox_ID.place(width=200, relx=0.28, rely=0.47, anchor='nw')
Label_ID = tk.Label(root, text='ID', font=('Franklin Gothic Heavy', 10), anchor='w')
Label_ID.config(bg='dodgerblue3')
Label_ID.place(width=200, relx=0.28, rely=0.42, anchor='nw')

# -----------------------------------------------------------DATABASE FUNCTIONS----------------------------------------------------------
def adduser_to_db(username):
    """Add a new user to the database or get their existing ID."""
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    return cursor.lastrowid

def save_item_to_db(user_id, item_name):
    """Save a new item to the database."""
    cursor.execute("INSERT INTO items (user_id, item_name, checked) VALUES (?, ?, 0)", (user_id, item_name))
    conn.commit()

def load_items_from_db(user_id):
    """Load items from the database for a specific user."""
    global items
    cursor.execute("SELECT item_name, checked FROM items WHERE user_id = ?", (user_id,))
    items = [{"name": row[0], "checked": bool(row[1])} for row in cursor.fetchall()]

def delete_item_from_db(user_id, item_name):
    """Delete an item from the database."""
    cursor.execute("DELETE FROM items WHERE user_id = ? AND item_name = ?", (user_id, item_name))
    conn.commit()

def update_item_checked_status(user_id, item_name, checked):
    """Update the checked status of an item in the database."""
    cursor.execute("UPDATE items SET checked = ? WHERE user_id = ? AND item_name = ?", (checked, user_id, item_name))
    conn.commit()

# -----------------------------------------------------------ADD, DELETE, UPDATE FUNCTIONS----------------------------------------------------------
def add():
    global current_user_id, current_username
    item = entryBox_Add.get()
    username = entryBox_name.get().strip()

    if not username:
        messagebox.showerror("Error", "Please enter a name.")
        return
    confirm = messagebox.askyesno("Confirmation", f"Do you really want to add '{item}'?")
    if not confirm:
        return
    


    current_user_id = adduser_to_db(username)
    current_username = username

    if current_user_id and item.strip():
        save_item_to_db(current_user_id, item)
        load_items_from_db(current_user_id)
        entryBox_Add.delete(0, tk.END)

        if View_Window:
            UpdateList(View_Window)

def UpdateList(window):
    for widget in window.winfo_children():
        widget.destroy()

    if items:
        prog_bar = tk.DoubleVar()
        completed = sum(1 for item in items if item["checked"])
        prog_bar.set((completed / len(items)) * 100 if items else 0)



        progress = ttk.Progressbar(window, orient='horizontal', length=200, mode='determinate', variable=prog_bar)
        progress.pack(pady=10)

        for index, item in enumerate(items):
            frame = tk.Frame(window)
            frame.config(bg='dodgerblue3')
            frame.pack(anchor='w', padx=10, pady=5, fill='x')

            check_var = tk.BooleanVar(value=item["checked"])

            def checked(var=check_var, idx=index):
                items[idx]["checked"] = var.get()
                update_item_checked_status(current_user_id, items[idx]["name"], var.get())
                prog_bar.set((sum(1 for i in items if i["checked"]) / len(items)) * 100)

            checkbox = tk.Checkbutton(frame, variable=check_var, command=checked, bg='dodgerblue3')
            checkbox.pack(side='right')

            label = tk.Label(frame, text=item["name"], font=("Arial Black", 14))
            label.config(bg='dodgerblue3')
            label.pack(side='left')

            delete_button = tk.Button(frame, text='Delete', command=lambda idx=index: delete(idx))
            delete_button.pack(side='right', padx=10)
    else:
        no_items_label = tk.Label(window, text='WALA PA NAKALAGAY', font=("Arial Black", 14))
        no_items_label.pack()

def delete(index):
    confirm = messagebox.askyesno("Confirmation", f"Do you really want to delete '{items[index]['name']}'?")
    if not confirm:
        return

    if current_user_id:
        delete_item_from_db(current_user_id, items[index]["name"])
    del items[index]
    if View_Window:
        UpdateList(View_Window)


def ViewList():
    global View_Window, current_user_id, current_username
    username = entryBox_name.get().strip()
    if not username:
        messagebox.showerror("Error", "Please enter a name.")
        return

    current_user_id = adduser_to_db(username)
    current_username = username
    load_items_from_db(current_user_id)

    if View_Window is None or not View_Window.winfo_exists():
        View_Window = tk.Toplevel()
        View_Window.title('MGA KAILANGAN GAWIN ')
        View_Window.geometry("1080x500")
        View_Window.config(bg='dodgerblue3')
        UpdateList(View_Window)
    if View_Window:
        View_Window.lift()

# -----------------------------------------------------------BUTTONS----------------------------------------------------------
AddButton = tk.Button(root, text='ADD', command=add)
AddButton.place(width=100, height=20, relx=0.50, rely=0.585, anchor='nw')

ViewButton = tk.Button(root, text="View List", command=ViewList)
ViewButton.place(width=100, height=20, relx=0.60, rely=0.585, anchor='nw')

root.mainloop()
