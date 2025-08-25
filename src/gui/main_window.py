from PyQt6.QtWidgets import QMainWindow, QStatusBar

from .ui_manager.ui_manager import UIManager
from ..core.controllers.main_controller import MainController
from ..services.ui_services.main_service import UIService
from ..core.signal_connectors.main_connector import SignalConnector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.ui_manager = UIManager(self)

        self.main_controller = MainController(self)

        self.ui_service = UIService(self)
        
        self.signal_connector = SignalConnector(self)
        self.signal_connector.connect_signals()