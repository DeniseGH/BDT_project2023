import sqlite3


def insert_loan_records(Client, Loan, rows):
    conn = sqlite3.connect('PROVA2.db')
    cur = conn.cursor()

    for _ in range(rows):
        clients = Client.create_random_client(Client)
        loans = Loan.create_random_loan(Loan)
        cur.execute("INSERT INTO loan_records (Costumer_ID, Name_Surname, Age, Annual_Income, CRIF_Delay, CR_suffering, Loan_ID, Loan_Status, Initial_Loan_amount, Purpose, Term) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (clients.costumer_id, clients.name, clients.age, clients.income, clients.delay, clients.suffering, loans.loan_id, loans.status, loans.amount, loans.purpose, loans.term))

        if clients.delay >= 2 or clients.suffering == "Yes":
            cur.execute("UPDATE loan_records SET Loan_Status = ? WHERE CRIF_delay = ? AND CR_suffering = ?", ("Declined", clients.delay, clients.suffering))

    conn.commit()
    conn.close()