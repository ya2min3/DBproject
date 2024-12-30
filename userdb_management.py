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
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Users (name, email, password) 
            VALUES (%s, %s, %s)
        ''', (name, email, hashed_password))  # Store the hashed password
        conn.commit()
        conn.close()
        return True
    except psycopg2.IntegrityError:
        print("An account with this email already exists.")
        return False

# Login function
def login(email, password):
    conn = psycopg2.connect(
        dbname=DATABASE_CONFIG["database"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        host=DATABASE_CONFIG["host"]
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT password FROM Users WHERE email = %s
    ''', (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password = result[0]
        # Check the password against the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):  # Make sure both are encoded
            return True
        else:
            return False    
    else:
        return False

# Get User ID
def get_userid(email):
    conn = psycopg2.connect(
        dbname=DATABASE_CONFIG["database"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        host=DATABASE_CONFIG["host"]
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM Users WHERE email = %s
    ''', (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]  # Return user ID
    else:
        return None

# Get User Name
def get_username(id):
    conn = psycopg2.connect(
        dbname=DATABASE_CONFIG["database"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        host=DATABASE_CONFIG["host"]
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name FROM Users WHERE id = %s
    ''', (id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]  # Return user name
    else:
        return None

# Get User Description
def get_description(user_id):
    conn = psycopg2.connect(
        dbname=DATABASE_CONFIG["database"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        host=DATABASE_CONFIG["host"]
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT description FROM Users WHERE id = %s
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]  # Return user description
    else:
        return "No description for now."
#update user description
def update_description(user_id, description):
    conn = psycopg2.connect(
        dbname=DATABASE_CONFIG["database"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        host=DATABASE_CONFIG["host"]
    )
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Users SET description = %s WHERE id = %s
    ''', (description, user_id))
    conn.commit()
    conn.close()
    return True

#update user cv
def update_cv(user_id, cv_path):
    conn = psycopg2.connect(
        dbname=DATABASE_CONFIG["database"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        host=DATABASE_CONFIG["host"]
    )
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Users SET cv_path = %s WHERE id = %s
    ''', (cv_path, user_id))
    conn.commit()
    conn.close()
    return True


#A modifier:--------------------------------------------------------------------------------------------------
# Create a Post
def create_post(user_id):
    content = input("Enter your post content: ")
    conn = conn = psycopg2.connect(
            dbname=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"]
        )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO posts (user_id, content) VALUES (?, ?)', (user_id, content))
    conn.commit()
    conn.close()
    return content

# Search for Users
def search_users():
    keyword = input("Enter a name or email to search: ")

    conn = psycopg2.connect(
            dbname=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"]
        )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, email FROM Users 
        WHERE name LIKE ? OR email LIKE ?
    ''', (f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    conn.close()

    if results:
        print("Search results:")
        for user in results:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    else:
        print("No users found.")

# View User Posts
def view_posts(user_id):
    conn = psycopg2.connect(
            dbname=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"]
        )
    cursor = conn.cursor()
    cursor.execute('SELECT content, timestamp FROM posts WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
    posts = cursor.fetchall()
    conn.close()

    if posts:
        print("Your posts:")
        for post in posts:
            print(f"- {post[1]}: {post[0]}")
    else:
        print("No posts found.")
