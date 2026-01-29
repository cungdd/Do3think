from PySide6.QtWidgets import QWidget, QApplication, QCheckBox
from PySide6.QtCore import QPoint, Qt, QPropertyAnimation, QRectF, Property, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QMouseEvent
import sys

class ToggleButton(QCheckBox):
    GOLDEN_RATIO = 1.618
    def __init__(
            self, 
            parent = None,
            width = None,
            height = None,
            bg_color = QColor(180, 180, 180),
            circle_color = QColor(255, 255, 255),
            active_color = QColor(0, 200, 0),
            animation_curve = QEasingCurve.Type.OutQuint
        ):
        super().__init__(parent)

        """
        h = self.height()/2 - 2
        w = self.width() - self.height() + 4
        w = 1.618*h
        w = self.height()*0.809 - 3.236

        self.width + 4 = self.height()*1.809 - 3.236
        self.width = self.height()*1.809 - 7.236

        """

        if width and height:
            self.setFixedSize(width, height)
        elif width:
            self.setFixedHeight((width)/1.809)
            self.setFixedWidth(width)
        elif height:
            self.setFixedHeight(height)
            self.setFixedWidth(height*1.809)
        else:
            self.setFixedWidth(int(self.sizeHint().height()*1.809))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._circle_position = 4  # Vị trí ban đầu của vòng tròn
        
        # MÀU SẮC
        self._background_color = bg_color  # Màu xám khi tắt
        self._circle_color = circle_color  # Màu trắng cho vòng tròn
        self._active_color = active_color  # Màu xanh khi bật
        
        # HÀNH ĐỔNG
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(300)
        
        # KẾT NỐI TÍN HIỆU THAY ĐỔI TRẠNG THÁI
        self.stateChanged.connect(self.start_animation)
        
    def get_circle_position(self):
        return self._circle_position
    
    def set_circle_position(self, value):
        self._circle_position = value
        self.update()
        
    circle_position = Property(float, get_circle_position, set_circle_position)
    
    def hitButton(self, pos: QPoint) -> bool:
        # self.contentsRect
        return self.contentsRect().contains(pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._background_color if not self.isChecked() else self._active_color)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height()/2, self.height()/2)

        # Draw circle
        painter.setBrush(self._circle_color)
        circle_size = self.height() - 8
        painter.drawEllipse(QRectF(self._circle_position, 4, circle_size, circle_size))
            
    def start_animation(self):
        # Tạo animation cho vị trí vòng tròn
        self.animation.stop()
        self.animation.setStartValue(4 if self.isChecked() else self.width() - self.height() + 4)
        self.animation.setEndValue(self.width() - self.height() + 4 if self.isChecked() else 4)
        self.animation.start()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    # window.setFixedSize(200, 100)
    
    toggle = ToggleButton(window, width=200)
    
    # toggle.move(70, 35)
    
    window.show()
    sys.exit(app.exec())