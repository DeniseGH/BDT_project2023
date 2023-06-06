import math
import random
import string
from faker import Faker

def random_IDs():
    # dividing ID in 5 parts
    p1 = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    p2 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    p3 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    p4 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    p5 = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    #uniting ID parts for creating complete ID
    IDs = f"{p1}-{p2}-{p3}-{p4}-{p5}"
    return IDs

def name_surname():
    faker = Faker('it_IT')  # choosing italian names
    first_name = faker.first_name()
    last_name = faker.last_name()
    complete_name = f"{first_name} {last_name}"
    return complete_name

def age():
    aging = random.randint(20, 60)
    return aging

def income():
    income = random.randint(100, 600)*100
    return income

def delay():
    weights = [0.7, 0.25, 0.05]
    choices = [0, 1, 2]
    delay = random.choices(choices, weights=weights)[0]
    return delay

def suffering():
    choices = ["No", "Yes"]
    weights = [0.8, 0.2]
    suffering = random.choices(choices, weights=weights)[0]
    return suffering

def status():
    status = ['Declined', 'Charged off', 'Fully Paid']
    weights = [0.05, 0.10, 0.85]
    loanStatus = random.choices(status, weights=weights)[0]
    return loanStatus

def amount(income, status):
    if status == "Declined":
        LA = random.randint(40, 60) * 1000
    else:
        LA = random.randint(20, 2*(income/100))*100
    return LA

def purpose(amount):
    purposes = ["Debt Consolidation", "Home improvement", "Vacation or travel", "Wedding expenses", "Education or tuition fees"]
    if amount > 30000:
        loanPurpose = random.choice(purposes[0:2])
    else:
        loanPurpose = random.choice(purposes)
    return loanPurpose

def term(amount):
    if amount > 10000:
        term = "Long Term"
    else:
        term = "Short Term"
    return term

def monthly_dept(income):
    mont_dept = (income/12) * 0.33
    #monthly_rate = random.randint(mont_dept-300, mont_dept)
    return round(mont_dept, 2)

def interest_rate(purpose):
    if purpose == "Debt Consolidation":
        interest_rate = random.uniform(2,3)
    else:
        interest_rate = random.uniform(2,3)
    return round(interest_rate, 1)


def duration(amount, interest_rate, monthly_dept):
    print("amount, interest_rate, monthly_dept")
    print(amount, interest_rate,monthly_dept )

    monthly_interest_rate = interest_rate / 12 / 100
    print(monthly_interest_rate)
    number_of_months = -math.log(1 - (monthly_interest_rate * amount) / monthly_dept) / math.log(1 + monthly_interest_rate)
    return round(number_of_months)


