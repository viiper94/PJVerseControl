import json
import os
import serial
import serial.tools.list_ports

MESSAGES_FILE = "messages.json"
PORTS_FILE = "ports_config.json"
NUM_PROJECTORS = 12
BAUDRATE = 115200


class ProjectorController:
    def __init__(self):
        self.messages = self.load_messages()
        self.projector_ports = {i: "" for i in range(1, NUM_PROJECTORS + 1)}
        self.load_ports_config()

    # ---------------- MESSAGES -----------------
    def load_messages(self):
        if not os.path.exists(MESSAGES_FILE):
            return {}
        try:
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading messages:", e)
            return {}

    # ---------------- PORT CONFIG -----------------
    def load_ports_config(self):
        if os.path.exists(PORTS_FILE):
            try:
                with open(PORTS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.projector_ports = {int(k): v for k, v in data.items()}
            except Exception as e:
                print("Error loading port config:", e)

    def save_ports_config(self):
        try:
            with open(PORTS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.projector_ports, f, indent=2)
        except Exception as e:
            print("Error saving ports config:", e)

    def available_ports(self):
        return [p.device for p in serial.tools.list_ports.comports()]

    def set_port(self, index, port):
        if port != "¯\_(ツ)_/¯":
            self.projector_ports[index] = port
        else:
            self.projector_ports[index] = ""
        self.save_ports_config()

    # ---------------- SERIAL SENDING -----------------
    def send_command(self, index, cmd_key):
        port = self.projector_ports.get(index)
        if not port or port == "Select COM Port":
            return f"Projector {index}: no port selected"

        cmd = self.messages.get(cmd_key)
        if not cmd:
            return f"Command '{cmd_key}' not found"

        try:
            with serial.Serial(port, BAUDRATE, timeout=1) as ser:
                if isinstance(cmd, str):
                    ser.write(cmd.encode("utf-8"))
                elif isinstance(cmd, list):
                    ser.write(bytes(cmd))
            return f"Sent {cmd_key} to projector {index} ({port})"
        except Exception as e:
            return f"Error sending to projector {index} ({port}): {e}"
