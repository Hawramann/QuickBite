import random
from datetime import datetime

# Menu data as a dictionary
menu = {
    "Main Course": {
        "m1": {"item_name": "Grilled Chicken", "item_price": 6.99, "item_availability": True},
        "m2": {"item_name": "Margherita Pizza", "item_price": 8.99, "item_availability": True},
        "m3": {"item_name": "Chicken Pasta", "item_price": 7.99, "item_availability": True},
        "m4": {"item_name": "Fish Fillet", "item_price": 9.99, "item_availability": False},
        "m5": {"item_name": "Lamb Chops", "item_price": 10.99, "item_availability": True}
    },
    "Sides": {
        "s1": {"item_name": "French Fries", "item_price": 2.99, "item_availability": True},
        "s2": {"item_name": "Garlic Bread", "item_price": 3.49, "item_availability": True},
        "s3": {"item_name": "Mash Potato", "item_price": 3.29, "item_availability": True},
        "s4": {"item_name": "Veg Soup", "item_price": 1.99, "item_availability": True},
        "s5": {"item_name": "Fruit Salad", "item_price": 2.99, "item_availability": True}
    },
    "Drinks": {
        "d1": {"item_name": "Coca Cola", "item_price": 0.85, "item_availability": True},
        "d2": {"item_name": "Pepsi", "item_price": 0.85, "item_availability": True},
        "d3": {"item_name": "7UP", "item_price": 0.85, "item_availability": True},
        "d4": {"item_name": "Orange Juice", "item_price": 1.99, "item_availability": True},
        "d5": {"item_name": "Mineral Water", "item_price": 1.00, "item_availability": True}
    }
}


def start_order():
    print("Press Enter to Start Your Order")
    input()
    order_list = []
    first_item_added = False

    while True:
        display_menu()  # Display menu details

        # Display chosen items after the menu
        if first_item_added:
            print("\n--------Your Chosen Items--------")
            display_order_list(order_list)
            total = sum(item['item_price'] for item in order_list)
            print("---------------------------------")
            print(f"{'Total:':<25} £{total:.2f}\n")

        # Prompt based on whether this is the first item being added
        if not first_item_added:
            print("Please Enter Your Desired Item Codes (e.g., m1, m2, s3).")
            item_codes = input("Add item code(s): ").strip().lower()
        else:
            print("Add more items by entering their codes (e.g., m1, m2, s3),")
            print("or press 'd' to delete an item, or press 'f' to finish order.")
            item_codes = input("Your input: ").strip().lower()

        # Handle options for deleting an item or finishing order
        if first_item_added:
            if item_codes == "d":
                delete_item(order_list)
                continue  # Go back to options after deletion

            elif item_codes == "f":
                checkout(order_list)
                break

        # Split the input into individual codes and process each
        codes = [code.strip() for code in item_codes.split(",") if code.strip()]

        # Validate and add items
        for code in codes:
            if not is_valid_item_code(code):
                print(f"The item code '{code}' is not valid, please try again.")
                continue
            else:
                item = get_item_details(code)
                order_list.append({"code": code, **item})
                first_item_added = True  # Set to True once an item is successfully added


def display_menu():
    print("\n    Main Course:                  | Sides                          | Drinks")
    print("Code  Name               Price    | Code  Name            Price    | Code  Name         Price")
    main_courses = {k: v for k, v in menu.get("Main Course", {}).items() if v["item_availability"]}
    sides = {k: v for k, v in menu.get("Sides", {}).items() if v["item_availability"]}
    drinks = {k: v for k, v in menu.get("Drinks", {}).items() if v["item_availability"]}

    # Get maximum number of rows needed for alignment
    max_rows = max(len(main_courses), len(sides), len(drinks))
    main_list = list(main_courses.items()) + [("", {})] * (max_rows - len(main_courses))
    side_list = list(sides.items()) + [("", {})] * (max_rows - len(sides))
    drink_list = list(drinks.items()) + [("", {})] * (max_rows - len(drinks))

    for i in range(max_rows):
        main_code, main_item = main_list[i]
        side_code, side_item = side_list[i]
        drink_code, drink_item = drink_list[i]

        main_name = main_item.get("item_name", "")
        main_price = f"£{main_item.get('item_price', ''):.2f}" if main_item else ""

        side_name = side_item.get("item_name", "")
        side_price = f"£{side_item.get('item_price', ''):.2f}" if side_item else ""

        drink_name = drink_item.get("item_name", "")
        drink_price = f"£{drink_item.get('item_price', ''):.2f}" if drink_item else ""

        print(f"{main_code:<5} {main_name:<18} {main_price:<8} | "
              f"{side_code:<5} {side_name:<15} {side_price:<8} | "
              f"{drink_code:<5} {drink_name:<12} {drink_price:<8}")


