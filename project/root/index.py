from flask import Flask, jsonify, request

from root.model.expense import Expense, ExpenseSchema
from root.model.income import Income, IncomeSchema
from root.model.transaction_type import TransactionType

app = Flask(__name__)

transactions = [
  Income('Salary', 5000),
  Income('Dividends', 200),
  Expense('pizza', 50),
  Expense('Rock Concert', 100)
]


@app.route('/')
def index():
  transactions[0].print()
  return "Hello, world!"#,transactions[0]

@app.route('/incomes')
def get_incomes():
  schema = IncomeSchema(many=True)
  incomes = schema.dump(
    filter(lambda t: t.type == TransactionType.INCOME, transactions)
  )
  return jsonify(incomes.data)


@app.route('/incomes', methods=['POST'])
def add_income():
  income = IncomeSchema().load(request.get_json())
  transactions.append(income.data)
  return "", 204


@app.route('/expenses')
def get_expenses():
  schema = ExpenseSchema(many=True)
  expenses = schema.dump(
      filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
  )
  return jsonify(expenses.data)


@app.route('/expenses', methods=['POST'])
def add_expense():
  expense = ExpenseSchema().load(request.get_json())
  transactions.append(expense.data)
  return "", 204


if __name__ == "__main__":
    app.run(debug=True)