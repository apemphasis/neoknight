import sys
import os
import ctypes
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView
from PySide6.QtCore import Qt
from gameScene import GameScene
from PySide6.QtGui import QIcon

if sys.platform == 'win32':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('myapp.1.0')

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Настройки окна (полноэкранный режим)
        self.fixed_screen_width = 1200
        self.fixed_screen_height = 700
        #self.setFixedSize(1200, 700)
        self.setWindowTitle("NeoKnight")
        self.showFullScreen()
        self.setWindowIcon(QIcon("source/icon.png"))
        icon_path = os.path.join(os.path.dirname(__file__), "/source/icon.ico")
        app = QApplication.instance()
        app.setWindowIcon(QIcon(icon_path))
        
        # Создаем сцену
        self.scene = GameScene(width=self.width(),height=self.height())
            
        # Создаем View и привязываем сцену
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setCentralWidget(self.view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())