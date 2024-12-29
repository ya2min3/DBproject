import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import userdb_management 

# Create the user table
userdb_management.create_users_table()

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Job")
        self.setGeometry(100, 100, 1000, 500)
        layout = QVBoxLayout()

        title = QLabel("Welcome to My Job!\nPlease sign up or login to continue.", self)
        title.setFont(QFont('Arial', 20))

        presentation_button = QPushButton('Learn more about "My Job"?', self)
        sign_up_button = QPushButton('Sign Up', self)
        login_button = QPushButton('Login', self)

        presentation_button.clicked.connect(self.presentation)
        sign_up_button.clicked.connect(self.open_sign_up)
        login_button.clicked.connect(self.open_login)

        layout.addWidget(title)
        layout.addWidget(presentation_button)
        layout.addWidget(sign_up_button)
        layout.addWidget(login_button)

        self.setLayout(layout)

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


class SignupPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setGeometry(100, 100, 1000, 500)
        layout = QVBoxLayout()

        title = QLabel("Please enter your information to sign up:", self)
        title.setFont(QFont('Arial', 20))

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


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 1000, 500)
        layout = QVBoxLayout()

        title = QLabel("Please enter your login information:", self)
        title.setFont(QFont('Arial', 20))

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

        user_id = userdb_management.login(email, password)
        if user_id:
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


class ProfilePage(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id  # Store the user's ID for fetching user-specific data
        self.setWindowTitle("Profile")
        self.setGeometry(100, 100, 1000, 500)
        layout = QVBoxLayout()

        title = QLabel(f"Welcome to your profile page, User {self.user_id}!", self)
        title.setFont(QFont('Arial', 20))

        layout.addWidget(title)
        self.setLayout(layout)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = HomePage()
    main_window.show()
    sys.exit(app.exec_())
