import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv

inventory_data = {}  # Initialize an empty dictionary for inventory data


def read_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_id = int(row["Product_id"])
            item_name = str(row['Name'])
            quantity = int(row['ItemCount'])
            price = float(row['PriceReg'])
            category = str(row['Category'])
            inventory_data[item_id] = {'item_name': item_name, "quantity": quantity, 'price': price,
                                       'category': category}


def open_inventory():
    root = tk.Tk()
    root.title("Inventory Management System")

    # Create Menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Add Menu Items
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="View Inventory", command=choose_view_inventory)
    file_menu.add_command(label="Add Item", command=add_item)
    file_menu.add_command(label="Remove Item", command=remove_item)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    view_inventory_button = tk.Button(root, text="View Current Inventory", command=choose_view_inventory)
    view_inventory_button.pack()
    add_item_button = tk.Button(root, text="Add Item to Inventory", command=add_item)
    add_item_button.pack()
    remove_item_button = tk.Button(root, text="Remove Item from Inventory", command=remove_item)
    remove_item_button.pack()
    root.mainloop()


def choose_view_inventory():
    choice = messagebox.askyesno("View Inventory", "Do you want to view inventory by categories?")
    if choice:
        view_inventory_by_category()
    else:
        view_inventory_all()


def view_inventory_by_category():
    category_window = tk.Toplevel()
    category_window.title("View Inventory by Category")

    food_button = tk.Button(category_window, text="Food", command=lambda: view_inventory_category("Food"))
    food_button.pack()
    electronic_button = tk.Button(category_window, text="Electronic",
                                  command=lambda: view_inventory_category("Electronic"))
    electronic_button.pack()
    clothing_button = tk.Button(category_window, text="Clothing", command=lambda: view_inventory_category("Clothing"))
    clothing_button.pack()


def view_inventory_category(category):
    inventory_window = tk.Toplevel()
    inventory_window.title(f"Current {category} Inventory")

    # Create Treeview widget with centered content
    tree = ttk.Treeview(inventory_window, columns=("Item ID", "Item Name", "Quantity", "Price"), show="headings")
    tree.heading("Item ID", text="Item ID")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")

    # Configure Treeview style to center the content
    for col in tree["columns"]:
        tree.column(col, anchor="center")

    # Insert inventory data into Treeview for the selected category
    for item_id, details in inventory_data.items():
        if details["category"] == category:
            tree.insert("", "end", values=(item_id, details["item_name"], details["quantity"], details["price"]),
                        tags=("center",))

    tree.pack(expand=True, fill=tk.BOTH)  # Expand the Treeview to fill the window

    # Add scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(inventory_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    inventory_window.mainloop()


def view_inventory_all():
    inventory_window = tk.Toplevel()
    inventory_window.title("Current Inventory - All Categories")

    # Create Treeview widget with centered content
    tree = ttk.Treeview(inventory_window, columns=("Item ID", "Item Name", "Category", "Quantity", "Price"),
                        show="headings")
    tree.heading("Item ID", text="Item ID")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Category", text="Category")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")

    # Configure Treeview style to center the content
    for col in tree["columns"]:
        tree.column(col, anchor="center")

    # Insert all inventory data into Treeview
    for item_id, details in inventory_data.items():
        tree.insert("", "end", values=(item_id, details["item_name"], details["category"], details["quantity"],
                                       details["price"]), tags=("center",))

    tree.pack(expand=True, fill=tk.BOTH)  # Expand the Treeview to fill the window

    # Add scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(inventory_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    inventory_window.mainloop()


def add_item():
    item_name = simpledialog.askstring("Add Item", "Enter item name:")
    if item_name:
        # Check if the item name already exists
        for item_id, details in inventory_data.items():
            if details["item_name"] == item_name:
                # Item already exists, update the quantity
                new_quantity = simpledialog.askinteger("Update Quantity",
                                                       "Item exists in DB. Enter additional quantity:")
                if new_quantity is not None:
                    inventory_data[item_id]["quantity"] += new_quantity

                    # Update the CSV file with the new quantity
                    with open('SalesKaggle3_2.csv', mode='r', newline='') as csvfile:
                        reader = csv.reader(csvfile)
                        header = next(reader)  # Skip the header row
                        rows = [row for row in reader]
                        for row in rows:
                            if int(row[0]) == item_id:
                                row[3] = inventory_data[item_id]["quantity"]  # Update quantity in CSV
                                break

                    # Rewrite the CSV file with updated quantity
                    with open('SalesKaggle3_2.csv', mode='w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(header)  # Write the header row back
                        writer.writerows(rows)

                    messagebox.showinfo("Update Quantity", f"Quantity updated for item '{item_name}'.")
                    return  # Exit the function after updating quantity

        # Item doesn't exist, add it to inventory
        item_id = len(inventory_data) + 1  # Generate a new item ID
        item_quantity = simpledialog.askinteger("Add Item", "Enter item quantity:")
        item_price = simpledialog.askfloat("Add Item", "Enter item price:")
        item_category = simpledialog.askstring("Add Item", "Enter item category:")  # Ask for category
        if item_quantity is not None and item_price is not None and item_category:
            inventory_data[item_id] = {"item_name": item_name, "quantity": item_quantity, "price": item_price,
                                       "category": item_category}
            # Append the new item to the CSV file
            with open('SalesKaggle3_2.csv', mode='a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([item_id, item_name, item_price, item_quantity, item_category])  # Write category to CSV
            messagebox.showinfo("Add Item", f"{item_name} added to inventory.")

# THIS WORKS NOW!
def remove_item():
    item_id = simpledialog.askinteger("Remove Item", "Enter item ID to remove:")
    if item_id in inventory_data:
        del inventory_data[item_id]

        # Read the CSV data and remove the item
        with open('SalesKaggle3_2.csv', mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip the header row
            rows = [row for row in reader if int(row[0]) != item_id]  # Remove item from CSV data

        # Rewrite the CSV file without the removed item
        with open('SalesKaggle3_2.csv', mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)  # Write the header row back
            writer.writerows(rows)

        # Update inventory_data dictionary by reading the CSV again
        read_csv('SalesKaggle3_2.csv')

        messagebox.showinfo("Remove Item", f"Item with ID {item_id} removed from inventory.")
    else:
        messagebox.showerror("Remove Item", f"Item with ID {item_id} not found in inventory.")

# NEED TO IMPLEMENT REPORT MISSING METHOD
# NEED TO WORK ON INVALID INPUTS ON MOST FUNCTIONS
# NEED TO IMPLEMENT DISCOUNT METHOD
# NEED TO ADD EXPIRY DATE FOR FOOD CATEGORY
# NEED TO ADD SIZE AVAILABILITY FOR CLOTHES (XS,S,M,L,XL) 
# MAYBE ALSO ADD SHOES SIZES FOR MEN AND WOMEN (ASSUME 6-10 FOR WOMEN, 8-12 FOR MEN)


read_csv('SalesKaggle3_2.csv')  # Read inventory data from CSV file
open_inventory()
