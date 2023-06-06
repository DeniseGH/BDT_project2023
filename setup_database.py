import sqlite3
def setup_database():
    conn = sqlite3.connect('PROVA2.db')
    cur = conn.cursor()

    # Creazione delle tabelle nel database
    loans_records = cur.execute('''CREATE TABLE IF NOT EXISTS loan_records
                        (Loan_ID TEXT,
                        Costumer_ID TEXT,
                        Name_Surname TEXT,
                        Age INTEGER,
                        CRIF_delay INTEGER,
                        CR_suffering BOOLEAN,
                        Initial_Loan_amount INTEGER,
                        Term TEXT,
                        Annual_income INTEGER,
                        Purpose TEXT,
                        Loan_Status TEXT)''')

    fully_paid = cur.execute('''CREATE TABLE IF NOT EXISTS fully_paid
                        (Loan_ID TEXT,
                        Loan_Amount INT,
                        Monthly_dept INT,
                        Duration INTEGER,
                        Interest_rate INT,
                        Delay INT)''')

    conn.commit()
    conn.close()
