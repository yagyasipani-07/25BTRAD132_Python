#Lab_Exercise_14
class Bank:
    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print("Deposited successfully!")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print("Withdrawn successfully!")
        else:
            print("Invalid transaction!")

    def display(self):
        print("Account:", self.name)
        print("Balance:", self.__balance)


b = Bank("Rahul", 5000)

while True:
    ch = int(input("\n1.Deposit 2.Withdraw 3.Balance 4.Exit: "))

    if ch == 1:
        b.deposit(float(input("Amount: ")))
    elif ch == 2:
        b.withdraw(float(input("Amount: ")))
    elif ch == 3:
        b.display()
    elif ch == 4:
        break
    else:
        print("Invalid choice!")

#Lab_Exercise_15
class Book:
    def __init__(self, title):
        self.title = title
        self.available = True

    def display(self):
        print(self.title, "-", self.available)


class Library(Book):
    def issue(self):
        if self.available:
            self.available = False
            print("Book issued!")
        else:
            print("Book unavailable!")

    def return_book(self):
        if not self.available:
            self.available = True
            print("Book returned!")
        else:
            print("Book already available!")


b = Library("Python Programming")

b.display()
b.issue()
b.display()
b.return_book()
b.display()

#Lab_Exercise_16
import random

def roll_dice(n):
    dice = []
    for i in range(n):
        dice.append(random.randint(1, 6))
    return dice

def frequency_counter(results):
    freq = {}
    for x in results:
        freq[x] = freq.get(x, 0) + 1
    return freq

n = int(input("Enter number of dice: "))
r = int(input("Enter number of rolls: "))

results = []

for i in range(r):
    dice = roll_dice(n)
    total = sum(dice)
    results.append(total)
    print("Dice:", dice, "Total:", total)

print("\nFrequency:", frequency_counter(results))