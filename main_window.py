import csv
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QWidget, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from lab5 import ImagePathIterator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотр датасета изображений — Лабораторная работа №5")
        self.resize(1100, 800)

        self.iterator: ImagePathIterator | None = None
        self.image_paths: list[str] = []
        self.current_index: int = -1

        # Центральный виджет и основной layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Кнопка загрузки аннотации
        self.btn_load = QPushButton("Выбрать файл annotation.csv")
        self.btn_load.clicked.connect(self.load_annotation)
        main_layout.addWidget(self.btn_load)

        # Метка для отображения изображения
        self.image_label = QLabel("Датасет не загружен — выберите annotation.csv")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid #888888; background-color: #f0f0f0;")
        self.image_label.setMinimumSize(800, 600)
        main_layout.addWidget(self.image_label, stretch=1)

        # Панель навигации
        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton("← Предыдущее")
        self.btn_next = QPushButton("Следующее →")

        self.btn_prev.clicked.connect(self.show_previous)
        self.btn_next.clicked.connect(self.show_next)

        self.btn_prev.setEnabled(False)
        self.btn_next.setEnabled(False)

        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_next)
        nav_layout.addStretch()

        main_layout.addLayout(nav_layout)

        # Информационная строка
        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 14px; padding: 8px;")
        main_layout.addWidget(self.info_label)

    def load_annotation(self):
        """Загрузка annotation.csv через диалог"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл annotation.csv",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        if not file_path:
            return

        try:
            self.image_paths = []
            with open(file_path, encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if row and row[0].strip():
                        self.image_paths.append(row[0].strip())

            if not self.image_paths:
                QMessageBox.warning(self, "Предупреждение", "В файле аннотации не найдено изображений!")
                return

            # Создаём итератор
            self.iterator = ImagePathIterator(file_path)

            self.current_index = 0
            self.show_current_image()

            # Активируем кнопки
            self.btn_prev.setEnabled(True)
            self.btn_next.setEnabled(True)
            self.update_info()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл аннотации:\n{str(e)}")

    def show_current_image(self):
        """Отображает изображение по текущему индексу"""
        if not (0 <= self.current_index < len(self.image_paths)):
            return

        abs_path = self.image_paths[self.current_index]

        pixmap = QPixmap(abs_path)
        if pixmap.isNull():
            self.image_label.setText(f"Ошибка загрузки изображения:\n{abs_path}")
            self.image_label.setPixmap(QPixmap())
        else:
            # Масштабируем с сохранением пропорций под размер метки
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

        self.update_info()

    def update_info(self):
        """Обновляет информационную строку"""
        if self.image_paths:
            basename = os.path.basename(self.image_paths[self.current_index])
            self.info_label.setText(
                f"Изображение {self.current_index + 1} из {len(self.image_paths)} — {basename}"
            )
            self.btn_prev.setEnabled(self.current_index > 0)
            self.btn_next.setEnabled(self.current_index < len(self.image_paths) - 1)
        else:
            self.info_label.setText("Датасет не загружен")

    def show_next(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.show_current_image()

    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_image()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.image_paths and self.current_index >= 0:
            self.show_current_image()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())