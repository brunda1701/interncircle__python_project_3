
import csv
import os
from datetime import datetime
from collections import defaultdict

FILE = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]


# Create CSV file if it does not exist
def create_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


# Load all expenses
def load_expenses():
    create_file()

    with open(FILE, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# Save a new expense
def save_expense(row):
    create_file()

    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(row)


# Add a new expense
def add_expense():
    print("\n--- Add New Expense ---")

    while True:
        date = input("Enter date (YYYY-MM-DD): ")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date! Please try again.")

    category = input("Enter category: ").strip()

    while not category:
        category = input("Category cannot be empty. Enter category: ").strip()

    description = input("Enter description: ").strip()

    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be positive.")
            else:
                break

        except ValueError:
            print("Please enter a valid number.")

    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": str(amount)
    }

    save_expense(expense)
    print("Expense added successfully!")


# Display all expenses
def view_expenses(rows=None):
    if rows is None:
        rows = load_expenses()

    print("\n--- Expense Records ---")

    if not rows:
        print("No expenses found.")
        return

    print("-" * 65)
    print(f"{'Date':<14}{'Category':<15}{'Description':<20}{'Amount':>10}")
    print("-" * 65)

    for row in rows:
        print(
            f"{row['date']:<14}"
            f"{row['category']:<15}"
            f"{row['description']:<20}"
            f"{float(row['amount']):>10.2f}"
        )

    print("-" * 65)


# Filter expenses
def filter_expenses():
    rows = load_expenses()

    print("\n1. Filter by Category")
    print("2. Filter by Month")

    choice = input("Enter your choice: ")

    if choice == "1":
        category = input("Enter category: ").strip().lower()

        filtered = [
            row for row in rows
            if row["category"].lower() == category
        ]

    elif choice == "2":
        month = input("Enter month (YYYY-MM): ").strip()

        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Invalid month format.")
            return

        filtered = [
            row for row in rows
            if row["date"][:7] == month
        ]

    else:
        print("Invalid choice.")
        return

    view_expenses(filtered)


# Calculate spending summaries
def show_summary():
    rows = load_expenses()

    if not rows:
        print("No expenses available.")
        return

    totals = defaultdict(float)

    grand_total = 0
    biggest = 0

    for row in rows:
        amount = float(row["amount"])

        totals[row["category"]] += amount
        grand_total += amount
        biggest = max(biggest, amount)

    print("\n--- Expense Summary ---")

    for category, total in totals.items():
        print(f"{category}: Rs. {total:.2f}")

    print("-" * 30)
    print(f"Grand Total: Rs. {grand_total:.2f}")
    print(f"Biggest Expense: Rs. {biggest:.2f}")


# Main menu
def main():
    create_file()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter Expenses")
        print("4. View Summary")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            filter_expenses()

        elif choice == "4":
            show_summary()


        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
