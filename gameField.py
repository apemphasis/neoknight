from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtCore import Qt, QTimer


class GameField(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.setAcceptHoverEvents(True)  # Включаем обработку hover-событий
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pass
            #window.attac_hero()
        
        # Важно вызвать родительский метод, чтобы не блокировать события
        super().mousePressEvent(event)