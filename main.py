import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QFontDatabase, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import userdb_management 
import jobsdb_management
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
        title.setFont(QFont('Arial', 20))

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


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_style(app)
    main_window = HomePage()
    main_window.show()
    sys.exit(app.exec_())