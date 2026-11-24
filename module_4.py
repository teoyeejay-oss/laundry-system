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
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
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

        # Automatically fit window width to GUI content
        self.root.update_idletasks()
        self.root.geometry(f"{self.root.winfo_reqwidth()}x650")

        # Center window on screen
        self.root.update_idletasks()

        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
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

        # Search Record
        for record in records:
            if record.get("order_id") == order_id:
                # Record Found
                self.update_error_label.config(text="")
                self.edit_frame.pack(fill="x")

                # Fill Existing Weight
                self.weight_entry.delete(0, tk.END)
                self.weight_entry.insert(0, record["weight"])

                self.washing_var.set(any(item["service"] == "Washing" for item in record["services"]))
                self.drying_var.set( any(item["service"] == "Drying" for item in record["services"]))
                self.ironing_var.set( any(item["service"] == "Ironing" for item in record["services"]))
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
            records = self.calculator.load_payment_records()

        except ValueError as error:
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
