from PyQt6.QtCore import QObject

class UIConnector(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ui_manager = main_window.ui_manager
        self.ui_service = main_window.ui_service
        
    def connect_signals(self):
        """Connect UI signals and slots."""
        self.ui_manager.nav_bar.page_changed.connect(self.ui_service.switch_view)