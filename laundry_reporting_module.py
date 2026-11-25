"""Laundry Service Assistant App - Manager Reporting Module

Expected data formats:
customers = [
    {"customer_id": "C001", "name": "Ali", "contact": "0123456789"},
]
orders = [
    {
        "order_id": "O001",
        "customer_id": "C001",
        "weight": 3.5,
        "services": ["Washing", "Drying"],
        "status": "Pending",       # or "Completed"
        "total_amount": 25.00,      # order charge calculated by Payment Module
        # Optional: "amount_paid": 25.00  # use this when tracking actual payments
    },
]

To integrate with another file, import reporting_menu and call:
    reporting_menu(customers, orders)
"""

from decimal import Decimal, InvalidOperation


def _to_decimal(value):
    """Convert a money value to Decimal safely; invalid/missing values become 0."""
    try:
        return Decimal(str(value if value is not None else 0))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal("0")


def _format_money(amount, currency):
    return f"{currency} {amount:,.2f}"


def total_registered_customers(customers):
    """Return the number of registered customer records."""
    return len(customers)


def total_orders(orders):
    """Return the number of recorded laundry orders."""
    return len(orders)


def count_orders_by_status(orders, status):
    """Count orders whose status matches Pending or Completed (case-insensitive)."""
    return sum(
        1 for order in orders
        if str(order.get("status", "")).strip().casefold() == status.casefold()
    )


def calculate_total_revenue(orders):
    """Calculate revenue from amount_paid, or total_amount if payment is not tracked.

    If your Payment Module tracks actual collections, provide amount_paid in each
    order. Otherwise, total_amount is treated as recorded order revenue.
    """
    total = Decimal("0")
    for order in orders:
        amount = order.get("amount_paid")
        if amount is None:
            amount = order.get("total_amount", 0)
        total += _to_decimal(amount)
    return total


def display_report(title, value):
    print("\n" + "=" * 48)
    print(f"{title:^48}")
    print("=" * 48)
    print(f"{value:^48}")
    print("=" * 48)


def reporting_menu(customers, orders, currency="RM"):
    """Display the manager's reporting menu until they choose Back to Menu.

    customers and orders should be the same lists used by the other app modules.
    Choosing option 6 returns control to the caller (the Main Menu).
    """
    while True:
        print("\n" + "=" * 48)
        print("       LAUNDRY SERVICE - REPORTING MODULE")
        print("                 MANAGER MENU")
        print("=" * 48)
        print("1. Total Registered Customers")
        print("2. Total Orders")
        print("3. Pending Orders")
        print("4. Completed Orders")
        print("5. Total Revenue")
        print("6. Back to Main Menu")
        print("=" * 48)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            count = total_registered_customers(customers)
            display_report("TOTAL REGISTERED CUSTOMERS", f"{count} customer(s)")

        elif choice == "2":
            count = total_orders(orders)
            display_report("TOTAL LAUNDRY ORDERS", f"{count} order(s)")

        elif choice == "3":
            count = count_orders_by_status(orders, "Pending")
            display_report("PENDING ORDERS", f"{count} order(s)")

        elif choice == "4":
            count = count_orders_by_status(orders, "Completed")
            display_report("COMPLETED ORDERS", f"{count} order(s)")

        elif choice == "5":
            revenue = calculate_total_revenue(orders)
            display_report("TOTAL REVENUE", _format_money(revenue, currency))

        elif choice == "6":
            print("\nReturning to Main Menu...")
            return

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

        input("\nPress Enter to return to the Reporting Menu...")


# The sample data below lets this file run independently for testing.
# Remove this section when integrating with your complete application.
if __name__ == "__main__":
    sample_customers = [
        {"customer_id": "C001", "name": "Ali", "contact": "0123456789"},
        {"customer_id": "C002", "name": "Mei Ling", "contact": "0134567890"},
        {"customer_id": "C003", "name": "Ravi", "contact": "0145678901"},
    ]

    sample_orders = [
        {"order_id": "O001", "customer_id": "C001", "status": "Pending", "total_amount": 25.00},
        {"order_id": "O002", "customer_id": "C002", "status": "Completed", "total_amount": 32.50},
        {"order_id": "O003", "customer_id": "C003", "status": "Pending", "total_amount": 18.00},
        {"order_id": "O004", "customer_id": "C001", "status": "Completed", "total_amount": 40.00},
    ]

    reporting_menu(sample_customers, sample_orders)