def is_valid_item_code(code):
    available_items = {**menu.get("Main Course", {}), **menu.get("Sides", {}), **menu.get("Drinks", {})}
    return code in available_items and available_items[code]["item_availability"]


def get_item_details(code):
    for category in menu.values():
        if code in category:
            return category[code]
    return None


def display_order_list(order_list):
    for item in order_list:
        print(f"{item['code']:>5}  {item['item_name']:<18} £{item['item_price']:.2f}")


def delete_item(order_list):
    display_order_list(order_list)
    item_to_delete = input("Enter the code of the item you wish to delete (or 'q' to quit deletion): ").strip().lower()

    for index, item in enumerate(order_list):
        if item['code'] == item_to_delete:
            removed_item = order_list.pop(index)
            print(f"One '{removed_item['item_name']}' removed from your order.")
            break
    else:
        print("Item not in your list to delete, please try again.")


def checkout(order_list):
    total = sum(item['item_price'] for item in order_list)
    print(f"\nTotal: £{total:.2f}")

    while True:
        payment_method = input("How would you like to pay? (1 - Cash, 2 - Card): ").strip()

        if payment_method == "2":  # Card payment
            print("Please tap or insert your card and press Enter")
            while True:
                confirm = input().strip()
                if confirm == "":  # Only proceed if Enter is pressed
                    generate_receipt(order_list, total, "Card", "Payment Successful")
                    return
                else:
                    print("Please tap or insert your card and press Enter to continue.")

        elif payment_method == "1":  # Cash payment
            cash_payment(total, order_list)
            return

        else:  # Invalid input handling
            print("Your choice is not valid, please try again, or press 'r' to reorder.")
            retry_choice = input("Press 'r' to reorder, or press any other key to try again: ").strip().lower()
            if retry_choice == "r":
                display_menu()
                start_order()
                return  # Exit checkout and restart ordering process
            elif retry_choice == "":  # User pressed Enter to try again
                continue  # Go back to the payment method prompt




def cash_payment(total, order_list):
    cash_received = 0
    while cash_received < total:
        try:
            # Prompt for cash input
            additional_cash = input(f"Total: £{total:.2f}. Enter cash amount: ").strip()
            if additional_cash == "":  # Check for Enter without any input
                print("Please enter a valid cash amount.")
                continue  # Retry the input if nothing is entered

            # Convert the input to a float
            additional_cash = float(additional_cash)
            cash_received += additional_cash

            # Check if additional cash received is still less than total
            if cash_received < total:
                print(f"Remaining amount: £{total - cash_received:.2f}")
            elif cash_received > total:
                change = cash_received - total
                generate_receipt(order_list, total, "Cash", f"Paid: £{cash_received:.2f}, Change: £{change:.2f}")
                return  # Exit the function after successful payment

        except ValueError:
            # Catch invalid input and prompt again
            print("Invalid amount. Please enter a valid number.")

    # When exact payment is made
    generate_receipt(order_list, total, "Cash", f"Paid: £{total:.2f}, Change: £0.00")



def generate_receipt(order_list, total, payment_method, payment_details):
    order_number = random.randint(1000, 9999)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\nThank you for your Order. Please pick up your order.")
    print(f"Your Order Number is: {order_number}")
    print("------------------------------------------")
    print("QuickBite  0121 123 4567")
    print("123 ABC Road")
    print("Birmingham")
    print("AB2 3YZ")
    print("------------------------------------------")

    for item in order_list:
        print(f"{item['item_name']} - £{item['item_price']:.2f}")
    print(f"Total: £{total:.2f}")
    print(f"Payment Method: {payment_method} ({payment_details})")
    print("------------------------------------------")
    print(f"Date & Time: {current_datetime}")
    print("Thank you for your purchase!\n")
    print("Next Customer")

    # Go back to the start of the order process
    start_order()


# Start the order process
start_order()
