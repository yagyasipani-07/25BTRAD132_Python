# Name: Yagya Sipani
# USN: 25BTRAD132

import random

# ==============================================================================
# Lab Exercise 5: Number guessing game.
# ==============================================================================
def guess_the_number(min_num=1, max_num=100):
    print(f"\n--- Game Started (Range: {min_num} to {max_num}) ---")
    secret_number = random.randint(min_num, max_num)
    attempts = 0

    while True:
        try:
            guess = int(input(f"Attempt {attempts + 1} - Your guess: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        attempts += 1

        if guess == secret_number:
            print(f"You found {secret_number} in {attempts} attempts.")
            break

        # Calculate how far off the guess is
        distance = abs(secret_number - guess)

        if distance <= 3:
            print("Extremely close!")
        elif distance <= 10:
            print("Warm!")
        elif distance <= 25:
            print("Far")
        else:
            print("Way off! Too far")


# ==============================================================================
# Lab Exercise 6: Prime Number and Factorial Programs.
# ==============================================================================
def is_prime(num):
    """Checks if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def check_prime_demo():
    try:
        number = int(input("Enter a number to check if it is prime: "))
        if is_prime(number):
            print(f"{number} is a prime number.")
        else:
            print(f"{number} is not a prime number.")
    except ValueError:
        print("Invalid input. Please enter an integer.")


def factorial(n):
    """Calculates the factorial of a non-negative integer."""
    if n < 0:
        return "Undefined for negative numbers"
    elif n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result


def factorial_demo():
    try:
        num = int(input("Enter a number to find its factorial: "))
        print(f"The factorial of {num} is {factorial(num)}.")
    except ValueError:
        print("Invalid input. Please enter an integer.")


# ==============================================================================
# Lab Exercise 7: Fibonacci series using recursion.
# ==============================================================================
def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def print_fibonacci_series(total_terms):
    print("Fibonacci Series:")
    for i in range(total_terms):
        number = fibonacci(i)
        print(number, end=" ")
    print()


def fibonacci_demo():
    try:
        terms = int(input("How many Fibonacci numbers do you want? "))
        if terms < 0:
            print("Please enter a non-negative integer.")
        else:
            print_fibonacci_series(terms)
    except ValueError:
        print("Invalid input. Please enter an integer.")


if __name__ == "__main__":
    print("=== Lab Exercise 5: Number Guessing Game ===")
    try:
        guess_the_number(1, 100)
    except (EOFError, KeyboardInterrupt):
        print("\nSkipped.")

    print("\n=== Lab Exercise 6: Prime Check & Factorial ===")
    try:
        check_prime_demo()
        factorial_demo()
    except (EOFError, KeyboardInterrupt):
        print("\nSkipped.")

    print("\n=== Lab Exercise 7: Fibonacci Series ===")
    try:
        fibonacci_demo()
    except (EOFError, KeyboardInterrupt):
        print("\nSkipped.")
