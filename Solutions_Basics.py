import sqlite3
import pandas as pd # Used to display results in a tabular format (DataFrame)

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
DB_NAME = 'lab1_bank.sqlite'

# -----------------------------------------------------------------------------
# Helper Function
# -----------------------------------------------------------------------------
def execute_and_display(query_title: str, sql_query: str):
    """
    Connects to the database, executes the SQL query, and displays the result
    in a tabular format (pandas DataFrame).
    """
    print("-" * 70)
    print(f"[{query_title}]")
    print(f"SQL: {sql_query.strip().replace('\n', ' ')}")
    print("-" * 70)
    
    try:
        # Connect to the database
        with sqlite3.connect(DB_NAME) as conn:
            # Execute the query and load results into a DataFrame
            # This provides a clean tabular output.
            df = pd.read_sql_query(sql_query, conn)
            
            # Print the DataFrame
            print(df.to_string(index=False))
            print("\n")
            
    except sqlite3.Error as e:
        print(f"Error executing the query: {e}\n")

# -----------------------------------------------------------------------------
# Query Definition and Execution (Queries 1 to 12: Simple Selection)
# -----------------------------------------------------------------------------

# Query 1: Get the id values of the first 5 clients from district_id = 1.
query_1 = """
SELECT
    client_id
FROM
    client
WHERE
    district_id = 1
ORDER BY
    client_id ASC
LIMIT
    5;
"""
execute_and_display("Query 1: First 5 clients from district_id = 1", query_1)

# Query 2: Get the id value of the last client where the district_id equals to 72.
query_2 = """
SELECT
    client_id
FROM
    client
WHERE
    district_id = 72
ORDER BY
    client_id DESC
LIMIT
    1;
"""
execute_and_display("Query 2: Last client with district_id = 72", query_2)

# Query 3: Get the 3 lowest amounts in the loan table.
query_3 = """
SELECT
    amount
FROM
    loan
ORDER BY
    amount ASC
LIMIT
    3;
"""
execute_and_display("Query 3: 3 lowest amounts in loan table", query_3)

# Query 4: What are the possible values for status, ordered alphabetically in ascending order in the loan table?
query_4 = """
SELECT DISTINCT
    status
FROM
    loan
ORDER BY
    status ASC;
"""
execute_and_display("Query 4: Unique status values in loan", query_4)

# Query 5: What is the loan_id of the highest payment received in the loan table?
query_5 = """
SELECT
    loan_id
FROM
    loan
ORDER BY
    payments DESC
LIMIT
    1;
"""
execute_and_display("Query 5: loan_id of the highest payment", query_5)

# Query 6: What is the loan amount of the lowest 5 account_ids in the loan table?
query_6 = """
SELECT
    account_id,
    amount
FROM
    loan
ORDER BY
    account_id ASC
LIMIT
    5;
"""
execute_and_display("Query 6: Loan amount for lowest 5 account_ids", query_6)

# Query 7: What are the account_ids with the lowest loan amount that have a loan duration of 60?
query_7 = """
SELECT
    account_id
FROM
    loan
WHERE
    duration = 60
ORDER BY
    amount ASC
LIMIT
    5;
"""
execute_and_display("Query 7: account_ids with lowest amount and duration=60", query_7)

# Query 8: What are the unique values of k_symbol in the 'order' table?
query_8 = """
SELECT DISTINCT
    k_symbol
FROM
    "order"
WHERE
    k_symbol IS NOT NULL AND k_symbol != ''
ORDER BY
    k_symbol ASC;
"""
execute_and_display("Query 8: Unique k_symbol values in 'order'", query_8)

# Query 9: In the 'order' table, what are the order_ids of the client with the account_id 34?
query_9 = """
SELECT
    order_id
FROM
    "order"
WHERE
    account_id = 34
ORDER BY
    order_id ASC;
"""
execute_and_display("Query 9: order_ids for account_id 34", query_9)

