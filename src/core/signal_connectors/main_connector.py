from PyQt6.QtCore import QObject

class SignalConnector(QObject):
    def __init__(self, main_window, ui, controller):
        super().__init__()