from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QPen, QFontDatabase, QFont

class CustomButton(QGraphicsItemGroup):
    def __init__(self, parent=None, text="Button", width=350, height=80, font_size=24):
        super().__init__(parent)
        self.text = text
        background = QGraphicsRectItem(0, 0, width, height)
        background.setBrush(QBrush("#47027B"))
        background.setPen(QPen("#673A8A"))
        self.addToGroup(background)

        font_id = QFontDatabase.addApplicationFont("source/font/MUNRO-sharedassets0.assets-232.otf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(font_family, font_size)
        txt_item = QGraphicsTextItem(text)
        txt_item.setDefaultTextColor(Qt.white)
        txt_item.setFont(custom_font)
        txt_item.setPos((width - txt_item.boundingRect().width()) // 2, (height - txt_item.boundingRect().height()) // 2)
        self.addToGroup(txt_item)

        self.setHandlesChildEvents(False)  # Отключаем передачу событий детям 
        self.setAcceptHoverEvents(True) 
    
    def mousePressEvent(self, event):
        if self.text == "Играть":
            self.scene().start_game()
        print(f"Группа {self.text} кликнута! Pos:", event.pos())
        super().mousePressEvent(event)