import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt, QTimer

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Настройки окна (полноэкранный режим)
        self.showFullScreen()
        
        # Размер игрового поля (квадрат 600x600)
        self.game_size = 600
        
        # Создаем сцену
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(QColor("#333333")))  # Серый фон

        # Игровое поле (белый квадрат по центру)
        self.game_field = QGraphicsRectItem(0, 0, self.game_size, self.game_size)
        self.game_field.setBrush(QBrush(Qt.white))
        self.game_field.setPen(QPen(Qt.black))
        self.scene.addItem(self.game_field)
        
        # Центрируем игровое поле
        screen = QApplication.primaryScreen().geometry()
        field_x = (screen.width() - self.game_size) // 2
        field_y = (screen.height() - self.game_size) // 2
        self.game_field.setPos(field_x, field_y)
        
        # Персонаж (красный квадрат 30x30)
        self.player = QGraphicsRectItem(0, 0, 30, 30)
        self.player.setBrush(QBrush(Qt.red))
        self.player.setPen(QPen(Qt.black))
        self.scene.addItem(self.player)
        
        # Начальная позиция персонажа (центр игрового поля)
        self.player.setPos(
            field_x + self.game_size // 2 - 15,
            field_y + self.game_size // 2 - 15
        )
        
        # Создаем View и привязываем сцену
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setCentralWidget(self.view)
        
        # Для плавного движения
        self.move_speed = 5
        self.keys_pressed = {
            Qt.Key_W: False,
            Qt.Key_A: False,
            Qt.Key_S: False,
            Qt.Key_D: False
        }
        
        # Таймер для обработки движения
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16)  # ~60 FPS
    
    def keyPressEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed[event.key()] = True
    
    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed[event.key()] = False
    
    def update_position(self):
        # Получаем текущие координаты персонажа
        x = self.player.x()
        y = self.player.y()
        
        # Границы игрового поля
        field_x = (self.width() - self.game_size) // 2
        field_y = (self.height() - self.game_size) // 2
        min_x = field_x
        max_x = field_x + self.game_size - self.player.rect().width()
        min_y = field_y
        max_y = field_y + self.game_size - self.player.rect().height()
        
        # Обработка движения
        if self.keys_pressed[Qt.Key_W] and y > min_y:
            y -= self.move_speed
        if self.keys_pressed[Qt.Key_S] and y < max_y:
            y += self.move_speed
        if self.keys_pressed[Qt.Key_A] and x > min_x:
            x -= self.move_speed
        if self.keys_pressed[Qt.Key_D] and x < max_x:
            x += self.move_speed
        
        # Обновляем позицию
        self.player.setPos(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())