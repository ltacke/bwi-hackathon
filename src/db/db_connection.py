
from datetime import datetime
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

        row_id = cur.fetchone()[0]
        # Close the cursor and connection
        cur.close()
        conn.close()
        return row_id

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def store_timestamp_id(table, id, column):
    try:
        # Connect to the Postgres database
        conn = get_connection()

        # Create a cursor object using the connection
        cur = conn.cursor()

        # Define the SQL query to insert the data into the table
        query = "UPDATE {} set {} = '{}' WHERE id = '{}';".format(
            table,
            column,
            str(datetime.now()),
            id,
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


def update_data_id(table, id, column, value):
    try:
        # Connect to the Postgres database
        conn = get_connection()

        # Create a cursor object using the connection
        cur = conn.cursor()

        # Define the SQL query to insert the data into the table
        query = "UPDATE {} set {} = '{}' WHERE id='{}'".format(
            table, column, value, id)
            
        print(query)
        # Execute the query
        cur.execute(query)

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def delete_row_id(table, id):
    try:
        # Connect to the Postgres database
        conn = get_connection()

        # Create a cursor object using the connection
        cur = conn.cursor()

        # Define the SQL query to insert the data into the table
        query = sql.SQL("DELETE FROM {} WHERE id = {}").format(
            sql.Identifier(table),
            sql.Literal(id)
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

def get_row_query(table, column, value):
    try:
        # Connect to the Postgres database
        conn = get_connection()

        # Create a cursor object using the connection
        cur = conn.cursor()
        
        # Define the SQL query to insert the data into the table
        query = sql.SQL("SELECT * FROM {} WHERE {} = {}").format(
            sql.Identifier(table),
            sql.Identifier(column),
            sql.Literal(value)
        )

        cur.execute(query)
        
        column_names = [desc[0] for desc in cur.description]
        #print("Column names:", column_names)

        row = cur.fetchone()
        cur.close()
        conn.close()
        return row, column_names

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

        #print(query)

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
        'job_id uuid',
        'name VARCHAR (80)',
        'phone VARCHAR (30)',
        'email VARCHAR(250)',
        'birthdate VARCHAR(30)',
        'address TEXT',
        'flag TEXT',
        'skills TEXT',
        'education TEXT',
        'experience TEXT',
        'gaps TEXT',
        'applicant_questions TEXT',
        'q1 TEXT',
        'q2 TEXT',
        'q3 TEXT',
        'q4 TEXT',
        'q5 TEXT',
        'a1 TEXT',
        'a2 TEXT',
        'a3 TEXT',
        'a4 TEXT',
        'a5 TEXT',
        'start_time_q1 TIMESTAMP',
        'end_time_q1 TIMESTAMP',
        'start_time_q2 TIMESTAMP',
        'end_time_q2 TIMESTAMP',
        'start_time_q3 TIMESTAMP',
        'end_time_q3 TIMESTAMP',
        'start_time_q4 TIMESTAMP',
        'end_time_q4 TIMESTAMP',
        'start_time_q5 TIMESTAMP',
        'end_time_q5 TIMESTAMP',
        'analysis1 json',
        'analysis2 json',
        'analysis3 json',
        'analysis4 json',
        'analysis5 json',
        'pdf BYTEA',
        'json json',
        'created timestamp default current_timestamp'
        ]
    create_table('applicants', applicant_table)

    job_table = [
        'id uuid PRIMARY KEY DEFAULT gen_random_uuid()',
        'title varchar(50)',
        'url varchar(200)',
        'job_role varchar(200)',
        'job_level varchar(50)',
        'pre_requirements_education text',
        'pre_requirements_experience text',
        'hard_skills text',
        'soft_skills text',
        'responsibilities text',
        'others text',
        'questions text',
        'job_json json',
        'missing_requirements text',
        'created timestamp default current_timestamp'
    ]
    
    #delete_table('jobs')
    create_table('jobs', job_table)


    
    

if __name__ == "__main__":
    
    create_tables()
    
    table_name="applicants"

    data_table = retrieve_data(table_name)

    print(data_table)

    table_name="jobs"

    data_table = retrieve_data(table_name)

    print(data_table)
    