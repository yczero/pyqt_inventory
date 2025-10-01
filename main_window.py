
# main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("과일 관리")
        self.db = DB(**DB_CONFIG)
        
        # # --- central widget ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        
        # 1. 전체 레이아웃
        vbox = QVBoxLayout()
        central_widget.setLayout(vbox)

        # --- 입력 영역 ---
        form_box = QHBoxLayout()
        self.fruit_name_input = QLineEdit()
        self.fruit_name_input.setPlaceholderText("과일명 입력")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("가격입력")
        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("재고 입력")  # 새로 추가


        self.add_btn = QPushButton("추가")
        self.add_btn.clicked.connect(self.add_fruit)

        
        form_box.addWidget(self.fruit_name_input)
        form_box.addWidget(self.stock_input)
        form_box.addWidget(self.price_input)
        form_box.addWidget(self.add_btn)
        

        # --- 테이블 ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "과일명", "재고", "가격"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        
        vbox.addLayout(form_box)
        vbox.addWidget(self.table)

        self.setLayout(vbox)

        # 버튼 이벤트
        
        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("재고 불러오기")
        self.load_btn.clicked.connect(self.load_data)

        self.delete_btn = QPushButton("삭제")
        self.delete_btn.clicked.connect(self.delete_fruit)
        self.update_btn = QPushButton("수정")
        self.update_btn.clicked.connect(self.update_fruit)
        btn_layout.addWidget(self.load_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.update_btn)
        vbox.addLayout(btn_layout)


        vbox.addWidget(self.table)

        self.load_data()


    def load_data(self):    
        rows = self.db.fetch_all_fruits()
        self.table.setRowCount(len(rows))

        for row, (fruit_id, fruit_name, stock, price) in enumerate(rows):
            self.table.setItem(row, 0, QTableWidgetItem(str(fruit_id)))
            self.table.setItem(row, 1, QTableWidgetItem(fruit_name))
            self.table.setItem(row, 2, QTableWidgetItem(str(stock))) 
            self.table.setItem(row, 3, QTableWidgetItem(str(price))) 
        self.table.resizeColumnsToContents()
        
        
    def add_fruit(self):
        fruit_name = self.fruit_name_input.text().strip()
        stock_text = self.stock_input.text().strip()
        price_text = self.price_input.text().strip()
        if not fruit_name:
            QMessageBox.warning(self, "경고", "과일명을 입력하세요")
            return
        try:
            stock = int(stock_text) if stock_text else 0
        except ValueError:
            QMessageBox.warning(self, "경고", "재고는 숫자로 입력하세요")
            return

        try:
            price = int(price_text) if price_text else 0
        except ValueError:
            QMessageBox.warning(self, "경고", "가격은 숫자로 입력하세요")
            return
        
        ok = self.db.insert_fruit(fruit_name,stock=stock,price = price)
        if ok:
            QMessageBox.information(self, "완료", "추가됨")
            self.fruit_name_input.clear()
            self.stock_input.clear()
            self.price_input.clear()
            self.load_data()
        else:
            QMessageBox.critical(self, "실패", "추가 중 오류 발생")


    def delete_fruit(self):
        selected =self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "경고", " 삭제 과일 선택 ")
            return

        fruit_name_item = self.table.item(selected,1)
        if not fruit_name_item:
            return
        
        fruit_name = fruit_name_item.text()

        ok = self.db.delete_fruit_by_name(fruit_name)
        if ok:
            QMessageBox.information(self, "완료", "삭제됨")
            self.load_data()
        else:
            QMessageBox.critical(self, "실패", "삭제 중 오류 발생")
    


    def update_fruit(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "경고", "수정할 과일을 선택하세요")
            return

        fruit_name = self.table.item(selected, 1).text()

        try:
            stock = int(self.stock_input.text())
            price = int(self.price_input.text())
        except ValueError:
            QMessageBox.warning(self, "경고", "재고와 가격은 숫자로 입력하세요")
            return

        ok = self.db.update_fruit(fruit_name, stock, price)
        if ok:
            QMessageBox.information(self, "완료", f"{fruit_name} 수정됨")
            self.fruit_name_input.clear()
            self.stock_input.clear()
            self.price_input.clear()
            self.load_data()
        else:
            QMessageBox.critical(self, "실패", "수정 중 오류 발생")
        



