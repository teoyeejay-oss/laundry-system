# Laundry Service Assistant - expanded single-file edition
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if __name__ == "__main__":
    os.chdir(BASE_DIR)

# =================================================================
# MODULE 1: module1.py
# =================================================================
if __name__ == "__main__" and sys.argv[1:] == ["--module", 'module1.py']:
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
    root.geometry("1100x700")
    root.resizable(True, True)
    try:
        root.state("zoomed")
    except tk.TclError:
        pass
    # Dark colour palette matching Modules 2, 3, 4 and 5.
    SIDEBAR_COLOR = "#1E293B"
    SIDEBAR_ACTIVE = "#334155"
    BG_COLOR = "#0F172A"
    WHITE = "#1E293B"
    TEXT_COLOR = "#F8FAFC"
    MUTED_COLOR = "#94A3B8"
    PRIMARY_COLOR = "#2563EB"
    SUCCESS_COLOR = "#22C55E"
    DANGER_COLOR = "#EF4444"
    root.configure(bg=BG_COLOR)

    # Table and form controls matching the shared dark dashboard theme.
    gui_style = ttk.Style(root)
    gui_style.theme_use("clam")
    gui_style.configure("Treeview", background=WHITE, fieldbackground=WHITE,
                         foreground=TEXT_COLOR, rowheight=28, bordercolor="#475569")
    gui_style.configure("Treeview.Heading", background="#334155",
                         foreground=TEXT_COLOR, font=("Arial", 10, "bold"))
    gui_style.map("Treeview", background=[("selected", PRIMARY_COLOR)],
                  foreground=[("selected", "#FFFFFF")])
    gui_style.configure("TScrollbar", background="#334155", troughcolor=BG_COLOR)

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
                        highlightthickness=1, highlightbackground="#475569")


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
            bd=1,
            bg=WHITE,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            highlightthickness=1,
            highlightbackground="#475569",
            highlightcolor=PRIMARY_COLOR
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

    tk.Frame(sidebar, bg="#475569", height=1).pack(fill="x", padx=15, pady=18)

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

    raise SystemExit(0)

