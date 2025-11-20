import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QFont

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("КонтрЗакупки · Поиск")
        self.setMinimumWidth(400)

        # Глобальный стиль для современного вида
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6fb;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 15px;
                color: #202945;
            }
            QLabel {
                font-weight: 600;
                font-size: 16px;
                margin-top: 16px;
                margin-bottom: 4px;
            }
            QComboBox, QLineEdit {
                border: 1px solid #d2d7e1;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 15px;
                background: #fff;
                margin-bottom: 8px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0057b7, stop:1 #228be6);
                color: #fff;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                padding: 10px 0;
                margin-top: 8px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #006add;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        self.region_label = QLabel("Регион")
        layout.addWidget(self.region_label)
        self.region_combo = QComboBox()
        regions = ["Москва", "Санкт-Петербург", "Новосибирск", "Красноярск", "Ростов-на-Дону", "Воронеж"]
        self.region_combo.addItems(regions)
        layout.addWidget(self.region_combo)

        self.keywords_label = QLabel("Ключевые слова")
        layout.addWidget(self.keywords_label)
        self.keywords_edit = QLineEdit()
        self.keywords_edit.setPlaceholderText("Например: мужские джинсы")
        layout.addWidget(self.keywords_edit)

        self.search_button = QPushButton("🔍 Найти закупки")
        self.search_button.clicked.connect(self.handle_search)
        layout.addWidget(self.search_button)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.setLayout(layout)

    def handle_search(self):
        region = self.region_combo.currentText()
        keywords = self.keywords_edit.text()
        QMessageBox.information(self, "Результаты поиска", f"Регион: {region}\nКлючевые слова: {keywords}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SearchApp()
    window.show()
    sys.exit(app.exec())
