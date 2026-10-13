import sys
import numpy as np
import cv2
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, 
    QVBoxLayout, QWidget, QLabel, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap


class MainWindow(QMainWindow):
    """Главное окно приложения «Просмотр изображения»."""
    
    def __init__(self):
        super().__init__()
        # 1. Устанавливаем заголовок и размеры окна согласно заданию
        self.setWindowTitle("Просмотр изображения")
        self.setGeometry(100, 100, 800, 600)
        
        self.init_ui()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Вертикальный макет для элементов (QVBoxLayout)
        layout = QVBoxLayout()
        
        # QLabel для отображения изображения
        self.image_label = QLabel("Изображение не загружено")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed #aaa; color: #555;")
        self.image_label.setMinimumSize(400, 400)
        
        # Кнопка «Загрузить изображение»
        self.load_button = QPushButton("Загрузить изображение")
        self.load_button.setMinimumHeight(40)
        
        # Подключаем сигнал нажатия кнопки к слоту
        self.load_button.clicked.connect(self.on_load_button_click)
        
        # Добавляем виджеты в макет
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        
        # Устанавливаем макет на центральный виджет
        central_widget.setLayout(layout)
    
    def on_load_button_click(self):
        """Слот: выбор файла через диалоговое окно, безопасная загрузка и отображение."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            try:
                # Безопасное чтение файла через байтовый буфер (исправляет проблему с кириллицей в путях Windows)
                with open(file_path, 'rb') as f:
                    chunk = f.read()
                byteArray = bytearray(chunk)
                stream = np.asarray(byteArray, dtype=np.uint8)
                cv_image = cv2.imdecode(stream, cv2.IMREAD_UNCHANGED)
                
                if cv_image is not None:
                    self.display_image(cv_image)
                else:
                    self.image_label.setText("Ошибка: не удалось декодировать файл")
            except Exception as e:
                self.image_label.setText(f"Ошибка: {e}")

    def display_image(self, cv_image):
        """Конвертация OpenCV изображения в QPixmap и вывод в QLabel с сохранением пропорций."""
        # Обработка цветных или черно-белых изображений
        if len(cv_image.shape) == 3:
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            h, w, channels = rgb_image.shape
            bytes_per_line = 3 * w
            qimage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        else:
            h, w = cv_image.shape
            bytes_per_line = w
            qimage = QImage(cv_image.data, w, h, bytes_per_line, QImage.Format.Format_Grayscale8)
            
        pixmap = QPixmap.fromImage(qimage)
        
        # Масштабируем изображение под размеры метки с сохранением пропорций
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.image_label.setPixmap(scaled_pixmap)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
