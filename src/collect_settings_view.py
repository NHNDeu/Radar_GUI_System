from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QComboBox, QFormLayout, QLabel, QPushButton
)
from PyQt6.QtCore import pyqtSignal

class CollectSettingsView(QWidget):
    # define signal
    refresh_ports_requested = pyqtSignal()
    port_connection_changed = pyqtSignal(str, bool) # port name, is connected

    def __init__(self):
        super().__init__()
        self.radar_port_combo = None
        self.ecg_port_combo = None
        self.btn_refresh = None
        self._init_ui()
        self._connect_internal_signals()

    def _init_ui(self):
        main_layout = QHBoxLayout()

        port_panel = QWidget()
        port_panel.setFixedSize(320,270)
        port_layout = QVBoxLayout(port_panel)

        self.radar_port_group = self._create_port_group("Radar Port", 921600)
        self.ecg_port_group = self._create_port_group("ECG Port", 115200)

        self.radar_port_combo = self.radar_port_group.findChild(QComboBox, "radar_port_combo")
        self.ecg_port_combo = self.ecg_port_group.findChild(QComboBox, "ecg_port_combo")

        self.btn_refresh = QPushButton("Refresh Ports")
        self.btn_refresh.setFixedSize(100,40)

        port_layout.addWidget(self.radar_port_group)
        port_layout.addWidget(self.ecg_port_group)
        port_layout.addWidget(self.btn_refresh)

        main_layout.addWidget(port_panel)

        self.setLayout(main_layout)

    def _create_port_group(self, title, baud_rate):
        group = QGroupBox(title)
        group.setFixedSize(300,90)
        group.setCheckable(True)
        group.setChecked(True)

        layout = QFormLayout(group)
        
        port_combo = QComboBox()
        port_combo.setObjectName(f"{title.lower().replace(' ', '_')}_combo")

        layout.addRow(QLabel("Port:"), port_combo)
        layout.addRow(QLabel("Baud Rate:"), QLabel(str(baud_rate)))

        group.toggled.connect(lambda checked: self._on_port_group_toggled(title, checked))

        return group
    
    def _connect_internal_signals(self):
        self.btn_refresh.clicked.connect(self._on_refresh_clicked)

    def _on_refresh_clicked(self):
        self.refresh_ports_requested.emit()

    def _on_port_group_toggled(self, port_name, checked):
        """Handle port group toggle events."""
        port_id = port_name.split()[0]  # Get port type (Radar or ECG)
        combo = self.radar_port_combo if "Radar" in port_name else self.ecg_port_combo
        if combo and combo.currentText():
            self.port_connection_changed.emit(combo.currentText(), checked)

    # public api
    def update_available_ports(self, ports):
        if not ports:
            return
        
        if self.radar_port_combo is None or self.ecg_port_combo is None:
            return

        current_radar = self.radar_port_combo.currentText()
        current_ecg = self.ecg_port_combo.currentText()

        self.radar_port_combo.clear()
        self.ecg_port_combo.clear()

        self.radar_port_combo.addItems(ports)
        self.ecg_port_combo.addItems(ports)
        
        print(f"Added {len(ports)} ports to combo boxes")

        radar_idx = self.radar_port_combo.findText(current_radar)
        if radar_idx >= 0:
            self.radar_port_combo.setCurrentIndex(radar_idx)

        ecg_idx = self.ecg_port_combo.findText(current_ecg)
        if ecg_idx >= 0:
            self.ecg_port_combo.setCurrentIndex(ecg_idx)
