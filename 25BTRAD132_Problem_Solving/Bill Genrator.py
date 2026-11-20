print("--- Quick Shop ---")
print("Available Items:")
print("1. Biscuit - 25")
print("2. Chips   - 15")
print("3. Pen     - 10")

# Keep track of what the user buys
biscuit_qty = 0
chips_qty = 0
pen_qty = 0

# Interactive buying step
while True:
    choice = input("\nWhat would you like to buy? (1-3, or type 'done' to finish): ").strip().lower()

    if choice == "1":
        biscuit_qty = int(input("How many Biscuit packs?: "))
    elif choice == "2":
        chips_qty = int(input("How many Chips bags?: "))
    elif choice == "3":
        pen_qty = int(input("How many Pens?: "))
    elif choice == "done":
        break
    else:
        print("Invalid choice, please pick 1, 2, 3, or type 'done'.")

# Calculate costs
biscuit_total = biscuit_qty * 25
chips_total = chips_qty * 15
pen_total = pen_qty * 10

subtotal = biscuit_total + chips_total + pen_total
tax = subtotal * 0.05
grand_total = subtotal + tax

# Print final bill
print("\n" + "=" * 25)
print("      YOUR BILL      ")
print("=" * 25)

if biscuit_qty > 0:
    print(f"Biscuit x{biscuit_qty} = {round(biscuit_total, 2)}")
if chips_qty > 0:
    print(f"Chips   x{chips_qty} = {round(chips_total, 2)}")
if pen_qty > 0:
    print(f"Pen     x{pen_qty} = {round(pen_total, 2)}")

print("-" * 25)
print(f"Subtotal: {round(subtotal, 2)}")
print(f"Tax (5%): {round(tax, 2)}")
print(f"TOTAL:    {round(grand_total, 2)}")
print("=" * 25)
print("Thank you for shopping!")