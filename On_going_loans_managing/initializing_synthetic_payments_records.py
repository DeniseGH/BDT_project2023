import csv
import random

import redis

def initialize_payment_redis(loan_ids):
    r = redis.Redis(host='localhost', port=6379, db=0)
    # Read loan IDs from the "ongoing loan ids" CSV file

    # Prepare data for Redis
    loan_amount = random.randint(2000, 40000)

    # Save data to Redis
    for customer_id, loan_id in zip(range(1, len(loan_ids) + 1), loan_ids):
        r.hset(loan_id, "customer_id", customer_id)
        r.hset(loan_id, "loan_amount", loan_amount)
        r.hset(loan_id, "months_left", random.randint(3, 15))
        r.hset(loan_id, "late_transactions", random.randint(0, 2))

    print(len(loan_ids), " payments records have been initialized in Redis.")


