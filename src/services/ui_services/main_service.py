from PyQt6.QtWidgets import QApplication

class UIService:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui_manager = main_window.ui_manager

    def center_window(self):
        '''Center the main window on the screen'''
        screen = QApplication.primaryScreen()
        if not screen:
            return
        screen_geo = screen.availableGeometry()
        fg = self.main_window.frameGeometry()
        fg.moveCenter(screen_geo.center())
        self.main_window.move(fg.topLeft())

    def switch_view(self, view_id):
        if view_id in self.ui_manager.views:
            index = self.ui_manager.content_stack.indexOf(self.ui_manager.views[view_id])
            self.ui_manager.content_stack.setCurrentIndex(index)
            self.ui_manager.nav_bar.set_active_page(view_id)

    def set_active_page(self, page_id):
        if page_id in self.ui_manager.nav_bar.buttons:
            self.ui_manager.nav_bar.buttons[page_id].setChecked(True)