# Module 5: Summary & Reporting
import os
import json
import tkinter as tk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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
    report = tk.Tk()
    report.title('Summary & Reporting')
    report.geometry('850x700')
    report.configure(bg='black')

    def heading(text):
        tk.Label(report, text=text, bg='black', fg='white',
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
        row = tk.Frame(report, bg='black')
        row.pack(fill='x', padx=20)
        tk.Label(row, text=name, bg='black', fg='white', font=('Arial', 11)).pack(side='left')
        tk.Label(row, text=value, bg='black', fg='white', font=('Arial', 11)).pack(side='right')

    # Simple bar chart using Tkinter Canvas
    heading('ORDER STATUS OVERVIEW')
    chart = tk.Canvas(report, width=500, height=95, bg='black', highlightthickness=0)
    chart.pack(anchor='w', padx=20)
    for name, count, y in [('Completed', completed, 5), ('Pending', pending, 35)]:
        chart.create_text(0, y + 10, text=name, fill='white', anchor='w')
        chart.create_rectangle(100, y, 400, y + 20, fill='#333333', outline='')
        if total > 0 and count > 0:
            chart.create_rectangle(100, y, 100 + 300 * count / total, y + 20,
                                   fill='white', outline='')
        chart.create_text(415, y + 10, text=str(count), fill='white', anchor='w')
    rate_text = f'{rate:.1f}%' if total else 'N/A'
    chart.create_text(0, 80, text='Order Completion Rate: ' + rate_text,
                      fill='white', anchor='w')

    # Display the latest ten payment records
    heading('RECENT HISTORY')
    history = tk.Frame(report, bg='black')
    history.pack(fill='both', expand=True, padx=20)
    for column, name in enumerate(['Order ID', 'Weight (kg)', 'Services', 'Total Payment']):
        tk.Label(history, text=name, bg='#333333', fg='white',
                 font=('Arial', 10, 'bold')).grid(row=0, column=column, sticky='ew', padx=1)
        history.columnconfigure(column, weight=1)
    for row, payment in enumerate(payments[-10:][::-1], start=1):
        services = []
        for service in payment.get('services', []):
            services.append(str(service.get('service', '')))
        values = [payment.get('order_id', '-'), payment.get('weight', '-'),
                  ', '.join(services) or '-', f"RM {float(payment.get('total_payment', 0) or 0):.2f}"]
        for column, value in enumerate(values):
            tk.Label(history, text=value, bg='black', fg='white', wraplength=320,
                     font=('Arial', 10)).grid(row=row, column=column, sticky='ew', pady=2)
    if not payments:
        tk.Label(history, text='No payment records yet.', bg='black', fg='white').grid(
            row=1, column=0, columnspan=4, pady=10)

    tk.Button(report, text='Close', command=report.destroy, bg='white',
              fg='black', width=12).pack(pady=15)
    report.mainloop()


if __name__ == "__main__":
    open_reporting_module()