# =================================================================
# MODULE 2: module2.py
# =================================================================
if __name__ == "__main__" and sys.argv[1:] == ["--module", 'module2.py']:
    """
AMCS1034 - Laundry Service Assistant App
Module 2: Laundry Order Management Module
Features: create, view, search, update and delete laundry orders
"""

    import json                              # predefined module: file storage
    import os                                # predefined module: check file exists
    from datetime import datetime            # predefined module: order date/time
    import tkinter as tk                     # predefined module: GUI
    from tkinter import ttk, messagebox

    ORDERS_FILE = "orders.json"
    CUSTOMERS_FILE = "customers.txt"         # written by Module 1
    SERVICES = ("Washing", "Drying", "Ironing")   # tuple: fixed list of services
    VALID_SERVICES = set(SERVICES)                # set: used to validate services
    STATUSES = ("Pending", "Completed")


    # ---------------------------------------------------------------
    # Classes (encapsulation + inheritance)
    # ---------------------------------------------------------------
    class Record:
        """Base class: every record has a read-only ID."""

        def __init__(self, record_id):
            self.__record_id = record_id      # private attribute

        @property
        def record_id(self):
            return self.__record_id


    class Order(Record):
        """A laundry order. Inherits from Record."""

        def __init__(self, order_id, customer_id, weight, services,
                     status="Pending", created=None):
            super().__init__(order_id)
            self.__customer_id = customer_id
            self.weight = weight              # uses setter (validated)
            self.services = services          # uses setter (validated)
            self.status = status              # uses setter (validated)
            self.__created = created or datetime.now().strftime("%Y-%m-%d %H:%M")

        # --- getters and setters (encapsulation) ---
        @property
        def customer_id(self):
            return self.__customer_id

        @customer_id.setter
        def customer_id(self, value):
            self.__customer_id = value

        @property
        def weight(self):
            return self.__weight

        @weight.setter
        def weight(self, value):
            if value <= 0:
                raise ValueError("Weight must be more than 0 kg.")
            self.__weight = value

        @property
        def services(self):
            return self.__services

        @services.setter
        def services(self, value):
            if len(value) == 0 or not set(value) <= VALID_SERVICES:
                raise ValueError("Please choose at least one valid service.")
            self.__services = list(value)

        @property
        def status(self):
            return self.__status

        @status.setter
        def status(self, value):
            if value not in STATUSES:
                raise ValueError("Status must be Pending or Completed.")
            self.__status = value

        @property
        def created(self):
            return self.__created

        def to_dict(self):
            """Convert the order to a dictionary for saving."""
            return {"order_id": self.record_id, "customer_id": self.customer_id,
                    "weight": self.weight, "services": self.services,
                    "status": self.status, "created": self.created}

        @staticmethod
        def from_dict(d):
            return Order(d["order_id"], d["customer_id"], d["weight"],
                         d["services"], d["status"], d["created"])


    # ---------------------------------------------------------------
    # File processing and helper functions
    # ---------------------------------------------------------------
    def load_orders():
        """Read orders.json and return a dictionary {order_id: Order}."""
        orders = {}
        if not os.path.exists(ORDERS_FILE):
            return orders
        try:
            with open(ORDERS_FILE, "r") as file:
                for d in json.load(file):
                    order = Order.from_dict(d)
                    orders[order.record_id] = order
        except (json.JSONDecodeError, KeyError, ValueError):
            messagebox.showwarning("File Error", "orders.json is damaged. Starting empty.")
        return orders


    def save_orders(orders):
        """Write all orders to orders.json."""
        with open(ORDERS_FILE, "w") as file:
            json.dump([o.to_dict() for o in orders.values()], file, indent=4)


    def load_customers():
        """Read registered customers from Module 1 -> {customer_id: name}."""
        customers = {}
        try:
            with open(CUSTOMERS_FILE, "r") as file:
                for line in file:
                    parts = line.strip().split(",")   # id,name,contact,date
                    if len(parts) == 4:
                        customers[parts[0]] = parts[1]   # dict removes duplicate IDs
        except OSError:
            pass                                      # file missing -> no customers
        return customers


    def format_order_id(text):
        """String processing: clean and validate an Order ID like O001."""
        text = text.strip().upper()
        if len(text) < 2 or text[0] != "O" or not text[1:].isdigit():
            raise ValueError("Order ID must look like O001.")
        return text


    def next_order_id(orders):
        """Suggest the next free Order ID."""
        number = len(orders) + 1
        while f"O{number:03d}" in orders:     # keep going until the ID is unused
            number += 1
        return f"O{number:03d}"


    # ---------------------------------------------------------------
    # GUI
    # ---------------------------------------------------------------
    class OrderApp:
        def __init__(self, window):
            self.window = window
            self.window.title("Laundry Order Management")
            self.window.geometry("1100x700")
            self.window.resizable(True, True)
            try:
                self.window.state("zoomed")
            except tk.TclError:
                pass
            self.window.configure(bg="#0F172A")

            # Shared dashboard-style header (same palette and typography as Main / Module 1).
            self.window.grid_columnconfigure(0, weight=0)
            self.window.grid_columnconfigure(1, weight=1)
            self.window.grid_rowconfigure(1, weight=1)
            header = tk.Frame(self.window, bg="#0F172A")
            header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=24, pady=(18, 10))
            title_area = tk.Frame(header, bg="#0F172A")
            title_area.pack(side="left", fill="x", expand=True)
            tk.Label(title_area, text="LAUNDRY SERVICE", font=("Arial", 20, "bold"),
                     bg="#0F172A", fg="#F8FAFC").pack(anchor="w")
            tk.Label(title_area, text="Order Management Dashboard", font=("Arial", 10),
                     bg="#0F172A", fg="#94A3B8").pack(anchor="w", pady=(3, 0))
            # Shared Module 4 GUI theme for ttk widgets.
            style = ttk.Style(self.window)
            style.theme_use("clam")
            style.configure("TFrame", background="#0F172A")
            style.configure("TLabelframe", background="#1E293B", foreground="#F8FAFC",
                            bordercolor="#475569")
            style.configure("TLabelframe.Label", background="#1E293B",
                            foreground="#F8FAFC", font=("Arial", 10, "bold"))
            style.configure("TLabel", background="#1E293B", foreground="#F8FAFC",
                            font=("Arial", 10))
            style.configure("TEntry", fieldbackground="#0F172A", foreground="#F8FAFC",
                            insertcolor="#F8FAFC")
            style.configure("TCombobox", fieldbackground="#0F172A", foreground="#F8FAFC",
                            background="#334155", arrowcolor="#F8FAFC")
            style.map("TCombobox", fieldbackground=[("readonly", "#0F172A")],
                      foreground=[("readonly", "#F8FAFC")])
            style.configure("TCheckbutton", background="#1E293B", foreground="#F8FAFC")
            style.map("TCheckbutton", background=[("active", "#1E293B")],
                      foreground=[("active", "#F8FAFC")])
            style.configure("TButton", background="#2563EB", foreground="#FFFFFF",
                            padding=(10, 6), borderwidth=0, font=("Arial", 9, "bold"))
            style.map("TButton", background=[("active", "#1D4ED8")],
                      foreground=[("active", "#FFFFFF")])
            style.configure("Treeview", background="#1E293B", fieldbackground="#1E293B",
                            foreground="#F8FAFC", rowheight=27, bordercolor="#475569")
            style.configure("Treeview.Heading", background="#334155", foreground="#F8FAFC",
                            font=("Arial", 9, "bold"))
            style.map("Treeview", background=[("selected", "#2563EB")],
                      foreground=[("selected", "#FFFFFF")])

            self.orders = load_orders()
            self.customers = load_customers()
            self.service_vars = {s: tk.BooleanVar() for s in SERVICES}

            self.build_form()
            self.build_table()
            tk.Button(self.window, text="Exit", command=self.window.destroy,
                      font=("Arial", 10, "bold"), bg="#334155", fg="#FFFFFF",
                      activebackground="#475569", activeforeground="#FFFFFF",
                      relief="flat", padx=22, pady=8, cursor="hand2").grid(
                          row=2, column=0, columnspan=2, pady=(8, 18))
            self.clear_form()
            self.refresh_table(self.orders.values())

            if not self.customers:
                messagebox.showwarning("No Customers",
                                       "No registered customers found.\n"
                                       "Please register customers in Module 1 first.")

        # ----- layout -----
        def build_form(self):
            form = ttk.LabelFrame(self.window, text="Order Details")
            form.grid(row=1, column=0, padx=(24, 10), pady=10, sticky="n")

            ttk.Label(form, text="Order ID").grid(row=0, column=0, sticky="w", pady=4)
            self.id_entry = ttk.Entry(form, width=25)
            self.id_entry.grid(row=0, column=1, pady=4)

            ttk.Label(form, text="Customer").grid(row=1, column=0, sticky="w", pady=4)
            names = [f"{cid} - {name}" for cid, name in self.customers.items()]
            self.customer_box = ttk.Combobox(form, values=names, state="readonly", width=22)
            self.customer_box.grid(row=1, column=1, pady=4)

            ttk.Label(form, text="Weight (kg)").grid(row=2, column=0, sticky="w", pady=4)
            self.weight_entry = ttk.Entry(form, width=25)
            self.weight_entry.grid(row=2, column=1, pady=4)

            ttk.Label(form, text="Services").grid(row=3, column=0, sticky="nw", pady=4)
            service_frame = ttk.Frame(form)
            service_frame.grid(row=3, column=1, sticky="w")
            for service in SERVICES:
                ttk.Checkbutton(service_frame, text=service,
                                variable=self.service_vars[service]).pack(anchor="w")

            ttk.Label(form, text="Status").grid(row=4, column=0, sticky="w", pady=4)
            self.status_box = ttk.Combobox(form, values=STATUSES, state="readonly", width=22)
            self.status_box.grid(row=4, column=1, pady=4)

            buttons = (("Add", self.add_order), ("Update", self.update_order),
                       ("Delete", self.delete_order), ("Clear", self.clear_form))
            button_frame = ttk.Frame(form)
            button_frame.grid(row=5, column=0, columnspan=2, pady=10)
            for text, command in buttons:
                ttk.Button(button_frame, text=text, command=command, width=8).pack(side="left", padx=3)

        def build_table(self):
            right = ttk.Frame(self.window)
            right.grid(row=1, column=1, padx=(10, 24), pady=10, sticky="nsew")

            # search bar
            search_frame = ttk.Frame(right)
            search_frame.pack(fill="x", pady=(0, 8))
            self.search_by = ttk.Combobox(search_frame, values=("Order ID", "Customer", "Status"),
                                          state="readonly", width=10)
            self.search_by.current(0)
            self.search_by.pack(side="left")
            self.search_entry = ttk.Entry(search_frame, width=20)
            self.search_entry.pack(side="left", padx=5)
            ttk.Button(search_frame, text="Search", command=self.search_orders).pack(side="left")
            ttk.Button(search_frame, text="Show All",
                       command=lambda: self.refresh_table(self.orders.values())).pack(side="left", padx=5)

            # order table
            columns = ("Order ID", "Customer", "Weight (kg)", "Services", "Status", "Created")
            self.table = ttk.Treeview(right, columns=columns, show="headings", height=12)
            for col in columns:
                self.table.heading(col, text=col)
                self.table.column(col, width=110)
            self.table.pack()
            self.table.bind("<<TreeviewSelect>>", self.on_select)

        # ----- helpers -----
        def refresh_table(self, orders_to_show):
            for row in self.table.get_children():
                self.table.delete(row)
            for order in orders_to_show:
                name = self.customers.get(order.customer_id, order.customer_id)
                self.table.insert("", "end", iid=order.record_id,
                                  values=(order.record_id, name, order.weight,
                                          ", ".join(order.services), order.status, order.created))

        def clear_form(self):
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, next_order_id(self.orders))
            self.customer_box.set("")
            self.weight_entry.delete(0, tk.END)
            for var in self.service_vars.values():
                var.set(False)
            self.status_box.set("Pending")

        def read_form(self):
            """Read and validate the form. Raises ValueError if input is wrong."""
            order_id = format_order_id(self.id_entry.get())
            if self.customer_box.get() == "":
                raise ValueError("Please select a registered customer.")
            customer_id = self.customer_box.get().split(" - ")[0]
            try:
                weight = float(self.weight_entry.get())
            except ValueError:
                raise ValueError("Weight must be a number.")
            services = [s for s in SERVICES if self.service_vars[s].get()]
            return order_id, customer_id, weight, services, self.status_box.get()

        def on_select(self, event):
            """Fill the form when a row in the table is clicked."""
            selected = self.table.selection()
            if not selected:
                return
            order = self.orders[selected[0]]
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, order.record_id)
            name = self.customers.get(order.customer_id, "Unknown")
            self.customer_box.set(f"{order.customer_id} - {name}")
            self.weight_entry.delete(0, tk.END)
            self.weight_entry.insert(0, str(order.weight))
            for service in SERVICES:
                self.service_vars[service].set(service in order.services)
            self.status_box.set(order.status)

        # ----- main operations -----
        def add_order(self):
            try:
                order_id, customer_id, weight, services, status = self.read_form()
                if order_id in self.orders:
                    raise ValueError(f"Order {order_id} already exists.")
                self.orders[order_id] = Order(order_id, customer_id, weight, services, status)
                save_orders(self.orders)
            except ValueError as error:
                messagebox.showerror("Invalid Input", str(error))
                return
            except OSError:
                messagebox.showerror("File Error", "Could not save orders.json.")
                return
            self.refresh_table(self.orders.values())
            self.clear_form()
            messagebox.showinfo("Success", f"Order {order_id} added.")

        def update_order(self):
            try:
                order_id, customer_id, weight, services, status = self.read_form()
                if order_id not in self.orders:
                    raise ValueError("Order not found. Click an order in the table first.")
                order = self.orders[order_id]
                order.customer_id = customer_id
                order.weight = weight
                order.services = services
                order.status = status
                save_orders(self.orders)
            except ValueError as error:
                messagebox.showerror("Invalid Input", str(error))
                return
            except OSError:
                messagebox.showerror("File Error", "Could not save orders.json.")
                return
            self.refresh_table(self.orders.values())
            messagebox.showinfo("Success", f"Order {order_id} updated.")

        def delete_order(self):
            order_id = self.id_entry.get().strip().upper()
            if order_id not in self.orders:
                messagebox.showerror("Not Found", "Click an existing order in the table first.")
                return
            if messagebox.askyesno("Confirm", f"Delete order {order_id}?"):
                del self.orders[order_id]
                try:
                    save_orders(self.orders)
                except OSError:
                    messagebox.showerror("File Error", "Could not save orders.json.")
                self.refresh_table(self.orders.values())
                self.clear_form()

        def search_orders(self):
            keyword = self.search_entry.get().strip().lower()
            field = self.search_by.get()
            results = []
            for order in self.orders.values():
                match field:                          # match statement
                    case "Order ID":
                        found = keyword in order.record_id.lower()
                    case "Customer":
                        name = self.customers.get(order.customer_id, "").lower()
                        found = keyword in name or keyword in order.customer_id.lower()
                    case _:                           # Status
                        found = keyword == order.status.lower()
                if found:
                    results.append(order)
            self.refresh_table(results)
            if len(results) == 0:
                messagebox.showinfo("No Result", "No matching orders found.")


    if __name__ == "__main__":
        root = tk.Tk()
        OrderApp(root)
        root.mainloop()

    raise SystemExit(0)

