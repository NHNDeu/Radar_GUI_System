from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal

class NavigationBar(QFrame):
    page_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)