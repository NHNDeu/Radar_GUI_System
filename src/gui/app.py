import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from pathlib import Path

from .main_window import MainWindow

def run():
    if os.name == 'nt':
        import ctypes
        # Set the application ID for Windows taskbar grouping
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('RadarGUISystem')

    app = QApplication(sys.argv)
    icon_path = Path(__file__).resolve().parent.parent.parent / "resources" / "Pic.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()
    try:
        window.ui_service.center_window()
    except Exception as e:
        pass
    
    sys.exit(app.exec())