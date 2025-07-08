import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt, QTimer
from entity import Entity 
import random

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Настройки окна (полноэкранный режим)
        self.showFullScreen()
        self.setWindowTitle("NeoKnight")
        
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
        self.Hero = Entity(self.scene, 123, 123, 5, screen.width() // 2 - 15, screen.height() // 2 - 15)

        # Список врагов
        self.Enemies = self.generate_enemies(5)
            
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
        self.timer.timeout.connect(self.render_hero)
        self.timer.timeout.connect(self.render_enemies)
        self.timer.start(16)  # ~60 FPS
    
    def keyPressEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed[event.key()] = True
    
    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed[event.key()] = False

    def generate_enemies(self, number):
        enemies = []
        for i in range(number):
            e = Entity(self.scene, 20, 20, 1, width=10, height=10, color=Qt.red)

            field_x = (self.width() - self.game_size) // 2
            field_y = (self.height() - self.game_size) // 2
            min_x = field_x
            max_x = field_x + self.game_size - e.get_width()
            min_y = field_y
            max_y = field_y + self.game_size - e.get_height()

            x, y = random.uniform(min_x, max_x), random.uniform(min_y, max_y)
            while (x - self.Hero.get_x()) ** 2 + (y - self.Hero.get_y()) ** 2 < 50:
                x, y = random.uniform(min_x, max_x), random.uniform(min_y, max_y)

            e.move(x, y)
            enemies.append(e)
        return enemies
    
    def render_hero(self):
        # Получаем текущие координаты персонажа
        x = self.Hero.get_x()
        y = self.Hero.get_y()
        move_speed = self.Hero.get_speed()

        # Границы игрового поля
        field_x = (self.width() - self.game_size) // 2
        field_y = (self.height() - self.game_size) // 2
        min_x = field_x
        max_x = field_x + self.game_size - self.Hero.get_width()
        min_y = field_y
        max_y = field_y + self.game_size - self.Hero.get_height()
        
        # Обработка движения
        if self.keys_pressed[Qt.Key_W] and y > min_y:
            y -= move_speed
        if self.keys_pressed[Qt.Key_S] and y < max_y:
            y += move_speed
        if self.keys_pressed[Qt.Key_A] and x > min_x:
            x -= move_speed
        if self.keys_pressed[Qt.Key_D] and x < max_x:
            x += move_speed
        
        # Обновляем позицию
        self.Hero.move(x, y)

    def render_enemies(self):
        hero_x = self.Hero.get_x()
        hero_y = self.Hero.get_y()
        
        for enemy in self.Enemies:
            x = enemy.get_x()
            y = enemy.get_y()
            speed = enemy.get_speed()

            # Границы игрового поля
            field_x = (self.width() - self.game_size) // 2
            field_y = (self.height() - self.game_size) // 2
            min_x = field_x
            max_x = field_x + self.game_size - self.Hero.get_width()
            min_y = field_y
            max_y = field_y + self.game_size - self.Hero.get_height()

            if x > hero_x and x > min_x:
                x -= speed
            elif x < hero_x and x < max_x:
                x += speed
            if y > hero_y and y > min_y:
                y -= speed
            elif y < hero_y and y < max_y:
                y += speed
            
            enemy.move(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())