import csv
import json
import os
from expense import Expense

class StorageManager:
    def load_from_file(self, filename):
        filename = filename.strip()
        if filename.lower().endswith(".json"):
            return self.load_json(filename)
        return self.load_csv(filename)

    def save_to_file(self, filename, expenses):
        filename = filename.strip()
        if filename.lower().endswith(".json"):
            return self.save_json(filename, expenses)
        return self.save_csv(filename, expenses)

    def load_csv(self, filename):
        expenses = []
        with open(filename, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expense = Expense(
                    date=row["date"],
                    category=row["category"],
                    amount=row["amount"],
                    description=row["description"],
                )
                expenses.append(expense)
        return expenses

    def save_csv(self, filename, expenses):
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        with open(filename, "w", encoding="utf-8", newline="") as file:
            fieldnames = ["date", "category", "amount", "description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for expense in expenses:
                writer.writerow(expense.to_dict())

    def load_json(self, filename):
        expenses = []
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                expense = Expense(
                    date=item["date"],
                    category=item["category"],
                    amount=item["amount"],
                    description=item.get("description", ""),
                )
                expenses.append(expense)
        return expenses

    def save_json(self, filename, expenses):
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([expense.to_dict() for expense in expenses], file, indent=2)

    