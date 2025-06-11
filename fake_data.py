import random
import datetime
import db


def generate_expenses(num_entries, start_date=None, end_date=None):
	categories = ["Food", "Transport", "Entertainment", "Health", "Education", "Others"]
	for _ in range(num_entries):
		expense_name = f"Expense {_}"
		category = random.choice(categories)
		cost = round(random.uniform(1, 500), 2)
		if start_date and end_date:
			time = random_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
		else:
			time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		db.insert_groceries(expense_name, category, cost, time)


def generate_balance(balance, num_entries, start_date=None, end_date=None):
	for _ in range(num_entries):
		if start_date and end_date:
			time = random_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
		else:
			time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		db.insert_balance(balance, time)


def random_date(start, end):
	return start + datetime.timedelta(
		seconds=random.randint(0, int((end - start).total_seconds())))
