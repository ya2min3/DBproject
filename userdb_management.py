import psycopg2
import bcrypt

# Connection credentials
DATABASE_CONFIG = {
    "database": "db",
    "user": "jass",
    "host": "localhost",
    "password": "Vomobdd23_"
}

# Create users table
def create_users_table():
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
                    CREATE TABLE IF NOT EXISTS Users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(320) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        description TEXT,
                        photo_path TEXT,
                        cv_path TEXT
                    );
                ''')
        print("Table 'Users' created successfully or already exists.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Sign-Up function: Stores the new user's info in the database
def sign_up(name, email, password):
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Encode and hash the password
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
                    INSERT INTO Users (name, email, password) 
                    VALUES (%s, %s, %s)
                ''', (name, email, hashed_password))  # Store the hashed password
        return True
    except psycopg2.IntegrityError:
        print("An account with this email already exists.")
        return False
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Login function
def login(email, password):
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
                    SELECT password FROM Users WHERE email = %s
                ''', (email,))
                result = cursor.fetchone()
        if result:
            stored_password = result[0]
            # Check the password against the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):  # Make sure both are encoded
                return True
            else:
                return False    
        else:
            return False
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return False

# Get User ID
def get_userid(email):
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
                    SELECT id FROM Users WHERE email = %s
                ''', (email,))
                result = cursor.fetchone()
        if result:
            return result[0]  # Return user ID
        else:
            return None
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return None

# Get User Name
def get_username(id):
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
                    SELECT name FROM Users WHERE id = %s
                ''', (id,))
                result = cursor.fetchone()
        if result:
            return result[0]  # Return user name
        else:
            return None
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return None

# Get User Description
def get_description(user_id):
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
                    SELECT description FROM Users WHERE id = %s
                ''', (user_id,))
                result = cursor.fetchone()
        if result:
            return result[0]  
        else:
            return "No description for now."
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return "No description for now."
    
# Update user description
def update_description(user_id, description):
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
                    UPDATE Users SET description = %s WHERE id = %s
                ''', (description, user_id))
                conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return False

# Update user CV
def update_cv(user_id, cv_path):
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
                    UPDATE Users SET cv_path = %s WHERE id = %s
                ''', (cv_path, user_id))
                conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return False

def get_cv(user_id):
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
                    SELECT cv_path FROM Users WHERE id = %s
                ''', (user_id,))
                result = cursor.fetchone()
        if result:
            return result[0]  
        else:
            return "No cv for now."
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return "No cv for now."

def remove_cv(user_id):
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
                    UPDATE Users SET cv_path = NULL WHERE id = %s
                ''', (user_id,))
                conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return False
