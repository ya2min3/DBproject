import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout()
label = QLabel("Hello, PyQt5!")
layout.addWidget(label)
window.setLayout(layout)
window.setWindowTitle("Test Window")
window.show()

sys.exit(app.exec_())
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication

# Couleurs du style
PRIMARY_COLOR = "#4CAF50"  # Vert clair
SECONDARY_COLOR = "#FFFFFF"  # Blanc
BACKGROUND_COLOR = "#F5F5F5"  # Gris clair
TEXT_COLOR = "#212121"  # Noir doux
HIGHLIGHT_COLOR = "#FFC107"  # Jaune clair
ERROR_COLOR = "#F44336"  # Rouge

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

# Exemple d'application
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    apply_style(app)
    
    # Continuez à créer et afficher vos widgets ici
    sys.exit(app.exec_())
    class HomePage(QWidget):
    app = QApplication(sys.argv)
    apply_style(app)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Job")
        self.setGeometry(100, 100, 1000, 500)

        # Ajouter le logo à la fenêtre
        self.add_logo_to_window("logo.jpg")

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

    # Déplacer cette méthode à l'intérieur de la classe HomePage
    def add_logo_to_window(self, logo_path, logo_size=(100, 100)):
        # Créer un QLabel pour afficher l'image
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(logo_path)  # Utilisez le chemin correct du logo
        logo_label.setPixmap(logo_pixmap.scaled(logo_size[0], logo_size[1]))
        logo_label.setAlignment(Qt.AlignCenter)
        
        # Ajouter le logo à la mise en page
        main_layout = self.layout()
        main_layout.addWidget(logo_label, 0, Qt.AlignCenter)

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
            "À propos de My Job", 
            "My Job est une plateforme qui vous permet de rechercher des offres d'emploi ou de publier des offres d'emploi ! "
            "Vous pouvez également rechercher d'autres utilisateurs et consulter leurs CV !"
        )

# Create a QLabel to display the logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(logo_path)  # Use the correct logo path
        logo_label.setPixmap(logo_pixmap.scaled(logo_size[0], logo_size[1]))  # Scale the image to the desired size
        logo_label.setAlignment(Qt.AlignCenter)  # Center the logo in the QLabel

        # Add the logo label to the layout
        main_layout = self.layout()  # Get the layout of the window
        if main_layout:
            main_layout.insertWidget(0, logo_label)  # Add the logo at the top of the layout