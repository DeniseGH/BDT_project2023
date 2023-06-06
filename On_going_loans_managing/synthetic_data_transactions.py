import csv
import random
import sqlite3
import string
from datetime import datetime, timedelta

from synthetic_data import monthly_dept


def generate_loan_ids_csv(num_rows):
    def generate_loan_id():
        characters = string.ascii_letters + string.digits
        loan_id = ''.join(random.choices(characters, k=16))
        return loan_id

    # Generate loan IDs
    loan_ids = [generate_loan_id() for _ in range(num_rows)]

    # Write loan IDs to CSV file
    filename = "ongoing_loan_ids.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["loan_id"]) # Write header
        writer.writerows([[loan_id] for loan_id in loan_ids])

    print(f"CSV file '{filename}' created successfully with {num_rows} rows.")


# Generate a random transaction amount
def generate_amount(loan_id):
    conn = sqlite3.connect("PROVA2.db")
    cursor = conn.cursor()

    query = "SELECT Initial_Loan_amount FROM ongoing_records WHERE loan_id = ?"
    cursor.execute(query, (loan_id,))
    row = cursor.fetchone()

    dept = monthly_dept(row[0])

    # Close the database connection
    conn.commit()
    conn.close()

    return dept

# Generate a random timestamp for a given day
def generate_timestamp():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f" {hour:02d}:{minute:02d}:{second:02d}"

def generate_transactions_for_day(loan_ids: list, day, num_transactions: int):
    transactions = []

    # Calculate the start and end dates for the 15-day range
    end_date = datetime.strptime(day, "%Y/%m/%d")
    print("I am now simulating transactions of 1 month until " + str(end_date))

    for i in range(len(loan_ids)):
        # Generate a random date within the interval
        random_date = end_date - timedelta(days=random.randint(0, 30))

        loan_id = loan_ids[i]
        amount = generate_amount(loan_id)
        timestamp = generate_timestamp()
        customer_id = random.randint(1, 1000)
        transaction = {
            "customer_id": customer_id,
            "loan_id": loan_id,
            "amount": amount,
            "day": random_date.strftime("%Y/%m/%d"),
            "time": timestamp
        }
        transactions.append(transaction)
        print(transaction)

    return transactions


def generate_transactions_for_day1(loan_ids, day, num_transactions: int):
    transactions = []

    # Calculate the start and end dates for the 15-day range
    end_date = datetime.strptime(day, "%Y/%m/%d")
    start_date = end_date - timedelta(days=30)
    print("I am now simulating transactions from "+str(start_date) + " to "+ str(end_date))

    for i in range(num_transactions):
        # Generate a random date within the 15-day range
        random_date = start_date + timedelta(days=random.randint(0, 15))

        loan_id = loan_ids[i]
        amount = generate_amount()
        timestamp = generate_timestamp()
        customer_id = random.randint(1, 1000)
        transaction = {
            "customer_id": customer_id,
            "loan_id": loan_id,
            "amount": amount,
            "day": random_date.strftime("%Y/%m/%d"),
            "time": timestamp
        }
        transactions.append(transaction)

    return transactions






