from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTextEdit,
    QScrollArea, QFrame, QSizePolicy, QLabel, QSpacerItem, QMainWindow
)
from PySide6.QtCore import Qt
from controller import ProjectorController, NUM_PROJECTORS


class ProjectorControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PJ Verse Control")
        # self.resize(850, 540)
        self.resize(755, 527)

        self.controller = ProjectorController(log_callback=self.log_message)

        self.init_ui()

    def init_ui(self):
        # --- main layout ---
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # --- scroll area for projector rows ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        scroll_area.setWidget(scroll_content)

        # --- all-projectors row ---
        group_row = QHBoxLayout()
        group_row.setAlignment(Qt.AlignLeft)
        group_row.addSpacing(26)

        for label, cmd in [
            ("All ON", "turn_on"),
            ("All OFF", "turn_off"),
            ("All Freeze", "freeze"),
            ("All Unfreeze", "unfreeze"),
            ("All Blank", "blank"),
            ("All Unblank", "unblank"),
            ("All HDMI1", "hdmi1"),
            ("All HDMI2", "hdmi2")
        ]:
            btn = QPushButton(label)
            btn.setProperty("cmd", cmd)
            btn.clicked.connect(self.handle_all_button)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            if cmd == "turn_on":
                btn.setStyleSheet("font-weight: bold;")
            elif cmd == "turn_off":
                btn.setStyleSheet("font-weight: bold;")

            if cmd in ('turn_off', 'unfreeze', 'unblank'):
                group_row.addWidget(btn)
                group_row.addItem(QSpacerItem(15, 0, QSizePolicy.Fixed, QSizePolicy.Fixed))
            else:
                group_row.addWidget(btn)

        scroll_layout.addLayout(group_row)

        # --- separator line ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        scroll_layout.addWidget(line)

        # --- per-projector rows ---
        for i in range(1, NUM_PROJECTORS + 1):
            row = QHBoxLayout()
            row.setAlignment(Qt.AlignLeft)
            if i == 4 or i == 7:
                row.setContentsMargins(0, 0, 0, 15)  # left, top, right, bottom
            name = QLabel()
            name.setText(f"{i}")
            name.setStyleSheet("font-weight: bold; min-width: 20px;")
            row.addWidget(name)

            for label, cmd in [
                ("Get Status", "ask_pwr"),
                ("On", "turn_on"),
                ("Off", "turn_off"),
                ("Freeze", "freeze"),
                ("Unfreeze", "unfreeze"),
                ("Blank", "blank"),
                ("Unblank", "unblank"),
                ("HDMI1", "hdmi1"),
                ("HDMI2", "hdmi2")
            ]:
                btn = QPushButton(label)
                btn.setProperty("cmd", cmd)
                btn.setProperty("index", i)
                btn.clicked.connect(self.handle_button)
                btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                if cmd in ('turn_off', 'unfreeze', 'unblank'):
                    row.addWidget(btn)
                    row.addItem(QSpacerItem(15, 0, QSizePolicy.Fixed, QSizePolicy.Fixed))
                else:
                    row.addWidget(btn)

            if i == 12:
                # --- separator line ---
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                scroll_layout.addWidget(line)

            # port_box = QComboBox()
            # ports = self.controller.available_ports()
            # port_box.addItem("¯\_(ツ)_/¯")
            # port_box.addItems(ports)
            # saved = self.controller.projector_ports.get(i)
            # if saved and saved in ports:
            #     port_box.setCurrentText(saved)
            # port_box.currentTextChanged.connect(lambda val, idx=i: self.controller.set_port(idx, val))
            # port_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            # row.addWidget(port_box)

            scroll_layout.addLayout(row)

        # --- add scroll area to main layout ---
        main_layout.addWidget(scroll_area)

        # --- log box ---
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(60)
        main_layout.addWidget(self.log)

        self.setLayout(main_layout)

    # ---------------- EVENTS -----------------
    def handle_button(self):
        btn = self.sender()
        cmd = btn.property("cmd")
        index = btn.property("index")
        self.controller.send_command(index, cmd)

    def handle_all_button(self):
        cmd = self.sender().property("cmd")
        self.controller.send_to_all(cmd)

    # ---------------- LOG -----------------
    def log_message(self, text):
        self.log.append(text)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
