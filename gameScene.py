import sys
from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsItemGroup, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen, QPixmap, QFont,  QFontDatabase, QTransform
from PySide6.QtCore import Qt, QTimer
from gameField import GameField
import random
from button import CustomButton
from animatedSprite import AnimatedSprite

class GameScene(QGraphicsScene):
    def __init__(self, parent=None, width=1200, height=700):
        super().__init__(parent)

        font_id = QFontDatabase.addApplicationFont("source/font/MUNRO-sharedassets0.assets-232.otf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(font_family, 14)

        background = QPixmap("source/bg.png")
        background = background.scaled(width, height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        back_item = QGraphicsPixmapItem(background)
        self.addItem(back_item)

        self.lobby_group = QGraphicsItemGroup()

        self.play_btn = CustomButton(text="Играть")
        self.play_btn.setPos(0, 0)
        self.lobby_group.addToGroup(self.play_btn)

        self.new_game_btn = CustomButton(text="Новая Игра")
        self.new_game_btn.setPos(0, 110)
        self.lobby_group.addToGroup(self.new_game_btn)

        self.exit_btn = CustomButton(text="Выйти")
        self.exit_btn.setPos(0, 220)
        self.lobby_group.addToGroup(self.exit_btn)


        self.stat_group = QGraphicsItemGroup()
    
        stat_back = QGraphicsRectItem(0, 0, 400, 300)
        stat_back.setBrush(QBrush("#2D034D"))
        stat_back.setPen(QPen("#673A8A"))
        self.stat_group.addToGroup(stat_back)

        self.stats = {
            "record": "3",
            "coins": "324",
            "attack_speed": "10",
            "damage": "10",
            "health": "10",
            "damage_cost": "20",
            "health_cost": "20"
        }

        record_txt = QGraphicsTextItem(f"Рекорд прожитых волн: {self.stats["record"]}")
        record_txt.setDefaultTextColor(Qt.white)
        record_txt.setFont(custom_font)
        record_txt.setPos(20, 20)
        self.stat_group.addToGroup(record_txt)

        coin_txt = QGraphicsTextItem(f"Монеты: {self.stats["coins"]}")
        coin_txt.setDefaultTextColor(Qt.white)
        coin_txt.setFont(custom_font)
        coin_txt.setPos(stat_back.boundingRect().width() - 20 - coin_txt.boundingRect().width(), 20)
        self.stat_group.addToGroup(coin_txt)

        anim_lobby = AnimatedSprite("source/hero/lobby2.png", 192, 192, 1, [10])
        anim_lobby.setPos((stat_back.boundingRect().width() - 192) // 2, stat_back.boundingRect().height() // 2 - 130)
        self.stat_group.addToGroup(anim_lobby)

        damage_txt = QGraphicsTextItem(f"Урон: {self.stats["damage"]}")
        damage_txt.setDefaultTextColor(Qt.white)
        damage_txt.setFont(custom_font)
        damage_txt.setPos(stat_back.boundingRect().width() // 2 + 20, 220)
        self.stat_group.addToGroup(damage_txt)

        health_txt = QGraphicsTextItem(f"Здоровье: {self.stats["health"]}")
        health_txt.setDefaultTextColor(Qt.white)
        health_txt.setFont(custom_font)
        health_txt.setPos(stat_back.boundingRect().width() // 2 - 20 - coin_txt.boundingRect().width(), 220)
        self.stat_group.addToGroup(health_txt)

        self.lobby_group.addToGroup(self.stat_group)
        self.stat_group.setPos(600, 0)

        self.lobby_group.setPos(100, 150)
        self.lobby_group.setHandlesChildEvents(False)  # Отключаем передачу событий детям 
        self.lobby_group.setAcceptHoverEvents(True) 
        self.addItem(self.lobby_group)
        
        
        self.arena_group = QGraphicsItemGroup()
        
        self.arena_back = GameField(0, 0, 600, 600)
        self.arena_group.addToGroup(self.arena_back)
        self.hero = AnimatedSprite("source/hero/hero.png", 96, 96, 4, [10, 16, 7, 4])
        self.hero_x = (self.arena_back.boundingRect().width() - 96) // 2
        self.hero_y = (self.arena_back.boundingRect().height() - 96) // 2
        self.hero.setPos((self.arena_back.boundingRect().width() - 96) // 2,
                         (self.arena_back.boundingRect().height() - 96) // 2)
        self.arena_group.addToGroup(self.hero)

        self.enemies = []

        self.arena_group.setPos((self.width() - self.arena_back.boundingRect().width()) // 2,
                                (self.height() - self.arena_back.boundingRect().height()) // 2)
        self.arena_group.setHandlesChildEvents(False)  # Отключаем передачу событий детям 
        self.arena_group.setAcceptHoverEvents(True) 
        
        # Для плавного движения
        self.move_speed = 5
        self.keys_pressed = {
            Qt.Key_W: False,
            Qt.Key_A: False,
            Qt.Key_S: False,
            Qt.Key_D: False
        }
    

        self.current_health = 7
        # Таймер для обработки движения
        self.timer = QTimer(self)
        #self.timer.timeout.connect(self.render_enemies)
        self.timer.start(16)  # ~60 FPS

    def start_game(self):
        self.removeItem(self.lobby_group)
        self.timer.timeout.connect(self.render_hero)
        self.generate_health()
        self.generate_enemies(3)
        self.timer.timeout.connect(self.render_enemies)
        
        self.addItem(self.arena_group)

    def keyPressEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed[event.key()] = True
        super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed[event.key()] = False
        super().keyReleaseEvent(event)

    def render_hero(self):
        # Получаем текущие координаты персонажа
        x = self.hero.pos().x() 
        y = self.hero.pos().y()
        move_speed = 5

        min_x = -25
        max_x = self.arena_back.boundingRect().width() - self.hero.boundingRect().width() + 25
        min_y = -35
        max_y = self.arena_back.boundingRect().height() - self.hero.boundingRect().height() + 10
        
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
        self.hero.setPos(x, y)

    def generate_health(self):
        healthbar = QGraphicsItemGroup()
        for i in range(int(self.stats["health"])):
            if i < self.current_health:
                url = "source/hero/heart.png"
            else: 
                url = "source/hero/heart_shape.png"
            heart = QGraphicsPixmapItem(QPixmap(url).scaled(25, 25, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
            healthbar.addToGroup(heart)
            heart.setPos(30 * i, 0)
        self.arena_group.addToGroup(healthbar)
        healthbar.setPos((600 - 30 * int(self.stats["health"]) + 5) // 2,
                         600 - 40)
        print(healthbar.boundingRect().width())
            
    def generate_enemies(self, n):
        min_x = 0
        max_x = self.arena_back.boundingRect().width() - 32
        min_y = 0
        max_y = self.arena_back.boundingRect().height() - 32
        for _ in range(n):
            #enemy = QGraphicsRectItem(0, 0, 30, 30)
            enemy = AnimatedSprite("source/hero/Zombie.png", 32, 32, 4, [8, 8, 7, 2] )
            enemy.set_animation(1, force_interrupt=True)
            
            #enemy.setBrush(QBrush("#DB0909"))
            x, y = random.uniform(min_x, max_x), random.uniform(min_y, max_y)
            while (x - self.hero.pos().x()) ** 2 + (y - self.hero.pos().y()) ** 2 < 50:
                x, y = random.uniform(min_x, max_x), random.uniform(min_y, max_y)
            self.enemies.append(enemy)
            self.arena_group.addToGroup(enemy)
            enemy.setPos(x, y)

    def render_enemies(self):
        min_x = 0
        max_x = self.arena_back.boundingRect().width() - 32
        min_y = 0
        max_y = self.arena_back.boundingRect().height() - 32

        for enemy in self.enemies:
            x = enemy.pos().x()
            y = enemy.pos().y()
            speed = 1

            # if self.collision(enemy) == True:
            #     continue
            reverse = QTransform()
            # Перемещаем в центр, отражаем, возвращаем обратно
            reverse.translate(enemy.boundingRect().center().x(), enemy.boundingRect().center().y())
            reverse.scale(-1, 1)
            reverse.translate(-enemy.boundingRect().center().x(), -enemy.boundingRect().center().y())



            if x > self.hero.pos().x() + 32 and x > min_x:
                enemy.setTransform(reverse)
                x -= speed
            elif x < self.hero.pos().x() + 32 and x < max_x:
                enemy.setTransform(QTransform().scale(1, 1))
                x += speed
            if y > self.hero.pos().y() + 32 and y > min_y:
                y -= speed
            elif y < self.hero.pos().y() + 32 and y < max_y:
                y += speed
            
            enemy.setPos(x, y)
    
    def attack_hero(self):
        print("attack")
        for enemy in self.enemies:
            enemy.set_animation(3, loop=False)

    # def collision(self, enemy):
    #     for e in self.enemies:
            
    #         if (e.pos().x() - enemy.pos().x()) ** 2 + (e.pos().y() - enemy.pos().y()) ** 2 < 32 and e != enemy:
    #             return True

    #     return False