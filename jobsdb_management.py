#For when user uses the search bar to look for jobs
import psycopg2

# Connection credentials
DATABASE_CONFIG = {
    "database": "db",
    "user": "jass",
    "host": "localhost",
    "password": "Vomobdd23_"
}

# Function to search for jobs based on the search parameters
#search_params: list of keywords
def search_jobs(search_params):
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"]
        )
        cursor = conn.cursor()
        where_clauses = []
        params = []

        # Verify search_params is a list of keywords
        if isinstance(search_params, str):
            search_params = [search_params]

        if search_params:
            for keyword in search_params:
                where_clauses.append("(designation ILIKE %s OR name ILIKE %s OR work_type ILIKE %s OR involvement ILIKE %s OR City ILIKE %s OR State ILIKE %s)")
                params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])

            # Combine conditions with OR
            where_clause = " OR ".join(where_clauses)
            query = f"""
            SELECT job_ID, designation, name, work_type, involvement, City, State 
            FROM jobs
            WHERE {where_clause};
            """
        else:
            # If no search parameters are provided, return jobs with designation "Other"
            query = """
            SELECT job_ID, designation, name, work_type, involvement, City, State 
            FROM jobs
            WHERE designation = 'Other';
            """
            params = []  # No parameters needed for this query

        # Debugging: Print query and parameters
        #print("Executing Query:", query)
        #print("With Parameters:", params)

        # Execute query
        cursor.execute(query, params)
        matching_jobs = cursor.fetchall()

        # Debugging: Print the results
        #print("Matching Jobs:", matching_jobs)

        return matching_jobs

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return []

    finally:
        # Ensure resources are closed
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

def get_job_details(id):
    print("ID: ", id)
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
                    WHERE job_ID = %s
                ''', (id,))  # Use the equality operator and pass the id as a tuple
                
                results = cursor.fetchall()
                return results 
    except psycopg2.Error as e:
        print(f"An error occurred while searching for job details: {e}")
        return []
    finally:
        if conn:
            conn.close()