# =================================================================
# MODULE 3: laundry_tracking_module3.py
# =================================================================
if __name__ == "__main__" and sys.argv[1:] == ["--module", 'laundry_tracking_module3.py']:
    # Module 3: Laundry Service Tracking
    # Uses the shared orders.json file created and maintained by Module 2.
    # Concepts: selection, loops, string processing, file processing, collections,
    # functions, encapsulation, inheritance, GUI, exception handling, comments, execution.

    import tkinter as tk
    from tkinter import messagebox, simpledialog
    import json
    import os


    # -------------------- Shared data from Module 2 --------------------
    # Module 3 uses the real orders created and saved by Module 2.
    # Order IDs are not hard-coded in this module.
    ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")

    def load_shared_orders():
        """Load the shared order records saved by Module 2."""
        if not os.path.exists(ORDERS_FILE):
            return []
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as file:
                records = json.load(file)
            if not isinstance(records, list):
                raise ValueError("Invalid orders.json format.")
            return [record for record in records if isinstance(record, dict)]
        except (OSError, json.JSONDecodeError, ValueError) as error:
            messagebox.showerror("File Error", f"Could not load orders.json:\n{error}")
            return []

    def save_shared_orders(orders):
        """Save tracking changes back to the same orders.json used by Module 2."""
        with open(ORDERS_FILE, "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)


    # -------------------- Parent class (Inheritance) --------------------
    class TrackingBase:
        def __init__(self, orders):
            # Encapsulation: store shared orders in a private attribute.
            # The list reference is shared so status changes affect the group data.
            self.__orders = orders

        def get_orders(self):
            # Return shared list so this module can read/update the same order records.
            return self.__orders


    # -------------------- Child class (Inheritance) --------------------
    class LaundryTrackingApp(TrackingBase):
        def __init__(self, orders):
            super().__init__(orders)
            self.root = tk.Tk()
            self.root.title("Laundry Service - Order Tracking")
            self.root.geometry("1100x700")
            self.root.resizable(True, True)
            try:
                self.root.state("zoomed")
            except tk.TclError:
                pass
            self.root.configure(bg="#0F172A")
            self.orders = self.get_orders()

            # Dashboard-style layout: sidebar navigation + main output card.
            sidebar = tk.Frame(self.root, bg="#1E293B", width=270)
            sidebar.pack(side="left", fill="y")
            sidebar.pack_propagate(False)
            tk.Label(sidebar, text="LAUNDRY SERVICE\nTRACKING",
                     font=("Arial", 16, "bold"), bg="#1E293B", fg="#F8FAFC",
                     justify="left").pack(anchor="w", padx=20, pady=(28, 30))

            content = tk.Frame(self.root, bg="#0F172A", padx=28, pady=24)
            content.pack(side="left", fill="both", expand=True)
            header = tk.Frame(content, bg="#0F172A")
            header.pack(fill="x", pady=(0, 18))
            title_area = tk.Frame(header, bg="#0F172A")
            title_area.pack(side="left", fill="x", expand=True)
            tk.Label(title_area, text="Dashboard", font=("Arial", 24, "bold"),
                     bg="#0F172A", fg="#F8FAFC").pack(anchor="w")
            tk.Label(title_area, text="Manage and track laundry orders",
                     font=("Arial", 10), bg="#0F172A", fg="#94A3B8").pack(anchor="w", pady=(4, 0))

            # Figure 1: Main Tracking Menu. Each original operation is retained.
            menu_items = [
                ("1. View All Orders", self.view_all_orders),
                ("2. Search Order", self.search_order),
                ("3. Update Order Status", self.update_order_status),
                ("4. Pending / Completed Orders", self.view_pending_completed),
                ("5. Check Order Progress", self.check_order_progress),
                ("6. Export Tracking Records", self.export_tracking_records),
            ]
            for label, action in menu_items:
                tk.Button(sidebar, text=label, width=25, command=action,
                          bg="#1E293B", fg="#F8FAFC", activebackground="#334155",
                          activeforeground="#FFFFFF", font=("Arial", 10, "bold"),
                          relief="flat", anchor="w", padx=18, pady=12,
                          cursor="hand2").pack(fill="x", padx=8, pady=2)

            tk.Frame(sidebar, bg="#475569", height=1).pack(fill="x", padx=15, pady=18)
            tk.Button(sidebar, text="Exit", width=25, command=self.root.destroy,
                      bg="#334155", fg="#FFFFFF", activebackground="#475569",
                      activeforeground="#FFFFFF", font=("Arial", 10, "bold"),
                      relief="flat", anchor="w", padx=18, pady=12,
                      cursor="hand2").pack(side="bottom", fill="x", padx=8, pady=18)

            output_card = tk.Frame(content, bg="#1E293B", padx=18, pady=18,
                                   highlightthickness=1, highlightbackground="#475569")
            output_card.pack(fill="both", expand=True)
            tk.Label(output_card, text="Tracking Results", font=("Arial", 14, "bold"),
                     bg="#1E293B", fg="#F8FAFC").pack(anchor="w", pady=(0, 12))
            self.output = tk.Text(output_card, height=10, width=60, wrap="word",
                                  bg="#0F172A", fg="#F8FAFC",
                                  insertbackground="#F8FAFC",
                                  font=("Arial", 10), relief="flat",
                                  padx=12, pady=10,
                                  highlightthickness=1, highlightbackground="#475569")
            self.output.pack(fill="both", expand=True)

            # -------------------- Dashboard Input Controls --------------------
            # All Module 3 inputs stay inside this dashboard; no extra dialog windows.
            controls = tk.Frame(content, bg="#1E293B", padx=18, pady=12,
                                highlightthickness=1, highlightbackground="#475569")
            controls.pack(fill="x", pady=(0, 12), before=output_card)

            tk.Label(controls, text="Order ID", bg="#1E293B", fg="#F8FAFC",
                     font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8))
            self.order_id_entry = tk.Entry(controls, width=22, font=("Arial", 10),
                                           bg="#0F172A", fg="#F8FAFC",
                                           insertbackground="#F8FAFC", relief="flat")
            self.order_id_entry.grid(row=0, column=1, sticky="ew", ipady=7, padx=(0, 12))

            tk.Label(controls, text="Status", bg="#1E293B", fg="#F8FAFC",
                     font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="w", padx=(0, 8))
            self.status_var = tk.StringVar(value="Pending")
            self.status_menu = tk.OptionMenu(controls, self.status_var, "Pending", "Completed")
            self.status_menu.configure(bg="#334155", fg="#FFFFFF", activebackground="#475569",
                                       activeforeground="#FFFFFF", relief="flat", highlightthickness=0)
            self.status_menu["menu"].configure(bg="#1E293B", fg="#FFFFFF")
            self.status_menu.grid(row=0, column=3, sticky="ew", padx=(0, 12))

            tk.Button(controls, text="Search", command=self.search_order,
                      bg="#2563EB", fg="#FFFFFF", activebackground="#1D4ED8",
                      relief="flat", padx=14, pady=7, cursor="hand2").grid(row=0, column=4, padx=3)
            tk.Button(controls, text="Update Status", command=self.update_order_status,
                      bg="#16A34A", fg="#FFFFFF", activebackground="#15803D",
                      relief="flat", padx=14, pady=7, cursor="hand2").grid(row=0, column=5, padx=3)
            tk.Button(controls, text="Filter Status", command=self.view_pending_completed,
                      bg="#475569", fg="#FFFFFF", activebackground="#64748B",
                      relief="flat", padx=14, pady=7, cursor="hand2").grid(row=0, column=6, padx=3)
            tk.Button(controls, text="Check Progress", command=self.check_order_progress,
                      bg="#475569", fg="#FFFFFF", activebackground="#64748B",
                      relief="flat", padx=14, pady=7, cursor="hand2").grid(row=0, column=7, padx=3)
            controls.columnconfigure(1, weight=1)

        # -------------------- Shared Data Refresh --------------------
        def refresh_orders(self):
            """Refresh the latest shared orders so changes from other modules appear."""
            self.orders = load_shared_orders()

        # -------------------- String Processing --------------------
        def clean_text(self, text):
            # Normalize input: remove surrounding spaces and make consistent case.
            return text.strip().upper()

        def format_order(self, order):
            services = ", ".join(order.get("services", []))
            return (
                f"Order ID: {order.get('order_id', 'N/A')}\n"
                f"Customer ID: {order.get('customer_id', 'N/A')}\n"
                f"Weight: {order.get('weight', 'N/A')} kg\n"
                f"Services: {services or 'N/A'}\n"
                f"Status: {order.get('status', 'N/A')}\n"
                "------------------------------"
            )

        def display_text(self, text):
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, text)

        # -------------------- Figure 2: View All Orders --------------------
        def view_all_orders(self):
            self.refresh_orders()
            if not self.orders:
                self.display_text("No Orders Available.")
                return

            lines = []
            # Loop through the collection (list of dictionaries).
            for order in self.orders:
                lines.append(self.format_order(order))
            self.display_text("\n".join(lines))

        # -------------------- Figure 3: Search Order --------------------
        def search_order(self):
            self.refresh_orders()
            search_id = self.clean_text(self.order_id_entry.get())
            if not search_id:
                self.display_text("Please enter an Order ID in the dashboard input field.")
                self.order_id_entry.focus_set()
                return

            # Linear search through the shared orders list.
            for order in self.orders:
                if self.clean_text(str(order.get("order_id", ""))) == search_id:
                    self.display_text(self.format_order(order))
                    return
            self.display_text("Order Not Found.")

        # -------------------- Figure 4: Update Order Status --------------------
        def update_order_status(self):
            self.refresh_orders()
            search_id = self.clean_text(self.order_id_entry.get())
            if not search_id:
                self.display_text("Please enter an Order ID before updating its status.")
                self.order_id_entry.focus_set()
                return

            target_order = None
            for order in self.orders:
                if self.clean_text(str(order.get("order_id", ""))) == search_id:
                    target_order = order
                    break

            if target_order is None:
                self.display_text("Order Not Found. Status was not changed.")
                return

            new_status = self.status_var.get().strip().title()
            # Selection: only accept the two assignment status values.
            if new_status not in ("Pending", "Completed"):
                self.display_text("Invalid Status. Select Pending or Completed.")
                return

            old_status = target_order.get("status", "N/A")
            target_order["status"] = new_status
            try:
                save_shared_orders(self.orders)
            except (OSError, TypeError, ValueError) as error:
                # Roll back the in-memory change if saving fails.
                target_order["status"] = old_status
                self.display_text(f"Could not save orders.json. Status was not changed.\n{error}")
                return

            self.display_text(
                f"Status Updated Successfully!\nPrevious Status: {old_status}\n"
                f"New Status: {new_status}\n\n{self.format_order(target_order)}"
            )

        # -------------------- Figure 5: Pending / Completed Orders --------------------
        def view_pending_completed(self):
            self.refresh_orders()
            selected_status = self.status_var.get().strip().title()
            if selected_status not in ("Pending", "Completed"):
                self.display_text("Select Pending or Completed from the Status menu.")
                return

            lines = []
            # Display every order that matches the selected status.
            for order in self.orders:
                if str(order.get("status", "")).strip().title() == selected_status:
                    lines.append(self.format_order(order))

            if lines:
                self.display_text(f"{selected_status} Orders\n\n" + "\n".join(lines))
            else:
                self.display_text(f"No {selected_status} Orders.")

        # -------------------- Figure 6: Check Order Progress --------------------
        def check_order_progress(self):
            self.refresh_orders()
            search_id = self.clean_text(self.order_id_entry.get())
            if not search_id:
                self.display_text("Please enter an Order ID to check its progress.")
                self.order_id_entry.focus_set()
                return

            for order in self.orders:
                if self.clean_text(str(order.get("order_id", ""))) == search_id:
                    status = str(order.get("status", "N/A")).strip().title()
                    if status == "Pending":
                        progress_message = "Order is Still Pending."
                    elif status == "Completed":
                        progress_message = "Order is Completed."
                    else:
                        progress_message = f"Unknown order status: {status}"

                    self.display_text(
                        f"Order ID: {order.get('order_id', 'N/A')}\n"
                        f"Customer ID: {order.get('customer_id', 'N/A')}\n"
                        f"Current Status: {status}\n\n{progress_message}"
                    )
                    return

            self.display_text("Order Not Found.")

        # -------------------- File Processing --------------------
        def export_tracking_records(self):
            self.refresh_orders()
            # Export a snapshot of the latest shared orders from orders.json.
            filename = "tracking_report.json"
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(self.orders, file, indent=4, ensure_ascii=False)
                messagebox.showinfo(
                    "Export Successful",
                    f"Tracking records exported to {filename}"
                )
            except (OSError, TypeError) as error:
                messagebox.showerror("File Error", f"Could not export records:\n{error}")


    # -------------------- Execution --------------------
    def main():
        try:
            app = LaundryTrackingApp(load_shared_orders())
            app.root.mainloop()
        except tk.TclError as error:
            print("GUI could not start:", error)


    if __name__ == "__main__":
        main()

    raise SystemExit(0)

