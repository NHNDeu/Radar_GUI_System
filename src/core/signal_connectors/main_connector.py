from PyQt6.QtCore import QObject, pyqtSignal
from .port_connector import PortConnector
from .ui_connector import UIConnector

class SignalConnector(QObject):
    status_message = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.ui_connector = UIConnector(main_window)
        self.port_connector = PortConnector(main_window)

    def connect_signals(self):
        """Connect all signals and slots."""
        self.ui_connector.connect_signals()
        self.port_connector.connect_signals()