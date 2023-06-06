import os
import sqlite3
from datetime import datetime
import datetime
import redis

from add_fully_paid import add_fully_paid
from classes import Fully_Paid
from synthetic_data import delay, duration, interest_rate, monthly_dept


def find_json(directory_path):
    '''
    :param directory_path: path of the directory containing the json files produced by Spark
    :return: a list (of length equal to the number of JSON files in the directory) containing JSON data.
    '''
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

    json_data_list = []

    for json_file in json_files:
        with open(os.path.join(directory_path, json_file), 'r') as file:
            json_data = file.read()

        json_data_list.append(json_data)

    return json_data_list


def create_directory_path(date):
    '''
    :param date:
    :return: the path to get to the directory
    '''
    parts = date.split('/')
    return 'loan_repayments_transactions_' + parts[0] + '/' + parts[1] + '/' + parts[2]


def check_loan_ids(transactions):
    '''
    :param transactions: list of the transactions of the selected month
    '''
    transactions_list_ontime = []
    transactions_list_late =[]

    for transaction in transactions:
        day = int(transaction.day.split("/")[2])  # Extract the day part and convert it to an integer
        if day <= 27:
            transactions_list_ontime.append(transaction)
        else:
            transactions_list_late.append(transaction)

    loan_ids_ontime = set(transaction.loan_id for transaction in transactions_list_ontime)
    loan_ids_late = set(transaction.loan_id for transaction in transactions_list_late)

    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, db=0)

    for loan_id in loan_ids_ontime.union(loan_ids_late):
        months_left = int(r.hget(loan_id, "months_left"))
        print(months_left)
        if months_left > 1:
            r.hset(loan_id, "months_left", months_left - 1)
            if loan_id in loan_ids_late:
                late_transactions = int(r.hget(loan_id, "late_transactions"))
                r.hset(loan_id, "late_transactions", late_transactions + 1)
        else:
            cancel_loan(loan_id, r)

    print("Loan data has been updated in Redis.")


def cancel_loan(loan_id, r):
    '''
    :param loan_id: loan_id that needs to be cancelled from the ongoing
    :param r: redis connector
    '''

    print("loan_id")
    print(loan_id)
    print("type(loan_id)")
    print(type(loan_id))
    # Connect to the SQLite database
    conn = sqlite3.connect("PROVA2.db")
    cursor = conn.cursor()

    # Execute a SELECT query to fetch all data from the table
    query = "SELECT * FROM ongoing_records WHERE loan_id = ?"
    cursor.execute(query, (loan_id,))

    row = cursor.fetchone()

    cursor.execute("INSERT INTO loan_records (Loan_ID, Costumer_ID, Name_Surname, Age, CRIF_delay, CR_suffering, Initial_Loan_amount, Term, Annual_income, Purpose, Loan_Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

    updated = "UPDATE loan_records SET Loan_Status = ? WHERE Loan_ID = ?"
    cursor.execute(updated, ("Fully Paid", loan_id))

    deleted = "DELETE FROM ongoing_records WHERE loan_id = ?"
    cursor.execute(deleted, (loan_id,))

    fully_paid_records = []

    query2 = "SELECT * FROM loan_records WHERE loan_id = ?"
    cursor.execute(query2, (loan_id,))

    rows = cursor.fetchone()
    record=[]
    for row in rows:
        record.append(row)

    fp_loans = []
   # for record in fully_paid_records:
    id_loan = record[0]
    loan_amount = int(record[6])
    purpose_fp = record[9]
    dept_mon = monthly_dept(loan_amount)
    rate_int = interest_rate(purpose_fp)
    dur_fp = duration(loan_amount, rate_int, dept_mon)
    delay_fp = delay()
    fp_loans.append([id_loan, loan_amount, dept_mon, dur_fp, rate_int, delay_fp])

    for row in fp_loans:
        cursor.execute("INSERT INTO fully_paid (Loan_ID, Loan_Amount, Monthly_dept, Duration, Interest_rate, Delay) VALUES (?, ?, ?, ?, ?, ?)",
            row)

    # Close the database connection
    conn.commit()
    conn.close()

    # Delete the loan from Redis
    r.delete(loan_id)
    print("Loan ID: ", loan_id, " has been canceled from Redis")

def get_first_day_of_next_month(date):
    '''
    :param date: takes a date in this format "%Y/%m/%d" with day 01
    :return: returns a date in this format "%Y/%m/%d" with day 01 and the following month
    '''
    # Parse the input date
    input_date = datetime.datetime.strptime(date, "%Y/%m/%d").date()

    # Get the year and month of the input date
    year = input_date.year
    month = input_date.month

    # Increment the month by 1
    if month == 12: # in case of December
        year += 1
        month = 1
    else:
        month += 1

    # Create a new date object for the first day of the next month
    first_day_of_next_month = datetime.date(year, month, 1)

    # Return the first day of the next month
    return first_day_of_next_month.strftime("%Y/%m/%d")

