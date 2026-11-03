import random
import datetime
from datetime import datetime
from tkinter import *
from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox, StringVar, OptionMenu,Scrollbar, Frame,simpledialog
from tkinter import ttk

FILENAME = "student_data.txt"
items_file = "items.txt"
transactions_file = "transactions.txt"
filename = "employees.txt"

# COLOURS USED / THEME
BG_COLOR = "#00008B"
FG_COLOR = "white"
BUTTON_COLOR = "#1E90FF"
global total_purchase_cost
total_purchase_cost = 0

#------------------------- SUBPROGRAMS ----------------------------------
def generate_student_id():
    def save_student():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()

        if not first_name.isalpha() or not last_name.isalpha():
            messagebox.showerror("Error", "Enter correct name format (no numbers)")
            return

        first_part = first_name[:3].capitalize()
        middle_part = str(random.randint(100, 999))
        last_part = last_name[-2:].capitalize()
        student_id = first_part + middle_part + last_part

        try:
            with open(FILENAME, "r") as file:
                if "StudentID" not in file.readline():
                    raise FileNotFoundError
        except FileNotFoundError:
            with open(FILENAME, "w") as file:
                file.write("StudentID,Name,Balance\n")

        with open(FILENAME, "a") as file:
            file.write(f"{student_id},{first_name},0\n")

        messagebox.showinfo("Success", f"Generated Student ID: {student_id}")
        add_cash = messagebox.askyesno("Add Cash", "Add cash to account?")
        if add_cash:
            record_deposit()
        student_window.destroy()

    student_window = Toplevel()
    student_window.title("Add New Student")
    student_window.configure(bg=BG_COLOR)
    student_window.geometry("600x400")  # Larger window size
    student_window.resizable(False, False)  # Disable resizing

    Label(student_window, text="First Name:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14)).grid(row=0, column=0, padx=20, pady=20)
    first_name_entry = Entry(student_window, font=("Arial", 14))
    first_name_entry.grid(row=0, column=1, padx=20, pady=20)

    Label(student_window, text="Last Name:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14)).grid(row=1, column=0, padx=20, pady=20)
    last_name_entry = Entry(student_window, font=("Arial", 14))
    last_name_entry.grid(row=1, column=1, padx=20, pady=20)

    Button(student_window, text="Save", command=save_student, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14)).grid(row=2, column=0, columnspan=2, pady=20)
#------------------------------------------------------------------------
def record_deposit():
    """Creates a deposit entry window with an option menu for selecting student ID and name."""
    deposit_window = Toplevel()
    deposit_window.title("Record Deposit")
    deposit_window.configure(bg=BG_COLOR)
    deposit_window.geometry("600x400")  # Set window size
    deposit_window.resizable(False, False)  # Disable resizing

    student_balances = {}
    student_names = {}
    student_options = []

    # Load student data from file
    try:
        with open(FILENAME, "r") as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip header row
                parts = line.strip().split(",")
                if len(parts) == 3:
                    sid, name, balance = parts
                    student_balances[sid] = int(float(balance))  # Convert to int
                    student_names[sid] = name
                    student_options.append(f"{sid} - {name}")
    except FileNotFoundError:
        messagebox.showerror("Error", f"'{FILENAME}' file not found.")
        return

    # Default selected student
    selected_student = StringVar(deposit_window)
    if student_options:
        selected_student.set(student_options[0])

    def save_deposit():
        selected_value = selected_student.get()
        student_id = selected_value.split(" - ")[0]  # Extract ID from selection
        amount = float(amount_entry.get())

        if amount > 400000:
            messagebox.showerror("Error", "CANNOT ADD MORE THAN 400,000 UGX")
            return

        # Update balance
        if student_id not in student_balances:
            messagebox.showinfo("Info", "Student ID not found. Creating a new account with zero UGX.")
            student_balances[student_id] = 0
            student_names[student_id] = "Unknown"

        student_balances[student_id] += int(amount)  # Convert to int

        # Save updated balances to file
        with open(FILENAME, "w") as file:
            file.write("StudentID,Name,Balance\n")
            for sid, balance in student_balances.items():
                name = student_names.get(sid, "Unknown")
                file.write(f"{sid},{name},{balance}\n")  # Save as int

        # Log transaction
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(transactions_file, "a") as file:
            file.write(f"{student_id},Deposit,{int(amount)},{current_datetime}\n")  # Save as int

        messagebox.showinfo("Success", "Deposit successful!")
        deposit_window.destroy()

    # UI Elements
    Label(deposit_window, text="Student ID:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14)).grid(row=0, column=0,
                                                                                                 padx=20, pady=20)
    OptionMenu(deposit_window, selected_student, *student_options).grid(row=0, column=1, padx=20,
                                                                        pady=20)  # Dropdown menu

    Label(deposit_window, text="Amount:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14)).grid(row=1, column=0, padx=20,
                                                                                             pady=20)
    amount_entry = Entry(deposit_window, font=("Arial", 14))
    amount_entry.grid(row=1, column=1, padx=20, pady=20)

    Button(deposit_window, text="Save", command=save_deposit, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14)).grid(
        row=2, column=0, columnspan=2, pady=20)
