#For when user uses the search bar to look for jobs
import psycopg2

# Connection credentials
DATABASE_CONFIG = {
    "database": "db",
    "user": "jass",
    "host": "localhost",
    "password": "Vomobdd23_"
}

def search_jobs(search_params):
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"]
        )
        cursor = conn.cursor()
        
        # Prepare a list to store the matching job offers
        matching_jobs = []
        
        # Create a query to check for keywords in the job descriptions
        for keyword in search_params:
            query = """
            SELECT job_ID, designation, name, work_type, involvement, City, State FROM jobs
            WHERE job_details ILIKE %s;
            """
            cursor.execute(query, (f"%{keyword}%",))
            # Fetch all matching rows
            rows = cursor.fetchall()
            # Add the rows to the matching_jobs list
            matching_jobs.extend(rows)
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        return matching_jobs
    
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()

#displays the job informations
import psycopg2

DATABASE_CONFIG = {
    "database": "db",
    "user": "jass",
    "host": "localhost",
    "password": "Vomobdd23_"
}

def job_details(id):
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"]
        )
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT job_details
                    FROM Jobs 
                    WHERE job_ID ILIKE %s
                ''', (f'%{id}%'))
                
                results = cursor.fetchall()
                return results 
    except psycopg2.Error as e:
        print(f"An error occurred while searching for job details: {e}")
        return []
    finally:
        if conn:
            conn.close()
