"""Challenge 17: Pizza Order Builder
Pick a size and up to 3 toppings, get an order summary with a made-up price.
"""

prices = {"small": 8, "medium": 11, "large": 14}

print("Welcome to PyZZA! 🍕")
size = input("Choose a size (small / medium / large): ").lower().strip()

if size not in prices:
    print("Unknown size — defaulting to medium.")
    size = "medium"

base_price = prices[size]

print("Choose up to 3 toppings (press Enter to skip):")
toppings = []
for i in range(1, 4):
    topping = input(f"  Topping {i}: ").strip()
    if topping:
        toppings.append(topping)

total = base_price + len(toppings) * 1.50

print("\n--- Your Order ---")
print(f"Size: {size.capitalize()}")
if toppings:
    print("Toppings: " + ", ".join(toppings))
else:
    print("Toppings: plain cheese")
print(f"Total: ${total:.2f}  (we made up that price)")
print("Thanks for ordering at PyZZA! 🍕")
