
def calculate_payment(weight, services):

    service_rates = {
        "washing": 2.00,
        "drying": 1.00,
        "ironing": 1.50
    }

    total = 0

    for service in services:

        if service in service_rates:
            charge = weight * service_rates[service]

            print(f"{service}: RM {charge:.2f}")

            total += charge

    print("------------------------")
    print(f"Total: RM {total:.2f}")

    return total
