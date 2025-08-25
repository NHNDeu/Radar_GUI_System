from PyQt6.QtCore import QObject

class MainController(QObject):
    '''
    Handle main application logic and communication between UI and backend.
    '''
    def __init__(self):
        super().__init__()