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
        
        # ======= left side =======
        left_side = QWidget()
        left_side_layout = QVBoxLayout(left_side)

        # port selection panel
        port_panel = QWidget()
        port_panel.setFixedWidth(320)
        port_layout = QVBoxLayout(port_panel)

        self.radar_dpct_port_group = self._create_port_group("DPCT Port", 921600)
        self.radar_TI_port_group = self._create_port_group('TI Port', 921600) # baud rate need fix
        self.radar_Rhine_port_group = self._create_port_group('Rhine Port', 921600) # baud rate need fix
        self.ecg_port_group = self._create_port_group("ECG Port", 115200)

        self.radar_dpct_port_combo = self.radar_dpct_port_group.findChild(QComboBox)
        self.radar_TI_port_combo = self.radar_TI_port_group.findChild(QComboBox)
        self.radar_Rhine_port_combo = self.radar_Rhine_port_group.findChild(QComboBox)
        self.ecg_port_combo = self.ecg_port_group.findChild(QComboBox)

        self.btn_refresh = self._create_botton("Refresh Ports", 120, 47)

        port_layout.addWidget(self.radar_dpct_port_group)
        port_layout.addWidget(self.radar_TI_port_group)
        port_layout.addWidget(self.radar_Rhine_port_group)
        port_layout.addWidget(self.ecg_port_group)
        port_layout.addWidget(self.btn_refresh)

        # layout arrangement
        left_side_layout.addWidget(port_panel)
        left_side_layout.addStretch()
        main_layout.addWidget(left_side)

        # ======= right side =======
        right_side = QWidget()
        right_side_layout = QVBoxLayout(right_side)

        # collect control panel
        control_panel = QWidget()
        control_panel.setFixedSize(300,140)
        control_layout = QVBoxLayout(control_panel)

        self.control_btn_group = self._create_control_group()
        control_layout.addWidget(self.control_btn_group)
        
        # label panel
        label_panel = QWidget()
        label_panel.setFixedWidth(300)
        label_layout = QVBoxLayout(label_panel)

        self.label_group = self._create_label_group()
        label_layout.addWidget(self.label_group)

        # log panel

        # right arrangement
        right_side_layout.addWidget(control_panel)
        right_side_layout.addWidget(label_panel)
        right_side_layout.addStretch()
        main_layout.addWidget(right_side)

        self.setLayout(main_layout)

    # region port group
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
        port_id = port_name.split()[0]  # Get port type (Radars or ECG)
        combo = self.radar_port_combo if "Radar" in port_name else self.ecg_port_combo
        if combo and combo.currentText():
            self.port_connection_changed.emit(combo.currentText(), checked)
    # endregion

    # region control group
    def _create_control_group(self):
        group = QGroupBox("Control")
        group.setFixedSize(280,120)

        layout = QVBoxLayout(group)

        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()
        self.btn_start = self._create_botton("Start")
        self.btn_stop  = self._create_botton("Stop", enable=False)
        self.btn_pause = self._create_botton("Pause", enable=False)
        self.btn_save  = self._create_botton("Save", enable=False)

        row1_layout.addWidget(self.btn_start)
        row1_layout.addWidget(self.btn_pause)
        row1_layout.addWidget(self.btn_stop)

        row2_layout.addWidget(self.btn_save)
        row2_layout.addStretch()

        layout.addLayout(row1_layout)
        layout.addLayout(row2_layout)

        return group
    # endregion

    # region lable group
    def _create_label_group(self):
        group = QGroupBox("Label")
        layout = QVBoxLayout(group)
        
        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()
        row3_layout = QHBoxLayout()

        self.btn_None = self._create_botton("None")
        self.btn_Stand = self._create_botton("Stand")
        self.btn_FallDown = self._create_botton("Fall Down")
        row1_layout.addWidget(self.btn_None)
        row1_layout.addWidget(self.btn_Stand)
        row1_layout.addWidget(self.btn_FallDown)

        self.btn_LieFlat = self._create_botton("Lie Flat")
        self.btn_LieSide = self._create_botton("Lie Side")
        self.btn_LieBack = self._create_botton("Lie Back") 
        row2_layout.addWidget(self.btn_LieFlat)
        row2_layout.addWidget(self.btn_LieSide)
        row2_layout.addWidget(self.btn_LieBack)

        self.btn_Choke = self._create_botton("Choke")
        row3_layout.addWidget(self.btn_Choke)
        row3_layout.addStretch()

        layout.addLayout(row1_layout)
        layout.addLayout(row2_layout)
        layout.addLayout(row3_layout)
        
        return group

    # endregion

    # region utils
    def _create_botton(self, name, H=84, W=36, enable=True):
        self.btn = QPushButton(name)
        self.btn.setFixedSize(H, W)
        self.btn.setEnabled(enable)

        return self.btn
    # endregion
        
    # region public api
    def update_available_ports(self, ports):
        if not ports:
            return
        
        if self.radar_port_combo is None or self.ecg_port_combo is None:
            return

        current_radar = self.radar_port_combo.currentText()
        current_ecg = self.ecg_port_combo.currentText()

        self.radar_port_combo.clear()
        self.ecg_port_combo.clear()

        for port in ports:
            self.radar_port_combo.addItem(port)
            self.ecg_port_combo.addItem(port)

        radar_idx = self.radar_port_combo.findText(current_radar)
        if radar_idx >= 0:
            self.radar_port_combo.setCurrentIndex(radar_idx)

        ecg_idx = self.ecg_port_combo.findText(current_ecg)
        if ecg_idx >= 0:
            self.ecg_port_combo.setCurrentIndex(ecg_idx)
    # endregion