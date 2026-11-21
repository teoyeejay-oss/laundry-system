from datetime import datetime
from tkinter import messagebox
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
#Create a child class for registered customers
class RegisteredCustomer(Customer):

    def __init__(self, customer_id, customer_name, contact_number, registration_date):
        super().__init__(
            customer_id,
            customer_name,
            contact_number,
            registration_date
        )

    def display_registration_status(self):
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
    customer_id = input("Enter Customer Id:").strip().upper()
    id_exists = False
    while True:
        id_exists = False
        for customer in customers:
            if customer.get_customer_details()["Customer ID"] == customer_id:
                id_exists = True
                print("Customer ID already exists!")
                customer_id = input("Enter Customer Id:").strip().upper()
                break
        if id_exists:
            continue
        else:
            break
    if id_exists == False:
        customer_name = input("Enter Customer Name:").strip()
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
            with open("customers.txt", "r") as file:
                for line in file:
                    print(line.strip())

        except FileNotFoundError:
            print("Customer file does not exist!")

        except OSError as e:
            print("File reading error:", e)

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

root.mainloop()