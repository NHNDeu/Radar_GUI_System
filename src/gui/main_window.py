from PyQt6.QtWidgets import QMainWindow, QStatusBar

from src.gui.ui_manager.ui_manager import UIManager
from src.services.ui_services.main_service import UIService
from src.core.signal_connectors.main_connector import SignalConnector
from src.core.controllers.main_controller import MainController

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