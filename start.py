import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

import src.utils.shared as shared
from src.ui.start import Ui_MainWindow
from src.components_ui.dialogs import Dialogs
from src.controller.start import StartController
from src.decorators.thread_runner import ThreadRunner
from src.utils.functions import (
    create_dirs
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        shared.path_data = f'{os.getcwd()}\\dados'
        create_dirs(shared.path_data)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__runner = None
        self.__controller = StartController()
        self.__controller.progress.connect(self.progress)
        self.__controller.error.connect(self.error)
        Dialogs.setup(self)

        self.ui.button_buscar_dados_anac.clicked.connect(self.search_data_anac)

    def start(self):
        self.show()

    def search_data_anac(self):
        self.run_function(
            self.__controller.search_periods_anac,
            callback=self.download_data_anac
        )

    def download_data_anac(self, years):
        if self.__controller.is_error():
            return

        if not years:
            Dialogs.info('Não foi encontrado nenhum ano para pesquisa!')
            return

        self.run_function(
            self.__controller.download_data_anac,
            years
        )

    def progress(self, result):
        if result:
            self.ui.progressbar_status.setValue(int(result[0]))
            self.ui.textedit_infos.append(result[1])

    def error(self, result):
        if result:
            self.ui.textedit_infos.append(f'ERRO: {result}')

        Dialogs.error('Erro ao realizar processo!')

    def run_function(self, func,  *args, callback=None, **kwargs):
        self.__runner = ThreadRunner(
            func,
            *args,
            **kwargs,
            callback=callback
        )
        self.__runner.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.start()
    sys.exit(app.exec())
