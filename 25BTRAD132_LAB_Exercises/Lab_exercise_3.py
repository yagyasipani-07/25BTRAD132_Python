#lab_Exercise_8
contacts = {}

while True:
    print("\n--- CONTACT BOOK ---")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Display Contacts")
    print("6. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        phone = input("Enter phone number: ")

        if phone in contacts:
            print("Contact already exists!")
        else:
            name = input("Enter name: ")
            email = input("Enter email: ")

            contacts[phone] = {
                "name": name,
                "email": email
            }

            print("Contact added successfully!")

    elif choice == 2:
        phone = input("Enter phone number: ")

        if phone in contacts:
            print(contacts[phone])
        else:
            print("Contact not found!")

    elif choice == 3:
        phone = input("Enter phone number: ")

        if phone in contacts:
            contacts[phone]["name"] = input("Enter new name: ")
            contacts[phone]["email"] = input("Enter new email: ")
            print("Contact updated!")
        else:
            print("Contact not found!")

    elif choice == 4:
        phone = input("Enter phone number: ")

        if phone in contacts:
            del contacts[phone]
            print("Contact deleted!")
        else:
            print("Contact not found!")

    elif choice == 5:
        if not contacts:
            print("Contact book is empty!")
        else:
            for phone, details in contacts.items():
                print("Phone:", phone, details)

    elif choice == 6:
        print("Exiting Contact Book...")
        break

    else:
        print("Invalid choice!")

#Lab_Exercise_9
def calculate_grade(marks):

    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    elif marks >= 70:
        return "C"
    elif marks >= 60:
        return "D"
    elif marks >= 50:
        return "E"
    else:
        return "F"


students = {}

n = int(input("Enter number of students: "))

for i in range(n):
    name = input("Enter student name: ")
    marks = float(input("Enter marks: "))

    if 0 <= marks <= 100:
        students[name] = marks
    else:
        print("Invalid marks!")

grades = {
    name: calculate_grade(marks)
    for name, marks in students.items()
}

print("\n--- STUDENT RESULTS ---")

for name, marks in students.items():
    print(f"Name: {name}")
    print(f"Marks: {marks}")
    print(f"Grade: {grades[name]}")
    print("-------------------")

#Lab_Exercise_10
n = int(input("Enter number of elements: "))

numbers = []

for i in range(n):
    value = int(input("Enter element: "))
    numbers.append(value)

frequency = {}

for num in numbers:
    if num in frequency:
        frequency[num] += 1
    else:
        frequency[num] = 1

print("\n--- ELEMENT FREQUENCY ---")

for num, count in frequency.items():
    print(num, ":", count)

