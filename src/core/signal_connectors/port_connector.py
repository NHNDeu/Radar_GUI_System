from PyQt6.QtCore import QObject
from ...gui.widgets.toast import Toast

class PortConnector(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ui_manager = main_window.ui_manager
        self.port_controller = main_window.main_controller.port_controller
        self.ui_service = main_window.ui_service

    def connect_signals(self):
        collect_view = self.ui_manager.views["collect_settings"]
        
        collect_view.refresh_ports_requested.connect(self._on_refresh_ports)
        collect_view.port_connection_changed.connect(self._on_port_connection_changed)
        self.port_controller.ports_refreshed.connect(collect_view.update_available_ports)
        self.port_controller.error_occurred.connect(self._on_error)

        self._on_refresh_ports()

    def _on_refresh_ports(self):
        """Handle port refresh requests."""
        success, message = self.port_controller.refresh_ports()
        self.ui_service.show_port_refresh_result(success, message)

    def _on_port_connection_changed(self, port_name, is_connected):
        """Handle port connection state changes."""
        if is_connected:
            baud_rate = 921600 if "Radar" in port_name else 115200
            success, message = self.port_controller.connect_port(port_name, baud_rate)
            if success:
                self.ui_service.show_toast(f"Connected to {port_name}")
            else:
                self.ui_service.show_toast(f"Failed to connect to {port_name}: {message}")
        else:
            success, message = self.port_controller.disconnect_port(port_name)
            if success:
                self.ui_service.show_toast(f"Disconnected from {port_name}")
            else:
                self.ui_service.show_toast(f"Failed to disconnect: {message}")

    def _on_error(self, title, message):
        """Handle errors."""
        self.ui_service.show_toast(f"{title}: {message}", 5000)