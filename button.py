from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsTextItem, QApplication
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QBrush, QPen, QFontDatabase, QFont
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import json

class CustomButton(QGraphicsItemGroup):
    def __init__(self, parent=None, text="Button", width=350, height=80, font_size=24):
        
        self.player = QMediaPlayer()
        self.player.setSource(QUrl.fromLocalFile("source/music/02-The-Prodigy-Breathe.wav"))
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
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile('source/music/off-button-on-table-lamp.wav'))
        self.player.play()
        if self.text == "Играть":
            self.scene().start_game()
        if self.text == "Выйти":
            with open('source\save\stat.json', 'w', encoding='utf-8') as file:
                json.dump(self.scene().stats, file, ensure_ascii=False, indent=4)
            QApplication.quit()
        if self.text == "Улучшить за 10 монет":
            self.scene().upgrade_hero()
        if self.text == "Вернуться в лобби":
            self.scene().goto_lobby()
        if self.text == "Новая Игра":
            self.scene().new_game()
        super().mousePressEvent(event)