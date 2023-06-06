import json
from typing import List


# Once the loan has been assigned, the bank receives daily transactions from its borrowers who repay their loans.
# It is essential for us to monitor these payments so that we can update our loan records file when the loan
# is fully paid off or when it is charged off. Therefore, we are creating the Transaction class here,
# which we will use when extracting data from a JSON file that we assume is provided to us every day at midnight,
# containing the day's transactions.

class Transaction:

    def __init__(self, customer_id, loan_id, amount, time, day):
        self.customer_id = customer_id
        self.loan_id = loan_id
        self.amount = amount
        self.day = day
        self.time = time

    def __str__(self):
        return f"Customer ID: {self.customer_id}\nLoan ID: {self.loan_id}\nAmount: {self.amount}\nDay: {self.day}\nTime: {self.time}\n------------------"


def read_json(json_file_name: str):
    '''
    :param json_file_name: name of the json file where the transactions are stored
    :return: the json data
    '''
    # Read JSON data from file
    with open(json_file_name, 'r') as file:
        json_data = file.read()

    print(type(json_data))
    print("--------------------------")
    return json_data


def _deserialize_transactions(json_data_list) -> List[Transaction]:
    '''
    :param json_data_list: it takes a list of json data
    :return: a list of elements of class Transaction
    '''
    # Deserialize JSON data into a list of Transaction objects
    transaction_list = []
    for json_data in json_data_list:
        lines = json_data.split('\n')  # Split the JSON data into separate lines

        for line in lines:
            if line.strip():  # Skip empty lines
                transaction_dict = json.loads(line)  # Parse each line as a separate JSON object
                transaction = Transaction(transaction_dict['customer_id'], transaction_dict['loan_id'],
                                          transaction_dict['amount'], transaction_dict['time'], transaction_dict['day'])
                transaction_list.append(transaction)

    return transaction_list
