from PyQt6.QtWidgets import QWidget, QVBoxLayout
class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()