#------------------------------------------------------------------------
def load_items_and_prices():
    try:
        with open(items_file, "r") as file:
            items = [line.strip().split(",") for line in file.readlines()]

        items_window = Toplevel()
        items_window.title("Menu Items")
        items_window.configure(bg=BG_COLOR)
        items_window.geometry("600x400")

        Label(items_window, text="Item", font=("Arial", 12, "bold"), bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=10, pady=5)
        Label(items_window, text="Price", font=("Arial", 12, "bold"), bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=1, padx=10, pady=5)

        col_limit = 10  # Split into two columns if more than 10 items
        row = 1
        col = 0

        for item in items:
            Label(items_window, text=item[0], bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12)).grid(row=row, column=col, padx=10, pady=2, sticky="w")
            Label(items_window, text=f"UGX {item[1]}", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12)).grid(row=row, column=col + 1, padx=10, pady=2, sticky="w")

            row += 1
            if row > col_limit:  # Move to second column
                row = 1
                col = 2

    except FileNotFoundError:
        messagebox.showerror("Error", "items.txt file not found.")
#------------------------------------------------------------------------
def purchase_items():
    global total_purchase_cost
    def add_item():

        global total_purchase_cost
        item = item_entry.get().capitalize()
        quantity = quantity_entry.get()

        if not item or not quantity:
            messagebox.showerror("Error", "Please enter both item and quantity.")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be a positive number.")
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        if item not in items:
            messagebox.showerror("Error", "Item not found in the menu.")
            return

        price = items[item]
        total_cost = price * quantity

        # Add item to the purchase list
        purchase_list.append((item, quantity, total_cost))

        # Update the items list display
        items_list.insert(END, f"{item} x{quantity} - UGX {total_cost}")

        # Update the total cost
        total_purchase_cost += total_cost

        total_label.config(text=f"Total: {total_purchase_cost} UGX")

        # Clear the input fields
        item_entry.delete(0, END)
        quantity_entry.delete(0, END)

    def close_window():
        # Perform all calculations and display the receipt when the "Done" button is clicked
        if not purchase_list:
            messagebox.showerror("Error", "No items added to the purchase.")
            return

        student_id = student_id_entry.get()
        if not student_id:
            messagebox.showerror("Error", "Please enter a student ID.")
            return

        # Load student balances
        student_balances = {}
        try:
            with open("student_data.txt", "r") as file:
                lines = file.readlines()
                for line in lines[1:]:
                    line = line.strip()
                    if line:
                        sid, name, balance = line.split(",")
                        student_balances[sid] = {'name': name, 'balance': int(float(balance))}
        except FileNotFoundError:
            messagebox.showerror("Error", "'student_data.txt' file not found.")
            return

        if student_id not in student_balances:
            messagebox.showerror("Error", "Student not found.")
            return

        student_name = student_balances[student_id]['name']
        current_balance = student_balances[student_id]['balance']

        if current_balance < total_purchase_cost:
            messagebox.showerror("Error", "Not enough balance for this purchase.")
            return

        # Deduct the total cost from the student's balance
        student_balances[student_id]['balance'] -= total_purchase_cost

        # Save updated balances back to the student data file
        with open("student_data.txt", "w") as file:
            file.write("StudentID,Name,Balance\n")
            for sid, data in student_balances.items():
                file.write(f"{sid},{data['name']},{data['balance']}\n")

        # Log the transaction
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        items_str = "; ".join([f"{item[0]} x{item[1]}" for item in purchase_list])
        with open(transactions_file, "a") as file:
            file.write(f"{student_id},Purchase,{total_purchase_cost},{current_datetime},{items_str}\n")

        # Display the receipt in the receipt_text widget
        receipt_text.config(state=NORMAL)  # Enable editing
        receipt_text.delete(1.0, END)  # Clear previous content

        # Format the receipt
        receipt_text.insert(END, "=" * 40 + "\n")
        now = datetime.now()
        receipt_text.insert(END, f"{now.strftime('%Y-%m-%d')}                                 {now.strftime('%H:%M:%S')}\n")
        receipt_text.insert(END, "-" * 72 + "\n")
        receipt_text.insert(END, f"Receipt for: {student_id}\n")
        receipt_text.insert(END, "-" * 72 + "\n")
        receipt_text.insert(END, "| {:<18}     |  {:>28} |\n".format("Item", "Price"))
        receipt_text.insert(END, "-" * 72 + "\n")

        for item, quantity, cost in purchase_list:
            receipt_text.insert(END, "| {:<18} | UGX {:>19} |\n".format(f"{item} x{quantity}", cost))

        receipt_text.insert(END, "-" * 72 + "\n")
        receipt_text.insert(END, "| {:<18}     | UGX {:>19} |\n".format("Total", total_purchase_cost))
        receipt_text.insert(END, "=" * 40 + "\n")

        # Clear all input fields and lists except menu items
        student_id_entry.delete(0, END)
        item_entry.delete(0, END)
        quantity_entry.delete(0, END)
        items_list.delete(0, END)
        purchase_list.clear()
    # Load items from the menu
    items = {}
    try:
        with open(items_file, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    item_name, price = line.split(",")
                    items[item_name.strip().capitalize()] = int(float(price))
    except FileNotFoundError:
        messagebox.showerror("Error", "'items.txt' file not found.")
        return

    # Initialize purchase list and total cost
    purchase_list = []

    # Create the purchase window
    purchase_window = Toplevel()
    purchase_window.title("Purchase Items")
    purchase_window.configure(bg=BG_COLOR)
    purchase_window.geometry("1200x600")  # Larger window size to fit everything
    purchase_window.resizable(False, False)  # Disable resizing

    # Main frame for the layout
    main_frame = Frame(purchase_window, bg=BG_COLOR)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Left frame for menu items
    left_frame = Frame(main_frame, bg=BG_COLOR)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    Label(left_frame, text="Menu Items", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

    # Display menu items in a grid
    menu_frame = Frame(left_frame, bg=BG_COLOR)
    menu_frame.pack(fill=BOTH, expand=True)

    row = 0
    col = 0
    for item, price in items.items():
        Label(menu_frame, text=f"{item} - UGX {price}", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14)).grid(row=row, column=col, padx=10, pady=5, sticky="w")
        col += 1
        if col > 1:  # Two columns for menu items
            col = 0
            row += 1

    # Middle frame for adding items and student ID
    middle_frame = Frame(main_frame, bg=BG_COLOR)
    middle_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Student ID input
    Label(middle_frame, text="Student ID:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14)).pack(pady=5)
    student_id_entry = Entry(middle_frame, font=("Arial", 14))
    student_id_entry.pack(pady=5)

    # Item and quantity input
    Label(middle_frame, text="Item:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14)).pack(pady=5)
    item_entry = Entry(middle_frame, font=("Arial", 14))
    item_entry.pack(pady=5)

    Label(middle_frame, text="Quantity:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14)).pack(pady=5)
    quantity_entry = Entry(middle_frame, font=("Arial", 14))
    quantity_entry.pack(pady=5)

    Button(middle_frame, text="Add Item", command=add_item, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14)).pack(pady=10)

    # Right frame for receipt and total
    right_frame = Frame(main_frame, bg=BG_COLOR)
    right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    Label(right_frame, text="Receipt", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

    # Receipt display
    receipt_text = Text(right_frame, font=("Arial", 12), bg="white", fg="black", state=NORMAL, height=20, width=40)
    receipt_text.pack(fill=BOTH, expand=True)

    # Total cost display
    total_label = Label(right_frame, text="Total: UGX 0", font=("Arial", 14, "bold"), bg=BG_COLOR, fg=FG_COLOR)
    total_label.pack(pady=13)

    # Done button
    done_button = Button(right_frame, text="Done", command=close_window, bg=BUTTON_COLOR, fg=FG_COLOR,
                         font=("Arial", 14), state=NORMAL)
    done_button.pack(pady=13)

    # Configure grid weights for main_frame
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    # Create the items_list widget
    items_list = Listbox(left_frame, font=("Arial", 14), bg="white", fg="black")
    items_list.pack(fill=BOTH, expand=True)

    def remove_item():
        selected_index = items_list.curselection()  # Get selected item index
        if not selected_index:
            messagebox.showerror("Error", "Please select an item to remove.")
            return

        index = selected_index[0]  # Get the first selected item index
        removed_item = purchase_list.pop(index)  # Remove item from the purchase list

        # Update the total purchase cost
        global total_purchase_cost
        total_purchase_cost -= removed_item[2]  # Subtract removed item's cost

        # Update the total label
        total_label.config(text=f"Total: UGX {total_purchase_cost}")

        # Remove item from the listbox
        items_list.delete(index)

    Button(middle_frame, text="Remove Item", command=remove_item, bg=BUTTON_COLOR, fg=FG_COLOR,font=("Arial", 14)).pack(pady=10)
#------------------------------------------------------------------------
def generate_transaction_report():
    # Create a new window for the report
    report_window = Toplevel()
    report_window.title("Transaction Report")
    report_window.configure(bg=BG_COLOR)
    report_window.geometry("1000x600")

    # Prompt user for report type selection
    report_choice = simpledialog.askinteger("Report Choice", "Enter 1 for Student Balances or 2 for Financial Summary")

    # Validate user input
    if report_choice != 1 and report_choice != 2:
        messagebox.showerror("Invalid Selection", "Please enter either 1 (Student Balances) or 2 (Financial Summary).")
        return

    # Create a frame to hold the Treeview and scrollbar
    frame = Frame(report_window, bg=BG_COLOR)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Define column names based on the selected report type
    if report_choice == 1:
        columns = ("ID", "Name", "Balance")  # Student balances
    else:
        columns = ("ID", "Type", "Amount", "Date", "Items", "Action Taken")  # Financial transactions

    # Create a Treeview widget with the defined columns
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Set up column headers and adjust width for better visibility
    for col in columns:
        tree.heading(col, text=col)  # Set column title
        tree.column(col, anchor="center", width=190)  # Center-align text

    # Create a vertical scrollbar for the Treeview
    scrollbar = Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # Pack the scrollbar and Treeview into the frame
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Load data into the Treeview based on the selected report type
    try:
        if report_choice == 1:  # Student balance report
            with open(FILENAME, "r") as file:
                lines = file.readlines()
                for line in lines[1:]:  # Skip header row
                    student_id, name, balance = line.strip().split(",")
                    tree.insert("", "end", values=(student_id, name, f"{int(balance):,} UGX"))
        elif report_choice == 2:  # Financial transactions report
            with open(transactions_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    transaction = line.strip().split(",")

                    # Handle "Deletion" separately
                    if len(transaction) == 4 and transaction[1] == "Deletion":
                        student_id, transaction_type, date_time, action_taken = transaction
                        amount = "N/A"  # No monetary value for deletions
                        items = ""  # No items involved
                    elif len(transaction) >= 4:  # Normal transaction with amount
                        student_id, transaction_type, amount, date_time = transaction[:4]
                        items = ",".join(transaction[4:])  # Combine any extra items
                        action_taken = ""  # No action taken for regular transactions
                    else:
                        continue  # Skip invalid or incorrectly formatted transactions

                    # Insert the transaction data into the Treeview
                    tree.insert("", "end", values=(student_id, transaction_type, amount, date_time, items, action_taken))
    except FileNotFoundError as e:
        # Display an error message if the required file is missing
        messagebox.showerror("Error", f"{e.filename} file not found.")
#------------------------------------------------------------------------
def delete_student():
    student_id = simpledialog.askstring("Delete Student", "Enter the Student ID to delete:")

    if not student_id:
        return

    with open(FILENAME, "r") as file:
        lines = file.readlines()

    new_lines = [lines[0]]
    found = False

    for line in lines[1:]:
        parts = line.strip().split(",")
        if parts[0] == student_id:
            found = True
            student_name = parts[1]
        else:
            new_lines.append(line)

    if not found:
        messagebox.showerror("Error", "Student ID not found.")
        return

    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete {student_name}'s account?")
    if not confirm:
        return

    with open(FILENAME, "w") as file:
        file.writelines(new_lines)

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(transactions_file, "a") as file:
        file.write(f"{student_id},Deletion,0 UGX,{current_datetime},Account Deleted\n")

    messagebox.showinfo("Success", f"Student {student_name} has been deleted.")
#-------------------------- MAIN PROGRAM --------------------------------
def canteen_system():
    root = Tk()
    root.title("BSK Canteen Management System")
    root.configure(bg=BG_COLOR)
    root.geometry("800x600")
    root.resizable(False, False)  # Disable resizing

    # Configure grid weights to center the buttons
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)

    try:
        icon = PhotoImage(file='logo.png')
        root.iconphoto(True, icon)  # Set the window icon
    except TclError:
        print("Icon image file not found or unsupported format. Ensure 'G.png' is present.")

    # Main window buttons in a 3x2 grid
    Label(root, text="-------- BSK CANTEEN ----------", font=("Arial", 20, "bold"), bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, columnspan=2, pady=20)
    Button(root, text="Add New Student", command=generate_student_id, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14), width=20).grid(row=1, column=0, padx=20, pady=20)
    Button(root, text="Open Canteen Register", command=purchase_items, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14), width=20).grid(row=1, column=1, padx=20, pady=20)
    Button(root, text="Make Cash Deposits", command=record_deposit, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14), width=20).grid(row=2, column=0, padx=20, pady=20)
    Button(root, text="Load Menu", command=load_items_and_prices, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14), width=20).grid(row=2, column=1, padx=20, pady=20)
    Button(root, text="View Canteen Reports", command=generate_transaction_report, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14), width=20).grid(row=3, column=0, padx=20, pady=20)
    Button(root, text="Delete Student Account", command=delete_student, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14), width=20).grid(row=3, column=1, padx=20, pady=20)
    root.mainloop()
