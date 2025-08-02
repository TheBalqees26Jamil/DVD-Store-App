import sys
import json
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QMessageBox,
)
from PyQt6.QtGui import QColor, QPalette


class DVD:
    def __init__(self, title, stars, producer, director, production_company, num_copies):
        self.title = title
        self.stars = stars
        self.producer = producer
        self.director = director
        self.production_company = production_company
        self.num_copies = num_copies

    def to_dict(self):
        return {
            "title": self.title,
            "stars": self.stars,
            "producer": self.producer,
            "director": self.director,
            "production_company": self.production_company,
            "num_copies": self.num_copies,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["stars"],
            data["producer"],
            data["director"],
            data["production_company"],
            data["num_copies"],
        )


class Customer:
    def __init__(self, first_name, last_name, account_number):
        self.first_name = first_name
        self.last_name = last_name
        self.account_number = account_number
        self.rented_dvds = []

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "account_number": self.account_number,
            "rented_dvds": self.rented_dvds,
        }

    @classmethod
    def from_dict(cls, data):
        customer = cls(data["first_name"], data["last_name"], data["account_number"])
        customer.rented_dvds = data["rented_dvds"]
        return customer


class DVDStoreApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DVD Store Management")
        self.setGeometry(100, 100, 600, 400)


        # Set background color for the main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fae8d4  ;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 2px solid #2d0687;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #2d0687;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QListWidget {
                background-color: #ffffff;
                border: 2px solid #2d0687;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                color: #b60bdc;
            }
        """)

        # Load data from JSON file
        self.load_data()

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Add DVD Section
        self.add_dvd_section()
        self.layout.addSpacing(20)

        # Rent/Return DVD Section
        self.rent_return_section()
        self.layout.addSpacing(20)

        # Display DVDs Section
        self.display_dvds_section()

        # Save data when closing the app
        self.closeEvent = self.save_data

    def add_dvd_section(self):
        layout = QHBoxLayout()

        self.dvd_title_input = QLineEdit(placeholderText="Title")
        self.dvd_stars_input = QLineEdit(placeholderText="Stars (comma separated)")
        self.dvd_producer_input = QLineEdit(placeholderText="Producer")
        self.dvd_director_input = QLineEdit(placeholderText="Director")
        self.dvd_company_input = QLineEdit(placeholderText="Production Company")
        self.dvd_copies_input = QLineEdit(placeholderText="Number of Copies")

        add_dvd_button = QPushButton("Add DVD")
        add_dvd_button.clicked.connect(self.add_dvd)

        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.dvd_title_input)
        layout.addWidget(QLabel("Stars:"))
        layout.addWidget(self.dvd_stars_input)
        layout.addWidget(QLabel("Producer:"))
        layout.addWidget(self.dvd_producer_input)
        layout.addWidget(QLabel("Director:"))
        layout.addWidget(self.dvd_director_input)
        layout.addWidget(QLabel("Company:"))
        layout.addWidget(self.dvd_company_input)
        layout.addWidget(QLabel("Copies:"))
        layout.addWidget(self.dvd_copies_input)
        layout.addWidget(add_dvd_button)

        self.layout.addLayout(layout)

    def rent_return_section(self):
        layout = QHBoxLayout()

        self.customer_name_input = QLineEdit(placeholderText="Customer Name")
        self.dvd_rent_input = QLineEdit(placeholderText="DVD Title to Rent/Return")

        rent_button = QPushButton("Rent DVD")
        rent_button.clicked.connect(self.rent_dvd)

        return_button = QPushButton("Return DVD")
        return_button.clicked.connect(self.return_dvd)

        layout.addWidget(QLabel("Customer:"))
        layout.addWidget(self.customer_name_input)
        layout.addWidget(QLabel("DVD Title:"))
        layout.addWidget(self.dvd_rent_input)
        layout.addWidget(rent_button)
        layout.addWidget(return_button)

        self.layout.addLayout(layout)

    def display_dvds_section(self):
        self.dvd_list = QListWidget()
        self.update_dvd_list()
        self.layout.addWidget(self.dvd_list)

    def add_dvd(self):
        title = self.dvd_title_input.text()
        stars = self.dvd_stars_input.text().split(",")
        producer = self.dvd_producer_input.text()
        director = self.dvd_director_input.text()
        company = self.dvd_company_input.text()
        copies = int(self.dvd_copies_input.text())

        new_dvd = DVD(title, stars, producer, director, company, copies)
        self.data["dvds"].append(new_dvd.to_dict())
        self.update_dvd_list()
        QMessageBox.information(self, "Success", "DVD added successfully!")

    def rent_dvd(self):
        customer_name = self.customer_name_input.text()
        dvd_title = self.dvd_rent_input.text()

        # Find DVD
        dvd = next((d for d in self.data["dvds"] if d["title"] == dvd_title), None)
        if not dvd:
            QMessageBox.warning(self, "Error", "DVD not found!")
            return

        # Rent DVD
        if dvd["num_copies"] > 0:
            dvd["num_copies"] -= 1
            self.update_dvd_list()
            QMessageBox.information(self, "Success", f"DVD '{dvd_title}' rented by {customer_name}!")
        else:
            QMessageBox.warning(self, "Error", "No copies available!")

    def return_dvd(self):
        customer_name = self.customer_name_input.text()
        dvd_title = self.dvd_rent_input.text()

        # Find DVD
        dvd = next((d for d in self.data["dvds"] if d["title"] == dvd_title), None)
        if not dvd:
            QMessageBox.warning(self, "Error", "DVD not found!")
            return

        # Return DVD
        dvd["num_copies"] += 1
        self.update_dvd_list()
        QMessageBox.information(self, "Success", f"DVD '{dvd_title}' returned by {customer_name}!")

    def update_dvd_list(self):
        self.dvd_list.clear()
        for dvd in self.data["dvds"]:
            self.dvd_list.addItem(f"{dvd['title']} ({dvd['num_copies']} copies available)")

    def load_data(self):
        try:
            with open("data.json", "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {"dvds": [], "customers": []}

    def save_data(self, event):
        with open("data.json", "w") as file:
            json.dump(self.data, file, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DVDStoreApp()
    window.show()
    sys.exit(app.exec())

# import sys
# import json
# from PyQt6.QtWidgets import (
#     QApplication,
#     QMainWindow,
#     QWidget,
#     QVBoxLayout,
#     QHBoxLayout,
#     QLabel,
#     QLineEdit,
#     QPushButton,
#     QListWidget,
#     QMessageBox,
# )
#
#
# class DVD:
#     def __init__(self, title, stars, producer, director, production_company, num_copies):
#         self.title = title
#         self.stars = stars
#         self.producer = producer
#         self.director = director
#         self.production_company = production_company
#         self.num_copies = num_copies
#
#     def to_dict(self):
#         return {
#             "title": self.title,
#             "stars": self.stars,
#             "producer": self.producer,
#             "director": self.director,
#             "production_company": self.production_company,
#             "num_copies": self.num_copies,
#         }
#
#     @classmethod
#     def from_dict(cls, data):
#         return cls(
#             data["title"],
#             data["stars"],
#             data["producer"],
#             data["director"],
#             data["production_company"],
#             data["num_copies"],
#         )
#
#
# class Customer:
#     def __init__(self, first_name, last_name, account_number):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.account_number = account_number
#         self.rented_dvds = []
#
#     def to_dict(self):
#         return {
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "account_number": self.account_number,
#             "rented_dvds": self.rented_dvds,
#         }
#
#     @classmethod
#     def from_dict(cls, data):
#         customer = cls(data["first_name"], data["last_name"], data["account_number"])
#         customer.rented_dvds = data["rented_dvds"]
#         return customer
#
#
# class DVDStoreApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("DVD Store Management")
#         self.setGeometry(100, 100, 600, 400)
#
#         # Load data from JSON file
#         self.load_data()
#
#         # Main widget and layout
#         self.main_widget = QWidget()
#         self.setCentralWidget(self.main_widget)
#         self.layout = QVBoxLayout(self.main_widget)
#
#         # Add DVD Section
#         self.add_dvd_section()
#         self.layout.addSpacing(20)
#
#         # Rent/Return DVD Section
#         self.rent_return_section()
#         self.layout.addSpacing(20)
#
#         # Display DVDs Section
#         self.display_dvds_section()
#
#         # Save data when closing the app
#         self.closeEvent = self.save_data
#
#     def add_dvd_section(self):
#         layout = QHBoxLayout()
#
#         self.dvd_title_input = QLineEdit(placeholderText="Title")
#         self.dvd_stars_input = QLineEdit(placeholderText="Stars (comma separated)")
#         self.dvd_producer_input = QLineEdit(placeholderText="Producer")
#         self.dvd_director_input = QLineEdit(placeholderText="Director")
#         self.dvd_company_input = QLineEdit(placeholderText="Production Company")
#         self.dvd_copies_input = QLineEdit(placeholderText="Number of Copies")
#
#         add_dvd_button = QPushButton("Add DVD")
#         add_dvd_button.clicked.connect(self.add_dvd)
#
#         layout.addWidget(QLabel("Title:"))
#         layout.addWidget(self.dvd_title_input)
#         layout.addWidget(QLabel("Stars:"))
#         layout.addWidget(self.dvd_stars_input)
#         layout.addWidget(QLabel("Producer:"))
#         layout.addWidget(self.dvd_producer_input)
#         layout.addWidget(QLabel("Director:"))
#         layout.addWidget(self.dvd_director_input)
#         layout.addWidget(QLabel("Company:"))
#         layout.addWidget(self.dvd_company_input)
#         layout.addWidget(QLabel("Copies:"))
#         layout.addWidget(self.dvd_copies_input)
#         layout.addWidget(add_dvd_button)
#
#         self.layout.addLayout(layout)
#
#     def rent_return_section(self):
#         layout = QHBoxLayout()
#
#         self.customer_name_input = QLineEdit(placeholderText="Customer Name")
#         self.dvd_rent_input = QLineEdit(placeholderText="DVD Title to Rent/Return")
#
#         rent_button = QPushButton("Rent DVD")
#         rent_button.clicked.connect(self.rent_dvd)
#
#         return_button = QPushButton("Return DVD")
#         return_button.clicked.connect(self.return_dvd)
#
#         layout.addWidget(QLabel("Customer:"))
#         layout.addWidget(self.customer_name_input)
#         layout.addWidget(QLabel("DVD Title:"))
#         layout.addWidget(self.dvd_rent_input)
#         layout.addWidget(rent_button)
#         layout.addWidget(return_button)
#
#         self.layout.addLayout(layout)
#
#     def display_dvds_section(self):
#         self.dvd_list = QListWidget()
#         self.update_dvd_list()
#         self.layout.addWidget(self.dvd_list)
#
#     def add_dvd(self):
#         title = self.dvd_title_input.text()
#         stars = self.dvd_stars_input.text().split(",")
#         producer = self.dvd_producer_input.text()
#         director = self.dvd_director_input.text()
#         company = self.dvd_company_input.text()
#         copies = int(self.dvd_copies_input.text())
#
#         new_dvd = DVD(title, stars, producer, director, company, copies)
#         self.data["dvds"].append(new_dvd.to_dict())
#         self.update_dvd_list()
#         QMessageBox.information(self, "Success", "DVD added successfully!")
#
#     def rent_dvd(self):
#         customer_name = self.customer_name_input.text()
#         dvd_title = self.dvd_rent_input.text()
#
#         # Find DVD
#         dvd = next((d for d in self.data["dvds"] if d["title"] == dvd_title), None)
#         if not dvd:
#             QMessageBox.warning(self, "Error", "DVD not found!")
#             return
#
#         # Rent DVD
#         if dvd["num_copies"] > 0:
#             dvd["num_copies"] -= 1
#             self.update_dvd_list()
#             QMessageBox.information(self, "Success", f"DVD '{dvd_title}' rented by {customer_name}!")
#         else:
#             QMessageBox.warning(self, "Error", "No copies available!")
#
#     def return_dvd(self):
#         customer_name = self.customer_name_input.text()
#         dvd_title = self.dvd_rent_input.text()
#
#         # Find DVD
#         dvd = next((d for d in self.data["dvds"] if d["title"] == dvd_title), None)
#         if not dvd:
#             QMessageBox.warning(self, "Error", "DVD not found!")
#             return
#
#         # Return DVD
#         dvd["num_copies"] += 1
#         self.update_dvd_list()
#         QMessageBox.information(self, "Success", f"DVD '{dvd_title}' returned by {customer_name}!")
#
#     def update_dvd_list(self):
#         self.dvd_list.clear()
#         for dvd in self.data["dvds"]:
#             self.dvd_list.addItem(f"{dvd['title']} ({dvd['num_copies']} copies available)")
#
#     def load_data(self):
#         try:
#             with open("data.json", "r") as file:
#                 self.data = json.load(file)
#         except FileNotFoundError:
#             self.data = {"dvds": [], "customers": []}
#
#     def save_data(self, event):
#         with open("data.json", "w") as file:
#             json.dump(self.data, file, indent=4)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DVDStoreApp()
#     window.show()
#     sys.exit(app.exec())