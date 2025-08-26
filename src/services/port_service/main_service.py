import serial
import serial.tools.list_ports

class PortService:
    """Handles port-related operations."""

    @staticmethod
    def get_available_ports():
        """Returns a list of available serial ports."""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports
    
    @staticmethod
    def test_ports_connection(port_name, baud_rate):
        """Tests the connection to a specific serial port."""
        try:
            ser = serial.Serial(port_name, baud_rate, timeout=1)
            if ser.is_open:
                ser.close()
                return True, None
            return False, "Port could not be opened"
        except Exception as e:
            return False, str(e)
        
    @staticmethod
    def open_port(port_name, baud_rate, timeout=1):
        """Opens a connection to a specific serial port."""
        try:
            ser = serial.Serial(port_name, baud_rate, timeout=timeout)
            return ser, None
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def close_port(port_name):
        """Close a serial port."""
        try:
            ser = serial.Serial(port_name)
            if ser.is_open:
                ser.close()
                return True, None
            return False, "Port is not open"
        except Exception as e:
            return False, str(e)
