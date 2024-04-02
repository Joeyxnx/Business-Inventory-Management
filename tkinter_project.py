import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
import matplotlib.pyplot as plt

inventory_data = {}  # Initialize an empty dictionary for inventory data


def read_csv(filename):
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item_id = int(row["Product_id"])
                inventory_data[item_id] = {
                    'item_name': row['Name'],
                    "quantity": int(row['ItemCount']),
                    'price': float(row['PriceReg']),
                    'category': row['Category'],
                    'missing_qty': int(row.get('MissingQty', 0))
                    # Handle missing field for backward compatibility
                }
    except Exception as e:
        messagebox.showerror("Error",
                             f"Failed to read the file {filename}: {e}")

def write_csv(filename, data):
    try:
        with open(filename, mode='w', newline='') as csvfile:
            fieldnames = ['Product_id', 'Name', 'ItemCount', 'PriceReg',
                          'Category', 'MissingQty']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item_id, details in data.items():
                writer.writerow({
                    'Product_id': item_id,
                    'Name': details['item_name'],
                    'ItemCount': details['quantity'],
                    'PriceReg': details['price'],
                    'Category': details['category'],
                    'MissingQty': details.get('missing_qty', 0)
                })
    except Exception as e:
        messagebox.showerror("Error",
                             f"An error occurred while writing to {filename}: {e}")


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
    file_menu.add_command(label="Report Missing Item",
                          command=report_missing_item)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    view_inventory_button = tk.Button(root, text="View Current Inventory",
                                      command=choose_view_inventory)
    view_inventory_button.pack()
    add_item_button = tk.Button(root, text="Add Item to Inventory",
                                command=add_item)
    add_item_button.pack()
    remove_item_button = tk.Button(root, text="Remove Item from Inventory",
                                   command=remove_item)
    remove_item_button.pack()
    report_missing_button = tk.Button(root, text="Report Missing Item",
                                      command=report_missing_item)
    report_missing_button.pack()
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

    food_button = tk.Button(category_window, text="Food",
                            command=lambda: view_inventory_category(
                                "Food"))  # Food Category
    food_button.pack()
    electronic_button = tk.Button(category_window, text="Electronic",
                                  command=lambda: view_inventory_category(
                                      # Electronics Category
                                      "Electronic"))
    electronic_button.pack()
    clothing_button = tk.Button(category_window, text="Clothing",
                                command=lambda: view_inventory_category(
                                    # Clothing Category
                                    "Clothing"))
    clothing_button.pack()
    shoe_button = tk.Button(category_window, text="Footwear",
                            command=lambda: view_inventory_category(
                                # Shoe Category
                                "Footwear Category"))
    shoe_button.pack()


