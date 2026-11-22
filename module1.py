from datetime import datetime
from tkinter import messagebox
import tkinter as tk
# Store all registered customer objects
customers_list = []
"""
Customer Registration System

This program allows users to register customers,
store customer information, and display registration details.
"""
#Define the Customer class
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

#Create a child class for registered customers
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

root = tk.Tk()
root.title("Customer Registration System")
root.geometry("450x400")
root.configure(bg="lightblue")
title_label = tk.Label(
    root,
    text="Customer Registration",
    font=("Arial", 18, "bold"),
    bg="lightblue"
)
title_label.pack(pady=15)

tk.Label(root, text="Customer ID:", bg="lightblue").pack()
customer_id_entry = tk.Entry(root)
customer_id_entry.pack()

tk.Label(root, text="Customer Name:", bg="lightblue").pack()
customer_name_entry = tk.Entry(root)
customer_name_entry.pack()

tk.Label(root, text="Contact Number:", bg="lightblue").pack()
contact_number_entry = tk.Entry(root)
contact_number_entry.pack()

#Handle customer registration through GUI
def register_customer_gui():
    customer_id = customer_id_entry.get().strip().upper()
    customer_name = customer_name_entry.get().strip()
    contact_number = contact_number_entry.get().strip()

    if customer_id == "" or customer_name == "" or contact_number == "":
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    for customer in customers_list:
        if customer.get_customer_details()["Customer ID"] == customer_id:
            messagebox.showerror("Error", "Customer ID already exists!")
            return
    if not contact_number.isdigit():
        messagebox.showerror("Error", "Contact Number must contain digits only!")
        return
    # Get the current registration date and time
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_customer = RegisteredCustomer(
        customer_id,
        customer_name,
        contact_number,
        registration_date
    )

    customers_list.append(new_customer)

    try:
        with open("customers.txt", "a") as file:
            file.write(
                f"{customer_id},{customer_name},{contact_number},{registration_date}\n"
            )

        customers_list.append(new_customer)

    except OSError as e:
        messagebox.showerror("File Error", str(e))
        return

    messagebox.showinfo("Success", "Customer registered successfully!")

    customer_id_entry.delete(0, tk.END)
    customer_name_entry.delete(0, tk.END)
    contact_number_entry.delete(0, tk.END)

register_button = tk.Button(
    root,
    text="Register Customer",
    command=register_customer_gui,
    bg="green",
    fg="white",
    font=("Arial", 11, "bold")
)

register_button.pack(pady=20)

def customer_register(customers):
    while True:
        customer_id = input("Enter Customer Id: ").strip().upper()

        if customer_id == "":
            print("Customer ID cannot be empty!")
        else:
            break
    while True:
        id_exists = False
        for registered_customer in customers:
            if registered_customer.get_customer_details()["Customer ID"] == customer_id:
                id_exists = True
                print("Customer ID already exists!")

                while True:
                    customer_id = input("Enter Customer Id: ").strip().upper()

                    if customer_id == "":
                        print("Customer ID cannot be empty!")
                    else:
                        break

                break
        if id_exists:
            continue
        else:
            break
    if id_exists == False:
        while True:
            customer_name = input("Enter Customer Name: ").strip()

            if customer_name == "":
                print("Customer Name cannot be empty!")
            else:
                break
        while True:
            try:
                contact_number = input("Enter Contact Number:").strip()

                if not contact_number.isdigit():
                    raise ValueError("Contact Number must contain digits only!")

                break

            except ValueError as e:
                print("Invalid input:", e)

        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_customer = RegisteredCustomer(
            customer_id,
            customer_name,
            contact_number,
            registration_date
        )
        customers.append(new_customer)
        #Handle possible input or file errors
        try:
            #Save customer details into the file
            with open("customers.txt", "a") as file:
                file.write(f"{customer_id},{customer_name},{contact_number},{registration_date}\n")

        except OSError as e:
            print("File writing error:", e)
        print("Registration successful!")
        print("\nSaved Customer Records:")

        try:
            # Save customer details into the file
            with open("customers.txt", "a") as file:
                file.write(
                    f"{customer_id},{customer_name},{contact_number},{registration_date}\n"
                )

            customers.append(new_customer)

        except OSError as e:
            print("File writing error:", e)
            return

