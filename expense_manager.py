class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def view_expenses(self):
        return list(self.expenses)

    def sort_by_date(self):
        self.expenses.sort(key=lambda expense: expense.date)

    def filter_by_month(self, year_month):
        return [expense for expense in self.expenses if expense.month_key() == year_month]

    def categories(self):
        return sorted({expense.category for expense in self.expenses})

    def clear(self):
        self.expenses.clear()