from db.db_connection import create_tables, delete_row_id, delete_table, retrieve_data
from db.db_tasks import get_job_description
from main import analyze_background


if __name__ == "__main__":

    delete_row_id("jobs", "fd6db6cf-9dff-4fe0-931f-f52978afa4b4")
    applicants= [
  "9b3b9fe7-7f02-4824-8cf2-96259774f0f6",
  "f0e19ec3-b60d-4793-b33d-349682f671d6"]
    # for a in applicants:
    #     delete_row_id('applicants', a)

    #delete_table("jobs")
    #delete_table('applicants')
    #create_tables()
    

    # data = {'description': 'test'}
    # print("storing data")
    # 
    # 
    table_name="applicants"
    # #store_data(table_name, data)

    #print(analyze_background("ba7f2734-da59-49d4-9d28-602f0b0ae616", 1))

    data_table = retrieve_data(table_name)
    
    print(data_table[['id', 'created']])

    print(data_table[['q5', 'start_time_q5']])
    print(data_table[['a5', 'end_time_q1']])
    
    print(data_table[['analysis5']])

    table_name="jobs"


    #delete_row_id('jobs', 'a2382693-77a1-4c9a-89ae-9e49ccf58af1')
    
    data_table = retrieve_data(table_name)
    print(data_table[[ 'title', 'created']])


    # job = get_job_description('Cloud-Engineer-57661')

    # print(job)
    