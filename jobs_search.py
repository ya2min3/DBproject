#For when user uses the search bar to look for jobs
import psycopg2

# Connection credentials
DATABASE_CONFIG = {
    "database": "db",
    "user": "jass",
    "host": "localhost",
    "password": "Vomobdd23_"
}

def search_bar():
    # Get input from the user
    user_input = input("Search for job offers:")
    # Split the input parameters into a list
    search_params = user_input.split()
    return search_params


def search_results(search_params):
    try:
        # Connect to the PostgreSQL database
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
            SELECT designation FROM jobs
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
