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
    
    # View output of CTE logic outside of CTE, EPastore 07/15/2026
    print(
        con.sql(
            f"""
                SELECT patient_id, discharge_date, LEAD(admission_date) OVER (PARTITION BY patient_id ORDER BY admission_date) AS next_admission_date 
                FROM {TABLE_NAME};
            """))
    
    # Business Question, EPastore 07/15/2026
    # The analytic task is to calculate the hospital's 30 day readmission rate. 
    # A discharge counts as a 30-day readmission when the same patient is admitted again within 30 days of their discharge date.
    # Day 30 is included in the readmission window.
    # Assume that all records in the dataset have had a full 30-day follow-up window.

    # Process, EPastore 07/15/2026
    # Use CTE to generate table with next admission date if present, otherwise NULL
    # Use main query to generate 1 or 0 value if date in 30 days, then sum and divde by total count
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