#------------------------------- LOGIN ----------------------------------
def login():
    root = Tk()
    root.title("Login")
    root.configure(bg=BG_COLOR)
    root.geometry("600x400")  # Larger window size
    root.resizable(False, False)  # Disable resizing

    try:
        icon = PhotoImage(file='logo.png')
        root.iconphoto(True, icon)  # Set the window icon
    except TclError:
        print("Icon image file not found or unsupported format. Ensure 'G.png' is present.")

    Label(root, text="------LOGIN TO BSK CANTEEN SYSTEM---------", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)
    Label(root, text="Enter Your Name:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14)).pack(pady=10)
    e_name_entry = Entry(root, font=("Arial", 14))
    e_name_entry.pack(pady=10)
    Label(root, text="Enter Your Employee Code:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14)).pack(pady=10)
    code_entry = Entry(root, font=("Arial", 14))
    code_entry.pack(pady=10)

    def check_login():
        e_name = e_name_entry.get().capitalize().strip()
        code = code_entry.get().strip()

        access_granted = False

        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    employee_details = line.split(",")
                    if e_name == employee_details[0] and code == employee_details[1]:
                        access_granted = True
                        root.destroy()
                        canteen_system()
                        break

            if not access_granted:
                messagebox.showerror("Error", "ACCESS DENIED")
        except FileNotFoundError:
            messagebox.showerror("Error", "'employees.txt' file not found.")

    Button(root, text="Login", command=check_login, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 14), width=15).pack(pady=20)

    root.mainloop()

login()


#tired