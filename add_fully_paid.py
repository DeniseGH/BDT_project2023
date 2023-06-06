import sqlite3


def add_fully_paid(Fully_Paid):
    conn = sqlite3.connect('PROVA2.db')
    cur = conn.cursor()

    fp_loans = Fully_Paid.adding_fully_paid_loans(Fully_Paid)
    for row in fp_loans:
        cur.execute("INSERT INTO fully_paid (Loan_ID, Loan_Amount, Monthly_dept, Duration, Interest_rate, Delay) VALUES (?, ?, ?, ?, ?, ?)",
            row)

    conn.commit()
    conn.close()