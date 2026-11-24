from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Store all registered customer objects
customers_list = []

"""
Customer Management System

This program allows users to register, search, view, update and delete
customer information. All operations are performed through the GUI.
Customer records are stored in customers.txt.
"""


# ---------------------------------------------------------
# CUSTOMER CLASSES
# ---------------------------------------------------------

class Customer:

    def __init__(self, customer_id, customer_name, contact_number, registration_date):
        self.__customer_id = customer_id
        self.__customer_name = customer_name
        self.__contact_number = contact_number
        self.__registration_date = registration_date

    def get_customer_details(self):
        return {
            "Customer ID": self.__customer_id,
            "Customer Name": self.__customer_name,
            "Contact Number": self.__contact_number,
            "Registration Date": self.__registration_date
        }

    def update_customer_details(self, customer_name, contact_number):
        self.__customer_name = customer_name
        self.__contact_number = contact_number


class RegisteredCustomer(Customer):

    def __init__(self, customer_id, customer_name, contact_number, registration_date):
        super().__init__(
            customer_id,
            customer_name,
            contact_number,
            registration_date
        )

    @staticmethod
    def display_registration_status():
        return "Registered"


# ---------------------------------------------------------
# DATABASE FUNCTIONS
# ---------------------------------------------------------

def save_customers_to_file(customers):
    """Rewrite customers.txt using the current customer records."""
    try:
        with open("customers.txt", "w", encoding="utf-8") as file:
            for customer in customers:
                details = customer.get_customer_details()
                file.write(
                    f'{details["Customer ID"]},'
                    f'{details["Customer Name"]},'
                    f'{details["Contact Number"]},'
                    f'{details["Registration Date"]}\n'
                )
        return True
    except OSError as e:
        messagebox.showerror("File Error", f"Unable to save customer records:\n{e}")
        return False


def load_customers_from_file():
    """Load existing customer records once when the program starts."""
    customers_list.clear()

    try:
        with open("customers.txt", "r", encoding="utf-8") as file:
            # Read one record at a time until the end of the file.
            line = file.readline()
            while line:
                details = line.strip().split(",")

                if len(details) == 4:
                    customer = RegisteredCustomer(
                        details[0],
                        details[1],
                        details[2],
                        details[3]
                    )
                    customers_list.append(customer)

                line = file.readline()

    except FileNotFoundError:
        # It is normal for the file not to exist on the first run.
        pass
    except OSError as e:
        messagebox.showerror("File Error", f"Unable to read customer records:\n{e}")


def find_customer(customer_id):
    """Return the customer with the matching ID, or None."""
    customer_id = customer_id.strip().upper()

    for customer in customers_list:
        details = customer.get_customer_details()

        existing_id = details["Customer ID"].strip().upper()

        if existing_id == customer_id:
            return customer

    return None


# ---------------------------------------------------------
# MAIN GUI WINDOW AND LAYOUT
# ---------------------------------------------------------

root = tk.Tk()
root.title("Customer Management System")
root.geometry("1000x650")
root.minsize(850, 550)
root.configure(bg="#F3F6FA")

# Main colours
SIDEBAR_COLOR = "#172B4D"
SIDEBAR_ACTIVE = "#29466F"
BG_COLOR = "#F3F6FA"
WHITE = "#FFFFFF"
TEXT_COLOR = "#243247"
MUTED_COLOR = "#65758B"
PRIMARY_COLOR = "#2563EB"
SUCCESS_COLOR = "#16834A"
DANGER_COLOR = "#C0392B"

