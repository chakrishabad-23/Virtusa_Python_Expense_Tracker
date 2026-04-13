import os
from datetime import datetime

from expense import Expense
from expense_manager import ExpenseManager
from storage_manager import StorageManager
from summary import Summary

DEFAULT_FILENAME = "expenses.csv"
CATEGORIES = ["Food", "Travel", "Bills", "Entertainment", "Health", "Shopping", "Other"]


def print_menu():
    print("\nSmart Expense Tracker")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Show monthly summary")
    print("4. Show category breakdown")
    print("5. Plot category breakdown")
    print("6. Load expenses from file")
    print("7. Save expenses to file")
    print("8. Exit")


def read_non_empty(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Please enter a value.")


def prompt_date():
    while True:
        value = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")


def prompt_category():
    print("Choose a category:")
    for index, category in enumerate(CATEGORIES, start=1):
        print(f"{index}. {category}")
    print(f"{len(CATEGORIES) + 1}. Other")
    while True:
        choice = input("Select category number: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            if choice == len(CATEGORIES) + 1:
                return read_non_empty("Enter custom category: ")
        print("Please enter a valid option.")


def prompt_amount():
    while True:
        value = input("Enter amount: ").strip()
        try:
            amount = float(value)
            if amount < 0:
                raise ValueError
            return amount
        except ValueError:
            print("Invalid amount. Enter a positive number.")


def add_expense(expense_manager, storage_manager, current_filename):
    print("\nAdd a new expense")
    date = prompt_date()
    category = prompt_category()
    amount = prompt_amount()
    description = input("Enter description: ").strip()
    expense = Expense(date=date, category=category, amount=amount, description=description)
    expense_manager.add_expense(expense)
    try:
        storage_manager.save_to_file(current_filename, expense_manager.view_expenses())
        print(f"Expense added and saved to {current_filename}.")
    except Exception as exc:
        print(f"Expense added, but failed to save automatically: {exc}")


def show_expenses(expense_manager):
    expenses = expense_manager.view_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    expense_manager.sort_by_date()
    print("\nDate       | Category       | Amount   | Description")
    print("" + "-" * 60)
    for exp in expenses:
        print(f"{exp.date} | {exp.category:13} | {exp.amount:8.2f} | {exp.description}")


def show_monthly_summary(expense_manager, summary):
    totals = summary.monthly_summary(expense_manager.view_expenses())
    if not totals:
        print("No expenses to summarize.")
        return
    print("\nMonthly summary:")
    for month, amount in totals.items():
        print(f"{month}: {amount:.2f}")
    total = summary.total_spent(expense_manager.view_expenses())
    print(f"Total spent across months: {total:.2f}")


def show_category_breakdown(expense_manager, summary):
    breakdown = summary.category_breakdown(expense_manager.view_expenses())
    if not breakdown:
        print("No expenses to analyze.")
        return
    print("\nCategory breakdown:")
    for category, amount in breakdown.items():
        print(f"{category:15} {amount:8.2f}")
    category, amount = summary.highest_spending_category(expense_manager.view_expenses())
    if category:
        print(f"\nHighest spending category: {category} ({amount:.2f})")
        print(f"Suggestion: Review your {category} expenses and find ways to reduce them.")


def plot_category_breakdown(expense_manager, summary):
    breakdown = summary.category_breakdown(expense_manager.view_expenses())
    if not breakdown:
        print("No expenses to plot.")
        return
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is required to plot charts. Install it with 'pip install matplotlib'.")
        return
    labels = list(breakdown.keys())
    values = list(breakdown.values())
    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%.1f%%", startangle=140)
    plt.title("Expense Category Breakdown")
    plt.tight_layout()
    plt.show()


def load_expenses(expense_manager, storage_manager):
    filename = read_non_empty("Enter filename to load (CSV or JSON): ")
    try:
        expenses = storage_manager.load_from_file(filename)
        expense_manager.clear()
        for expense in expenses:
            expense_manager.add_expense(expense)
        print(f"Loaded {len(expenses)} expenses from {filename}.")
        return filename
    except FileNotFoundError:
        print("File not found. Check the filename and try again.")
    except Exception as exc:
        print(f"Failed to load expenses: {exc}")
    return None


def save_expenses(expense_manager, storage_manager):
    if not expense_manager.view_expenses():
        print("No expenses to save.")
        return
    filename = read_non_empty("Enter filename to save (CSV or JSON): ")
    try:
        storage_manager.save_to_file(filename, expense_manager.view_expenses())
        print(f"Saved {len(expense_manager.view_expenses())} expenses to {filename}.")
    except Exception as exc:
        print(f"Failed to save expenses: {exc}")


def load_default(expense_manager, storage_manager):
    if os.path.exists(DEFAULT_FILENAME):
        try:
            expenses = storage_manager.load_from_file(DEFAULT_FILENAME)
            for expense in expenses:
                expense_manager.add_expense(expense)
            print(f"Loaded {len(expenses)} expenses from {DEFAULT_FILENAME}.")
        except Exception:
            print(f"Could not load default file {DEFAULT_FILENAME}. Start with an empty ledger.")


def main():
    expense_manager = ExpenseManager()
    summary = Summary()
    storage_manager = StorageManager()
    current_filename = DEFAULT_FILENAME
    load_default(expense_manager, storage_manager)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_expense(expense_manager, storage_manager, current_filename)
        elif choice == "2":
            show_expenses(expense_manager)
        elif choice == "3":
            show_monthly_summary(expense_manager, summary)
        elif choice == "4":
            show_category_breakdown(expense_manager, summary)
        elif choice == "5":
            plot_category_breakdown(expense_manager, summary)
        elif choice == "6":
            loaded_filename = load_expenses(expense_manager, storage_manager)
            if loaded_filename:
                current_filename = loaded_filename
        elif choice == "7":
            save_expenses(expense_manager, storage_manager)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Please select a valid menu option.")


if __name__ == "__main__":
    main()