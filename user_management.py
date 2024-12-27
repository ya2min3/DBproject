import sqlite3
import bcrypt
import os
from datetime import datetime

# Database connection function
def connect_db():
    return sqlite3.connect("mabdd")  

# Sign-Up function
def sign_up():
    name = input("user_name: ")
    email = input("email: ")
    password = input("password: ")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, password) 
            VALUES (?, ?, ?)
        ''', (name, email, hashed_password))
        conn.commit()
        conn.close()
        print("Sign-Up successful!")
    except sqlite3.IntegrityError:
        print("An account with this email already exists.")

# Login function
def login():
    email = input("email: ")
    password = input("password: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT password FROM users WHERE email = ?
    ''', (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            print("Login successful!")
        else:
            print("Incorrect password.")
    else:
        print("No account found with this email.")
         return None
# Create a Post
def create_post(user_id):
    content = input("Enter your post content: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO posts (user_id, content) VALUES (?, ?)', (user_id, content))
    conn.commit()
    conn.close()
    print("Post created successfully!")

# Search for Users
def search_users():
    keyword = input("Enter a name or email to search: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, email FROM users 
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
    conn = connect_db()
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

# Main program
if __name__ == "__main__":
    while True:
        print("\n1. Sign Up")
        print("2. Login")
        print("3. Search Users")
        print("4. Create Post")
        print("5. View My Posts")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            user_id = login()
        elif choice == "3":
            search_users()
        elif choice == "4":
            if 'user_id' in locals() and user_id:
                create_post(user_id)
            else:
                print("You must log in first!")
        elif choice == "5":
            if 'user_id' in locals() and user_id:
                view_posts(user_id)
            else:
                print("You must log in first!")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")