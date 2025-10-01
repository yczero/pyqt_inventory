
# main_window.py
from PyQt5.QtWidgets import QMainWindow,QHeaderView, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox
from db_helper import DB, DB_CONFIG
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtWidgets import QCheckBox, QWidget, QHBoxLayout

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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["선택","ID", "과일명", "재고", "가격"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # 행 단위 선택
        self.table.verticalHeader().setVisible(False)

        
        # self.table.resizeColumnsToContents()
        # self.table.resizeRowsToContents()


        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)



        vbox.addLayout(form_box)
        vbox.addWidget(self.table)

        self.setLayout(vbox)

        # 버튼 이벤트
        
        btn_layout = QHBoxLayout()
        # self.load_btn = QPushButton("재고 불러오기")
        # self.load_btn.clicked.connect(self.load_data)

        self.delete_btn = QPushButton("삭제")
        self.delete_btn.clicked.connect(self.delete_fruit)
        self.update_btn = QPushButton("수정")
        self.update_btn.clicked.connect(self.update_fruit)
        self.table.cellClicked.connect(self.fill_inputs)
        # btn_layout.addWidget(self.load_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.update_btn)
        vbox.addLayout(btn_layout)


        vbox.addWidget(self.table)

        self.load_data()
    def on_check_state_changed(self, row, state):
        model = self.table.selectionModel()
        idx = self.table.model().index(row, 0)
        if state == Qt.Checked:
            # 해당 row 전체 선택
            model.select(idx, QItemSelectionModel.Select | QItemSelectionModel.Rows)
            # 현재 포커스를 과일명 셀로 이동 (so currentRow 가 설정됨)
            self.table.setCurrentCell(row, 2)
        else:
            model.select(idx, QItemSelectionModel.Deselect | QItemSelectionModel.Rows)


    def load_data(self):    
        rows = self.db.fetch_all_fruits()
        self.table.setRowCount(len(rows))

        for row, (fruit_id, fruit_name, stock, price) in enumerate(rows):
  # 체크박스 추가
            chk = QCheckBox()
            chk.setChecked(False)
            chk.stateChanged.connect(lambda state, r=row: self.on_check_state_changed(r, state))

                        # 체크박스를 셀 위젯으로 감싸서 중앙 정렬
            chk_widget = QWidget()
            layout = QHBoxLayout(chk_widget)
            layout.addWidget(chk)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            chk_widget.setLayout(layout)
            self.table.setCellWidget(row, 0, chk_widget)


            self.table.setItem(row, 1, QTableWidgetItem(str(fruit_id)))
            self.table.setItem(row, 2, QTableWidgetItem(fruit_name))
            self.table.setItem(row, 3, QTableWidgetItem(str(stock))) 
            self.table.setItem(row, 4, QTableWidgetItem(str(price))) 
        # self.table.resizeColumnsToContents()
        # self.table.resizeRowsToContents()
        
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

        fruit_name_item = self.table.item(selected,2)
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

        fruit_name = self.table.item(selected, 2).text()

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



# 새로 추가하는 함수
    def fill_inputs(self, row, column=None):
    # 선택한 행(row)의 값 가져오기
        fruit_name = self.table.item(row, 2).text()
        # stock = self.table.item(row, 2).text()
        # price = self.table.item(row, 3).text()

        # 입력창에 값 채우기
        self.fruit_name_input.setText(fruit_name)
        # self.stock_input.setText(stock)
        # self.price_input.setText(price)


    def on_check_state_changed(self, row, state):
        model = self.table.selectionModel()
        idx = self.table.model().index(row, 0)
        if state == Qt.Checked:
            for r in range(self.table.rowCount()):
                if r != row:
                    chk_widget = self.table.cellWidget(r, 0)
                    if chk_widget:
                        chk = chk_widget.findChild(QCheckBox)
                        if chk and chk.isChecked():
                            chk.blockSignals(True)  # 시그널 임시 차단
                            chk.setChecked(False)
                            chk.blockSignals(False)
            # 해당 row 선택
            model.select(idx, QItemSelectionModel.Select | QItemSelectionModel.Rows)
            self.table.setCurrentCell(row, 2)

            # 👉 체크되면 입력창에 값 채우기
            self.fill_inputs(row,2)

        else:
            model.select(idx, QItemSelectionModel.Deselect | QItemSelectionModel.Rows)
            self.fruit_name_input.clear()
