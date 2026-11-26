# Name: Yagya Sipani
# USN: 25BTRAD132

"""
Problem Solving - Task 1
Covers basic Python I/O, escape sequences, comments, variables, type conversions,
user input, string formatting, arithmetic operations, and basic conditionals.
"""

# ==============================================================================
# Task 1: Print Name, Department, College
# ==============================================================================
def task1():
    print("--- Task 1 ---")
    print("Yagya Sipani")
    print("Computer Science Engineering with specialisation in Artificial Intelligence and Data Engineering")
    print("Jain Deemed-to-be-university Faculty of Engineering and Technology")


# ==============================================================================
# Task 2: Print Pattern
# ==============================================================================
def task2():
    print("\n--- Task 2 ---")
    print("*******")
    print("*******")
    print("*******")


# ==============================================================================
# Task 3: Single Print Statement
# ==============================================================================
def task3():
    print("\n--- Task 3 ---")
    print("Python is Easy")


# ==============================================================================
# Task 4: Number Triangle
# ==============================================================================
def task4():
    print("\n--- Task 4 ---")
    print("1")
    print("12")
    print("123")
    print("1234")
    print("12345")


# ==============================================================================
# Task 5: Use \n
# ==============================================================================
def task5():
    print("\n--- Task 5 ---")
    print("Computer\nScience\nEngineering")


# ==============================================================================
# Task 6: Use \t
# ==============================================================================
def task6():
    print("\n--- Task 6 ---")
    print("Yagya\t19\tBengaluru")


# ==============================================================================
# Task 7: Single-line Comment
# ==============================================================================
def task7():
    print("\n--- Task 7 ---")
    # This program prints a welcome message
    print("Welcome")


# ==============================================================================
# Task 8: Multi-line Comments
# ==============================================================================
def task8():
    print("\n--- Task 8 ---")
    """
    This program
    prints a message
    using multiple lines of comment
    """
    print("Hello")


# ==============================================================================
# Task 9: Three Comments & Three Print Statements
# ==============================================================================
def task9():
    print("\n--- Task 9 ---")
    # Comment 1: print name
    print("Yagya Sipani")
    # Comment 2: print age
    print(19)
    # Comment 3: print city
    print("Bengaluru")


# ==============================================================================
# Task 10: Variable Name
# ==============================================================================
def task10():
    print("\n--- Task 10 ---")
    name = "Yagya Sipani"
    print(name)


# ==============================================================================
# Task 11: Three Variables
# ==============================================================================
def task11():
    print("\n--- Task 11 ---")
    a = 10
    b = 20
    c = 30
    print(a)
    print(b)
    print(c)


# ==============================================================================
# Task 12: String to Integer Conversion
# ==============================================================================
def task12():
    print("\n--- Task 12 ---")
    num = int("100")
    print(num)
    print(type(num))


# ==============================================================================
# Task 13: Integer / Float Conversion
# ==============================================================================
def task13():
    print("\n--- Task 13 ---")
    num = float("25.6")
    print(num)
    print(type(num))


# ==============================================================================
# Task 14: Input Age
# ==============================================================================
def task14():
    print("\n--- Task 14 ---")
    try:
        age = int(input("Enter your age: "))
        print(f"Age: {age}")
    except ValueError:
        print("Invalid input! Please enter an integer.")


# ==============================================================================
# Task 15: Input Two Numbers and Sum
# ==============================================================================
def task15():
    print("\n--- Task 15 ---")
    try:
        n1 = int(input("Enter first number: "))
        n2 = int(input("Enter second number: "))
        print(f"The sum of {n1} and {n2} is: {n1 + n2}")
    except ValueError:
        print("Invalid input! Please enter integers.")


# ==============================================================================
# Task 16: Student Details Formatting
# ==============================================================================
def task16():
    print("\n--- Task 16 ---")
    try:
        sname = input("Enter name: ")
        sage = int(input("Enter age: "))
        cgpa = float(input("Enter CGPA: "))
        print(f"My name is {sname}. I am {sage} years old and my CGPA is {cgpa}.")
    except ValueError:
        print("Invalid input! Please enter valid numeric values for age and CGPA.")


# ==============================================================================
# Task 17: Celsius to Fahrenheit Conversion
# ==============================================================================
def task17():
    print("\n--- Task 17 ---")
    try:
        c = float(input("Enter temperature in Celsius: "))
        f = (c * 9 / 5) + 32
        print(f"Temperature in Fahrenheit: {f:.2f}")
    except ValueError:
        print("Invalid input! Please enter a valid number.")


# ==============================================================================
# Task 18: Even or Odd Determination
# ==============================================================================
def task18():
    print("\n--- Task 18 ---")
    try:
        number = int(input("Enter number: "))
        if number % 2 == 0:
            print(f"{number} is Even")
        else:
            print(f"{number} is Odd")
    except ValueError:
        print("Invalid input! Please enter an integer.")


def run_all():
    # Non-interactive tasks
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()
    task9()
    task10()
    task11()
    task12()
    task13()

    # Interactive tasks (wrapped to safely catch exit)
    try:
        task14()
        task15()
        task16()
        task17()
        task18()
    except (EOFError, KeyboardInterrupt):
        print("\nInput skipped.")


if __name__ == "__main__":
    run_all()
