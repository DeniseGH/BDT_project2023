import sqlite3
import numpy as np
import pandas as pd
from gower import gower_matrix
from scipy.cluster.hierarchy import linkage, fcluster
import scipy.spatial.distance as ssd


def extract_data(database_file: str, table_name: str):
    '''
    :param database_file: name of the SQL file
    :param table_name: name of the table in the SQL file
    :return: list of rows in the SQL file
    '''

    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Execute a SELECT query to fetch all data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    return rows


def hierarchical_clustering(rows, new_loan):
    '''
    :param rows: a list of rows containing the records of the past loans given from a bank
    :param new_loan: the new loan request
    :return: the loan ids and the status of the loans in the same cluster of the new_loan
    '''
    loan_ids = [row[1] for row in rows]
    loan_ids.append(new_loan[0])
    status = [row[-1] for row in rows]
    status.append("Unknown")

    data = [row[1:-1] for row in rows]
    data.append(new_loan[1:])

    # Convert the data list to a pandas DataFrame
    df = pd.DataFrame(data)


    # Calculate the Gower distance matrix
    distance_matrix = ssd.squareform(gower_matrix(df))

    # Perform hierarchical clustering on the distance matrix
    linkage_matrix = linkage(distance_matrix, method='ward')
    clusters = fcluster(linkage_matrix, t=15, criterion='maxclust')

    # Find the cluster of the new loan
    new_loan_cluster = clusters[-1]

    # Filter the statuses based on the cluster of the new loan
    cluster_loan_ids = [loan_ids[i] for i, cluster in enumerate(clusters) if cluster == new_loan_cluster]
    cluster_statuses = [status[i] for i, cluster in enumerate(clusters) if cluster == new_loan_cluster]

    # Create a matrix with the loan IDs and statuses of loans in the same cluster as the new loan
    cluster_matrix = np.column_stack((cluster_loan_ids, cluster_statuses))

    return cluster_matrix

# This function takes a decision looking at the status of the closest loans
def predict_unknown_status(cluster_matrix):
    statuses = cluster_matrix[:-1, 1]
    unique_statuses, counts = np.unique(statuses, return_counts=True)

    if "Fully Paid" in unique_statuses:
        if counts[unique_statuses == "Fully Paid"][0] > (counts[(unique_statuses == "Declined")] + counts[(unique_statuses == "Charged off")][0]):
            return "Accepted"

    return "Declined"


#fare funzione che simula request di loan
new_loan = ['AmPrdoBC-7rbw-RiNU-lxne-cMm2rFG6lljk',
  'DH8FASE2-7bNU-tU7h-hpYS-cWDz1OKbNbbb','Barbara Pacetta', 55, 0, "No", 72550, "Long Term", 27733, 'Vacation or travel']

cluster_matrix_result = hierarchical_clustering(extract_data("PROVA2.db", "loan_records"), new_loan)

print("closest loans: ")
print(cluster_matrix_result)
print("the new loan will be")
print(predict_unknown_status(cluster_matrix_result))


# The
# pip uninstall numpy (Y)
# pip install numpy
# pip uninstall pandas (Y)
# pip install pandas
# pip uninstall scipy (Y)
# pip install scipy


