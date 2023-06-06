import math
from datetime import datetime


def calculate_loan_duration(amount, interest_rate, annual_income):
    monthly_payment = (annual_income/12) * 0.3
    monthly_interest_rate = interest_rate / 12 / 100
    number_of_months = -math.log(1 - (monthly_interest_rate * amount) / monthly_payment) / math.log(1 + monthly_interest_rate)
    return round(number_of_months, 2)


loan_amount = 15000
interest_rate_annual = 9.3
annual_income = 22492

#loan_duration = calculate_loan_duration(loan_amount, interest_rate_annual, annual_income)
#print("The loan will be repaid in approximately", loan_duration, "months.")

def check_loan_ids_csv(transactions_list_ontime, transactions_list_late, csv_file_path):
    loan_ids_ontime = set(transaction.loan_id for transaction in transactions_list_ontime)
    loan_ids_late = set(transaction.loan_id for transaction in transactions_list_late)

    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)  # Store the header row

        # Find the index of the loan_id, months_left, and late_transactions columns in the header
        loan_id_index = header.index("loan_id")
        months_left_index = header.index("months_left")
        late_transactions_index = header.index("late_transactions")

        # Create a list to hold the updated rows
        updated_rows = []

        for row in csv_reader:
            loan_id = row[loan_id_index]
            months_left = int(row[months_left_index])
            late_transactions = int(row[late_transactions_index])

            if loan_id in loan_ids_ontime:
                months_left -= 1
            elif loan_id in loan_ids_late:
                months_left -= 1
                late_transactions += 1

            row[months_left_index] = str(months_left)
            row[late_transactions_index] = str(late_transactions)
            updated_rows.append(row)

    # Overwrite the same CSV file with the updated rows
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)  # Write the header row
        csv_writer.writerows(updated_rows)  # Write the updated rows

    return csv_file_path

# check_loan_ids_csv(transactions_list_ontime, transactions_list_late, csv_file_path)



import sqlite3

# Database file path
database_file = "../PROVA(2).db"

# Connect to the database
conn = sqlite3.connect(database_file)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Query to retrieve table names
table_query = "SELECT name FROM sqlite_master WHERE type='table'"

# Execute the query
cursor.execute(table_query)

# Fetch all rows from the result set
tables = cursor.fetchall()

# Print the table names
for table in tables:
    print(table[0])

# Close the cursor and the connection
cursor.close()
conn.close()



def initialize_payment_csv():
    # Read loan IDs from the "ongoing loan ids" CSV file
    with open('ongoing_loan_ids.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        loan_ids = [row[0] for row in reader]

    # Prepare data for CSV rows
    customer_ids = range(1, len(loan_ids) + 1)
    payment_amount = 100 # DA PRENDERE da un altro file ---------------------------
    late_transactions = 0
    months_left = 100
    loan_amount = 40000


    # Create the CSV file and write rows
    with open('payments_records.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'loan_id', 'payment_amount', 'loan_amount', 'months_left', 'late_transactions'])
        for customer_id, loan_id in zip(customer_ids, loan_ids):
            print(loan_id)
            writer.writerow([customer_id, loan_id, payment_amount, loan_amount, months_left, late_transactions])


#print("CSV file 'payments_records.csv' has been created.")
#initialize_payment_csv()


# def _deserialize_transactions(json_data) -> List[Transaction]:
# #     '''
# #     :param json_data: the data extracted from the json files
# #     :return: list of elements of class Transaction
# #     '''
# #     # Deserialize JSON data into a list of Transaction objects
# #     transaction_list = []
# #     json_list = json.loads(json_data)
# #     for item in json_list:
# #         transaction = Transaction(item['customer_id'], item['loan_id'], item['amount'], item['time'], item['day'])
# #         transaction_list.append(transaction)
# #
# #     return transaction_list



# directory_path = create_directory_path("2023/05/01")
# print(directory_path)
#
# json_data_ontime = find_json(directory_path)
# transactions_list_ontime = _deserialize_transactions(json_data_ontime)
#
# directory_path_late = create_directory_path("2023/05/16")
# json_data_late = find_json(directory_path_late)
# transactions_list_late =_deserialize_transactions(json_data_late)
#
# csv_file_path="payments_records.csv"


    # for loan_id in loan_ids_ontime:
    #     months_left = int(r.hget(loan_id, "months_left"))
    #     if months_left > 0:
    #         r.hset(loan_id, "months_left", months_left - 1)
    #     else:
    #         cancel_loan(loan_id, r)
    #
    # for loan_id in loan_ids_late:
    #     months_left = int(r.hget(loan_id, "months_left"))
    #     late_transactions = int(r.hget(loan_id, "late_transactions"))
    #     if months_left > 0:
    #         r.hset(loan_id, "months_left", months_left - 1)
    #         r.hset(loan_id, "late_transactions", late_transactions + 1)
    #     else:
    #         cancel_loan(loan_id, r)





# number_of_loans=10
#
# # We assume all the payments are due the same day, the user can choose the date here:
# date = "2023/06/15"
#
# json_file_path = "loan_repayments_transactions"
#
# # Update the JSON file creating 2 directories:
# update_json_file(json_file_path, date, number_of_loans)
#
# # To be updated
# directory_path = create_directory_path(date)
#
# # json data of the transactions on time
# json_data_ontime = find_json(directory_path)
# print(json_data_ontime)
# # json data deserialized in a list of transactions
# transactions_list_ontime = _deserialize_transactions(json_data_ontime)
# print(transactions_list_ontime[1])
#
# new_date = get_date_after_16_days(date)
# # To be updated
# directory_path_late = create_directory_path(new_date)
#
# # json data of the transactions late
# json_data_late = find_json(directory_path_late)
#
# # json data deserialized in a list of transactions
# transactions_list_late =_deserialize_transactions(json_data_late)
#
# # Main function that updates the Redis file, updating the late transactions and the months left
# check_loan_ids(transactions_list_ontime, transactions_list_late)


import datetime

def get_first_day_of_next_month1(date):
    # Parse the input date
    input_date = datetime.datetime.strptime(date, "%Y/%m/%d").date()

    # Get the year and month of the input date
    year = input_date.year
    month = input_date.month

    # Increment the month by 1
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1

    # Create a new date object for the first day of the next month
    first_day_of_next_month = datetime.date(year, month, 1)

    # Return the first day of the next month
    return first_day_of_next_month.strftime("%Y/%m/%d")

date = "2023/04/01"
first_day_of_next_month = get_first_day_of_next_month(date)
print(type(first_day_of_next_month))
