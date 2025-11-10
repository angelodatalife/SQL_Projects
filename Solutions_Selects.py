import sqlite3
import pandas as pd # Used to display results in a tabular format (DataFrame)

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
DB_NAME = 'publications.sqlite'

# -----------------------------------------------------------------------------
# Helper Function
# -----------------------------------------------------------------------------
def execute_and_display(query_title: str, sql_query: str):
    """
    Connects to the database, executes the SQL query, and displays the result
    in a tabular format (pandas DataFrame).
    """
    print("=" * 70)
    print(f"[{query_title}]")
    # Display the query for reference
    print(f"SQL: {sql_query.strip().replace('\n', ' ')}")
    print("=" * 70)
    
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
# Query Definition and Execution (Challenges 1 to 4)
# -----------------------------------------------------------------------------

# Challenge 1: Who Have Published What At Where?
# Find out what titles each author has published at which publishers.
query_1 = """
SELECT
    A.au_id AS "AUTHOR ID",
    A.au_lname AS "LAST NAME",
    A.au_fname AS "FIRST NAME",
    T.title AS "TITLE",
    P.pub_name AS "PUBLISHER"
FROM
    authors AS A
-- Join to link authors to titles
INNER JOIN
    titleauthor AS TA ON A.au_id = TA.au_id
-- Join to get title information
INNER JOIN
    titles AS T ON TA.title_id = T.title_id
-- Join to get publisher information
INNER JOIN
    publishers AS P ON T.pub_id = P.pub_id
ORDER BY
    A.au_id ASC,
    T.title ASC;
"""
execute_and_display("Challenge 1: Who Have Published What At Where?", query_1)

# ---

# Challenge 2: Fewer Titles
# Identify which publishers have published 2 or fewer titles.
query_2 = """
SELECT
    P.pub_name AS "PUBLISHER",
    COUNT(T.title_id) AS "TITLE COUNT"
FROM
    publishers AS P
-- INNER JOIN is used here as we are only interested in published titles
INNER JOIN
    titles AS T ON P.pub_id = T.pub_id
GROUP BY
    P.pub_name
HAVING
    COUNT(T.title_id) <= 2;
"""
execute_and_display("Challenge 2: Publishers with 2 or Fewer Titles", query_2)

# ---

# Challenge 3: Best Selling Authors
# Find the top 3 authors who have sold the highest number of titles.
query_3 = """
SELECT
    A.au_id AS "AUTHOR ID",
    A.au_lname AS "LAST NAME",
    A.au_fname AS "FIRST NAME",
    SUM(T.sales) AS "TOTAL"
FROM
    authors AS A
-- Link authors to titles
INNER JOIN
    titleauthor AS TA ON A.au_id = TA.au_id
-- Link titles to sales data (implicitly via the 'sales' column in the titles table)
INNER JOIN
    titles AS T ON TA.title_id = T.title_id
GROUP BY
    A.au_id, A.au_lname, A.au_fname
ORDER BY
    "TOTAL" DESC
LIMIT
    3;
"""
execute_and_display("Challenge 3: Top 3 Best Selling Authors", query_3)

# ---

# Challenge 4: Best Selling Authors Ranking
# Display all 23 authors ranked by total sales, showing 0 for authors with no sales.
query_4 = """
SELECT
    A.au_id AS "AUTHOR ID",
    A.au_lname AS "LAST NAME",
    A.au_fname AS "FIRST NAME",
    -- Use COALESCE to replace NULL (no sales) with 0
    COALESCE(SUM(T.sales), 0) AS "TOTAL"
FROM
    authors AS A
-- Use LEFT JOIN to ensure all authors are included, even those with no sales data
LEFT JOIN
    titleauthor AS TA ON A.au_id = TA.au_id
LEFT JOIN
    titles AS T ON TA.title_id = T.title_id
GROUP BY
    A.au_id, A.au_lname, A.au_fname
ORDER BY
    "TOTAL" DESC;
"""
execute_and_display("Challenge 4: All Authors Ranking (0 for NULL sales)", query_4)

# -----------------------------------------------------------------------------
# Script Finalization
# -----------------------------------------------------------------------------
print("\nThe Python script has finished executing all challenges for 'publications.sqlite'.")
# Note: This script assumes you have the 'publications.sqlite' file in the same
# directory as the Python script, and that the 'pandas' library is installed
# (pip install pandas).