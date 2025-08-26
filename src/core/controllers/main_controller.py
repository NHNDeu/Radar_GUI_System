from PyQt6.QtCore import QObject, pyqtSignal
from .port_controller import PortController

class MainController(QObject):
    '''
    Handle main application logic and communication between UI and backend.
    '''

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.port_controller = PortController()

    
    def _connect_controllers(self):
        pass