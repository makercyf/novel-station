import sys

from PySide6.QtWidgets import QApplication

from core.gui import DownloaderGUI


if __name__ == '__main__':
    app = QApplication([])
    gui = DownloaderGUI()
    gui.show()
    sys.exit(app.exec())