def view_inventory_category(category):
    inventory_window = tk.Toplevel()
    inventory_window.title(f"Current {category} Inventory")

    tree = ttk.Treeview(inventory_window, columns=(
    "Item ID", "Item Name", "Available Qty", "Missing Qty", "Price"),
                        show="headings")  # Updated For Missing QTY / avlble
    for col in (
    "Item ID", "Item Name", "Available Qty", "Missing Qty", "Price"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    for item_id, details in inventory_data.items():
        if details["category"] == category:
            available_quantity = details["quantity"] - details[
                "missing_qty"]  # Takes qty - missing qty = avaiblle qty
            tree.insert("", "end", values=(
                item_id, details["item_name"], available_quantity,
                details["missing_qty"], details["price"]), tags=("center",))

    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar = ttk.Scrollbar(inventory_window, orient="vertical",
                              command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    inventory_window.mainloop()


def view_inventory_all():
    inventory_window = tk.Toplevel()
    inventory_window.title("Current Inventory - All Categories")

    tree = ttk.Treeview(inventory_window, columns=(
    "Item ID", "Item Name", "Category", "Available Qty", "Missing Qty",
    "Price"), show="headings")
    for col in (
    "Item ID", "Item Name", "Category", "Available Qty", "Missing Qty",
    "Price"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    for item_id, details in inventory_data.items():
        available_quantity = details["quantity"] - details["missing_qty"] #same math as above func
        tree.insert("", "end", values=(
            item_id, details["item_name"], details["category"],
            available_quantity, details["missing_qty"], details["price"]),
                    tags=("center",))

    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar = ttk.Scrollbar(inventory_window, orient="vertical",
                              command=tree.yview)
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


def plot_sales():
    sales_2024 = []
    sales_2023 = []

    with open('SalesKaggle3_2.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if '2024_Sales' in row and '2023_Sales' in row:
                sales_2024.append(float(row['2024_Sales']))
                sales_2023.append(float(row['2023_Sales']))
                
    if not sales_2024 or not sales_2023:
        messagebox.showwarning("Data Missing", "Sales data for 2024 or 2023 is missing.")
        return
        
    fig, ax = plt.subplots()

    ax.plot(sales_2024, label='2024 Sales')
    ax.plot(sales_2023, label='2023 Sales')
    ax.set_xlabel('Item ID')
    ax.set_ylabel('Sales')
    ax.set_title('Sales Comparison: 2024 vs 2023')
    ax.legend()
    plt.show()


def plot_lifetime_sales():
    lifetime_sales = []
    with open('SalesKaggle3_2.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'Lifetime_Sales' in row:
                lifetime_sales.append(float(row['Lifetime_Sales']))
                
    if not lifetime_sales:
        messagebox.showwarning("Data Missing", "Lifetime sales data is missing.")
        return

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the data
    ax.plot(lifetime_sales, label='Lifetime Sales')
    ax.set_xlabel('Item ID')
    ax.set_ylabel('Sales')
    ax.set_title('Lifetime Sales')
    ax.legend()
    plt.show()


def display_discounted_items():
    discounted_items = [details["item_name"] for item_id, details in inventory_data.items() if details["discount"] > 0]
    if discounted_items:
        messagebox.showinfo("Discounted Items", f"The following items are on discount:\n{', '.join(discounted_items)}")
    else:
        messagebox.showinfo("Discounted Items", "No items are currently on discount.")

def refresh_inventory_views():
    for window in open_inventory_windows:
        window.refresh_view()  # would refresh content

# NEED TO IMPLEMENT REPORT MISSING METHOD (Further implementations?)
def report_missing_item():
    item_name = simpledialog.askstring("Update Missing Quantity",
                                       "Enter the name of the item:")
    if not item_name:
        return
    for item_id, details in inventory_data.items():
        if details["item_name"].lower() == item_name.lower():
            new_missing_qty = simpledialog.askinteger("Missing Quantity",
                                                      "Enter the missing quantity:",
                                                      initialvalue=details.get(
                                                          'missing_qty', 0))
            if new_missing_qty is not None:
                inventory_data[item_id]['missing_qty'] = new_missing_qty
                write_csv(CSV_FILENAME, inventory_data)
                messagebox.showinfo("Updated",
                                    f"Missing quantity for '{item_name}' updated.")
                refresh_inventory_views()  # Refresh view
            return
    messagebox.showerror("Not Found", "Item not found in inventory.")    


def invalid_input(input_val: any) -> str:
    """
    Checks if the input value is valid or not.
    Returns True if the input is invalid, False otherwise.
    """
    if input_val is None:
        return "Please input data"
    if isinstance(input_val, str) and not input_val.strip():
        # Check for empty strings after whitespace stripping
        return "Please type again"
    if isinstance(input_val, (int, float)) and input_val < 0:
        # Check for negative numbers to deem invalid
        return "Invalid negative input"
    return "Try again"


def expiry_date(month: int, year: int) -> tuple:
    """
    Returns the expiry date as a tuple of (month, year) for [food] category items.
    Validate month and year to ensure the date is valid
    """
    if not 1 <= month <= 12:
        raise ValueError("Month must be between 1 and 12.")
    if year < 2020:  # Assume the inventory system started after 2020
        raise ValueError("Year must be greater than 2020.")
    return month, year


def size_exist(XS: str, S: str, M: str, L: str, XL: str) -> str:
    """
    Check if sizes XS, S, M, L, and XL are available for [clothing] items.
    Returns True if any of the sizes are available, False otherwise.
    """
    # Example: Check if at least one size is available
    if XS or S or M or L or XL:
        return "Available"
    return "Not Available"


def shoe_size(us_size: float, eu_size: float) -> str:
    """
    Determines the shoe size category based on US and Euro sizing.
    Returns the category of shoe size (e.g., 'Small', 'Medium', 'Large').
    """
    if not us_size or not eu_size:
        return 'Invalid size'

    if 8 <= us_size <= 12 or 41 <= eu_size <= 45:
        return 'Medium'
    elif us_size < 8 or eu_size < 41:
        return 'Small'
    elif us_size > 12 or eu_size > 45:
        return 'Large'

    return 'Other'


read_csv('SalesKaggle3_2.csv')  
open_inventory()
