# Module 3: Laundry Service Tracking
# Standalone demo. Replace sample_orders with the shared orders list from your group.
# Concepts: selection, loops, string processing, file processing, collections,
# functions, encapsulation, inheritance, GUI, exception handling, comments, execution.

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime


# -------------------- Shared data (DEMO ONLY) --------------------
# In the integrated group program, remove this sample list and receive
# the shared "orders" list created by Member 2 (Order Management).
sample_orders = [
    {
        "order_id": "O001",
        "customer_id": "C001",
        "weight": 3.0,
        "services": ["Washing", "Drying"],
        "status": "Pending"
    },
    {
        "order_id": "O002",
        "customer_id": "C002",
        "weight": 2.5,
        "services": ["Washing", "Ironing"],
        "status": "Completed"
    },
]


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
        self.root.geometry("520x420")
        self.root.configure(padx=12, pady=12)
        self.orders = self.get_orders()

        title = tk.Label(self.root, text="Laundry Service Tracking",
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 12))

        # Figure 1: Main Tracking Menu
        tk.Button(self.root, text="1. View All Orders", width=32,
                  command=self.view_all_orders).pack(pady=4)
        tk.Button(self.root, text="2. Search Order", width=32,
                  command=self.search_order).pack(pady=4)
        tk.Button(self.root, text="3. Update Order Status", width=32,
                  command=self.update_order_status).pack(pady=4)
        tk.Button(self.root, text="4. Pending / Completed Orders", width=32,
                  command=self.view_pending_completed).pack(pady=4)
        tk.Button(self.root, text="5. Check Order Progress", width=32,
                  command=self.check_order_progress).pack(pady=4)
        tk.Button(self.root, text="6. Export Tracking Records", width=32,
                  command=self.export_tracking_records).pack(pady=4)
        tk.Button(self.root, text="7. Return to Main Menu / Close", width=32,
                  command=self.root.destroy).pack(pady=4)

        self.output = tk.Text(self.root, height=10, width=60, wrap="word")
        self.output.pack(pady=(12, 0), fill="both", expand=True)

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
        search_id = simpledialog.askstring("Search Order", "Enter Order ID:")
        if search_id is None:
            return
        search_id = self.clean_text(search_id)
        if not search_id:
            messagebox.showwarning("Invalid Input", "Order ID cannot be empty.")
            return

        # Linear search through the shared orders list.
        for order in self.orders:
            if self.clean_text(str(order.get("order_id", ""))) == search_id:
                self.display_text(self.format_order(order))
                return
        self.display_text("Order Not Found.")

    # -------------------- Figure 4: Update Order Status --------------------
    def update_order_status(self):
        search_id = simpledialog.askstring("Update Status", "Enter Order ID:")
        if search_id is None:
            return
        search_id = self.clean_text(search_id)
        if not search_id:
            messagebox.showwarning("Invalid Input", "Order ID cannot be empty.")
            return

        target_order = None
        for order in self.orders:
            if self.clean_text(str(order.get("order_id", ""))) == search_id:
                target_order = order
                break

        if target_order is None:
            self.display_text("Order Not Found.")
            return

        current_status = target_order.get("status", "N/A")
        new_status = simpledialog.askstring(
            "Update Status",
            f"Current status: {current_status}\nEnter new status (Pending/Completed):"
        )
        if new_status is None:
            return
        new_status = new_status.strip().title()

        # Selection: only accept the two assignment status values.
        if new_status not in ("Pending", "Completed"):
            messagebox.showerror("Invalid Status", "Enter Pending or Completed.")
            return

        target_order["status"] = new_status
        self.display_text(
            f"Status Updated Successfully!\n\n{self.format_order(target_order)}"
        )

    # -------------------- Figure 5: Pending / Completed Orders --------------------
    def view_pending_completed(self):
        selected_status = simpledialog.askstring(
            "Filter Orders", "Enter status to view (Pending/Completed):"
        )
        if selected_status is None:
            return
        selected_status = selected_status.strip().title()

        if selected_status not in ("Pending", "Completed"):
            messagebox.showerror("Invalid Status", "Enter Pending or Completed.")
            return

        found = False
        lines = []
        # Display every order that matches the selected status.
        for order in self.orders:
            if order.get("status", "").strip().title() == selected_status:
                lines.append(self.format_order(order))
                found = True

        if found:
            self.display_text("\n".join(lines))
        else:
            self.display_text("No Matching Orders.")

    # -------------------- Figure 6: Check Order Progress --------------------
    def check_order_progress(self):
        search_id = simpledialog.askstring("Check Progress", "Enter Order ID:")
        if search_id is None:
            return
        search_id = self.clean_text(search_id)
        if not search_id:
            messagebox.showwarning("Invalid Input", "Order ID cannot be empty.")
            return

        for order in self.orders:
            if self.clean_text(str(order.get("order_id", ""))) == search_id:
                status = order.get("status", "N/A")
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
        # Export a snapshot only; it does not replace or reload shared group data.
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
        app = LaundryTrackingApp(sample_orders)
        app.root.mainloop()
    except tk.TclError as error:
        print("GUI could not start:", error)


if __name__ == "__main__":
    main()
