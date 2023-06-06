import csv
import random

import redis

from On_going_loans_managing.synthetic_data_transactions import generate_transactions_for_day
from pyspark.sql import SparkSession
from datetime import datetime, timedelta

def update_json_file(json_file_path, day, num_transactions):
    loan_ids=[]

    r = redis.Redis(host='localhost', port=6379, db=0)

    keys = r.keys()
    for key in keys:
        loan_ids.append(key.decode())

    transactions = generate_transactions_for_day(loan_ids, day, num_transactions)


    # Create a Spark session
    spark = SparkSession.builder.appName("TransactionUpdater").getOrCreate()

    # Convert the transactions list to a Spark DataFrame
    df = spark.createDataFrame(transactions)

    # Write the DataFrame to a JSON file (overwrite the existing file)
    output_file = json_file_path + "_" + day
    df.coalesce(4).write.mode("overwrite").format("json").save(output_file)

    # Stop the Spark session
    spark.stop()


# Function to update the transactions file
def update_json_file1(json_file_path, day, num_transactions):
    loan_ids=[]

    r = redis.Redis(host='localhost', port=6379, db=0)

    keys = r.keys()
    for key in keys:
        loan_ids.append(key.decode())

    num_transactions_percentage = random.uniform(0.5, 0.9)  # Random percentage between 10% and 90%
    num_transactions = round(num_transactions_percentage * len(loan_ids))

    random.shuffle(loan_ids)

    transactions = generate_transactions_for_day(loan_ids[:num_transactions], day, num_transactions)

    new_date = get_date_after_n_days(day, 30)

    transactions2 = generate_transactions_for_day(loan_ids[(num_transactions):], new_date, len(loan_ids)-num_transactions)

    # Create a Spark session
    spark = SparkSession.builder.appName("TransactionUpdater").getOrCreate()

    # Convert the transactions list to a Spark DataFrame
    df = spark.createDataFrame(transactions)
    df2 = spark.createDataFrame(transactions2)

    # Write the DataFrame to a JSON file (overwrite the existing file)
    output_file = json_file_path + "_" + day
    df.coalesce(4).write.mode("overwrite").format("json").save(output_file)

    output_file2 = json_file_path + "_" + new_date
    df2.coalesce(4).write.mode("overwrite").format("json").save(output_file2)
    # Stop the Spark session
    spark.stop()

def get_date_after_n_days(date, n):
    # Converti la data fornita nel formato "YYYY/MM/DD"
    input_date = datetime.strptime(date, "%Y/%m/%d")

    # Calcola la data dopo 15 giorni
    new_date = input_date + timedelta(days=n)

    # Restituisci la data nel formato desiderato
    formatted_date = new_date.strftime("%Y/%m/%d")
    return formatted_date
