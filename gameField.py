from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QBrush, QPen

class GameField(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.setBrush(QBrush("#271F2D"))
        self.setPen(QPen("#8246B0"))
        self.setAcceptHoverEvents(True)  # Включаем обработку hover-событий
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.scene().attack_hero()
        # Важно вызвать родительский метод, чтобы не блокировать события
        super().mousePressEvent(event)