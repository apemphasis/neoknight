import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView
from PySide6.QtCore import Qt
from gameScene import GameScene


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Настройки окна (полноэкранный режим)
        self.fixed_screen_width = 1200
        self.fixed_screen_height = 700
        self.setFixedSize(1200, 700)
        self.setWindowTitle("NeoKnight")
        
        # Создаем сцену
        self.scene = GameScene()
            
        # Создаем View и привязываем сцену
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setCentralWidget(self.view)
        
        
    def delete_en(self):
        for e in self.Enemies:
            self.scene.removeItem(e.get_regdoll())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())