# Sidebar
sidebar = tk.Frame(root, bg=SIDEBAR_COLOR, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

brand_label = tk.Label(
    sidebar,
    text="CUSTOMER\nMANAGEMENT",
    font=("Arial", 16, "bold"),
    bg=SIDEBAR_COLOR,
    fg="white",
    justify="left"
)
brand_label.pack(anchor="w", padx=20, pady=(28, 35))

# Main content area
content_area = tk.Frame(root, bg=BG_COLOR)
content_area.pack(side="right", fill="both", expand=True)

page_title = tk.Label(
    content_area,
    text="Dashboard",
    font=("Arial", 22, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
page_title.pack(anchor="w", padx=30, pady=(25, 5))

page_subtitle = tk.Label(
    content_area,
    text="Manage customer records using the menu on the left.",
    font=("Arial", 10),
    bg=BG_COLOR,
    fg=MUTED_COLOR
)
page_subtitle.pack(anchor="w", padx=30, pady=(0, 20))

page_container = tk.Frame(content_area, bg=BG_COLOR)
page_container.pack(fill="both", expand=True, padx=30, pady=(0, 25))

current_page = {"name": None}
sidebar_buttons = []


def clear_page():
    for widget in page_container.winfo_children():
        widget.destroy()


def set_page_heading(title, subtitle=""):
    page_title.config(text=title)
    page_subtitle.config(text=subtitle)


def make_card(parent, padding=20):
    return tk.Frame(parent, bg=WHITE, padx=padding, pady=padding,
                    highlightthickness=1, highlightbackground="#E1E7EF")


def make_label(parent, text, font=("Arial", 10), **kwargs):
    return tk.Label(
        parent,
        text=text,
        font=font,
        bg=kwargs.pop("bg", WHITE),
        fg=kwargs.pop("fg", TEXT_COLOR),
        **kwargs
    )


def make_entry(parent, width=35):
    return tk.Entry(
        parent,
        width=width,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )


def make_action_button(parent, text, command, color=PRIMARY_COLOR):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=16,
        pady=9
    )


def set_active_sidebar(button):
    for item in sidebar_buttons:
        item.config(bg=SIDEBAR_COLOR)
    button.config(bg=SIDEBAR_ACTIVE)


# ---------------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------------

def show_dashboard():
    current_page["name"] = "Dashboard"
    set_page_heading(
        "Dashboard",
        "Welcome to the Customer Management System."
    )
    clear_page()

    card = make_card(page_container, padding=25)
    card.pack(fill="x", pady=5)

    make_label(
        card,
        "Welcome!",
        font=("Arial", 20, "bold")
    ).pack(anchor="w")

    make_label(
        card,
        "Choose an operation from the sidebar to manage customer records.",
        font=("Arial", 11),
        fg=MUTED_COLOR
    ).pack(anchor="w", pady=(8, 18))

    count = len(customers_list)
    make_label(
        card,
        f"Total registered customers: {count}",
        font=("Arial", 13, "bold"),
        fg=PRIMARY_COLOR
    ).pack(anchor="w")

    quick_card = make_card(page_container, padding=20)
    quick_card.pack(fill="x", pady=15)

    make_label(
        quick_card,
        "Available Operations",
        font=("Arial", 14, "bold")
    ).pack(anchor="w", pady=(0, 12))

    for text, command in [
        ("Register Customer", show_register_page),
        ("Search Customer", show_search_page),
        ("View All Customers", show_view_page),
        ("Update Customer", show_update_page),
        ("Delete Customer", show_delete_page)
    ]:
        make_action_button(quick_card, text, command).pack(
            anchor="w", fill="x", pady=4
        )


# ---------------------------------------------------------
# REGISTER CUSTOMER PAGE
# ---------------------------------------------------------

def show_register_page():
    current_page["name"] = "Register"
    set_page_heading(
        "Register Customer",
        "Enter the customer's details below to create a new record."
    )
    clear_page()

    card = make_card(page_container)
    card.pack(anchor="nw", fill="x")

    make_label(card, "Customer ID:").pack(anchor="w", pady=(0, 5))
    customer_id_entry = make_entry(card)
    customer_id_entry.pack(anchor="w", pady=(0, 15))

    make_label(card, "Customer Name:").pack(anchor="w", pady=(0, 5))
    customer_name_entry = make_entry(card)
    customer_name_entry.pack(anchor="w", pady=(0, 15))

    make_label(card, "Contact Number:").pack(anchor="w", pady=(0, 5))
    contact_number_entry = make_entry(card)
    contact_number_entry.pack(anchor="w", pady=(0, 20))

    def register_customer_gui():
        customer_id = customer_id_entry.get().strip().upper()
        customer_name = customer_name_entry.get().strip()
        contact_number = contact_number_entry.get().strip()

        if customer_id == "" or customer_name == "" or contact_number == "":
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        if find_customer(customer_id) is not None:
            messagebox.showerror("Error", "Customer ID already exists!")
            return

        if not contact_number.isdigit():
            messagebox.showerror(
                "Error",
                "Contact Number must contain digits only!"
            )
            return

        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_customer = RegisteredCustomer(
            customer_id,
            customer_name,
            contact_number,
            registration_date
        )

        customers_list.append(new_customer)

        if not save_customers_to_file(customers_list):
            customers_list.remove(new_customer)
            return

        messagebox.showinfo("Success", "Customer registered successfully!")

        customer_id_entry.delete(0, tk.END)
        customer_name_entry.delete(0, tk.END)
        contact_number_entry.delete(0, tk.END)

    make_action_button(
        card,
        "Register Customer",
        register_customer_gui,
        SUCCESS_COLOR
    ).pack(anchor="w")


# ---------------------------------------------------------
# SEARCH CUSTOMER PAGE
# ---------------------------------------------------------

def show_search_page():
    current_page["name"] = "Search Customer"
    set_page_heading(
        "Search Customer",
        "Search for a customer using their Customer ID."
    )
    clear_page()

    card = make_card(page_container)
    card.pack(anchor="nw", fill="x")

    make_label(card, "Customer ID:").pack(anchor="w", pady=(0, 5))
    search_id_entry = make_entry(card)
    search_id_entry.pack(anchor="w", pady=(0, 15))

    result_label = make_label(
        card,
        "Search results will appear here.",
        font=("Arial", 10),
        fg=MUTED_COLOR,
        justify="left",
        anchor="w"
    )
    result_label.pack(fill="x", pady=(10, 15))

    def search_customer_gui():
        customer_id = search_id_entry.get().strip().upper()

        if customer_id == "":
            messagebox.showerror("Error", "Customer ID cannot be empty!")
            return

        customer = find_customer(customer_id)

        if customer is None:
            result_label.config(
                text="Customer not found!",
                fg=DANGER_COLOR
            )
            return

        details = customer.get_customer_details()
        result_label.config(
            text=(
                "Customer Found!\n\n"
                f'Customer ID: {details["Customer ID"]}\n'
                f'Customer Name: {details["Customer Name"]}\n'
                f'Contact Number: {details["Contact Number"]}\n'
                f'Registration Date: {details["Registration Date"]}\n'
                f"Registration Status: {customer.display_registration_status()}"
            ),
            fg=TEXT_COLOR
        )

    make_action_button(card, "Search Customer", search_customer_gui).pack(anchor="w")


# ---------------------------------------------------------
# VIEW ALL CUSTOMERS PAGE
# ---------------------------------------------------------

def show_view_page():
    current_page["name"] = "View All Customers"
    set_page_heading(
        "View All Customers",
        "A list of all customer records saved in the system."
    )
    clear_page()

    card = make_card(page_container, padding=15)
    card.pack(fill="both", expand=True)

    columns = ("id", "name", "contact", "date", "status")
    tree = ttk.Treeview(card, columns=columns, show="headings", height=15)

    headings = {
        "id": "Customer ID",
        "name": "Customer Name",
        "contact": "Contact Number",
        "date": "Registration Date",
        "status": "Registration Status"
    }

    widths = {
        "id": 100,
        "name": 160,
        "contact": 120,
        "date": 170,
        "status": 140
    }

    for column in columns:
        tree.heading(column, text=headings[column])
        tree.column(column, width=widths[column], anchor="w")

    scrollbar = ttk.Scrollbar(card, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for customer in customers_list:
        details = customer.get_customer_details()
        tree.insert(
            "",
            "end",
            values=(
                details["Customer ID"],
                details["Customer Name"],
                details["Contact Number"],
                details["Registration Date"],
                customer.display_registration_status()
            )
        )

    if not customers_list:
        make_label(
            card,
            "No customer records found.",
            fg=MUTED_COLOR
        ).pack(anchor="w", pady=10)


# ---------------------------------------------------------
# UPDATE CUSTOMER PAGE
# ---------------------------------------------------------

def show_update_page():
    current_page["name"] = "Update Customer"
    set_page_heading(
        "Update Customer",
        "Find a customer by ID and update their name or contact number."
    )
    clear_page()

    card = make_card(page_container)
    card.pack(anchor="nw", fill="x")

    make_label(card, "Customer ID:").pack(anchor="w", pady=(0, 5))
    customer_id_entry = make_entry(card)
    customer_id_entry.pack(anchor="w", pady=(0, 15))

    make_label(card, "New Customer Name:").pack(anchor="w", pady=(0, 5))
    customer_name_entry = make_entry(card)
    customer_name_entry.pack(anchor="w", pady=(0, 15))

    make_label(card, "New Contact Number:").pack(anchor="w", pady=(0, 5))
    contact_number_entry = make_entry(card)
    contact_number_entry.pack(anchor="w", pady=(0, 20))

    def update_customer_gui():
        customer_id = customer_id_entry.get().strip().upper()
        customer_name = customer_name_entry.get().strip()
        contact_number = contact_number_entry.get().strip()

        if customer_id == "":
            messagebox.showerror("Error", "Customer ID cannot be empty!")
            return

        customer = find_customer(customer_id)

        if customer is None:
            messagebox.showerror("Error", "Customer not found!")
            return

        if customer_name == "" or contact_number == "":
            messagebox.showerror("Error", "Fields cannot be empty!")
            return

        if not contact_number.isdigit():
            messagebox.showerror(
                "Error",
                "Contact Number must contain digits only!"
            )
            return

        old_details = customer.get_customer_details()
        old_name = old_details["Customer Name"]
        old_contact = old_details["Contact Number"]

        customer.update_customer_details(customer_name, contact_number)

        if not save_customers_to_file(customers_list):
            customer.update_customer_details(old_name, old_contact)
            return

        messagebox.showinfo("Success", "Customer updated successfully!")

        customer_id_entry.delete(0, tk.END)
        customer_name_entry.delete(0, tk.END)
        contact_number_entry.delete(0, tk.END)

    make_action_button(
        card,
        "Update Customer",
        update_customer_gui
    ).pack(anchor="w")


# ---------------------------------------------------------
# DELETE CUSTOMER PAGE
# ---------------------------------------------------------

def show_delete_page():
    current_page["name"] = "Delete Customer"
    set_page_heading(
        "Delete Customer",
        "Enter the Customer ID of the record you want to delete."
    )
    clear_page()

    card = make_card(page_container)
    card.pack(anchor="nw", fill="x")

    make_label(card, "Customer ID:").pack(anchor="w", pady=(0, 5))
    customer_id_entry = make_entry(card)
    customer_id_entry.pack(anchor="w", pady=(0, 20))

    def delete_customer_gui():
        customer_id = customer_id_entry.get().strip().upper()

        if customer_id == "":
            messagebox.showerror("Error", "Customer ID cannot be empty!")
            return

        customer = find_customer(customer_id)

        if customer is None:
            messagebox.showerror("Error", "Customer not found!")
            return

        details = customer.get_customer_details()
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this customer?\n\n"
            f'Customer ID: {details["Customer ID"]}\n'
            f'Customer Name: {details["Customer Name"]}'
        )

        if not confirm:
            messagebox.showinfo("Deletion", "Deletion cancelled!")
            return

        customers_list.remove(customer)

        if not save_customers_to_file(customers_list):
            customers_list.append(customer)
            return

        messagebox.showinfo("Success", "Customer deleted successfully!")
        customer_id_entry.delete(0, tk.END)

    make_action_button(
        card,
        "Delete Customer",
        delete_customer_gui,
        DANGER_COLOR
    ).pack(anchor="w")


# ---------------------------------------------------------
# SIDEBAR NAVIGATION BUTTONS
# ---------------------------------------------------------

def add_sidebar_button(text, command):
    button = tk.Button(
        sidebar,
        text=text,
        command=lambda: (set_active_sidebar(button), command()),
        font=("Arial", 11),
        bg=SIDEBAR_COLOR,
        fg="white",
        activebackground=SIDEBAR_ACTIVE,
        activeforeground="white",
        relief="flat",
        anchor="w",
        padx=22,
        pady=12,
        cursor="hand2"
    )
    button.pack(fill="x", padx=8, pady=2)
    sidebar_buttons.append(button)
    return button


dashboard_button = add_sidebar_button("  Dashboard", show_dashboard)
register_nav_button = add_sidebar_button("  Register Customer", show_register_page)
search_nav_button = add_sidebar_button("  Search Customer", show_search_page)
view_nav_button = add_sidebar_button("  View All Customers", show_view_page)
update_nav_button = add_sidebar_button("  Update Customer", show_update_page)
delete_nav_button = add_sidebar_button("  Delete Customer", show_delete_page)

tk.Frame(sidebar, bg="#40536D", height=1).pack(fill="x", padx=15, pady=18)

exit_button = tk.Button(
    sidebar,
    text="  Exit",
    command=lambda: (
        root.destroy()
        if messagebox.askyesno("Exit", "Are you sure you want to exit?")
        else None
    ),
    font=("Arial", 11),
    bg=SIDEBAR_COLOR,
    fg="white",
    activebackground=SIDEBAR_ACTIVE,
    activeforeground="white",
    relief="flat",
    anchor="w",
    padx=22,
    pady=12,
    cursor="hand2"
)
exit_button.pack(fill="x", padx=8, pady=2)


# ---------------------------------------------------------
# START PROGRAM
# ---------------------------------------------------------

load_customers_from_file()
set_active_sidebar(dashboard_button)
show_dashboard()

# The GUI starts immediately. No input() or Console Menu is required.
root.mainloop()
