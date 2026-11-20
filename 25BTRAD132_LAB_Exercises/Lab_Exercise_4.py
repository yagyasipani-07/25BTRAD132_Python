#Lab_Exercise_11
def read_log():
    try:
        f = open("log.txt", "r")

        error = warning = info = 0

        for line in f:
            if "ERROR" in line:
                error += 1
            if "WARNING" in line:
                warning += 1
            if "INFO" in line:
                info += 1

        f.close()

        print("ERROR:", error)
        print("WARNING:", warning)
        print("INFO:", info)

    except FileNotFoundError:
        print("File not found!")

read_log()

#Lab_Exercise_12
def add():
    f = open("student.txt", "a")
    r = input("Roll: ")
    n = input("Name: ")
    m = input("Marks: ")
    f.write(r + "," + n + "," + m + "\n")
    f.close()

def display():
    f = open("student.txt", "r")
    for line in f:
        print(line.strip())
    f.close()

def search():
    r = input("Enter roll: ")
    f = open("student.txt", "r")

    for line in f:
        data = line.strip().split(",")
        if data[0] == r:
            print("Name:", data[1], "Marks:", data[2])
            break
    else:
        print("Not found!")

    f.close()

def update():
    r = input("Enter roll to update: ")
    f = open("student.txt", "r")
    records = f.readlines()
    f.close()

    f = open("student.txt", "w")
    found = False

    for line in records:
        data = line.strip().split(",")
        if data[0] == r:
            data[1] = input("New name: ")
            data[2] = input("New marks: ")
            found = True
        f.write(",".join(data) + "\n")

    f.close()
    print("Updated!" if found else "Not found!")

def main():
    while True:
        ch = input("\n1.Add 2.Display 3.Search 4.Update 5.Exit: ")

        if ch == '1':
            add()
        elif ch == '2':
            display()
        elif ch == '3':
            search()
        elif ch == '4':
            update()
        elif ch == '5':
            break

main()

#Lab_Exercise_13
import csv

# Create and write CSV file
def create_file():
    with open("employee.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["Name", "Basic"])

        n = int(input("Enter number of employees: "))

        for i in range(n):
            name = input("Enter employee name: ")
            basic = float(input("Enter basic salary: "))
            writer.writerow([name, basic])

    print("\nEmployee file created successfully!")


# Read CSV and calculate payroll
def payroll():
    with open("employee.csv", "r") as f:
        reader = csv.DictReader(f)

        print("\n--- PAYROLL SUMMARY ---")

        for row in reader:
            name = row["Name"]
            basic = float(row["Basic"])

            hra = basic * 0.20
            da = basic * 0.10
            pf = basic * 0.12

            gross = basic + hra + da
            net = gross - pf

            print("\nEmployee:", name)
            print("Basic Salary:", basic)
            print("HRA:", hra)
            print("DA:", da)
            print("Gross Salary:", gross)
            print("Deduction:", pf)
            print("Net Salary:", net)


create_file()
payroll()