# =================================================================
# MODULE 4: module_4.py
# =================================================================
if __name__ == "__main__" and sys.argv[1:] == ["--module", 'module_4.py']:
    import tkinter as tk
    import json
    import os

    # GUI Colour Settings
    BG_COLOR = "#0F172A"
    CARD_COLOR = "#1E293B"
    TEXT_COLOR = "#F8FAFC"
    MUTED_COLOR = "#94A3B8"
    BLUE_COLOR = "#2563EB"
    SUCCESS_COLOR = "#22C55E"
    ERROR_COLOR = "#EF4444"

    # ==========================================
    # 1. Payment Calculator - Core Logic
    # ==========================================

    class PaymentCalculator:

        def __init__(self):
            self.__service_rates = {
                "Washing": 2.00,
                "Drying": 1.00,
                "Ironing": 1.50
            }

            # Read the same order file created and maintained by Module 2.
            self.__orders_file = os.path.join(BASE_DIR, "orders.json")
            self.__file_name = os.path.join(BASE_DIR, "payment_records.json")

        def load_orders(self):
            """Load the latest orders from Module 2's shared orders.json file."""
            if not os.path.exists(self.__orders_file):
                return {}

            try:
                with open(self.__orders_file, "r", encoding="utf-8") as file:
                    saved_orders = json.load(file)
            except json.JSONDecodeError:
                raise ValueError("orders.json is damaged or has an invalid format.")
            except OSError as error:
                raise ValueError(f"Unable to read orders.json: {error}")

            if not isinstance(saved_orders, list):
                raise ValueError("Invalid orders.json format.")

            orders = {}
            for order in saved_orders:
                if not isinstance(order, dict):
                    continue
                order_id = str(order.get("order_id", "")).strip().upper()
                if order_id:
                    orders[order_id] = order
            return orders

        def update_shared_order_details(self, order_id, weight, services):
            """Update weight/services in Module 2's orders.json, preserving other fields."""
            if not os.path.exists(self.__orders_file):
                raise ValueError("orders.json was not found. Create the order in Module 2 first.")

            try:
                with open(self.__orders_file, "r", encoding="utf-8") as file:
                    saved_orders = json.load(file)
            except json.JSONDecodeError:
                raise ValueError("orders.json is damaged or has an invalid format.")
            except OSError as error:
                raise ValueError(f"Unable to read orders.json: {error}")

            if not isinstance(saved_orders, list):
                raise ValueError("Invalid orders.json format.")

            target = None
            for saved_order in saved_orders:
                if (isinstance(saved_order, dict)
                        and str(saved_order.get("order_id", "")).strip().upper() == order_id):
                    target = saved_order
                    break

            if target is None:
                raise KeyError("Order ID not found in orders.json.")

            target["weight"] = weight
            target["services"] = list(services)

            try:
                with open(self.__orders_file, "w", encoding="utf-8") as file:
                    json.dump(saved_orders, file, indent=4, ensure_ascii=False)
            except OSError as error:
                raise ValueError(f"Unable to update orders.json: {error}")

        def save_updated_records(self, records):
            with open(self.__file_name, "w") as file:
                json.dump(records, file, indent=4)

        def get_service_rate(self, service):
            return self.__service_rates[service]

        # Calculate payment
        def calculate_payment(self, order_id):

            order_id = order_id.strip().upper()

            if not order_id:
                raise ValueError("Order ID cannot be empty.")

            # Follow Module 2's format: O followed by one or more digits.
            if (len(order_id) < 2
                    or not order_id.startswith("O")
                    or not order_id[1:].isdigit()):
                raise ValueError("Order ID invalid.")

            # Refresh from orders.json every time so new/updated Module 2
            # orders are available without maintaining a second order list.
            self.__orders = self.load_orders()
            if order_id not in self.__orders:
                raise KeyError("Order ID not found.")

            order = self.__orders[order_id]

            try:
                weight = float(order["weight"])
                services = order["services"]
            except (KeyError, TypeError, ValueError):
                raise ValueError("The selected order has incomplete order details.")

            if weight <= 0 or not isinstance(services, list) or not services:
                raise ValueError("The selected order has invalid weight or services.")

            total_amount = 0
            service_charges = []

            for service in services:

                if service not in self.__service_rates:
                    raise ValueError("Invalid service found.")

                charge = self.__service_rates[service] * weight

                total_amount += charge

                service_charges.append({
                    "service": service,
                    "charge": charge
                })

            return order_id, weight, service_charges, total_amount

        # Load payment records from JSON
        def load_payment_records(self):

            if not os.path.exists(self.__file_name):
                return []

            try:
                with open(self.__file_name, "r") as file:
                    records = json.load(file)

            except json.JSONDecodeError:
                raise ValueError("Payment records file is corrupted.")

            if not isinstance(records, list):
                raise ValueError("Invalid payment records format.")

            # Reconcile older payment snapshots with the latest shared order data.
            # This prevents Module 4 history from showing a different KG/services
            # after the order was changed in Module 2 or Module 4.
            shared_orders = self.load_orders()
            changed = False
            for record in records:
                if not isinstance(record, dict):
                    continue
                order_id = str(record.get("order_id", "")).strip().upper()
                order = shared_orders.get(order_id)
                if not order:
                    continue
                try:
                    weight = float(order["weight"])
                    services = order["services"]
                    if weight <= 0 or not isinstance(services, list) or not services:
                        continue
                    charges = []
                    total = 0.0
                    for service in services:
                        if service not in self.__service_rates:
                            raise ValueError("Invalid service found in orders.json.")
                        charge = self.__service_rates[service] * weight
                        total += charge
                        charges.append({"service": service, "charge": charge})
                except (KeyError, TypeError, ValueError):
                    continue

                if (record.get("weight") != weight
                        or record.get("services") != charges
                        or record.get("total_payment") != total):
                    record["weight"] = weight
                    record["services"] = charges
                    record["total_payment"] = total
                    changed = True

            if changed:
                with open(self.__file_name, "w", encoding="utf-8") as file:
                    json.dump(records, file, indent=4)

            return records

        # Save payment record into JSON
        def save_payment_record(self, record):

            records = self.load_payment_records()

            index = 0

            while index < len(records):
                existing_record = records[index]

                if existing_record.get("order_id") == record["order_id"]:
                    raise ValueError("Payment record already exists.")

                index += 1

            records.append(record)

            with open(self.__file_name, "w") as file:
                json.dump(records, file, indent=4)


    # ==========================================
    # 2. Payment Calculator GUI - User Interface
    # ==========================================

    class PaymentCalculatorGUI(tk.Frame):
        def __init__(self, root):
            root.configure(bg=BG_COLOR)
            super().__init__(root, padx=30, pady=25,  bg=BG_COLOR)

            self.root = root
            self.root.title("Laundry Service - Payment Calculator")
            self.root.geometry("1100x700")
            self.root.resizable(True, True)
            try:
                self.root.state("zoomed")
            except tk.TclError:
                pass
            self.pack(fill="both", expand=True)

            # Header
            self.header_frame = tk.Frame(self,bg=BG_COLOR)
            self.header_frame.pack(fill="x",pady=(0, 25))
            self.header_text_frame = tk.Frame(self.header_frame, bg=BG_COLOR)
            self.header_text_frame.pack(side="left", fill="x", expand=True)

            self.title_label = tk.Label(
            self.header_text_frame,
            text="LAUNDRY SERVICE",
            font=("Arial", 22, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
            )
            self.title_label.pack(anchor="w")

            self.subtitle_label = tk.Label(
            self.header_text_frame,
            text="Payment Management Dashboard",
            font=("Arial", 10),
            bg=BG_COLOR,
            fg=MUTED_COLOR
            )
            self.subtitle_label.pack(anchor="w", pady=(5, 0))

            self.exit_button = tk.Button(
                self.header_frame,
                text="Exit",
                font=("Arial", 10, "bold"),
                bg="#334155",
                fg=TEXT_COLOR,
                activebackground="#475569",
                activeforeground=TEXT_COLOR,
                relief="flat",
                padx=20,
                pady=8,
                cursor="hand2",
                command=self.root.destroy
            )
            self.exit_button.pack(side="right", anchor="ne")

            self.calculator = PaymentCalculator()

            # Main Area
            self.main_area = tk.Frame(self,bg=BG_COLOR)
            self.main_area.pack(fill="both", expand=True)


            # Left Column
            self.left_column = tk.Frame(
                 self.main_area,
                 bg=BG_COLOR
            )
            self.left_column.pack(side="left", fill="both", expand=True,padx=(0, 10))


            # Right Column
            self.right_column = tk.Frame(
                 self.main_area,
                 bg=BG_COLOR
            )
            self.right_column.pack(side="right", fill="both", expand=True,padx=(10, 0))

            #Calculator Card
            self.input_frame = tk.Frame(
            self.left_column,
            bg=CARD_COLOR,
            padx=20,
            pady=20
            )
            self.input_frame.pack(fill="x",pady=(0, 20))

            self.calculator_title = tk.Label(
            self.input_frame,
            text="Payment Calculator",
            font=("Arial", 15, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
            )

            self.calculator_title.pack(anchor="w", pady=(0, 15))

            # Input Area
            self.input_area = tk.Frame(
            self.input_frame,
            bg=CARD_COLOR
            )
            self.input_area.pack(fill="x")

            # Order ID Label
            self.order_label = tk.Label(
            self.input_area,
            text="Enter Order ID:",
            font=("Arial", 11),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
            )

            self.order_label.grid(row=0, column=0, padx=5)

            # Order ID Entry
            self.order_entry = tk.Entry(
                self.input_area,
                font=("Arial", 11),
                width=20,
                bg="#0F172A",
                fg=TEXT_COLOR,
                insertbackground=TEXT_COLOR,
                relief="flat",
                bd=0,
                highlightthickness=1,
                highlightbackground="#475569",
                highlightcolor=BLUE_COLOR
            )
            self.order_entry.grid(row=0, column=1, padx=5,pady=5,sticky="w")

            self.error_label = tk.Label(
                self.input_area,
                text="",
                font=("Arial", 9),
                fg="red",
                bg=CARD_COLOR,
                bd=0,
                highlightthickness=0,
                anchor="e"
            )

            self.error_label.grid(
                row=1,
                column=1,
                sticky="e",
                padx=5
            )

            # Calculate Button
            self.calculate_button = tk.Button(
                self.input_area,
                text="Calculate",
                font=("Arial", 10, "bold"),
                width=13,
                bg=BLUE_COLOR,
                fg=TEXT_COLOR,
                activebackground="#1D4ED8",
                activeforeground=TEXT_COLOR,
                command=self.calculate
            )
            self.calculate_button.grid(row=0, column=2, padx=5, pady=5)

            # Search Button
            self.search_button = tk.Button(
                self.input_area,
                text="Search",
                font=("Arial", 10, "bold"),
                width=10,
                bg="#334155",
                fg=TEXT_COLOR,
                activebackground="#475569",
                activeforeground=TEXT_COLOR,
                command=self.search_record
            )
            self.search_button.grid(row=0, column=3, padx=5, pady=5)

            # Payment Result Card
            self.result_frame = tk.Frame(
            self.left_column,
            bg=CARD_COLOR,
            padx=20,
            pady=20
            )
            self.result_frame.pack(
            fill="x",
            pady=(0, 20)
            )

            # Result Title
            self.result_title = tk.Label(
            self.result_frame,
            text="Payment Result",
            font=("Arial", 15, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
            )
            self.result_title.pack(anchor="w", pady=(0, 15))

            # Result Label
            self.result_label = tk.Label(
            self.result_frame,
            text="Payment result will appear here.",
            font=("Arial", 11),
            justify="left",
            anchor="w",
            bg=CARD_COLOR,
            fg=TEXT_COLOR
            )
            self.result_label.pack(anchor="w")

            #Clear button
            self.clear_button = tk.Button(
                self.result_frame,
                text="Clear Result",
                font=("Arial", 11, "bold"),
                width=12,
                bg="#334155",
                fg=TEXT_COLOR,
                activebackground="#475569",
                activeforeground=TEXT_COLOR,
                command=self.clear_result
            )
            self.clear_button.pack(anchor="w", pady=10)

            # Payment History Card
            self.history_frame = tk.Frame(
            self.left_column,
            bg=CARD_COLOR,
            padx=20,
            pady=20 
            )
            self.history_frame.pack(fill="x",pady=(0, 20))

            # Update Payment Card
            self.update_frame = tk.Frame(
                self.right_column,
                bg=CARD_COLOR,
                padx=20,
                pady=20
            )
            self.update_frame.pack(fill="x", pady=(0, 20))

            # Update Payment Title
            self.update_title = tk.Label(
                self.update_frame,
                text="Update Payment",
                font=("Arial", 14, "bold"),
                bg=CARD_COLOR,
                fg=TEXT_COLOR
            )
            self.update_title.pack(anchor="w", pady=(0, 5))

            # Update Input Area
            self.update_input_area = tk.Frame(
                 self.update_frame,
                 bg=CARD_COLOR
                 )
            self.update_input_area.pack(fill="x")

            # Update Order ID Entry
            self.update_id_entry = tk.Entry(
                self.update_input_area,
                font=("Arial", 11),
                width=20,
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                insertbackground=TEXT_COLOR,
                relief="flat",
                bd=0,
                highlightthickness=1,
                highlightbackground="#475569",
                highlightcolor=BLUE_COLOR
            )
            self.update_id_entry.grid(row=0, column=0, padx=5, pady=5)

            # Update Button
            self.update_button = tk.Button(
                self.update_input_area,
                text="Update",
                font=("Arial", 10, "bold"),
                width=13,
                bg=BLUE_COLOR,
                fg=TEXT_COLOR,
                activebackground="#1D4ED8",
                activeforeground=TEXT_COLOR,
                command=self.search_update_record
            )
            self.update_button.grid(row=0, column=1, padx=5, pady=5)


            # Update Error Label
            self.update_error_label = tk.Label(
                self.update_frame,
                text="",
                font=("Arial", 9),
                bg=CARD_COLOR,
                fg=ERROR_COLOR
            )
            self.update_error_label.pack(anchor="w", padx=5, pady=5)

            # Edit Payment Details Frame
            self.edit_frame = tk.Frame(
                self.update_frame,
                bg=CARD_COLOR,
                padx=5,
                pady=10
            )

            # Edit Payment Details Title
            self.edit_title = tk.Label(
                self.edit_frame,
                text="Edit Payment Details",
                font=("Arial", 12, "bold"),
                bg=CARD_COLOR,
                fg=TEXT_COLOR
            )
            self.edit_title.pack(anchor="w", pady=(5, 10))

            # Weight Input Area
            self.weight_area = tk.Frame(
                 self.edit_frame,
                 bg=CARD_COLOR
                 )
            self.weight_area.pack(fill="x", pady=5)


            # Weight Label
            self.weight_label = tk.Label(
                 self.weight_area,
                 text="Weight (kg)",
                 font=("Arial", 11),
                 bg=CARD_COLOR,
                 fg=TEXT_COLOR
            )
            self.weight_label.grid(row=0, column=0, padx=5, pady=5)


            # Weight Entry
            self.weight_entry = tk.Entry(
                 self.weight_area,
                 font=("Arial", 11),
                 width=10,
                 bg=BG_COLOR,
                 fg=TEXT_COLOR,
                 insertbackground=TEXT_COLOR,
                 relief="flat",
                 bd=0
            )
            self.weight_entry.grid(row=0, column=1, padx=10, pady=5)


            # Services Area
            self.services_area = tk.Frame(
                 self.edit_frame,
                 bg=CARD_COLOR
            )
            self.services_area.pack(fill="x", pady=10)


            # Services Title
            self.services_title = tk.Label(
                 self.services_area,
                 text="Services",
                 font=("Arial", 11, "bold"),
                 bg=CARD_COLOR,
                 fg=TEXT_COLOR
            )
            self.services_title.pack(anchor="w", padx=5, pady=5)

            self.washing_var = tk.BooleanVar(value=False)
            self.drying_var = tk.BooleanVar(value=False)
            self.ironing_var = tk.BooleanVar(value=False)

            # Washing Checkbutton
            self.washing_check = tk.Checkbutton(
                 self.services_area,
                 text="Washing",
                 variable=self.washing_var,
                 font=("Arial", 10),
                 bg=CARD_COLOR,
                 fg=TEXT_COLOR,
                 selectcolor=BG_COLOR,
                 activebackground=CARD_COLOR,
                 activeforeground=TEXT_COLOR
            )
            self.washing_check.pack(anchor="w", padx=10, pady=2)

            self.drying_check = tk.Checkbutton(
                         self.services_area,
                         text="Drying",
                         variable=self.drying_var,
                         font=("Arial", 10),
                         bg=CARD_COLOR,
                         fg=TEXT_COLOR,
                         selectcolor=BG_COLOR,
                         activebackground=CARD_COLOR,
                         activeforeground=TEXT_COLOR
                    )
            self.drying_check.pack(anchor="w", padx=10, pady=2)

            self.ironing_check = tk.Checkbutton(
                         self.services_area,
                         text="Ironing",
                         variable=self.ironing_var,
                         font=("Arial", 10),
                         bg=CARD_COLOR,
                         fg=TEXT_COLOR,
                         selectcolor=BG_COLOR,
                         activebackground=CARD_COLOR,
                         activeforeground=TEXT_COLOR
                    )
            self.ironing_check.pack(anchor="w", padx=10, pady=2)

            # Save Changes Button
            self.save_changes_button = tk.Button(
                 self.edit_frame,
                 text="Save Changes",
                 font=("Arial", 10, "bold"),
                 width=15,
                 bg=BLUE_COLOR,
                 fg=TEXT_COLOR,
                 activebackground="#1D4ED8",
                 activeforeground=TEXT_COLOR,
                 command=self.save_updated_record
            )
            self.save_changes_button.pack(anchor="w", pady=10)



            # History Title
            self.history_title = tk.Label(
            self.history_frame,
            text="Payment History",
            font=("Arial", 15, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
            )
            self.history_title.pack(anchor="w",pady=(0, 15))

            # View Records Button
            self.records_button = tk.Button(
            self.history_frame,
            text="View Payment Records",
            font=("Arial", 10, "bold"),
            bg=BLUE_COLOR,
            fg=TEXT_COLOR,
            activebackground="#1D4ED8",
            activeforeground=TEXT_COLOR,
            command=self.view_records
            )
            self.records_button.pack(anchor="w",pady=(0, 15))

            # History Text Area
            self.history_text = tk.Text(
            self.history_frame,
            height=8,
            width=65,
            font=("Consolas", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0,
            padx=10,
            pady=10
            )
            self.history_text.pack(fill="x")

            # All module windows use the same fixed 1100 x 700 dimensions.
        
        # Calculate Button Function
        def calculate(self):

            order_id = self.order_entry.get()
            self.error_label.config(text="")

            try:
                order_id, weight, charges, total = (
                    self.calculator.calculate_payment(order_id)
                )

                # Create payment record
                record = {
                    "order_id": order_id,
                    "weight": weight,
                    "services": charges,
                    "total_payment": total
                }

                # Save record into JSON
                self.calculator.save_payment_record(record)

            except ValueError as error:
                self.error_label.config(text=str(error))

            except KeyError:
                self.error_label.config(text="Order ID does not exist.")

            else:

                result = f"Order ID: {order_id}\n"
                result += f"Weight: {weight} KG\n\n"

                for item in charges:
                    result += (
                        f"{item['service']}: "
                        f"RM{item['charge']:.2f}\n"
                    )

                result += f"\nTotal Payment: RM{total:.2f}"
                result += "\n\nPayment record saved successfully."

                self.result_label.config(text=result)

                # Clear Order ID Entry
                self.order_entry.delete(0, tk.END)

                # Refresh payment history
                self.view_records()

        # View Payment Records Function
        def view_records(self):

            try:
                records = self.calculator.load_payment_records()

            except ValueError as error:

                self.history_text.delete("1.0", tk.END)
                self.history_text.insert(
                    tk.END,
                    f"File Error: {error}"
                )
                return

            self.history_text.delete("1.0", tk.END)

            if not records:
                self.history_text.insert(
                    tk.END,
                    "No payment records found."
                )
                return

            for record in records:

                self.history_text.insert(
                    tk.END,
                    f"Order ID: {record.get('order_id', 'N/A')}\n"
                )

                self.history_text.insert(
                    tk.END,
                    f"Weight: {record.get('weight', 'N/A')} KG\n"
                )

                self.history_text.insert(
                    tk.END,
                    "\nServices:\n"
                    )

                for item in record.get("services", []):
                    service_name = item.get("service", "N/A")
                    charge = item.get("charge", 0)

                    self.history_text.insert(
                        tk.END,
                        f"- {service_name}: RM{charge:.2f}\n"
                        )

                self.history_text.insert(
                    tk.END,
                    f"Total Payment: RM"
                    f"{record.get('total_payment', 0):.2f}\n"
                )

                self.history_text.insert(
                    tk.END,
                    "------------------------------\n"
                )

        #Clear result function       
        def clear_result(self):
            self.result_label.config(
            text="Payment result will appear here."
        )
        #Search record function
        def search_record(self):

            # Get Order ID
            order_id = self.order_entry.get().strip().upper()

            # Load payment records
            try:
                records = self.calculator.load_payment_records()

            except ValueError as error:
                self.error_label.config(text=str(error))
                return

            # Search records
            for record in records:
              if record.get("order_id") == order_id:
                self.display_record(record)
                self.order_entry.delete(0, tk.END)
                return

            # Record not found
            self.error_label.config(text="Record not found.")

        def display_record(self, record):
            order_id = record.get("order_id")
            weight = record.get("weight")
            total = record.get("total_payment")
            services = record.get("services")
            service_text = ""

            for service in services:
                name = service.get("service")
                charge = service.get("charge")
                service_text += f"{name}: RM{charge:.2f}\n"

            result = (  
                f"Order ID: {order_id}\n"
                f"Weight: {weight} kg\n"
                f"{service_text}"
                f"Total Payment: RM{total:.2f}"
            )

            self.result_label.config(text=result)
            self.error_label.config(text="")

        def search_update_record(self):
            self.edit_frame.pack_forget()
            # Get Order ID
            order_id = self.update_id_entry.get().strip().upper()

            # Load Existing Payment Records
            try:
                records = self.calculator.load_payment_records()

            except ValueError as error:
                self.update_error_label.config(text=str(error))
                return

            # Search the payment record, then get the authoritative order details
            # from Module 2's shared orders.json file.
            for record in records:
                if record.get("order_id") == order_id:
                    try:
                        shared_order = self.calculator.load_orders().get(order_id)
                        if shared_order is None:
                            raise KeyError("Order ID not found in orders.json.")
                        weight = shared_order["weight"]
                        services = shared_order["services"]
                    except (KeyError, TypeError) as error:
                        self.update_error_label.config(text=str(error), fg=ERROR_COLOR)
                        return

                    self.update_error_label.config(text="")
                    self.edit_frame.pack(fill="x")

                    # Fill from the latest shared order, not an old payment snapshot.
                    self.weight_entry.delete(0, tk.END)
                    self.weight_entry.insert(0, str(weight))

                    self.washing_var.set("Washing" in services)
                    self.drying_var.set("Drying" in services)
                    self.ironing_var.set("Ironing" in services)
                    return

            # Record Not Found
            self.update_error_label.config(text="Record not found.", fg=ERROR_COLOR)

        def save_updated_record(self):
            # Get Updated Weight
            weight = self.weight_entry.get()

            # Get Selected Services
            services = []

            if self.washing_var.get():
                services.append("Washing")

            if self.drying_var.get():
                services.append("Drying")

            if self.ironing_var.get():
                services.append("Ironing")

            # Validate Weight
            try:
                weight = float(weight)

                if weight <= 0:
                    raise ValueError("Weight must be greater than 0.")

            except ValueError:
                self.update_error_label.config(text="Invalid weight.")
                return

            # Validate Services
            if not services:
                self.update_error_label.config(
                    text="Please select at least one service."
                )
                return

            # Recalculate Payment
            total_amount = 0
            service_charges = []

            for service in services:
                # Get Service Rate
                rate = self.calculator.get_service_rate(service)

                # Calculate Individual Charge
                charge = weight * rate

                # Add to Total
                total_amount += charge

                # Store Service Details
                service_charges.append({
                    "service": service,
                    "charge": charge
            })
            order_id = self.update_id_entry.get().strip().upper()
            try:
                # Keep Module 2, Module 3 and Module 4 on the same weight/services.
                self.calculator.update_shared_order_details(order_id, weight, services)
                records = self.calculator.load_payment_records()

            except (ValueError, KeyError) as error:
                self.update_error_label.config(text=str(error),fg=ERROR_COLOR)
                return
        
            for record in records:
                if record["order_id"] == order_id:
                    # Update this record
                    record["weight"] = weight
                    record["services"] = service_charges
                    record["total_payment"] = total_amount

                    # Save Updated Records
                    try:
                        self.calculator.save_updated_records(records)

                    except OSError as error:
                        self.update_error_label.config(text=str(error), fg=ERROR_COLOR)
                        return

                    # Update GUI
                    self.update_error_label.config(text="")

                    self.display_record(record)
                    self.view_records()

                    self.update_error_label.config(
                        text="Payment record updated successfully.",
                        fg=SUCCESS_COLOR
                    )

                    break


    # ==========================================
    # 3. Main Program
    # ==========================================

    def main():

        root = tk.Tk()

        app = PaymentCalculatorGUI(root)

        root.mainloop()


    main()

    raise SystemExit(0)

# MODULE 5: REPORTING AND MAIN MENU
import os
import sys
import subprocess
import json
import tkinter as tk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES = [
    ("Module 1  |  Customer Management", "module1.py"),
    ("Module 2  |  Laundry Order Management", "module2.py"),
    ("Module 3  |  Laundry Service Tracking", "laundry_tracking_module3.py"),
    ("Module 4  |  Payment Calculator", "module_4.py"),
]

# Exact palette from Module 4
BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
TEXT_COLOR = "#F8FAFC"
MUTED_COLOR = "#94A3B8"
BLUE_COLOR = "#2563EB"
SUCCESS_COLOR = "#22C55E"
ERROR_COLOR = "#EF4444"
BORDER_COLOR = "#475569"
ACTIVE_BLUE = "#1D4ED8"


def launch_module(filename):
    try:
        subprocess.Popen([sys.executable, os.path.abspath(__file__), "--module", filename], cwd=BASE_DIR)
    except OSError as err:
        messagebox.showerror("Launch Error", str(err))


def open_reporting_module():
    # Read the saved data files
    def read_json(filename):
        path = os.path.join(BASE_DIR, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []

    customers = 0
    try:
        path = os.path.join(BASE_DIR, 'customers.txt')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip() and len(line.strip().split(',')) == 4:
                        customers += 1
        orders = read_json('orders.json')
        payments = read_json('payment_records.json')
        pending = 0
        completed = 0
        revenue = 0
        for order in orders:
            status = str(order.get('status', 'Pending')).strip().lower()
            if status == 'pending':
                pending += 1
            elif status == 'completed':
                completed += 1
        for payment in payments:
            revenue += float(payment.get('total_payment', 0) or 0)
    except (OSError, ValueError, TypeError, AttributeError) as error:
        messagebox.showerror('Report Error', str(error))
        return

    total = len(orders)
    rate = 0
    if total > 0:
        rate = completed / total * 100

    # Create the black and white reporting window
    report = tk.Toplevel(root)
    report.title('Summary & Reporting')
    report.geometry('1100x700')
    report.resizable(True, True)
    try:
        report.state("zoomed")
    except tk.TclError:
        pass
    report.configure(bg=BG_COLOR)

    def heading(text):
        tk.Label(report, text=text, bg=BG_COLOR, fg=TEXT_COLOR,
                 font=('Arial', 15, 'bold')).pack(anchor='w', padx=20, pady=10)

    heading('SUMMARY & REPORTING')
    summary = [
        ('Total Registered Customers', customers),
        ('Total Orders', total),
        ('Pending Orders', pending),
        ('Completed Orders', completed),
        ('Total Revenue Recorded', f'RM {revenue:.2f}')
    ]
    for name, value in summary:
        row = tk.Frame(report, bg=BG_COLOR)
        row.pack(fill='x', padx=20)
        tk.Label(row, text=name, bg=BG_COLOR, fg=TEXT_COLOR, font=('Arial', 11)).pack(side='left')
        tk.Label(row, text=value, bg=BG_COLOR, fg=TEXT_COLOR, font=('Arial', 11, 'bold')).pack(side='right')

    # Simple bar chart using Tkinter Canvas
    heading('ORDER STATUS OVERVIEW')
    chart = tk.Canvas(report, width=500, height=95, bg=BG_COLOR, highlightthickness=0)
    chart.pack(anchor='w', padx=20)
    for name, count, y in [('Completed', completed, 5), ('Pending', pending, 35)]:
        chart.create_text(0, y + 10, text=name, fill=TEXT_COLOR, anchor='w')
        chart.create_rectangle(100, y, 400, y + 20, fill=CARD_COLOR, outline='')
        if total > 0 and count > 0:
            chart.create_rectangle(100, y, 100 + 300 * count / total, y + 20,
                                   fill=TEXT_COLOR, outline='')
        chart.create_text(415, y + 10, text=str(count), fill=TEXT_COLOR, anchor='w')
    rate_text = f'{rate:.1f}%' if total else 'N/A'
    chart.create_text(0, 80, text='Order Completion Rate: ' + rate_text,
                      fill=TEXT_COLOR, anchor='w')

    # Display the latest ten payment records
    heading('RECENT HISTORY')
    history = tk.Frame(report, bg=BG_COLOR)
    history.pack(fill='both', expand=True, padx=20)
    for column, name in enumerate(['Order ID', 'Weight (kg)', 'Services', 'Total Payment']):
        tk.Label(history, text=name, bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=('Arial', 10, 'bold')).grid(row=0, column=column, sticky='ew', padx=1)
        history.columnconfigure(column, weight=1)
    for row, payment in enumerate(payments[-10:][::-1], start=1):
        services = []
        for service in payment.get('services', []):
            services.append(str(service.get('service', '')))
        values = [payment.get('order_id', '-'), payment.get('weight', '-'),
                  ', '.join(services) or '-', f"RM {float(payment.get('total_payment', 0) or 0):.2f}"]
        for column, value in enumerate(values):
            tk.Label(history, text=value, bg=BG_COLOR, fg=TEXT_COLOR, wraplength=320,
                     font=('Arial', 10)).grid(row=row, column=column, sticky='ew', pady=2)
    if not payments:
        tk.Label(history, text='No payment records yet.', bg=BG_COLOR, fg=MUTED_COLOR).grid(
            row=1, column=0, columnspan=4, pady=10)

    tk.Button(report, text='Exit', command=report.destroy, bg='#334155',
              fg='white', activebackground='#475569', activeforeground='white',
              relief='flat', font=('Arial', 10, 'bold'), width=12, pady=7,
              cursor='hand2').pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Laundry Service Assistant")
    root.geometry("1100x700")
    root.resizable(True, True)
    try:
        root.state("zoomed")
    except tk.TclError:
        pass
    root.configure(bg=BG_COLOR)
    sidebar = tk.Frame(root, bg=CARD_COLOR, width=250)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    tk.Label(sidebar, text="LAUNDRY SERVICE\nASSISTANT", font=("Arial", 17, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR, justify="left").pack(anchor="w", padx=20, pady=(30, 35))
    content = tk.Frame(root, bg=BG_COLOR, padx=30, pady=28)
    content.pack(side="left", fill="both", expand=True)
    tk.Label(content, text="Dashboard", font=("Arial", 26, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w")
    tk.Label(content, text="Manage your laundry service in one place", font=("Arial", 11), bg=BG_COLOR, fg=MUTED_COLOR).pack(anchor="w", pady=(5, 22))
    entries = [
        ("01", "Customer Management", "Register and manage customer records", lambda: launch_module("module1.py")),
        ("02", "Laundry Order Management", "Create and manage laundry orders", lambda: launch_module("module2.py")),
        ("03", "Laundry Service Tracking", "View laundry tracking and order status", lambda: launch_module("laundry_tracking_module3.py")),
        ("04", "Payment Calculator", "Calculate charges and manage payment records", lambda: launch_module("module_4.py")),
        ("05", "Summary & Reporting", "View customer, order and revenue statistics", open_reporting_module),
    ]
    for number, name, desc, action in entries:
        tk.Button(sidebar, text=number + "   " + name, command=action, bg=CARD_COLOR, fg=TEXT_COLOR, activebackground="#334155", activeforeground="white", font=("Arial", 10, "bold"), relief="flat", anchor="w", padx=14, pady=14, cursor="hand2").pack(fill="x", padx=8, pady=3)
        card = tk.Frame(content, bg=CARD_COLOR, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=10)
        card.pack(fill="x", pady=5)
        tk.Label(card, text=number, font=("Arial", 18, "bold"), bg=CARD_COLOR, fg="#93C5FD", width=3).pack(side="left", padx=(0, 12))
        details = tk.Frame(card, bg=CARD_COLOR)
        details.pack(side="left", fill="x", expand=True)
        tk.Label(details, text=name, font=("Arial", 12, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        tk.Label(details, text=desc, font=("Arial", 9), bg=CARD_COLOR, fg=MUTED_COLOR).pack(anchor="w", pady=(3, 0))
        tk.Button(card, text="Open", command=action, bg=BLUE_COLOR, fg="white", activebackground=ACTIVE_BLUE, activeforeground="white", relief="flat", font=("Arial", 10, "bold"), padx=18, pady=7, cursor="hand2").pack(side="right")
    tk.Button(sidebar, text="Exit", command=root.destroy, bg="#334155", fg="white", activebackground="#475569", activeforeground="white", relief="flat", padx=15, pady=12, cursor="hand2").pack(side="bottom", fill="x", padx=16, pady=22)
    root.mainloop()