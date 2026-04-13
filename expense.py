from datetime import datetime

class Expense:
    def __init__(self, date, category, amount, description):
        self.date = self._parse_date(date)
        self.category = category.strip()
        self.amount = self._parse_amount(amount)
        self.description = description.strip()

    def _parse_amount(self, amount):
        try:
            return float(amount)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid amount: {amount}")

    def _parse_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

    def month_key(self):
        return self.date[:7]  # YYYY-MM

    def to_dict(self):
        return {
            "date": self.date,
            "category": self.category,
            "amount": f"{self.amount:.2f}",
            "description": self.description,
        }

    def __repr__(self):
        return f"Expense(date={self.date!r}, category={self.category!r}, amount={self.amount:.2f}, description={self.description!r})"