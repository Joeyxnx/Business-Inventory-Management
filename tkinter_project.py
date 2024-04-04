import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
import matplotlib.pyplot as plt
import bcrypt

inventory_data = {}


def authenticate_user(username, password):
    try:
        with open('users.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader: # go through user and pass
                stored_username, stored_hashed_pw = row
                if stored_username == username: #authenticate
                    return bcrypt.checkpw(password.encode('utf-8'),
                                          stored_hashed_pw.encode('utf-8'))
    except FileNotFoundError:
        messagebox.showerror("Error", "User database not found.")
    return False


def login(master):
    while True: # loop so u can retry
        username = simpledialog.askstring("Login", "Enter your username:",
                                          parent=master)
        if not username:
            return False

        password = simpledialog.askstring("Login", "Enter your password:",
                                          show="*", parent=master) #prompt for pass
        if not password:  # Check if the dialog was cancelled
            return False

        if authenticate_user(username, password):
            return True  # exit when authenticated
        else:
            # try again
            try_again = messagebox.askretrycancel("Login Failed",
                                                  "Incorrect username or password. Would you like to try again?")
            if not try_again:
                return False


def main():
    root_2 = tk.Tk()
    root_2.withdraw()

    choice = messagebox.askquestion("Start", "Do you have an account?",
                                    icon='question')
    if choice == 'yes':
        if login(root_2):
            #root.deiconify()
            open_inventory() #open if pass

        else:
            messagebox.showerror("Login Failed", "The login was unsuccessful.") # if fail
            root_2.destroy()
    elif choice == 'no': # user doesnt have an account
        if create_user_gui(root_2):
            messagebox.showinfo("Registration",
                                "Please log in with your new credentials.")
            if login(root_2):
                #root.deiconify()
                open_inventory()
            else:
                messagebox.showerror("Login Failed",
                                     "The login was unsuccessful.")
                root_2.destroy()
        else:
            root_2.destroy()

    root_2.mainloop()


def create_user_gui(master):
    new_username = simpledialog.askstring("Register", "Enter new username:",
                                          parent=master)
    if not new_username:
        messagebox.showinfo("Registration", "Registration cancelled.")
        return False

    new_password = simpledialog.askstring("Register", "Enter new password:",
                                          show="*", parent=master)
    if not new_password:
        messagebox.showinfo("Registration", "Registration cancelled.")
        return False

    confirm_password = simpledialog.askstring("Register", "Confirm password:",
                                              show="*", parent=master)
    if new_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return False

    hashed_pw = hash_password(new_password) #hash/encrypt da password
    with open('users.csv', 'a', newline='') as f:
        writer = csv.writer(f) #stores new user
        writer.writerow([new_username, hashed_pw.decode('utf-8')])

    messagebox.showinfo("Registration", "User registered successfully.")
    return True


def hash_password(password):
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def create_user(username, password):
    """Store a new user with a hashed password."""
    hashed_pw = hash_password(password)
    # Append the new user to your user storage
    with open('users.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, hashed_pw.decode('utf-8')])


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


# Function to open the inventory management system GUI
def open_inventory():
    root_1 = tk.Tk()
    root_1.title("Inventory Management System")
    # Create Menu
    menu_bar = tk.Menu(root_1)
    root_1.config(menu=menu_bar)

    # Add Menu Items
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Create Left Frame for View, Add, Remove buttons
    left_frame = tk.Frame(root_1)
    left_frame.pack(side="left", padx=20, pady=20)

    view_inventory_button = ttk.Button(left_frame, text="View Inventory", command=view_inventory_all)
    view_inventory_button.pack(fill=tk.BOTH, padx=10, pady=10)
    add_item_button = ttk.Button(left_frame, text="Add Item", command=add_item)
    add_item_button.pack(fill=tk.BOTH, padx=10, pady=10)
    remove_item_button = ttk.Button(left_frame, text="Remove Item", command=remove_item)
    remove_item_button.pack(fill=tk.BOTH, padx=10, pady=10)

    # Create Right Frame for other buttons
    right_frame = tk.Frame(root_1)
    right_frame.pack(side="right", padx=20, pady=20)

    plot_sales_button = ttk.Button(right_frame, text="2022/2023 Sales Data", command=plot_sales)
    plot_sales_button.pack(fill=tk.BOTH, padx=10, pady=10)

    plot_new_sales_button = ttk.Button(right_frame, text="2024 Sales Data", command=plot_new_sales)
    plot_new_sales_button.pack(fill=tk.BOTH, padx=10, pady=10)

    missing_items_button = ttk.Button(left_frame, text="Report Missing Items", command=report_missing_items)
    missing_items_button.pack(fill=tk.BOTH, padx=10, pady=10)

    # Add a button for selling items in your GUI
    sell_item_button = ttk.Button(right_frame, text="Sell Item", command=sell_item)
    sell_item_button.pack(fill=tk.BOTH, padx=10, pady=10)

    root_1.mainloop()


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
        row_values = (item_id, details["item_name"], details["category"], details["quantity"],
                      details["price"])

        tree.insert("", "end", values=row_values)

    tree.pack(expand=True, fill=tk.BOTH)  # Expand the Treeview to fill the window

    # Define style for highlighting rows
    tree.tag_configure("highlight", background="yellow")

    # Add scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(inventory_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    inventory_window.mainloop()


def add_item():
    item_name = simpledialog.askstring("Add Item", "Enter item name:")
    if item_name:
        item_name_upper = item_name.upper()  # Convert item name to uppercase for case-insensitive comparison
        # Check if the item name already exists
        for item_id, details in inventory_data.items():
            if details["item_name"].upper() == item_name_upper:
                # Item already exists, update the quantity
                new_quantity = simpledialog.askinteger("Update Quantity",
                                                       "Item exists in DB. Enter additional quantity:")
                if new_quantity is not None:
                    inventory_data[item_id]["quantity"] += new_quantity
                    inventory_data[item_id].setdefault("MissingQty", 0)  # Initialize MissingQty if not present
                    inventory_data[item_id].setdefault("2024_Sales", 0)  # Initialize 2024_Sales if not present
                    # Update the CSV file with the new quantity and retain 2024_Sales
                    update_csv(item_id, inventory_data[item_id]["quantity"], inventory_data[item_id]["2024_Sales"])
                    messagebox.showinfo("Update Quantity", f"Quantity updated for item '{item_name}'.")
                    return  # Exit the function after updating quantity
        # Item doesn't exist, add it to inventory with MissingQty and 2024_Sales initialized
        item_id = len(inventory_data) + 1  # Generate a new item ID
        item_quantity = simpledialog.askinteger("Add Item", "Enter item quantity:")
        item_price = simpledialog.askfloat("Add Item", "Enter item price:")
        item_category = simpledialog.askstring("Add Item", "Enter item category:")  # Ask for category
        if item_quantity is not None and item_price is not None and item_category:
            inventory_data[item_id] = {"item_name": item_name, "quantity": item_quantity, "price": item_price,
                                       "category": item_category, "MissingQty": 0, "2024_Sales": 0}  # Initialize MissingQty and 2024_Sales here
            # Append the new item to the CSV file with MissingQty and 2024_Sales set to 0
            with open('SalesKaggle3new.csv', mode='a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([item_id, item_name, item_price, item_quantity, item_category, 0, 0])  # Write 0 for MissingQty and 2024_Sales
            messagebox.showinfo("Add Item", f"{item_name} added to inventory.")


def update_csv(item_id, quantity, curr_sold_2024):
    with open('SalesKaggle3new.csv', mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header row
        rows = [row for row in reader]
        for row in rows:
            if int(row[0]) == item_id:
                row[3] = quantity  # Update quantity in CSV
                row[-1] = curr_sold_2024  # Update Curr_Sold in CSV
                break

    # Rewrite the CSV file with updated quantity and Curr_Sold
    with open('SalesKaggle3new.csv', mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write the header row back
        writer.writerows(rows)


def remove_item():
    item_id = simpledialog.askinteger("Remove Item", "Enter item ID to remove:")
    if item_id in inventory_data:
        del inventory_data[item_id]

        # Read the CSV data and remove the item
        with open('SalesKaggle3new.csv', mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip the header row
            rows = [row for row in reader if int(row[0]) != item_id]  # Remove item from CSV data

        # Rewrite the CSV file without the removed item
        with open('SalesKaggle3new.csv', mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)  # Write the header row back
            writer.writerows(rows)

        # Update inventory_data dictionary by reading the CSV again
        read_csv('SalesKaggle3new.csv')

        messagebox.showinfo("Remove Item", f"Item with ID {item_id} removed from inventory.")
    else:
        messagebox.showerror("Remove Item", f"Item with ID {item_id} not found in inventory.")


def plot_sales():
    # Initialize empty lists for sales data
    sales_2022 = []
    sales_2023 = []

    # Read the CSV file to get the latest sales data
    with open('SalesKaggle3new.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if '2022_Sales' in row and '2023_Sales' in row:
                sales_2022.append(float(row['2022_Sales']))
                sales_2023.append(float(row['2023_Sales']))

    # Check if there is data to plot
    if not sales_2022 or not sales_2023:
        messagebox.showwarning("Data Missing", "Sales data for 2022 or 2023 is missing.")
        return

    # Create a figure and axis
    fig, ax = plt.subplots()

    ax.plot(sales_2022, label='2022 Sales')
    ax.plot(sales_2023, label='2023 Sales')
    ax.set_xlabel('Item ID')
    ax.set_ylabel('Sales')
    ax.set_title('Sales Comparison: 2022 vs 2023')
    ax.legend()
    plt.show()


def plot_new_sales():
    # Initialize empty lists for item IDs and sales data
    item_ids = []
    sales_2024 = []

    # Read the CSV file to get the latest sales data
    with open('SalesKaggle3new.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if '2024_Sales':
                item_id = int(row['Product_id'])
                item_ids.append(item_id)
                sales_2024.append(float(row['2024_Sales']))

    # https://stackoverflow.com/questions/55061846/how-to-zip-items-in-2-lists-only-when-a-condition-is-met-python
    # Got this code from StackOverflow
    item_ids_filtered = [item_id for item_id, sales in zip(item_ids, sales_2024) if sales != 0]
    sales_2024_filtered = [sales for sales in sales_2024 if sales != 0]

    # Check if there is data to plot after filtering
    if not sales_2024_filtered:
        messagebox.showwarning("Data Missing", "Filtered sales data for 2024 is empty.")
        return

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot a dot for each item's sales (filtered)
    ax.plot(item_ids_filtered, sales_2024_filtered, marker='o', linestyle='', markersize=8, label='2024 Sales',
            color='blue')

    ax.set_xlabel('Item ID')
    ax.set_ylabel('Sales')
    ax.set_title('2024 Sales Data (Dot Plot)')
    ax.legend()
    plt.show()


def report_missing_items():
    item_id = simpledialog.askinteger("Report Missing Items", "Enter item ID for the missing item:")
    if item_id in inventory_data:
        missing_quantity = simpledialog.askinteger("Report Missing Items", "Enter the missing quantity:")
        if missing_quantity is not None and missing_quantity > 0:
            inventory_data[item_id].setdefault("MissingQty", 0)  # Initialize MissingQty if not present
            inventory_data[item_id]["quantity"] -= missing_quantity
            inventory_data[item_id]["MissingQty"] += missing_quantity

            # Update the CSV file with the missing quantity
            update_csv(item_id, inventory_data[item_id]["quantity"], inventory_data[item_id]["MissingQty"])

            messagebox.showinfo("Report Missing Items", f"{missing_quantity} units of item {item_id} reported as "
                                                        f"missing.")
        else:
            messagebox.showwarning("Report Missing Items", "Please enter a valid missing quantity (greater than 0).")
    else:
        messagebox.showerror("Report Missing Items", f"Item with ID {item_id} not found in inventory.")


def sell_item():
    item_id = simpledialog.askinteger("Sell Item", "Enter item ID for the item sold:")
    if item_id in inventory_data:
        sold_quantity = simpledialog.askinteger("Sell Item", "Enter the quantity sold:")
        if sold_quantity is not None and sold_quantity > 0:
            # Get current sales for 2024 or default to 0
            curr_sold_2024 = inventory_data[item_id].get("2024_Sales", 0)
            # Add sold quantity to existing 2024_Sales
            inventory_data[item_id]["2024_Sales"] = curr_sold_2024 + sold_quantity

            if inventory_data[item_id]["quantity"] >= sold_quantity:
                inventory_data[item_id]["quantity"] -= sold_quantity

                # Update the CSV file with the sold quantity and updated 2024_Sales
                update_csv(item_id, inventory_data[item_id]["quantity"], inventory_data[item_id]["2024_Sales"])

                messagebox.showinfo("Sell Item", f"{sold_quantity} units of item {item_id} sold.")
            else:
                messagebox.showwarning("Sell Item", f"Insufficient quantity for item {item_id}.")
        else:
            messagebox.showwarning("Sell Item", "Please enter a valid quantity (greater than 0).")
    else:
        messagebox.showerror("Sell Item", f"Item with ID {item_id} not found in inventory.")


if __name__ == "__main__":
    read_csv('SalesKaggle3new.csv')
    root = tk.Tk()
    root.withdraw()
    main()



