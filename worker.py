import threading
import serial
import time


class ProjectorWorker(threading.Thread):
    def __init__(self, index, port, baudrate, command, message, log_callback=None):
        super().__init__(daemon=True)
        self.index = index
        self.port = port
        self.baudrate = baudrate
        self.command = command
        self.message = message
        self.log_callback = log_callback  # function to call for logging

    def run(self):
        """Thread entry point."""
        if not self.port:
            self._log(f"Projector {self.index}: No COM port specified")
            return

        try:
            # Try to open the port and send
            with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                self._log(f"[P{self.index}] Sending '{self.command}' to {self.port}")
                ser.write(self.message.encode())

                # Give the device a moment to respond
                time.sleep(0.6)
                reply = ser.readline().decode(errors="ignore").strip()

                if reply:
                    self._log(f"[P{self.index}] Reply from {self.port}: {reply}")
                else:
                    self._log(f"[P{self.index}] No reply from {self.port}")

        except serial.SerialException as e:
            self._log(f"[P{self.index}] Serial error on {self.port}: {e}")
        except Exception as e:
            self._log(f"[P{self.index}] Unexpected error on {self.port}: {e}")

    def _log(self, text):
        """Thread-safe logging via callback."""
        if callable(self.log_callback):
            self.log_callback(text)
        else:
            print(text)
