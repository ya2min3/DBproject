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
        # Connect to the database
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        # Base SQL query
        query = """
        SELECT designation, name, work_type, involvement, industry, city, state
        FROM jobs
        WHERE 1=1
        """
        values = []

        # Add filters dynamically based on user input
        if 'keywords' in search_params:
            query += " AND (designation ILIKE %s OR work_type ILIKE %s OR involvement ILIKE %s)"
            keyword = f"%{search_params['keywords']}%"
            values.extend([keyword, keyword, keyword])

        if 'location' in search_params:
            query += " AND (city ILIKE %s OR state ILIKE %s)"  # Grouped with parentheses
            location = f"%{search_params['location']}%"
            values.extend([location, location])  # Two placeholders for city and state

        if 'field' in search_params:
            query += " AND industry ILIKE %s"
            values.append(f"%{search_params['field']}%")

        if 'company' in search_params:
            query += " AND name ILIKE %s"
            values.append(f"%{search_params['company']}%")

        # Execute the query with the collected values
        cursor.execute(query, tuple(values))
        jobs = cursor.fetchall()

        return jobs
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()
