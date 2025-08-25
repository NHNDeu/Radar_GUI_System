from PyQt6.QtWidgets import QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget
from src.gui.widgets.nav_bar import NavigationBar
from src.gui.views.collect_settings_view import CollectSettingsView
from src.gui.views.display_data_view import DisplayDataView
from src.gui.views.settings_view import SettingsView

class UIManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.views = {}
        self._setup_ui()

    def _setup_ui(self):
        self.main_window.setWindowTitle("Radar GUI System")
        self.main_window.setGeometry(100, 100, 1200, 712)
        
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        self.nav_bar = NavigationBar()
        content_layout.addWidget(self.nav_bar)

        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack)

        self._init_views()
    
    def _init_views(self):
        self.views["collect_settings"] = CollectSettingsView()
        self.views["display_data"] = DisplayDataView()
        self.views["settings"] = SettingsView()
        
        for view in self.views.values():
            self.content_stack.addWidget(view)
            
    def switch_view(self, view_id):
        if view_id in self.views:
            index = self.content_stack.indexOf(self.views[view_id])
            self.content_stack.setCurrentIndex(index)
            self.nav_bar.set_active_page(view_id)