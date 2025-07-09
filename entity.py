from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt, QTimer
import sys

class Entity:
    
    def __init__(self, scene, health, damage, speed, x = 0, y = 0, width = 30, height = 30, color = Qt.blue):
        self.regdoll = QGraphicsRectItem(0, 0, width, height)
        self.regdoll.setBrush(QBrush(color))
        self.regdoll.setPos(x, y)
        scene.addItem(self.regdoll)
        self.health = health
        self.damage = damage
        self.speed = speed

    def move(self, x, y):
        self.regdoll.setPos(x, y)

    def get_x(self):
        return self.regdoll.x()

    def get_y(self):
        return self.regdoll.y()
    
    def get_width(self):
        return self.regdoll.rect().width()

    def get_height(self):
        return self.regdoll.rect().height()
    
    def get_speed(self):
        return self.speed
    
    def get_regdoll(self):
        return self.regdoll