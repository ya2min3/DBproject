import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QFontDatabase, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import userdb_management 
import jobsdb_management
import parse_jobs_csv
import subprocess
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import tkinter as tk  # Importer Tkinter

def add_logo_to_window(self, logo_path, logo_size=(100, 100)):
    # Create a QLabel to display the logo
    logo_label = QLabel(self)
    logo_pixmap = QPixmap(logo_path)  # Use the correct logo path
    logo_label.setPixmap(logo_pixmap.scaled(logo_size[0], logo_size[1]))  # Scale the image to the desired size
    logo_label.setAlignment(Qt.AlignCenter)  # Center the logo in the QLabel

    # Add the logo label to the layout
    main_layout = self.layout()  # Get the layout of the window
    if main_layout:
        main_layout.insertWidget(0, logo_label)  # Add the logo at the top of the layout

# Couleurs du style
PRIMARY_COLOR = "#6A1B9A"  # Violet
SECONDARY_COLOR = "#E1BEE7"  # Violet clair
BACKGROUND_COLOR = "#F3E5F5"  # Fond violet très clair
TEXT_COLOR = "#212121"  # Gris foncé pour un bon contraste sur fond clair
HIGHLIGHT_COLOR = "#8E24AA"  # Violet plus clair
ERROR_COLOR = "#D32F2F"  # Rouge (pour l'erreur)

# Police globale
DEFAULT_FONT = "Arial"
FONT_SIZE = 12

# Application du style
def apply_style(app):
    # Appliquer la police globale
    app.setFont(QFont(DEFAULT_FONT, FONT_SIZE))
    
    # Définir les feuilles de style globales
    app.setStyleSheet(f"""
        QWidget {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
            font-family: {DEFAULT_FONT};
            font-size: {FONT_SIZE}px;
        }}
        QPushButton {{
            background-color: {PRIMARY_COLOR};
            color: {SECONDARY_COLOR};
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
        }}
        QPushButton:hover {{
            background-color: {HIGHLIGHT_COLOR};
            color: {TEXT_COLOR};
        }}
        QPushButton:pressed {{
            background-color: {ERROR_COLOR};
            color: {SECONDARY_COLOR};
        }}
        QLabel {{
            color: {TEXT_COLOR};
        }}
        QLineEdit {{
            background-color: {SECONDARY_COLOR};
            color: {TEXT_COLOR};
            border: 1px solid {PRIMARY_COLOR};
            padding: 5px;
            border-radius: 3px;
        }}
        QLineEdit:focus {{
            border: 1px solid {HIGHLIGHT_COLOR};
        }}
    """)


# Create the user table
userdb_management.create_users_table()
# Create the jobs table
jobsdb_management.create_jobs_table()
# Check if the jobs table is empty
if jobsdb_management.is_jobs_table_empty():  # Function to check if the table is empty
    # Create file jobs_data.sql
    with open('jobs_data.sql', 'w') as output_file:
    # Execute the command and redirect the output to the file
        result = subprocess.run(['python3', 'parse_jobs_csv.py'], stdout=output_file, stderr=subprocess.PIPE)
    # Check for errors
    if result.returncode == 0:
        print("Command executed successfully, output written to jobs_data.sql")
        # Execute file to fill table:
        jobsdb_management.fill_jobs_table()
    else:
        print("Command failed with return code:", result.returncode)
        print("Error:", result.stderr.decode())
    

