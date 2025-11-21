# notification_manager.py
import random
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QFont

class NotificationWidget(QWidget):
    """Красивое всплывающее уведомление"""
    closed = pyqtSignal()
    
    def __init__(self, title, message, notification_type="info", parent=None):
        super().__init__(parent)
        # Настройки окна уведомления
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(380, 140)
        
        # Цветовые схемы для разных типов уведомлений
        color_schemes = {
            "info": {
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e8f4fd, stop:1 #d4edda)",
                "border": "#bee5eb",
                "header_bg": "#17a2b8",
                "icon": "💡"
            },
            "warning": {
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #fff3cd, stop:1 #ffeaa7)",
                "border": "#ffeaa7",
                "header_bg": "#ffc107",
                "icon": "⚠️"
            },
            "success": {
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d4edda, stop:1 #c3e6cb)",
                "border": "#c3e6cb",
                "header_bg": "#28a745",
                "icon": "✅"
            },
            "error": {
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f8d7da, stop:1 #f5c6cb)",
                "border": "#f5c6cb",
                "header_bg": "#dc3545",
                "icon": "❌"
            }
        }
        
        scheme = color_schemes.get(notification_type, color_schemes["info"])
        
        self.setStyleSheet(f"""
            QWidget {{
                background: {scheme['background']};
                border: 2px solid {scheme['border']};
                border-radius: 12px;
            }}
            QLabel {{
                background: transparent;
                color: #2c3e50;
            }}
            QPushButton {{
                background: rgba(255,255,255,0.9);
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 500;
                color: #495057;
            }}
            QPushButton:hover {{
                background: rgba(255,255,255,1);
                border: 1px solid rgba(0,0,0,0.2);
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Шапка уведомления с иконкой и заголовком
        header_widget = QWidget()
        header_widget.setStyleSheet(f"""
            background: {scheme['header_bg']};
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            padding: 8px 12px;
        """)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(f"{scheme['icon']} {title}")
        title_label.setStyleSheet("""
            color: white;
            font-size: 14px;
            font-weight: 600;
            background: transparent;
        """)
        title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        header_layout.addWidget(title_label)
        header_widget.setLayout(header_layout)
        layout.addWidget(header_widget)
        
        # Основное содержимое уведомления
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            background: transparent;
            padding: 12px;
        """)
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Текст сообщения
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            font-size: 13px;
            color: #495057;
            line-height: 1.4;
            background: transparent;
            padding: 5px 0px;
        """)
        message_label.setFont(QFont("Segoe UI", 10))
        message_label.setWordWrap(True)
        content_layout.addWidget(message_label)
        
        # Кнопка закрытия
        close_btn = QPushButton("Понятно")
        close_btn.setFixedSize(80, 28)
        close_btn.clicked.connect(self.close_notification)
        content_layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        content_widget.setLayout(content_layout)
        layout.addWidget(content_widget)
        
        self.setLayout(layout)
        
        # Автоматическое закрытие через 10 секунд
        self.auto_close_timer = QTimer()
        self.auto_close_timer.timeout.connect(self.close_notification)
        self.auto_close_timer.start(10000)
    
    def close_notification(self):
        """Плавное закрытие уведомления"""
        self.auto_close_timer.stop()
        self.closed.emit()
        self.close()

class SmartNotificationManager:
    """Менеджер умных уведомлений для системы закупок"""
    
    def __init__(self):
        self.active_notifications = []
        
        # База шаблонов уведомлений с естественными формулировками
        self.procurement_notifications = [
            {
                "type": "info",
                "title": "Новые возможности",
                "templates": [
                    "В {region} появились новые закупки по теме '{product}'. Рекомендуем ознакомиться с актуальными тендерами.",
                    "Обнаружены подходящие закупки в вашем регионе. Проверьте обновления по запросу '{product}'.",
                    "Система нашла несколько интересных предложений по {product} в {region}. Возможно, вас заинтересуют эти варианты."
                ]
            },
            {
                "type": "success", 
                "title": "Отличная находка",
                "templates": [
                    "Найдена выгодная закупка '{product}' с минимальной конкуренцией. Идеальный вариант для участия!",
                    "Обнаружен тендер с прекрасными условиями по {product}. Шансы на победу высоки!",
                    "Подобрана закупка, полностью соответствующая вашим критериям. Рекомендуем подать заявку."
                ]
            },
            {
                "type": "warning",
                "title": "Внимание, сроки",
                "templates": [
                    "Закупка по '{product}' завершается через несколько часов. Успейте подать заявку!",
                    "Напоминаем: срок подачи предложений по тендеру '{product}' подходит к концу.",
                    "Осталось мало времени для участия в интересной закупке. Не упустите возможность!"
                ]
            },
            {
                "type": "info",
                "title": "Статистика поиска",
                "templates": [
                    "За последнее время в {region} появилось 15+ новых закупок по вашему запросу '{product}'.",
                    "По вашему фильтру найдено несколько перспективных тендеров. Рекомендуем изучить детали.",
                    "Система отслеживает 8 активных закупок, соответствующих запросу '{product}' в {region}."
                ]
            }
        ]
    
    def generate_smart_notification(self, region, keywords):
        """
        Генерирует понятное и полезное уведомление на основе контекста
        
        Args:
            region (str): Выбранный регион поиска
            keywords (str): Ключевые слова запроса
            
        Returns:
            dict: Данные для формирования уведомления
        """
        if not keywords.strip():
            keywords = "различные товары и услуги"
        else:
            keywords = f"'{keywords}'"
        
        # Выбираем случайный шаблон уведомления
        notification_data = random.choice(self.procurement_notifications)
        template = random.choice(notification_data["templates"])
        
        # Форматируем сообщение с реальными данными
        message = template.format(
            product=keywords,
            region=region
        )
        
        return {
            "type": notification_data["type"],
            "title": notification_data["title"],
            "message": message
        }