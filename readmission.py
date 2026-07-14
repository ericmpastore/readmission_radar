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

    # Algorithm, EPastore 07/12/2026
    # Calculate readmission rate as readmission_rate / admission_count
    # admission_count is simply a COUNT of all rows
    # readmission_rate is a COUNT of rows where other rows have the same name but a date less than the discharge date plus 30 days 
    # LEAD(admission_date) OVER (PARTITION BY patient_id ORDER BY admission_date) 

    print(
        con.sql(
            f"""
            WITH dates AS (
                SELECT patient_id, discharge_date, LEAD(admission_date) OVER (PARTITION BY patient_id ORDER BY admission_date) AS next_admission_date
                FROM {TABLE_NAME}
            )
            SELECT ROUND(SUM(CASE WHEN next_admission_date <= discharge_date + INTERVAL 30 DAY THEN 1 ELSE 0 END) * 100.0 
                / COUNT(*),0) AS readmission_rate
            FROM dates;
            """
        )
    )


if __name__ == '__main__':
    main()

