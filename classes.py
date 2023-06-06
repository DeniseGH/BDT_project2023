from synthetic_data import random_IDs, name_surname, age, income, delay, suffering, status, amount, purpose, term, \
    monthly_dept, interest_rate, duration
import sqlite3


class Client:

    def __init__(self, costumer_id: str, name: str, age: int, income: int, delay: int, suffering: bool):
        self.costumer_id = costumer_id
        self.name = name
        self.age = age
        self.income = income
        self.delay = delay
        self.suffering = suffering

    def create_random_client(self):
        client = self(random_IDs(), name_surname(), age(), income(), delay(), suffering())
        return client


class Loan:

    def __init__(self, loan_id: str, status: str, amount: int, purpose: str, term: str):
        self.loan_id = loan_id
        self.status = status
        self.amount = amount
        self.purpose = purpose
        self.term = term

    def create_random_loan(self):
        income = Client.create_random_client(Client).income
        statuss = status()
        loan_amount = amount(income, statuss)

        loan = self(random_IDs(), statuss, loan_amount, purpose(loan_amount), term(loan_amount))
        return loan


class Fully_Paid(Loan):

    def __init__(self, loan_id, status, amount, purpose, term, monthly_dept, interest_rate, duration):
        super().__init__(loan_id, status, amount, purpose, term)
        self.monthly_dept = monthly_dept
        self.interest_rate = interest_rate
        self.duration = duration
        self.delay = delay

    def adding_fully_paid_loans(self):
        conn = sqlite3.connect('PROVA2.db')
        cur = conn.cursor()

        fully_paid_records = []
        cur.execute("SELECT * FROM loan_records WHERE Loan_Status = 'Fully Paid'")
        rows = cur.fetchall()

        for row in rows:
            fully_paid_records.append(row)

        fp_loans = []
        for record in fully_paid_records:
            id_loan = record[0]
            loan_amount = record[6]
            income =record[8]
            purpose_fp = record[9]
            dept_mon = monthly_dept(income)
            rate_int = interest_rate(purpose_fp)
            dur_fp = duration(loan_amount, rate_int, dept_mon)
            delay_fp = delay()
            fp_loans.append([id_loan, loan_amount, dept_mon, dur_fp, rate_int, delay_fp])

        return fp_loans


