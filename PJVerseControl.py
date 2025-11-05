import sys
from PySide6.QtWidgets import QApplication
from ui import ProjectorControlApp


def main():
    app = QApplication(sys.argv)
    win = ProjectorControlApp()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
