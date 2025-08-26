import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def test_ui():
    app = QApplication(sys.argv)

    from PyQt6.QtGui import QIcon
    icon_path = Path(__file__).resolve().parent.parent / "resources" / "Pic.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    if os.name == 'nt':
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('RadarGUISystem.Test')
    
    window = MainWindow()
    window.show()
    
    try:
        window.ui_service.center_window()
    except Exception as e:
        print(f"无法居中窗口: {e}")
    
    print("UI测试已启动")
    print(f"可用视图: {list(window.ui_manager.views.keys())}")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_ui())