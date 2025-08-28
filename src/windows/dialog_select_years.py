from PySide6.QtWidgets import (
    QMessageBox,
    QDialog
)

from src.ui.dialog_select_years import Ui_Form


class DialogSelectYears(QDialog):
    def __init__(self, years, parent=None):
        super().__init__(parent=parent)
        self.__years = years
        self.__selected_years = []

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.button_select_all.clicked.connect(self.select_all)
        self.ui.button_deselect_all.clicked.connect(self.deselect_all)
        self.ui.button_save.clicked.connect(self.save)

        self.add_options_interface()
        self.show()

    def add_options_interface(self):
        for year in reversed(self.__years):
            self.ui.list_years.addItem(str(year))

    def save(self):
        self.__selected_years = [item.text() for item in self.ui.list_years.selectedItems()]
        self.accept()

    def select_all(self):
        self.ui.list_years.selectAll()

    def deselect_all(self):
        self.ui.list_years.clearSelection()

    def get_selected_years(self):
        return self.__selected_years

    def closeEvent(self, event):
        response = QMessageBox.question(self.parent(), 'Confirmação', 'Deseja realmente encerrar sem salvar?')
        if response == 16384:
            event.accept()
        else:
            event.ignore()
