import sys
import psycopg2
from urllib.parse import urlparse
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class DatabaseViewer(QMainWindow):
    def __init__(self, db_url):  # Принимаем URL как аргумент
        super().__init__()
        self.db_url = db_url
        self.initUI()

    def initUI(self):
        self.setWindowTitle('RosDataTech - Database Viewer')
        self.setGeometry(100, 100, 1000, 700)

        # Основной виджет и layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Заголовок приложения
        self.title_label = QLabel('RosDataTech')
        self.title_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #2E86C1;
                padding: 20px;
                border-bottom: 2px solid #2E86C1;
            }
        """)
        self.layout.addWidget(self.title_label)

        # Выпадающий список для выбора таблицы
        self.table_label = QLabel('Выберите таблицу:')
        self.table_label.setFont(QFont('Arial', 12))
        self.table_label.setStyleSheet("color: #34495E;")

        self.table_combobox = QComboBox()
        self.table_combobox.setFont(QFont('Arial', 12))
        self.table_combobox.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #2E86C1;
                border-radius: 5px;
                background-color: #F4F6F7;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #2E86C1;
            }
        """)
        self.table_combobox.currentIndexChanged.connect(self.load_table_data)

        # Layout для выпадающего списка
        combobox_layout = QHBoxLayout()
        combobox_layout.addWidget(self.table_label)
        combobox_layout.addWidget(self.table_combobox)
        self.layout.addLayout(combobox_layout)

        # Таблица для отображения данных
        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #F4F6F7;
                alternate-background-color: #E5E8E8;
                gridline-color: #2E86C1;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #2E86C1;
                color: white;
                padding: 5px;
                font-size: 14px;
                border: none;
            }
        """)
        self.table_widget.setAlternatingRowColors(True)
        self.layout.addWidget(self.table_widget)

        self.load_table_list()  # Загружаем список таблиц

    def load_table_list(self):
        url = urlparse(self.db_url)  

        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],
            user=url.username,
            password=url.password
        )
        cur = conn.cursor()

        cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' 
        AND table_name NOT LIKE 'pg%'
        """)
        tables = cur.fetchall()

        for table in tables:
            self.table_combobox.addItem(table[0].title())

        cur.close()
        conn.close()

    def load_table_data(self):
        selected_table = self.table_combobox.currentText()
        if not selected_table:
            return

        url = urlparse(self.db_url)  

        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],
            user=url.username,
            password=url.password
        )
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM {selected_table}')
        rows = cur.fetchall()

        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(rows[0])) if rows else 0

        column_names = [desc[0] for desc in cur.description]
        self.table_widget.setHorizontalHeaderLabels(column_names)

        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                item.setForeground(QColor("#2C3E50"))
                self.table_widget.setItem(i, j, item)

        cur.close()
        conn.close()
