import sqlite3
from classes import Client, Loan
import random
def create_ongoing_table(rows):

    conn = sqlite3.connect('PROVA2.db')
    cur = conn.cursor()

    # Creazione della nuova tabella "ongoing_records" con la stessa struttura di "loan_records"
    cur.execute('''CREATE TABLE IF NOT EXISTS ongoing_records
                AS SELECT * FROM loan_records
                WHERE 0''')
    for _ in range(rows):
        clients = Client.create_random_client(Client)
        loans = Loan.create_random_loan(Loan)
    # Impostazione di tutti i valori della colonna "status" come "ongoing"
        delay = random.randint(0,1)
        loan_status = "Ongoing"
        suffering = "No"
        cur.execute(
            "INSERT INTO ongoing_records (Costumer_ID, Name_Surname, Age, Annual_Income, CRIF_Delay, CR_suffering, Loan_ID, Loan_Status, Initial_Loan_amount, Purpose, Term) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                clients.costumer_id, clients.name, clients.age, clients.income, delay, suffering, loans.loan_id,
                loan_status, loans.amount, loans.purpose, loans.term))

    conn.commit()
    conn.close()
