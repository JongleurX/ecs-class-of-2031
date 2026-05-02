print("Superhero Registry")
print("------------------")

# Inputs
name = input("Superhero code name: ")
while True:
    try:
        age = int(input("Age: "))
        if age < 1: raise ValueError
        break
    except ValueError:
        print("Invalid age, try again!")
while True:
    try:
        speed = float(input("Speed (mph): "))
        if speed < 0: raise ValueError
        break
    except ValueError:
        print("Invalid speed, try again!")

# Outputs
tags = ["Dog years", "Power level", "Lucky number"]
facts = [age * 7, age ** 2, age % 10]
print(f"Superhero {name.upper()} registered!")
for i in range(3):
    print(f"{tags[i] + ':':<15} {facts[i]}")
print(f"{'KPH:':<15} {round(speed * 1.6, 1)}")
