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

        self.__orders = {
            "O001": {
                "weight": 4,
                "services": ["Washing", "Ironing"]
            },
            "O002": {
                "weight": 5,
                "services": ["Washing", "Drying"]
            }
        }

        self.__file_name = "payment_records.json"

    # Calculate payment
    def calculate_payment(self, order_id):

        order_id = order_id.strip().upper()

        if not order_id:
            raise ValueError("Order ID cannot be empty.")

        if (not order_id.startswith("O")
                or len(order_id[1:]) != 3
                or not order_id[1:].isdigit()):
            raise ValueError("Order ID invalid.")

        if order_id not in self.__orders:
            raise KeyError("Order ID not found.")

        order = self.__orders[order_id]

        weight = order["weight"]
        services = order["services"]

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

        return records

    # Save payment record into JSON
    def save_payment_record(self, record):

        records = self.load_payment_records()

        for existing_record in records:

            if existing_record.get("order_id") == record["order_id"]:
                raise ValueError("Payment record already exists.")

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
        self.root.geometry("650x650")
        self.root.resizable(False, False)
        self.pack(fill="both", expand=True)

        # Header
        self.header_frame = tk.Frame(self,bg=BG_COLOR)
        self.header_frame.pack(fill="x",pady=(0, 25))

        self.title_label = tk.Label(
        self.header_frame,
        text="LAUNDRY SERVICE",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
        self.header_frame,
        text="Payment Management Dashboard",
        font=("Arial", 10),
        bg=BG_COLOR,
        fg=MUTED_COLOR
        )
        self.subtitle_label.pack(anchor="w", pady=(5, 0))

        self.calculator = PaymentCalculator()

        self.input_frame = tk.Frame(
        self,
        bg=CARD_COLOR,
        padx=20,
        pady=20
        )
        self.input_frame.pack(
        fill="x",
        pady=(0, 20)
        )

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
            self,
            text="Calculate Payment",
            font=("Arial", 11, "bold"),
            width=22,
            bg=BLUE_COLOR,
            fg=TEXT_COLOR,
            activebackground="#1D4ED8",
            activeforeground=TEXT_COLOR,
            command=self.calculate
        )
        self.calculate_button.pack(pady=5)

        #Clear button
        self.clear_button = tk.Button(
            self,
            text="Clear Result",
            font=("Arial", 11),
            width=22,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            command=self.clear_result
        )
        self.clear_button.pack(pady=5)

        # Payment Result Card
        self.result_frame = tk.Frame(
        self,
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

        # Payment History Card
        self.history_frame = tk.Frame(
        self,
        bg=CARD_COLOR,
        padx=20,
        pady=20 
        )
        self.history_frame.pack(fill="x",pady=(0, 20))

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


# ==========================================
# 3. Main Program
# ==========================================

def main():

    root = tk.Tk()

    app = PaymentCalculatorGUI(root)

    root.mainloop()


main()
