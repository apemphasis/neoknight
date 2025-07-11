import sys
from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsItemGroup, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen, QPixmap, QFont,  QFontDatabase, QTransform
from PySide6.QtCore import Qt, QTimer
from gameField import GameField
import random
from button import CustomButton
from animatedSprite import AnimatedSprite
from enemy import Enemy
import math

class GameScene(QGraphicsScene):
    def __init__(self, parent=None, width=1200, height=700):
        super().__init__(parent)

        font_id = QFontDatabase.addApplicationFont("source/font/MUNRO-sharedassets0.assets-232.otf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(font_family, 14)

        self.stats = {
                    "record": "0",
                    "coins": "0",
                    "damage": "10",
                    "health": "10",
                }


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

        
        self.record_txt = QGraphicsTextItem(f"Рекорд прожитых волн: {self.stats["record"]}")
        self.record_txt.setDefaultTextColor(Qt.white)
        self.record_txt.setFont(custom_font)
        self.record_txt.setPos(20, 20)
        self.stat_group.addToGroup(self.record_txt)

        self.coin_txt = QGraphicsTextItem(f"Монеты: {self.stats["coins"]}")
        self.coin_txt.setDefaultTextColor(Qt.white)
        self.coin_txt.setFont(custom_font)
        self.coin_txt.setPos(stat_back.boundingRect().width() - 20 - self.coin_txt.boundingRect().width(), 20)
        self.stat_group.addToGroup(self.coin_txt)

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
        health_txt.setPos(stat_back.boundingRect().width() // 2 - 20 - health_txt.boundingRect().width(), 220)
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
        

        self.enemies = []

        self.arena_group.setPos((self.width() - self.arena_back.boundingRect().width()) // 2,
                                (self.height() - self.arena_back.boundingRect().height()) // 2)
        self.arena_group.setHandlesChildEvents(False)  # Отключаем передачу событий детям 
        self.arena_group.setAcceptHoverEvents(True) 
        
        # Для плавного движения
        self.move_speed = 3
        self.keys_pressed = {
            Qt.Key_W: False,
            Qt.Key_A: False,
            Qt.Key_S: False,
            Qt.Key_D: False
        } 

        self.current_health = 7
        self.current_wave = 1
        self.current_money = int(self.stats["coins"])
        # Таймер для обработки движения
        self.timer = QTimer(self)
        self.timer.start(16)  # ~60 FPS

    def start_game(self):
        self.removeItem(self.lobby_group)
        self.generate_hero()
        self.generate_health()
        self.wave_generate()
        self.addItem(self.arena_group)
        self.timer.timeout.connect(self.render_hero)
        self.timer.timeout.connect(self.render_enemies)
        self.timer.timeout.connect(self.wave_generate)

    def wave_generate(self):
        if self.current_health >= 0:
            if len(self.enemies) == 0:
                self.current_wave += 1
                print(self.current_wave)
                n = 4
                if self.current_wave <= 10:
                    n += self.current_wave
                else:
                    n += 10
                self.generate_enemies(n)

    def generate_hero(self):
        self.hero = AnimatedSprite("source/hero/hero.png", 96, 96, 4, [10, 16, 7, 4])
        self.hero.set_animation(0, force_interrupt=True)
        self.arena_group.addToGroup(self.hero)
        #self.hero_x = (self.arena_back.boundingRect().width() - 96) // 2
        #self.hero_y = (self.arena_back.boundingRect().height() - 96) // 2
        self.hero.setPos((self.arena_back.boundingRect().width() - 96) // 2,
                         (self.arena_back.boundingRect().height() - 96) // 2)
        print(self.hero.pos())
        self.current_health = int(self.stats["health"])

    def end_game(self):
        for e in self.enemies:
            e.clear_timer()
            self.removeItem(e)
            e = None
        self.enemies.clear()
        self.removeItem(self.hero)
        self.hero = None
        self.timer.timeout.disconnect(self.render_hero)
        self.timer.timeout.disconnect(self.render_enemies)
        self.removeItem(self.arena_group)
        self.addItem(self.lobby_group)
        self.timer.timeout.disconnect(self.wave_generate)

        self.update_stat()

    def keyPressEvent(self, event):
        if event.key() in self.keys_pressed:
            if self.hero != None and self.hero.current_animation == 0:
                self.hero.set_animation(1, force_interrupt=True)
            self.keys_pressed[event.key()] = True
        super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed[event.key()] = False
        if all(f is False for f in self.keys_pressed.values()):
            if self.hero != None:
                self.hero.set_animation(0, force_interrupt=True)
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
        
        reverse = QTransform()
            # Перемещаем в центр, отражаем, возвращаем обратно
        reverse.translate(self.hero.boundingRect().center().x(), self.hero.boundingRect().center().y())
        reverse.scale(-1, 1)
        reverse.translate(-self.hero.boundingRect().center().x(), -self.hero.boundingRect().center().y())
        # Обработка движения
        if self.keys_pressed[Qt.Key_W] and y > min_y:
            y -= move_speed
        if self.keys_pressed[Qt.Key_S] and y < max_y:
            y += move_speed
        if self.keys_pressed[Qt.Key_A] and x > min_x:
            self.hero.setTransform(reverse)
            x -= move_speed
        if self.keys_pressed[Qt.Key_D] and x < max_x:
            self.hero.setTransform(QTransform().scale(1, 1))
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
            
    def generate_enemies(self, n):
        min_x = 0
        max_x = self.arena_back.boundingRect().width() - 32
        min_y = 0
        max_y = self.arena_back.boundingRect().height() - 32
        for _ in range(n):
            enemy = Enemy("source/hero/Zombie.png", 32, 32, 4, [8, 8, 7, 2], 20)
            enemy.set_animation(0, force_interrupt=True)
            
            x, y = random.uniform(min_x, max_x), random.uniform(min_y, max_y)
            while (x - self.hero.pos().x()) ** 2 + (y - self.hero.pos().y()) ** 2 < 200:
                x, y = random.uniform(min_x, max_x), random.uniform(min_y, max_y)
            self.enemies.append(enemy)
            self.arena_group.addToGroup(enemy)
            enemy.setPos(x, y)

    def render_enemies(self):
        min_x = 0
        max_x = self.arena_back.boundingRect().width() - 32
        min_y = 0
        max_y = self.arena_back.boundingRect().height() - 32
        hero_x = self.hero.pos().x() + 48
        hero_y = self.hero.pos().y() + 48
        for enemy in self.enemies:
            if enemy.is_dead():
                continue
            x = enemy.pos().x()
            y = enemy.pos().y()
            vector = (x + 16 - hero_x, y + 16 - hero_y)
            sinus = abs(vector[1]) / (vector[0] ** 2 + vector[1] ** 2) ** 0.5
            cosinus = abs(vector[0]) / (vector[0] ** 2 + vector[1] ** 2) ** 0.5
            
            speed = 1
            coll, coll_vector = self.collision(enemy)
            if coll:
                enemy.setPos(x + coll_vector[0], y + coll_vector[1])
                continue

            reverse = QTransform()
            # Перемещаем в центр, отражаем, возвращаем обратно
            reverse.translate(enemy.boundingRect().center().x(), enemy.boundingRect().center().y())
            reverse.scale(-1, 1)
            reverse.translate(-enemy.boundingRect().center().x(), -enemy.boundingRect().center().y())

            if x > self.hero.pos().x() + 32 and x > min_x:
                if x > self.hero.pos().x() + 32 + 20:
                    enemy.setTransform(reverse)
                x -= speed * cosinus
            elif x < self.hero.pos().x() + 32 and x < max_x:
                enemy.setTransform(QTransform().scale(1, 1))
                x += speed * cosinus
            if y > self.hero.pos().y() + 32 and y > min_y:
                y -= speed * sinus
            elif y < self.hero.pos().y() + 32 and y < max_y:
                y += speed * sinus
            
            enemy.setPos(x, y)
    
    def attack_hero(self, position):
        self.hero.set_animation(2, loop=False)
        hero_x = self.hero.pos().x() + 48
        hero_y = self.hero.pos().y() + 48
        h_v = (position.x() - hero_x, position.y() - hero_y)
        for enemy in self.enemies:
            if enemy.is_dead():
                continue
            x = enemy.pos().x() + 16
            y = enemy.pos().y() + 16
            e_v = (x - hero_x, y - hero_y)
            cos_value = (h_v[0] * e_v[0] + h_v[1] * e_v[1]) / ((h_v[0] ** 2 + h_v[1] ** 2) * (e_v[0] ** 2 + e_v[1] ** 2)) ** 0.5
            arccos = math.acos(cos_value)
            if arccos < 0.5 and (e_v[0] ** 2 + e_v[1] ** 2) ** 0.5 < 70:
                enemy.get_damage(int(self.stats["damage"]))
                if enemy.is_dead():
                    enemy.die()
                    self.enemies.remove(enemy)
                    self.current_money += 1
                    print(self.current_money)
                else:
                    enemy.set_animation(3, loop=False)

    def attack_enemy(self, enemy):
        hero_x = self.hero.pos().x() + 48
        hero_y = self.hero.pos().y() + 48
        x = enemy.pos().x() + 16
        y = enemy.pos().y() + 16
        e_v = (x - hero_x, y - hero_y)
        if (e_v[0] ** 2 + e_v[1] ** 2) ** 0.5 < 40:
            enemy.set_animation(2, loop=False)
            self.hero.set_animation(3, loop=False)
            self.current_health -= 1
            if self.current_health <= 0:
                self.end_game()
            self.generate_health()

    def collision(self, enemy):
        for e in self.enemies:
            abs_vect = ((e.pos().x() - enemy.pos().x()) ** 2 + (e.pos().y() - enemy.pos().y()) ** 2) ** 0.5
            if abs_vect < 32 and e != enemy:
                return True, ((enemy.pos().x() - e.pos().x()) / abs_vect, (enemy.pos().y() - e.pos().y()) / abs_vect)
        return False, tuple()
    
    def update_stat(self):
        if self.current_wave > int(self.stats["record"]):
            self.stats["record"] = str(self.current_wave)
        self.stats["coins"] = self.current_money
        self.record_txt.setPlainText(f"Рекорд прожитых волн: {self.stats["record"]}")
        self.coin_txt.setPlainText(f"Монеты: {self.stats["coins"]}")