#Application Home Page
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Job")
        self.setGeometry(100, 100, 1000, 500)

        # Layout pour organiser les éléments de la fenêtre
        self.layout = QVBoxLayout(self)  # Utilisation d'un QVBoxLayout ici
        self.setLayout(self.layout) 

        # Ajouter le logo
        self.add_logo_to_window("logo.jpg")  # Ajouter le logo (ajuste le chemin selon ton fichier)

        # Ajouter le titre
        title = QLabel("Welcome to My Job!\nPlease sign up or login to continue.", self)
        title.setFont(QFont('Arial', 60))
        title.setAlignment(Qt.AlignCenter)  # Align the text to the center
        # Ajouter les boutons
        presentation_button = QPushButton('Learn more about "My Job"?', self)
        sign_up_button = QPushButton('Sign Up', self)
        login_button = QPushButton('Login', self)

        # Connexion des boutons à leurs fonctions
        presentation_button.clicked.connect(self.presentation)
        sign_up_button.clicked.connect(self.open_sign_up)
        login_button.clicked.connect(self.open_login)

       # Add the widgets to the layout
        self.layout.addWidget(title)
        self.layout.addWidget(presentation_button)
        self.layout.addWidget(sign_up_button)
        self.layout.addWidget(login_button)

        # Apply the layout to the window
        self.setLayout(self.layout)

    def add_logo_to_window(self, logo_path):
        """Ajouter un logo à la fenêtre sans découper l'image"""
        try:
            # Charger l'image avec QPixmap
            logo = QPixmap(logo_path)
            
            # Créer un QLabel pour l'afficher
            logo_label = QLabel(self)
            logo_label.setPixmap(logo)
            logo_label.setAlignment(Qt.AlignCenter)  # Centrer l'image
            
            # Redimensionner l'image pour l'adapter à la taille du label, sans déformation
            logo_label.setScaledContents(True)  # Permet de redimensionner sans découper
            
            # Ajouter l'image au layout
            self.layout.addWidget(logo_label)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image: {e}")

    def open_sign_up(self):
        self.signup_page = SignupPage()
        self.signup_page.show()
        self.close()

    def open_login(self):
        self.login_page = LoginPage()
        self.login_page.show()
        self.close()

    def presentation(self):
        QMessageBox.information(
            self, 
            "About My Job", 
            "My Job is a platform that allows you to search for job offers or post job offers! "
            "You can also search for other users and view their CVs!"
        )

# Application Sign-Up Page
class SignupPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setGeometry(100, 100, 1000, 500)
        layout = QVBoxLayout()

        title = QLabel("Please enter your information to sign up:", self)
        title.setFont(QFont('Arial', 50))
        title.setAlignment(Qt.AlignCenter)  # Align the text to the center

        self.name_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        sign_up_button = QPushButton('Sign Up', self)
        home_page_button = QPushButton('Go back to Home Page', self)

        sign_up_button.clicked.connect(self.sign_up)
        home_page_button.clicked.connect(self.go_home)

        layout.addWidget(title)
        layout.addWidget(QLabel("Name", self))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email", self))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Password", self))
        layout.addWidget(self.password_input)
        layout.addWidget(sign_up_button)
        layout.addWidget(home_page_button)

        self.setLayout(layout)

    def sign_up(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not name or not email or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "Input Error", "Please enter a valid email address.")
            return
        
        if len(password) < 8 or not any(char.isdigit() for char in password):
            QMessageBox.warning(self, "Input Error", "Password must be at least 8 characters long and include a number.")
            return

        if userdb_management.sign_up(name, email, password):
            QMessageBox.information(self, "Success", "Sign-Up successful!")
            self.go_profile(email)
        else:
            QMessageBox.warning(self, "Error", "An account with this email already exists.")

    def go_home(self):
        self.home_page = HomePage()
        self.home_page.show()
        self.close()
        
    def go_profile(self, email):
        user_id = userdb_management.get_userid(email)
        self.profile_page = ProfilePage(user_id)
        self.profile_page.show()
        self.close()

#Application Login Page
class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 1000, 500)
        layout = QVBoxLayout()

        title = QLabel("Please enter your login information:", self)
        title.setFont(QFont('Arial', 50))
        title.setAlignment(Qt.AlignCenter)  # Align the text to the center

        self.email_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton('Login', self)
        home_page_button = QPushButton('Go back to Home Page', self)

        login_button.clicked.connect(self.login)
        home_page_button.clicked.connect(self.go_home)

        layout.addWidget(title)
        layout.addWidget(QLabel("Email", self))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Password", self))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(home_page_button)

        self.setLayout(layout)

    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        success = userdb_management.login(email, password)
        user_id = userdb_management.get_userid(email)
        if success:
            QMessageBox.information(self, "Success", "Login successful!")
            self.open_profile(user_id)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password.")
        
    def go_home(self):
        self.home_page = HomePage()
        self.home_page.show()
        self.close()

    def open_profile(self, user_id):
        self.profile_page = ProfilePage(user_id)
        self.profile_page.show()
        self.close()

