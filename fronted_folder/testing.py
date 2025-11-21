import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QMessageBox, 
    QSpacerItem, QSizePolicy, QCheckBox
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.set_background_image('start.jpg')
        
    def set_background_image(self, image_path):
        """Устанавливает изображение как фон"""
        try:
            full_path = os.path.join(os.path.dirname(__file__), image_path)
            
            if os.path.exists(full_path):
                pixmap = QPixmap(full_path)
                
                palette = self.palette()
                palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap.scaled(
                    self.size(), 
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )))
                self.setPalette(palette)
            else:
                print(f"Файл изображения не найден: {full_path}")
        except Exception as e:
            print(f"Ошибка при загрузке фона: {e}")

    def resizeEvent(self, event):
        """Переопределяем метод для обновления фона при изменении размера окна"""
        self.set_background_image('background.jpg')
        super().resizeEvent(event)
        
    def setup_ui(self):
        self.setWindowTitle("КонтрЗакупки · Поиск")
        # self.setMinimumWidth(1910)
        # self.setMinimumHeight(1050)

        # Загрузка стилей из файла
        self.load_styles()

        # Основной вертикальный макет
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 80, 30, 30)
        main_layout.setSpacing(12)

        # Добавляем основные виджеты
        self.keywords_edit = QLineEdit()
        self.keywords_edit.setPlaceholderText("\u25BC Введите ключевые слова для поиска ТЗ")
        main_layout.addWidget(self.keywords_edit)

        self.region_label = QLabel("Регион поставки")
        main_layout.addWidget(self.region_label)
        self.region_combo = QComboBox()
        regions = ["Нижегородская область"]
        self.region_combo.addItems(regions)
        main_layout.addWidget(self.region_combo)

        # Кнопка загрузки ТЗ
        self.download_button = QPushButton("\U0001F4C4 Загрузить ТЗ")  # Переименовал для ясности
        self.download_button.setObjectName("searchButton")
        self.download_button.clicked.connect(self.dowland_tz)
        main_layout.addWidget(self.download_button)

        # Растягивающийся спейсер, который займет все доступное пространство
        main_layout.addStretch(1)

        # Горизонтальный макет для нижней части с кнопкой "Найти"
        bottom_layout = QHBoxLayout()
        
        # Кнопка "Найти" выровнена по левому краю
        self.search_button = QPushButton("Найти")
        self.search_button.clicked.connect(self.dowland_tz)  # Замените на нужный метод
        bottom_layout.addWidget(self.search_button)
        
        # Растягивающийся спейсер справа, чтобы кнопка осталась слева
        bottom_layout.addStretch(1)
        
        # Добавляем нижний макет в основной
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def load_styles(self):
        """Загрузка стилей из файла CSS"""
        try:
            css_file_path = os.path.join(os.path.dirname(__file__), 'styles.css')
            with open(css_file_path, 'r', encoding='utf-8') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Файл стилей styles.css не найден. Используются стандартные стили.")
        except Exception as e:
            print(f"Ошибка при загрузке стилей: {e}")

    def dowland_tz(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл ТЗ",
            "",
            "All Files (*)"
        )
        if file_path:
            print(f"Выбран файл: {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SearchApp()
    window.showMaximized()
    sys.exit(app.exec())