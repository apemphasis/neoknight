from animatedSprite import AnimatedSprite
from PySide6.QtCore import Qt, QTimer

class Enemy(AnimatedSprite):
    def __init__(self, sprite_sheet_path, frame_width, frame_height, rows, cols, health = 10):
        super().__init__(sprite_sheet_path, frame_width, frame_height, rows, cols)
        self.health = health

        self.etimer = QTimer(self.scene())
        self.etimer.timeout.connect(self.attack)
        self.etimer.start(1000)  # ~60 FPS
    
    def get_damage(self, d):
        self.health -= d

    def is_dead(self):
        return True if self.health <= 0 else False
    
    def die(self):
        if self.is_dead():
            self.set_animation(1)
            QTimer.singleShot(480, lambda: [self.scene().removeItem(self)])

    def attack(self):
        try:
            self.scene().attack_enemy(self)
        except Exception as exc:
            pass 
        
    def clear_timer(self):
        self.etimer.stop()  # Останавливаем
        self.etimer.deleteLater()  # Помечаем на удаление
        self.etimer = None