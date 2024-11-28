from db.db_connection import create_tables, delete_row_id, delete_table, retrieve_data
from db.db_tasks import get_job_description


if __name__ == "__main__":

    print(get_job_description("Cloud-Engineer-57661"))

    #delete_table("jobs")
    create_tables()
    

    data = {'description': 'test'}
    print("storing data")
    table_name="applicants"
    #store_data(table_name, data)

    data_table = retrieve_data(table_name)

    print(data_table)

    table_name="jobs"


    #delete_row_id('jobs', 'a2382693-77a1-4c9a-89ae-9e49ccf58af1')
    
    data_table = retrieve_data(table_name)
    print(data_table[['id', 'title', 'created']])


    job = get_job_description('Cloud-Engineer-57661')

    print(job)
    