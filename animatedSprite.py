from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer

class AnimatedSprite(QGraphicsPixmapItem):
    def __init__(self, sprite_sheet_path, frame_width, frame_height, rows, cols):
        super().__init__()
        self.sprite_sheet = QPixmap(sprite_sheet_path)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.rows = rows  # Количество анимаций (idle, run, attack, hurt)
        self.cols = cols  # Количество кадров в каждой анимации

        # Состояния персонажа
        self.is_moving = False
        self.is_attacking = False
        self.is_hurt = False

        # Загрузка всех кадров
        self.frames = []
        self.load_frames()

        # Настройки анимации
        self.current_animation = 0  # 0 = idle, 1 = run, 2 = attack, 3 = hurt
        self.current_frame = 0
        self.animation_speed = 60
        self.loop_animation = True

        # Таймер
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(self.animation_speed)

    def load_frames(self):
        """Разбивает спрайтшит на кадры."""
        for row in range(self.rows):
            animation_frames = []
            for col in range(self.cols[row]):
                frame = self.sprite_sheet.copy(
                    col * self.frame_width,
                    row * self.frame_height,
                    self.frame_width,
                    self.frame_height
                )
                animation_frames.append(frame)
            self.frames.append(animation_frames)

    def set_animation(self, animation_index, loop=True, force_interrupt=False):
        """
        Переключает анимацию с приоритетом.
        Параметры:
            animation_index: 0=idle, 1=run, 2=attack, 3=hurt
            loop: зациклить ли анимацию?
            force_interrupt: можно ли прервать текущую анимацию (для урона)
        """
        # Если анимация не прерываемая и уже играется - игнорируем
        if (self.is_attacking or self.is_hurt) and not force_interrupt:
            return

        # Обновляем состояние
        self.is_moving = (animation_index == 1)
        self.is_attacking = (animation_index == 2 and not loop)
        self.is_hurt = (animation_index == 3 and not loop)

        # Переключаем анимацию
        if self.current_animation != animation_index or force_interrupt:
            self.current_animation = animation_index
            self.current_frame = 0
            self.loop_animation = loop
            self.timer.setInterval(self.animation_speed)

    def update_frame(self):
        """Обновляет кадр с учетом приоритетов."""
        # Проверяем, закончилась ли одноразовая анимация
        if not self.loop_animation and self.current_frame >= len(self.frames[self.current_animation]) - 1:
            if self.is_attacking:
                self.is_attacking = False
                self.set_animation(0)  # Возврат в idle после атаки
            elif self.is_hurt:
                self.is_hurt = False
                self.set_animation(0)  # Возврат в idle после урона
            return

        # Циклическое проигрывание
        self.current_frame = (self.current_frame + 1) % len(self.frames[self.current_animation])
        self.setPixmap(self.frames[self.current_animation][self.current_frame])