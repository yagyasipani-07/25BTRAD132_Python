products = []

def read_non_negative_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Enter a non-negative whole number.")

def read_non_negative_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Enter a non-negative number.")

def add_product():
    name = input("Enter product name: ")

    if not name.strip():
        print("Product name cannot be empty!")
        return

    if any(p["name"].lower() == name.lower() for p in products):
        print("Product already exists!")
        return

    qty = read_non_negative_int("Enter quantity: ")
    price = read_non_negative_float("Enter price: ")

    products.append({
        "name": name,
        "quantity": qty,
        "price": price
    })

def update_product():
    name = input("Enter product name: ")

    for p in products:
        if p["name"].lower() == name.lower():
            p["quantity"] = read_non_negative_int("New quantity: ")
            p["price"] = read_non_negative_float("New price: ")
            return

    print("Product not found!")

def analyze():
    if not products:
        print("No product records available!")
        return

    total = 0
    highest = None

    for p in products:
        revenue = p["quantity"] * p["price"]
        total += revenue

        print(p["name"], "Revenue:", revenue)

        if highest is None or p["quantity"] > highest["quantity"]:
            highest = p

    print("Total Sales:", total)

    if highest:
        print("Highest Selling:", highest["name"])

def main():
    while True:
        try:
            ch = input("\n1.Add 2.Update 3.Analyze 4.Exit: ")

            if ch == '1':
                add_product()
            elif ch == '2':
                update_product()
            elif ch == '3':
                analyze()
            elif ch == '4':
                break
            else:
                print("Invalid choice! Try again.")
        except EOFError:
            print("\nInput closed. Exiting.")
            break


main()
