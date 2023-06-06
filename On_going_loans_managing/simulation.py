import redis
from On_going_loans_managing.analyzing_transactions import create_directory_path, find_json, check_loan_ids, \
    get_first_day_of_next_month
from On_going_loans_managing.initializing_synthetic_payments_records import initialize_payment_redis
from On_going_loans_managing.spark import get_date_after_n_days, update_json_file
from On_going_loans_managing.synthetic_data_transactions import generate_loan_ids_csv
from On_going_loans_managing.transaction import _deserialize_transactions

r = redis.Redis(host='localhost', port=6379, db=0)

# ################### Our Synthetic Data ################### #
# ------------------------------------------------------------

# Decide the number of ongoing loans we want to simulate
number_of_loans = 1000

# The name we want to assign to the main directory (the year will be concatenated)
print("You started your simulation with a number of loans equal to = ", number_of_loans)

# It creates a CSV file with list of loans
# generate_loan_ids_csv(number_of_loans)

# It initializes the payment records using Redis
initialize_payment_redis()

date = "2023/04/01"

json_file_path = "loan_repayments_transactions"

print("The directory will begin with the following name: ", json_file_path)
print("You chose to start your simulation the: ", date)

# We assume all the payments are due the same day (tipically the 27th of the month), the user can choose the date here:
for _ in range(1, 5):
    # Update the JSON file creating 2 directories:
    update_json_file(json_file_path, date, number_of_loans)

    # The 2 directory paths of the folders
    directory_path = create_directory_path(date)
    # directory_path_late = create_directory_path(new_date)

    # json data of the transactions on time
    json_data_ontime = find_json(directory_path)

    # json data deserialized in a list of transactions
    transactions_list_ontime = _deserialize_transactions(json_data_ontime)

    check_loan_ids(transactions_list_ontime)

    date = str(get_first_day_of_next_month(date))



# It removes the information from Redis to get ready for another simulation
r.flushall()
print("Redis is now flushed, you are ready to procede with another simulation")
