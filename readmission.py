import duckdb
import os

def load_db(in_file,table_name,db_path):
    # Connect to Database, EPastore 05/15/2026
    con = duckdb.connect(db_path)

    # Load data into database and close connection, EPastore 05/15/2026
    con.sql(
        f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_csv('{in_file}')
        """
    )

    con.close()

def main():
    # Declare Constants, EPastore 05/17/2026
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE = os.path.join(SCRIPT_DIR,'inpatient_admissions.csv')
    TABLE_NAME = 'inpatient_admissions'
    DB_PATH = os.path.join(SCRIPT_DIR,"my_database.duckdb")

    # Create table in database, EPastore 05/17/2026
    load_db(CSV_FILE,TABLE_NAME,DB_PATH)

    # Connect to the database, EPastore 05/17/2026
    con = duckdb.connect(DB_PATH)

    # Test connection, EPastore 05/17/2026
    print(
    con.sql(
        f"""
            SELECT * FROM {TABLE_NAME} LIMIT 10;
        """))
    
    # Business Question
    # The analytic task is to calculate the hospital's 30 day readmission rate. 
    # A discharge counts as a 30-day readmission when the same patient is admitted again within 30 days of their discharge date.
    # Day 30 is included in the readmission window.
    # Assume that all records in the dataset have had a full 30-day follow-up window.

    # print(
    #     con.sql(
    #         f"""
           
    #         """
    #     )
    # )

if __name__ == '__main__':
    main()

