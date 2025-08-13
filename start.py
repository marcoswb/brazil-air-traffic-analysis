import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from src.ui.start import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.button_buscar_dados_anac.clicked.connect(self.download_data_anac)

    def start(self):
        self.show()

    def download_data_anac(self):
        print('buscar dados anac')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.start()
    sys.exit(app.exec())
