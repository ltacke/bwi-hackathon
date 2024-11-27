
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import pandas as pd


load_dotenv(override=True)

def get_connection():
    
    load_dotenv(override=True)
    try:
        # Connect to the Postgres database
        conn = psycopg2.connect(
            host= os.environ["PG_HOST"],
            port = os.environ["PG_PORT"],
            database=os.environ["PG_DATABASE"],
            user = os.environ["PG_USER"],
            password = os.environ["PG_PASSWORD"]
        )

        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None


def store_data(table, data):
    try:
        # Connect to the Postgres database
        conn = get_connection()

        # Create a cursor object using the connection
        cur = conn.cursor()

        # Define the SQL query to insert the data into the table
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(", ").join(map(sql.Identifier, data.keys())),
            sql.SQL(", ").join(sql.Literal(value) for value in data.values())
        )

        # Execute the query
        cur.execute(query)

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def create_table(table_name, columns):
    try:
        # Connect to the Postgres database
        conn = get_connection()

        # Create a cursor object using the connection
        cur = conn.cursor()

        # Define the SQL query to create the table
        query = sql.SQL(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})")

        print(query)

        # Execute the query
        cur.execute(query)

        # Commit the changes to the database
        conn.commit()

        #cur = conn.cursor()
        print(f"Fields in {table_name}:")
        cur.execute("SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name = '{}'; ".format(table_name))
        for f in cur.fetchall():
            print("{}\t{}".format(f[1],f[2]))
        print()
        
        # Close the cursor and connection
        cur.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while creating table in PostgreSQL", error)

def delete_table(table_name):
    conn = get_connection()
    
    cur = conn.cursor()
    query = f"DROP TABLE IF EXISTS {table_name}"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


def retrieve_data(table_name):
    conn = get_connection()
    
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def create_tables():

    applicant_table  = [
        'id uuid PRIMARY KEY DEFAULT gen_random_uuid()', 
        'description TEXT', 
        'start_time_q1 TIMESTAMP',
        'end_time_q1 TIMESTAMP',
        'start_time_q2 TIMESTAMP',
        'end_time_q2 TIMESTAMP',
        'start_time_q3 TIMESTAMP',
        'end_time_q3 TIMESTAMP',
        'start_time_u_q1 TIMESTAMP',
        'end_time_u_q1 TIMESTAMP',
        'start_time_u_q2 TIMESTAMP',
        'end_time_u_q2 TIMESTAMP',
        'start_time_u_q3 TIMESTAMP',
        'end_time_u_q3 TIMESTAMP',]
    #delete_table('applicants')
    create_table('applicants', applicant_table)

    job_table = [
        'id uuid PRIMARY KEY DEFAULT gen_random_uuid()',
        'title varchar(50)',
        'url varchar(200)',
        'job_role varchar(200)',
        'job_level varchar(50)',
        'pre_requirements_education varchar(255)',
        'pre_requirements_experience varchar(255)',
        'hard_skills text',
        'soft_skills text',
        'responsibilities text',
        'others text',
        'questions text',
        'job_json json'
    ]
    
    delete_table('jobs')
    create_table('jobs', job_table)


    
    

if __name__ == "__main__":
    
    create_tables()
    

    data = {'description': 'test'}
    print("storing data")
    table_name="applicants"
    store_data(table_name, data)

    data_table = retrieve_data(table_name)

    print(data_table)

    table_name="jobs"

    data_table = retrieve_data(table_name)

    print(data_table)
    