from PyQt5.QtWidgets import *
from db_helper import DB, DB_CONFIG
# from main_window import *

class UpdateDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("수정")
        self.db = DB(**DB_CONFIG)


        self.name = QLineEdit()
        self.price = QLineEdit()
        self.stock = QSpinBox()

        form = QFormLayout()

        form.addRow("상품명", self.name)

        form.addRow("가격", self.price)
        form.addRow("재고", self.stock)

        
        buttonBox = QHBoxLayout()

        self.btn_submit = QPushButton("수정")
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel = QPushButton("취소")
        self.btn_cancel.clicked.connect(self.reject)

        buttonBox.addWidget(self.btn_submit)
        buttonBox.addWidget(self.btn_cancel)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(buttonBox)
        self.setLayout(layout)


    def submit(self):
        name = self.name.text().strip()
        price = self.price.text().strip()
        stock = self.stock.value()
        if not name or not price or not stock:
            QMessageBox.warning(self, "오류", "데이터를 빠짐없이 입력하세요.")
            return
        ok = self.db.update_fruit(name, price, stock)
        if ok:
            QMessageBox.information(self, "완료","수정되었습니다.")
        else:
            QMessageBox.critical(self, "실패","실패함")
        self.accept()