# Query 10: In the 'order' table, which account_ids were responsible for orders between order_id 29540 and 29560 (inclusive)?
query_10 = """
SELECT DISTINCT
    account_id
FROM
    "order"
WHERE
    order_id BETWEEN 29540 AND 29560
ORDER BY
    account_id ASC;
"""
execute_and_display("Query 10: account_ids in order_id range", query_10)

# Query 11: In the 'order' table, what are the individual amounts that were sent to (account_to) id 30067122?
query_11 = """
SELECT
    amount
FROM
    "order"
WHERE
    account_to = 30067122;
"""
execute_and_display("Query 11: Amounts sent to account_to 30067122", query_11)

# Query 12: In the trans table, show the trans_id, date, type and amount of the 10 first transactions from account_id 793, newest to oldest.
query_12 = """
SELECT
    trans_id,
    date,
    type,
    amount
FROM
    trans
WHERE
    account_id = 793
ORDER BY
    date DESC,
    trans_id DESC
LIMIT
    10;
"""
execute_and_display("Query 12: First 10 transactions for account_id 793 (newest first)", query_12)

# -----------------------------------------------------------------------------
# Query Definition and Execution (Queries 13 to 18: Aggregation)
# -----------------------------------------------------------------------------

# Query 13: Of all districts with a district_id lower than 10, how many clients are from each district_id?
query_13 = """
SELECT
    district_id,
    COUNT(client_id)
FROM
    client
WHERE
    district_id < 10
GROUP BY
    district_id
ORDER BY
    district_id ASC;
"""
execute_and_display("Query 13: Client count per district_id (< 10)", query_13)

# Query 14: In the card table, how many cards exist for each type? Rank the result starting with the most frequent type.
query_14 = """
SELECT
    type,
    COUNT(card_id)
FROM
    card
GROUP BY
    type
ORDER BY
    COUNT(card_id) DESC;
"""
execute_and_display("Query 14: Card count by type (most frequent first)", query_14)

# Query 15: Print the top 10 account_ids based on the sum of all of their loan amounts.
query_15 = """
SELECT
    account_id,
    SUM(amount) AS total_amount
FROM
    loan
GROUP BY
    account_id
ORDER BY
    total_amount DESC
LIMIT
    10;
"""
execute_and_display("Query 15: Top 10 account_ids by loan amount sum", query_15)

# Query 16: Retrieve the number of loans issued for each day, before (excl) 930907, ordered by date in descending order.
query_16 = """
SELECT
    date,
    COUNT(loan_id)
FROM
    loan
WHERE
    date < 930907
GROUP BY
    date
ORDER BY
    date DESC;
"""
execute_and_display("Query 16: Loan count per day before 930907", query_16)

# Query 17: For each day in December 1997, count the number of loans issued for each unique loan duration.
query_17 = """
SELECT
    date,
    duration,
    COUNT(loan_id)
FROM
    loan
WHERE
    date BETWEEN 971201 AND 971231
GROUP BY
    date,
    duration
ORDER BY
    date ASC,
    duration ASC;
"""
execute_and_display("Query 17: Loan count per day and duration in Dec 1997", query_17)

# Query 18: For account_id 396, sum the amount of transactions for each type. Sort alphabetically by type.
query_18 = """
SELECT
    account_id,
    type,
    SUM(amount) AS total_amount
FROM
    trans
WHERE
    account_id = 396
GROUP BY
    account_id,
    type
ORDER BY
    type ASC;
"""
execute_and_display("Query 18: Sum of transactions for account_id 396 by type", query_18)

# -----------------------------------------------------------------------------
# Script Finalization
# -----------------------------------------------------------------------------
print("\nThe script has finished executing all queries.")
# Note: This script assumes you have the 'lab1_bank.sqlite' file in the same 
# directory as the Python script, and that the 'pandas' library is installed 
# (pip install pandas). If you do not wish to use pandas, you can replace the 
# 'pd.read_sql_query' logic with 'conn.cursor()' and 'cursor.fetchall()'.