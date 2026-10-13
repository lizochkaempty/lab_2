"""
Лабораторная работа 2.1 — Вариант 2: Окно со слайдером
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, 
    QVBoxLayout, QWidget, QLabel, QSlider
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    """Главное окно приложения «Настройки»."""
    
    def __init__(self):
        super().__init__()
        # 1. Устанавливаем заголовок и размеры окна
        self.setWindowTitle("Настройки")
        self.setGeometry(100, 100, 400, 250)
        
        self.init_ui()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Вертикальный макет для элементов
        layout = QVBoxLayout()
        
        # Текстовая метка для громкости
        self.value_label = QLabel("Текущая громкость: 50%")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Слайдер (от 0 до 100)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        
        # Подключаем сигнал изменения значения к слоту
        self.slider.valueChanged.connect(self.on_slider_change)
        
        # Добавляем виджеты в макет
        layout.addWidget(self.value_label)
        layout.addWidget(self.slider)
        
        # Устанавливаем макет на центральный виджет
        central_widget.setLayout(layout)
    
    def on_slider_change(self, value):
        """Слот: обновление текста при перемещении слайдера."""
        self.value_label.setText(f"Текущая громкость: {value}%")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()