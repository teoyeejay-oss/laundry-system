import tkinter as tk
import json
import os


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

class PaymentCalculatorGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Laundry Service - Payment Calculator")
        self.root.geometry("650x650")
        self.root.resizable(False, False)

        # Connect to PaymentCalculator
        self.calculator = PaymentCalculator()

        # Main Frame
        self.main_frame = tk.Frame(
            self.root,
            padx=30,
            pady=25
        )
        self.main_frame.pack(fill="both", expand=True)

        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text="Laundry Service",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=5)

        # Subtitle
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="Payment Calculator",
            font=("Arial", 13)
        )
        self.subtitle_label.pack(pady=5)

        # Input Frame
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(pady=20)

        # Order ID Label
        self.order_label = tk.Label(
            self.input_frame,
            text="Enter Order ID:",
            font=("Arial", 11)
        )
        self.order_label.grid(row=0, column=0, padx=5)

        # Order ID Entry
        self.order_entry = tk.Entry(
            self.input_frame,
            font=("Arial", 11),
            width=20
        )
        self.order_entry.grid(row=0, column=1, padx=5)

        self.error_label = tk.Label(
            self.input_frame,
            text="",
            font=("Arial", 9),
            fg="red",
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
            self.main_frame,
            text="Calculate Payment",
            font=("Arial", 11, "bold"),
            width=22,
            command=self.calculate
        )
        self.calculate_button.pack(pady=5)

        #Clear button
        self.clear_button = tk.Button(
            self.main_frame,
            text="Clear Result",
            font=("Arial", 11),
            width=22,
            command=self.clear_result
        )
        self.clear_button.pack(pady=5)

        # View Records Button
        self.records_button = tk.Button(
            self.main_frame,
            text="View Payment Records",
            font=("Arial", 11),
            width=22,
            command=self.view_records
        )
        self.records_button.pack(pady=5)

        # Result Label
        self.result_label = tk.Label(
            self.main_frame,
            text="Payment result will appear here.",
            font=("Arial", 11),
            justify="left",
            anchor="w"
        )
        self.result_label.pack(pady=15, anchor="w")

        # History Title
        self.history_title = tk.Label(
            self.main_frame,
            text="Payment Records",
            font=("Arial", 12, "bold")
        )
        self.history_title.pack(anchor="w", pady=5)

        # History Text Area
        self.history_text = tk.Text(
            self.main_frame,
            height=10,
            width=65,
            font=("Arial", 10)
        )
        self.history_text.pack()

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

        except KeyError as error:
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
