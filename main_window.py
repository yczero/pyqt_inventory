# main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("과일 관리")
        self.db = DB(**DB_CONFIG)


        central = QWidget()
        self.setCentralWidget(central)


        vbox= QVBoxLayout(central)
        
        form_box = QHBoxLayout()
        self.input_fruit = QLineEdit()
        self.input_stock = QLineEdit()
        self.btn_add = QPushButton("추가")

