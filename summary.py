from collections import defaultdict

class Summary:
    def total_spent(self, expenses):
        return sum(exp.amount for exp in expenses)

    def monthly_summary(self, expenses):
        totals = defaultdict(float)
        for exp in expenses:
            totals[exp.month_key()] += exp.amount
        return dict(sorted(totals.items()))

    def category_breakdown(self, expenses):
        totals = defaultdict(float)
        for exp in expenses:
            totals[exp.category] += exp.amount
        return dict(sorted(totals.items(), key=lambda pair: pair[1], reverse=True))

    def highest_spending_category(self, expenses):
        breakdown = self.category_breakdown(expenses)
        if not breakdown:
            return None, 0.0
        category, amount = next(iter(breakdown.items()))
        return category, amount

    def average_daily_spending(self, expenses):
        totals = defaultdict(float)
        for exp in expenses:
            totals[exp.date] += exp.amount
        if not totals:
            return 0.0
        return sum(totals.values()) / len(totals)