def search_customer(customers):
    while True:
        customer_id = input("Enter Customer ID to search: ").strip().upper()

        if customer_id == "":
            print("Customer ID cannot be empty!")
        else:
            break

    found = False

    for customer in customers:
        customer_details = customer.get_customer_details()

        if customer_details["Customer ID"] == customer_id:
            print("Customer Found!")
            print(customer_details)
            found = True
            break

    if found == False:
        print("Customer not found!")


def view_all_customers(customers):
    if len(customers) == 0:
        print("No customer records found!")
        return

    print("\n===== All Customer Records =====")

    for customer in customers:
        customer_details = customer.get_customer_details()

        print("------------------------------")
        print("Customer ID:", customer_details["Customer ID"])
        print("Customer Name:", customer_details["Customer Name"])
        print("Contact Number:", customer_details["Contact Number"])
        print("Registration Date:", customer_details["Registration Date"])
        print("Registration Status:", customer.display_registration_status())

    print("------------------------------")

def update_customer(customers):
    while True:
        customer_id = input("Enter Customer ID to update: ").strip().upper()

        if customer_id == "":
            print("Customer ID cannot be empty!")
        else:
            break

    found = False

    for customer in customers:
        customer_details = customer.get_customer_details()

        if customer_details["Customer ID"] == customer_id:
            found = True

            print("Customer Found!")
            print(customer_details)

            customer_name = input("Enter New Customer Name: ").strip()
            contact_number = input("Enter New Contact Number: ").strip()

            if customer_name == "" or contact_number == "":
                print("Fields cannot be empty!")
                return

            if not contact_number.isdigit():
                print("Contact Number must contain digits only!")
                return

            customer.update_customer_details(customer_name, contact_number)
            save_customers_to_file(customers)
            print("Customer updated successfully!")
            break
    if found == False:
        print("Customer not found!")

def delete_customer(customers):
    while True:
        customer_id = input("Enter Customer ID to delete: ").strip().upper()

        if customer_id == "":
            print("Customer ID cannot be empty!")
        else:
            break

    found = False

    for customer in customers:
        customer_details = customer.get_customer_details()

        if customer_details["Customer ID"] == customer_id:
            found = True

            print("Customer Found!")
            print(customer_details)

            confirm = input("Are you sure you want to delete this customer? (yes/no): ").strip().lower()

            if confirm == "yes":
                customers.remove(customer)
                save_customers_to_file(customers)
                print("Customer deleted successfully!")
            else:
                print("Deletion cancelled!")

            break

    if found == False:
        print("Customer not found!")

def save_customers_to_file(customers):
    with open("customers.txt", "w") as file:
        for customer in customers:
            details = customer.get_customer_details()

            file.write(
                f'{details["Customer ID"]},'
                f'{details["Customer Name"]},'
                f'{details["Contact Number"]},'
                f'{details["Registration Date"]}\n'
            )

def load_customers_from_file():
    try:
        with open("customers.txt", "r") as file:
            for line in file:
                details = line.strip().split(",")

                if len(details) == 4:
                    customer = RegisteredCustomer(
                        details[0],
                        details[1],
                        details[2],
                        details[3]
                    )

                    customers_list.append(customer)

    except FileNotFoundError:
        print("Customer file does not exist yet.")

    except OSError as e:
        print("File reading error:", e)


# Load existing customer records
load_customers_from_file()


while True:
    customer_register(customers_list)
    choice = input("Do you want to register another customer? (yes/no): ").strip().lower()

    match choice:
        case "yes":
            continue

        case "no":
            print("Thank you!")
            break

        case _:
            print("Invalid choice. Please enter yes or no.")


for customer in customers_list:
    print(customer.get_customer_details())
    print("Registration Status:", customer.display_registration_status())

# Load existing customer records
load_customers_from_file()

# Start GUI
root.mainloop()

# Start Console Menu
while True:
    print("\n===== Customer Management System =====")
    print("1. Register Customer")
    print("2. Search Customer")
    print("3. View All Customers")
    print("4. Update Customer")
    print("5. Delete Customer")
    print("6. Exit")

    choice = input("Enter your choice: ")

    match choice:
        case "1":
            customer_register(customers_list)

        case "2":
            search_customer(customers_list)

        case "3":
            view_all_customers(customers_list)

        case "4":
            update_customer(customers_list)

        case "5":
            delete_customer(customers_list)

        case "6":
            print("Thank you!")
            break

        case _:
            print("Invalid choice! Please try again.")