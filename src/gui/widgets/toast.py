from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QFont

class Toast(QWidget):
    def __init__(self, parent, message, duration=3000):
        super().__init__(parent)
        
        # 设置无边框窗口
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # 保存属性
        self.parent = parent
        self.duration = duration
        self.bg_color = QColor(40, 40, 40, 220)  # 半透明深灰色
        
        # 创建UI
        self._init_ui(message)
        
        # 设置动画
        self.animation_in = QPropertyAnimation(self, b"geometry")
        self.animation_out = QPropertyAnimation(self, b"geometry")
        
        # 显示和自动关闭定时器
        self.show_timer = QTimer(self)
        self.show_timer.setSingleShot(True)
        self.show_timer.timeout.connect(self._animate_out)
    
    def _init_ui(self, message):
        """初始化UI组件"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # 消息文本
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.label.setFont(QFont("Segoe UI", 10))
        self.label.setStyleSheet("color: white;")
        
        layout.addWidget(self.label)
        
        # 设置固定宽度，但自适应高度
        self.setFixedWidth(300)
        self.adjustSize()
    
    def show(self):
        """显示Toast并设置自动关闭"""
        # 计算位置
        parent_rect = self.parent.rect()
        width = self.width()
        height = self.height()
        
        # 默认位置：右下角
        start_x = parent_rect.width()
        target_x = parent_rect.width() - width - 20
        y = parent_rect.height() - height - 20
        
        # 调整位置以避免与其他toast重叠
        for widget in self.parent.findChildren(Toast):
            if widget != self and widget.isVisible():
                y = min(y, widget.y() - height - 10)
        
        # 设置初始几何属性
        self.setGeometry(start_x, y, width, height)
        super().show()
        
        # 进入动画
        self.animation_in.setDuration(300)
        self.animation_in.setStartValue(QRect(start_x, y, width, height))
        self.animation_in.setEndValue(QRect(target_x, y, width, height))
        self.animation_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation_in.start()
        
        # 设置自动关闭定时器
        self.show_timer.start(self.duration)
    
    def _animate_out(self):
        """退出动画"""
        rect = self.geometry()
        end_x = self.parent.width() + 50
        
        self.animation_out.setDuration(300)
        self.animation_out.setStartValue(rect)
        self.animation_out.setEndValue(
            QRect(end_x, rect.y(), rect.width(), rect.height()))
        self.animation_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self.animation_out.finished.connect(self.deleteLater)
        self.animation_out.start()
    
    def paintEvent(self, event):
        """自定义绘制圆角背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 8, 8)
        
        painter.fillPath(path, self.bg_color)