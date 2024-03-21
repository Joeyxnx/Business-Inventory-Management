import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv

inventory_data = {} 


def read_inventory_from_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_id = int(row["Product_id"])
            item_name = str(row['Name'])
            quantity = int(row['ItemCount'])
            price = float(row['PriceReg'])
            inventory_data[item_id] = {'item_name': item_name, "quantity": quantity, 'price': price}


def open_inventory_window():
    root = tk.Tk()
    root.title("Inventory Management System")

    # Create Menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Add Menu Items
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="View Inventory", command=view_inventory)
    file_menu.add_command(label="Add Item", command=add_item)
    file_menu.add_command(label="Remove Item", command=remove_item)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    view_inventory_button = tk.Button(root, text="View Current Inventory", command=view_inventory)
    view_inventory_button.pack()
    add_item_button = tk.Button(root, text="Add Item to Inventory", command=add_item)
    add_item_button.pack()
    remove_item_button = tk.Button(root, text="Remove Item from Inventory", command=remove_item)
    remove_item_button.pack()
    root.mainloop()


def view_inventory():
    inventory_window = tk.Toplevel()
    inventory_window.title("Current Inventory")

    # Create Treeview widget with centered content
    tree = ttk.Treeview(inventory_window, columns=("Item ID", "Item Name", "Quantity", "Price"), show="headings")
    tree.heading("Item ID", text="Item ID")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")

    # Configure Treeview style to center the content
    tree.tag_configure("center", anchor="center")
    for col in tree["columns"]:
        tree.column(col, anchor="center")

    # Insert inventory data into Treeview
    for item_id, details in inventory_data.items():
        tree.insert("", "end", values=(item_id, details["item_name"], details["quantity"], details["price"]), tags=("center",))

    tree.pack(expand=True, fill=tk.BOTH)  # Expand the Treeview to fill the window

    # Add scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(inventory_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    inventory_window.mainloop()


def add_item():
    item_name = simpledialog.askstring("Add Item", "Enter item name:")
    if item_name:
        item_id = len(inventory_data) + 1  # Generate a new item ID
        item_quantity = simpledialog.askinteger("Add Item", "Enter item quantity:")
        item_price = simpledialog.askfloat("Add Item", "Enter item price:")
        if item_quantity is not None and item_price is not None:
            inventory_data[item_id] = {"item_name": item_name, "quantity": item_quantity, "price": item_price}
            # Append the new item to the CSV file
            with open('SalesKaggle3.csv', mode='a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([item_id, item_name, item_price, item_quantity])
            messagebox.showinfo("Add Item", f"{item_name} added to inventory.")


# Needs Work
def remove_item():
    item_id = simpledialog.askinteger("Remove Item", "Enter item ID to remove:")
    if item_id in inventory_data:
        del inventory_data[item_id]
        messagebox.showinfo("Remove Item", f"Item with ID {item_id} removed from inventory.")
    else:
        messagebox.showerror("Remove Item", f"Item with ID {item_id} not found in inventory.")


read_inventory_from_csv('SalesKaggle3.csv')  # Read inventory data from CSV file
open_inventory_window()
