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
        self.orders = load_orders()
        self.customers = load_customers()
        self.service_vars = {s: tk.BooleanVar() for s in SERVICES}

        self.build_form()
        self.build_table()
        self.clear_form()
        self.refresh_table(self.orders.values())

        if not self.customers:
            messagebox.showwarning("No Customers",
                                   "No registered customers found.\n"
                                   "Please register customers in Module 1 first.")

    # ----- layout -----
    def build_form(self):
        form = ttk.LabelFrame(self.window, text="Order Details")
        form.grid(row=0, column=0, padx=10, pady=10, sticky="n")

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
        right.grid(row=0, column=1, padx=10, pady=10, sticky="n")

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
