from PyQt6.QtCore import QObject, pyqtSignal
from ...services.port_service.main_service import PortService

class PortController(QObject):
    '''
    Handle communication between the UI and the PortService.
    '''
    # define signals
    ports_refreshed = pyqtSignal(list)      # list of available ports
    port_connected = pyqtSignal(str, int)   # port name, baud rate
    port_disconnected = pyqtSignal(str)     # port name
    error_occurred = pyqtSignal(str, str)   # title, message

    def __init__(self):
        super().__init__()
        self.port_service = PortService()
        self.connected_ports = {}

    def refresh_ports(self):
        """Refresh the list of available ports."""
        try:
            ports = self.port_service.get_available_ports()
            self.ports_refreshed.emit(ports)
            return True, None
        except Exception as e:
            self.error_occurred.emit("Error Refreshing Ports", str(e))
            return False, str(e)
        
    def connect_port(self, port_name, baud_rate):
        """Connect to a serial port."""
        if port_name in self.connected_ports:
            return True, "Port is already connected."
        
        try:
            success, message = self.port_service.test_ports_connection(port_name, baud_rate)
            if success:
                self.connected_ports[port_name] = baud_rate
                self.port_connected.emit(port_name, baud_rate)
                return True, None
            else:
                self.error_occurred.emit("Error Connecting to Port", message)
                return False, message
        except Exception as e:
            self.error_occurred.emit("Error Connecting to Port", str(e))
            return False, str(e)
        
    def disconnect_port(self, port_name):
        """Disconnect from a serial port."""
        if port_name not in self.connected_ports:
            return True, "Port is not connected."

        try:
            success, message = self.port_service.test_ports_connection(port_name)
            if success:
                del self.connected_ports[port_name]
                self.port_disconnected.emit(port_name)
                return True, None
            else:
                self.error_occurred.emit("Error Disconnecting from Port", message)
                return False, message
        except Exception as e:
            self.error_occurred.emit("Error Disconnecting from Port", str(e))
            return False, str(e)
        
    def get_connected_ports(self):
        """Get a list of currently connected ports."""
        return self.connected_ports