#Application Profile Page
class ProfilePage(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id  # Store the user's ID
        self.username = userdb_management.get_username(user_id)
        self.setWindowTitle("Profile")
        self.setGeometry(100, 100, 1000, 500)
        layout = QVBoxLayout()

        title = QLabel(f"Welcome to your profile page, {self.username}!", self)
        title.setFont(QFont('Arial', 50))
        title.setAlignment(Qt.AlignCenter)  # Align the text to the center

        # Description label
        self.description_label = QLabel(self)
        self.update_description_label()

        # CV label
        self.cv_label = QLabel(self)
        self.update_cv_label()

        # Buttons
        self.add_description_button = QPushButton('Add/Modify your description', self)
        self.add_cv_button = QPushButton('Add CV', self)
        self.search_jobs_button = QPushButton('Search for Jobs', self)
        self.sign_out_button = QPushButton('Sign Out', self)

        # Functions
        self.sign_out_button.clicked.connect(self.sign_out)
        self.add_description_button.clicked.connect(self.add_modify_description)
        self.add_cv_button.clicked.connect(self.add_cv)
        self.search_jobs_button.clicked.connect(self.search_jobs)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(self.description_label)
        layout.addWidget(self.add_description_button)
        layout.addWidget(self.cv_label)  # Add cv_label to the layout
        layout.addWidget(self.add_cv_button)
        layout.addWidget(self.search_jobs_button)
        layout.addWidget(self.sign_out_button)

        self.setLayout(layout)

    def update_description_label(self):
        description = userdb_management.get_description(self.user_id)
        if description:
            self.description_label.setText(f"Description: {description}")
        else:
            self.description_label.setText("Description: No description available.")

    def update_cv_label(self):
        cv = userdb_management.get_cv(self.user_id)
        if cv:
            self.cv_label.setText(f"CV: {cv}")
        else:
            self.cv_label.setText("CV: No CV available.")
            
    def sign_out(self):
        self.home_page = HomePage() 
        self.home_page.show()
        self.close()

    def add_modify_description(self):
        text, ok = QInputDialog.getText(self, "Add/Modify Description", "Enter your description:")
        if ok and text:
            # Save the description to the database
            success = userdb_management.update_description(self.user_id, text) 
            if success:
                QMessageBox.information(self, "Success", "Description updated successfully!")
                self.update_description_label()  # Update the description label
            else:
                QMessageBox.warning(self, "Error", "Failed to update description.")

    def add_cv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CV File", "", "PDF Files (*.pdf);;Word Files (*.docx);;All Files (*)", options=options)
        if file_path:
            success = userdb_management.update_cv(self.user_id, file_path) 
            if success:
                QMessageBox.information(self, "Success", "CV uploaded successfully!")
                self.update_cv_label()  # Update the CV label to show the new CV
            else:
                QMessageBox.warning(self, "Error", "Failed to upload CV.")

    def search_jobs(self):
        self.jobs_search_page = JobsSearchPage(self.user_id)
        self.jobs_search_page.show()
        self.close()
    
    # Ajouter ce bouton dans __init__ de ProfilePage
        self.view_applied_jobs_button = QPushButton('Afficher les jobs postulés', self)
        self.view_applied_jobs_button.clicked.connect(self.view_applied_jobs)
        layout.addWidget(self.view_applied_jobs_button)

    # Ajouter la fonction suivante dans ProfilePage
    def view_applied_jobs(self):
        self.applied_jobs_page = AppliedJobsPage(self.user_id)
        self.applied_jobs_page.show()


#Application Jobs Search Page
class JobsSearchPage(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Search for Jobs")
        self.setGeometry(100, 100, 1000, 600)  
        layout = QVBoxLayout()

        title = QLabel("Search for Jobs", self)
        title.setFont(QFont('Arial', 20))

        search_button = QPushButton('Search', self)
        help_button = QPushButton('How to apply?', self)
        profile_button = QPushButton('Go back to Profile', self)
        signout_button = QPushButton('Sign out', self)

        search_button.clicked.connect(self.search)
        help_button.clicked.connect(self.help)
        profile_button.clicked.connect(self.go_profile)
        signout_button.clicked.connect(self.go_home)

        # Results table
        self.results_table = QTableWidget(self)
        self.results_table.setColumnCount(8)  # Number of columns for job details
        self.results_table.setHorizontalHeaderLabels(["Job ID", "Title", "Company", "Type", "Involvement", "City", "State", " "])
        self.results_table.setFixedHeight(300)  # Set a fixed height for the table
        self.results_table.setMinimumWidth(900)  # Set a minimum width for the table

        layout.addWidget(title)
        layout.addWidget(QLabel("Enter keywords for job:", self))
        self.keyword_input = QLineEdit(self)
        layout.addWidget(self.keyword_input)
        layout.addWidget(search_button)
        layout.addWidget(help_button)
        layout.addWidget(signout_button)
        layout.addWidget(profile_button)
        layout.addWidget(self.results_table) 

        self.setLayout(layout)

    def search(self):
        keyword = self.keyword_input.text().strip()  # search bar for user
        if not keyword:
            QMessageBox.warning(self, "Input Error", "Please enter a keyword.")
            return
        # Search for jobs in the database:
        results = jobsdb_management.search_jobs(keyword)
        # Clear previous results in the table
        self.results_table.setRowCount(0)
        if results:
            # Fill table with search results
            self.results_table.setRowCount(len(results))
            for row_index, row_data in enumerate(results):
                for column_index, data in enumerate(row_data):
                    self.results_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
                # Create a "More" button for each job entry
                apply_button = QPushButton("More")
                apply_button.clicked.connect(lambda checked, job_id=row_data[0]: self.show_job_details(job_id))
                self.results_table.setCellWidget(row_index, self.results_table.columnCount() - 1, apply_button)  # Add button to the last column

        else:
            QMessageBox.information(self, "No Results", "No jobs found for the given keyword.")

    def show_job_details(self, job_id):
        if job_id:
            job_details = jobsdb_management.get_job_details(job_id)  # get job details from database

        if job_details:
            # Convert job_details list to a string
            job_details_str = "\n".join([str(detail) for detail in job_details])

            # Create a message box to display job details
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Job Description")
            msg_box.setText(job_details_str)
            msg_box.setIcon(QMessageBox.Information)
            # Add an "Apply" button to the message box
            apply_button = msg_box.addButton("Apply", QMessageBox.AcceptRole)
            msg_box.addButton(QMessageBox.Cancel)

            # Show the message box
            msg_box.exec_()

            # If the user clicks the "Apply" button, handle the application
            if msg_box.clickedButton() == apply_button:
                self.apply_for_job(job_id)  # Call the apply function

    def apply_for_job(self, job_id):
        success = jobsdb_management.update_total_applicants(job_id)
        if success:
            QMessageBox.information(self, "Application Sent", f"You have applied for the job with ID: {job_id}")
        else:
            QMessageBox.warning(self, "Application Failed", "Failed to apply for the job. Try again later.")
    def help(self):
        QMessageBox.information(self, "How to apply?", "To apply for a job, click on 'More'")

    def go_home(self):
        self.home_page = HomePage()
        self.home_page.show()
        self.close()
        
    def go_profile(self):
        self.profile_page = ProfilePage(self.user_id)
        self.profile_page.show()
        self.close()

class AppliedJobsPage(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Jobs Postulés")
        self.setGeometry(100, 100, 800, 400)

        layout = QVBoxLayout()
        title = QLabel("Liste des jobs postulés", self)
        title.setFont(QFont('Arial', 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Table pour afficher les jobs
        self.jobs_table = QTableWidget(self)
        self.jobs_table.setColumnCount(6)
        self.jobs_table.setHorizontalHeaderLabels(["Job ID", "Titre", "Entreprise", "Type", "Ville", "État"])
        layout.addWidget(self.jobs_table)

        # Charger les données
        self.load_jobs()

        # Bouton retour
        back_button = QPushButton("Retour au profil", self)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def load_jobs(self):
        jobs = jobsdb_management.get_applied_jobs(self.user_id)
        if jobs:
            self.jobs_table.setRowCount(len(jobs))
            for row_index, row_data in enumerate(jobs):
                for column_index, data in enumerate(row_data):
                    self.jobs_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
        else:
            QMessageBox.information(self, "Info", "Aucun job postulé trouvé.")

    def go_back(self):
        self.close()


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_style(app)
    main_window = HomePage()
    main_window.show()
    sys.exit(app.exec_())

userdb_managemeent.py 
import psycopg2
import bcrypt

# Connection credentials
DATABASE_CONFIG = {
    "database": "mabdd",
    "user": "samelis",
    "host": "localhost",
    "password": "Melissa20%03"
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


    jobsdb_management .py 
    #For when user uses the search bar to look for jobs
import psycopg2

# Connection credentials
DATABASE_CONFIG = {
    "database": "mabdd",
    "user": "samelis",
    "host": "localhost",
    "password": "Melissa20%03"
}

def create_jobs_table():
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
                    CREATE TABLE IF NOT EXISTS Jobs (
                        job_ID numeric (10,0),
                        designation text,
                        company_id numeric(5,1),
                        name text,
                        work_type text,
                        involvement text,
                        employees_count numeric(5,0),
                        total_applicants numeric(5,0),
                        followers numeric,
                        job_details text,
                        details_id numeric(5,0),
                        industry text,
                        level text,
                        City text,
                        State text,
                        PRIMARY KEY (job_ID)
                    );
                ''')
        print("Table 'Jobs' created successfully or already exists.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# function to verify if the jobs table is empty
def is_jobs_table_empty():
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"]
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Jobs;") 
        count = cursor.fetchone()[0] 
        return count == 0 
    
    except Exception as e:
        print(f"Error checking if jobs table is empty: {e}")
        return True  

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def fill_jobs_table():
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"]
        )
        with conn:
            with conn.cursor() as cursor:
                # Read the SQL file
                with open('jobs_data.sql', 'r') as file:
                    sql_commands = file.read()
                
                # Execute the SQL commands
                cursor.execute(sql_commands)
                print("Jobs table filled successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

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
            FROM Jobs
            WHERE {where_clause};
            """
        else:
            # If no search parameters are provided, return jobs with designation "Other"
            query = """
            SELECT job_ID, designation, name, work_type, involvement, City, State 
            FROM Jobs
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
    #print("ID: ", id)  debugging
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

def update_total_applicants(job_id):
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
                    UPDATE Jobs
                    SET total_applicants = total_applicants + 1
                    WHERE job_ID = %s
                ''', (job_id,))
    except psycopg2.Error as e:
        print(f"An error occurred while updating the total applicants: {e}")
        return False
    finally:
        if conn:
            conn.close()
            return True        

def get_applied_jobs(user_id):
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
                    SELECT j.job_ID, j.designation, j.name, j.work_type, j.City, j.State
                    FROM apply a
                    INNER JOIN Jobs j ON a.job_id = j.job_ID
                    WHERE a.user_id = %s
                ''', (user_id,))
                return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if conn:
            conn.close()
create table apply (
    application_id SERIAL PRIMARY KEY,   -- Identifiant unique de la postulation
    user_id INT NOT NULL,                -- L'ID de l'utilisateur qui a postulé
    job_id INT NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,  -- Clé étrangère vers la table `users`
    FOREIGN KEY (job_id) REFERENCES jobs(job_ID) ON DELETE CASCADE     -- Clé étrangère vers la table `jobs`
)