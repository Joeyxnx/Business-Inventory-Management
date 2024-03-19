import tkinter as tk
from tkinter import messagebox, simpledialog

# Log-in Info
valid_username = "admin"
valid_password = "admin123"

# data for now
inventory_data = {
    "Apples": {"quantity": 10, "price": 2.99},
    "Bananas": {"quantity": 5, "price": 1.99},
}


def authenticate(username, password):
    if username == valid_username and password == valid_password:
        return True
    else:
        return False


def handle_login():
    username = username_entry.get()
    password = password_entry.get()

    if authenticate(username, password):
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        open_inventory_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def open_inventory_window():
    root.withdraw()
    inventory_window = tk.Toplevel()
    inventory_window.title("Inventory Management System")
    view_inventory_button = tk.Button(inventory_window, text="View Current Inventory", command=view_inventory)
    view_inventory_button.pack()
    add_item_button = tk.Button(inventory_window, text="Add Item to Inventory", command=add_item)
    add_item_button.pack()
    remove_item_button = tk.Button(inventory_window, text="Remove Item from Inventory", command=remove_item)
    remove_item_button.pack()
    report_missing_button = tk.Button(inventory_window, text="Report Missing Merchandise", command=report_missing)
    report_missing_button.pack()


def view_inventory():
    inventory_window = tk.Toplevel()
    inventory_window.title("Current Inventory")

    for item, details in inventory_data.items():
        label = tk.Label(inventory_window, text=f"{item}: Quantity - {details['quantity']}, Price - ${details['price']}"
                         )
        label.pack()


def add_item():
    item_name = simpledialog.askstring("Add Item", "Enter item name:")
    if item_name:
        item_quantity = simpledialog.askinteger("Add Item", "Enter item quantity:")
        item_price = simpledialog.askfloat("Add Item", "Enter item price:")
        if item_quantity is not None and item_price is not None:
            inventory_data[item_name] = {"quantity": item_quantity, "price": item_price}
            messagebox.showinfo("Add Item", f"{item_name} added to inventory.")


def remove_item():
    item_name = simpledialog.askstring("Remove Item", "Enter item name to remove:")
    if item_name in inventory_data:
        del inventory_data[item_name]
        messagebox.showinfo("Remove Item", f"{item_name} removed from inventory.")
    else:
        messagebox.showerror("Remove Item", f"{item_name} not found in inventory.")


def report_missing():
    item_name = simpledialog.askstring("Report Missing Merchandise", "Enter missing item name:")
    if item_name in inventory_data:
        inventory_data[item_name]["missing"] = True
        messagebox.showinfo("Report Missing Merchandise", f"{item_name} reported as missing.")
    else:
        messagebox.showerror("Report Missing Merchandise", f"{item_name} not found in inventory.")


root = tk.Tk()
root.title("Login System")
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")  # Show asterisks for password
password_entry.pack()
login_button = tk.Button(root, text="Login", command=handle_login)
login_button.pack()
root.mainloop()
