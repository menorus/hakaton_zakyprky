import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QMessageBox, 
    QSpacerItem, QSizePolicy, QCheckBox
)
from PyQt6.QtCore import QTimer
from notification_manager import SmartNotificationManager, NotificationWidget

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.notification_manager = SmartNotificationManager()
        self.setup_ui()
        self.setup_notification_timer()
        
    def setup_ui(self):
        self.setWindowTitle("КонтрЗакупки · Поиск")
        self.setMinimumWidth(400)
        self.setMinimumHeight(550)

        # Установка стилей
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
            QCheckBox {
                font-size: 14px;
                margin: 5px 0;
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

        # Чекбоксы фильтров
        self.only_actual_checkbox = QCheckBox("Только актуальные закупки")
        self.only_actual_checkbox.setChecked(True)
        layout.addWidget(self.only_actual_checkbox)

        self.with_electronic_signature_checkbox = QCheckBox("Только с электронной подписью")
        layout.addWidget(self.with_electronic_signature_checkbox)

        self.include_archive_checkbox = QCheckBox("Включая архивные")
        layout.addWidget(self.include_archive_checkbox)

        self.search_button = QPushButton("🔍 Найти закупки")
        self.search_button.clicked.connect(self.handle_search)
        layout.addWidget(self.search_button)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.setLayout(layout)

    def setup_notification_timer(self):
        """Настройка таймера для показа уведомлений каждые 30 секунд"""
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.show_random_notification)
        self.notification_timer.start(5000)  # 30 секунд
        
        # Таймер для позиционирования уведомлений
        self.position_timer = QTimer()
        self.position_timer.timeout.connect(self.reposition_notifications)
        self.position_timer.start(100)

    def show_random_notification(self):
        """Показ случайного умного уведомления"""
        region = self.region_combo.currentText()
        keywords = self.keywords_edit.text()
        
        notification_data = self.notification_manager.generate_smart_notification(region, keywords)
        self.show_notification(notification_data)

    def show_notification(self, notification_data):
        """Показ уведомления в углу экрана"""
        notification = NotificationWidget(
            notification_data["title"],
            notification_data["message"],
            notification_data["type"],
            self
        )
        
        notification.closed.connect(lambda: self.remove_notification(notification))
        self.notification_manager.active_notifications.append(notification)
        
        self.reposition_notifications()
        notification.show()

    def remove_notification(self, notification):
        """Удаление уведомления из списка активных"""
        if notification in self.notification_manager.active_notifications:
            self.notification_manager.active_notifications.remove(notification)

    def reposition_notifications(self):
        """Позиционирование уведомлений в правом нижнем углу"""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        margin = 20
        notification_height = 120
        spacing = 10
        
        for i, notification in enumerate(self.notification_manager.active_notifications):
            x = screen_geometry.width() - notification.width() - margin
            y = screen_geometry.height() - (notification_height + spacing) * (i + 1) - margin
            notification.move(x, y)

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

    def closeEvent(self, event):
        """Закрытие всех уведомлений при закрытии приложения"""
        for notification in self.notification_manager.active_notifications[:]:
            notification.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SearchApp()
    window.show()
    sys.exit(app.exec())