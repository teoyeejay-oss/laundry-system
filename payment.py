# Predefined service rates (RM per kg)
service_rates = {
    "washing": 2.00,
    "drying": 1.00,
    "ironing": 1.50
}

# Temporary order data for testing
orders = {
    "O001": {
        "weight": 4,
        "services": ["washing", "ironing"]
    },
    "O002": {
        "weight": 5,
        "services": ["washing", "drying"]
    }
}


# Main payment calculation function
def calculate_payment():

    order_id = input("Enter Order ID: ").strip().upper()

    if order_id not in orders:
        print("Order Not Found.")
        return

    order_details = orders[order_id]
    weight = order_details["weight"]
    selected_services = order_details["services"]

    print("\nOrder Found!")
    print(f"Order ID: {order_id}")
    print(f"Weight:{weight}kg")

    # Calculate individual service charges
    print("\n========== SERVICE CHARGES ==========")

    total_amount = 0

    for service in selected_services:
        rate = service_rates[service]
        service_charge = weight * rate
        print(f"{service.title()}: RM {service_charge:.2f}")

        total_amount += service_charge

    # Display total amount payable
    print("------------------------------------")
    print(f"Total Amount Payable: RM {total_amount:.2f}")


# Main program
def main():
    print("================================")
    print("       PAYMENT CALCULATOR")
    print("================================")

    calculate_payment()


# Start program
if __name__ == "__main__":
    main()