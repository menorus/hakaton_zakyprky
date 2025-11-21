import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QMessageBox, 
    QSpacerItem, QSizePolicy, QCheckBox
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt

# Убедитесь, что импорт корректный
# from notification_manager import SmartNotificationManager, NotificationWidget

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        # self.notification_manager = SmartNotificationManager()
        self.setup_ui()
        self.set_background_image('start.jpg')  # Добавьте эту строку
        
    def set_background_image(self, image_path):
        """Устанавливает изображение как фон"""
        try:
            # Полный путь к изображению
            full_path = os.path.join(os.path.dirname(__file__), image_path)
            
            if os.path.exists(full_path):
                pixmap = QPixmap(full_path)
                
                # Создаем палитру для установки фона
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
        self.setMinimumWidth(1920)
        self.setMinimumHeight(1080)

        # Загрузка стилей из файла
        self.load_styles()

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 80, 30, 30)
        layout.setSpacing(12)

        self.keywords_edit = QLineEdit()
        self.keywords_edit.setPlaceholderText("\u25BC Введите ключевые слова для поиска ТЗ")
        layout.addWidget(self.keywords_edit)


        self.region_label = QLabel("Регион поставки")
        layout.addWidget(self.region_label)
        self.region_combo = QComboBox()
        regions = ["Нижегородская область"]
        self.region_combo.addItems(regions)
        layout.addWidget(self.region_combo)


        # Чекбоксы фильтров
        self.only_actual_checkbox = QCheckBox("Сохранить шаблон")
        self.only_actual_checkbox.setChecked(False)
        layout.addWidget(self.only_actual_checkbox)

        self.search_button = QPushButton("\U0001F4C4 Загрузить ТЗ")
        self.search_button.setObjectName("searchButton")
        self.search_button.clicked.connect(self.handle_search)
        layout.addWidget(self.search_button)

        self.search_button = QPushButton("Найти")
        self.search_button.clicked.connect(self.handle_search)
        layout.addWidget(self.search_button)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.setLayout(layout)

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

    def handle_search(self):
        region = self.region_combo.currentText()
        keywords = self.keywords_edit.text()
        only_actual = self.only_actual_checkbox.isChecked()
        with_electronic_signature = self.with_electronic_signature_checkbox.isChecked()
        include_archive = self.include_archive_checkbox.isChecked()
        
        message = (f"Регион: {region}\n"
                  f"Ключевые слова: {keywords}\n"
                  f"Только актуальные: {'Да' if only_actual else 'Нет'}\n"
                  f"С электронной подписью: {'Да' if with_electronic_signature else 'Нет'}\n"
                  f"Включая архивные: {'Да' if include_archive else 'Нет'}")
        
        QMessageBox.information(self, "Результаты поиска", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SearchApp()
    window.show()
    sys.exit(app.exec())