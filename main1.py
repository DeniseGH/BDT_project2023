from classes import Client, Loan, Fully_Paid
from setup_database import setup_database
from insert_loan_records import insert_loan_records
from add_fully_paid import add_fully_paid
from create_ongoing_records import create_ongoing_table

# configuring database
setup_database()

# creating records and adding to "loan_records" table
insert_loan_records(Client, Loan, 100)


# adding records to "fully_paid" table
add_fully_paid(Fully_Paid)

# creating ongoing records and adding to table
create_ongoing_table(50)

print("Operazioni completate con successo.")