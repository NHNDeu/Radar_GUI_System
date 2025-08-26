from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QPushButton, QButtonGroup
)
from PyQt6.QtCore import pyqtSignal, Qt

class NavigationBar(QFrame):
    # define signal
    page_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("NavigationBar")
        self.setMinimumWidth(200)
        self.setMaximumWidth(250)
        '''
        self.setStyleSheet("""
            #NavigationBar {
                background-color: #F5F5F7;
                border-right: 1px solid #E5E5E5;
            }
            
            QPushButton {
                text-align: left;
                padding: 10px 15px;
                border: none;
                color: #333333;
                font-size: 14px;
                border-radius: 6px;
                margin: 2px 8px;
            }
            
            QPushButton:hover {
                background-color: #E5E5E5;
            }
            
            QPushButton:checked {
                background-color: #DEEAFF;
                color: #0066FF;
            }
        """)
        '''
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.buttons = {}   # store buttons info
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 20, 0, 0)

        self.btn_collect_settings = self._add_nav_button("采集设置", "collect_settings", layout)
        self.btn_display_data = self._add_nav_button("数据显示", "display_data", layout)
        self.btn_settings = self._add_nav_button("设置", "settings", layout)

        layout.addStretch()
        self.button_group.buttonClicked.connect(self._on_button_clicked)
        if self.button_group.buttons():
            self.button_group.buttons()[0].setChecked(True)

    def _add_nav_button(self, text, page_id, layout):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setProperty("page_id", page_id)

        self.button_group.addButton(btn)
        layout.addWidget(btn)
        self.buttons[page_id] = btn

        return btn
    
    def _on_button_clicked(self, button):
        page_id = button.property("page_id")
        self.page_changed.emit(page_id)

    # public api
    def set_active_page(self, page_id):
        """Set current active page without emitting signal"""
        if page_id in self.buttons:
            self.buttons[page_id].setChecked(True)