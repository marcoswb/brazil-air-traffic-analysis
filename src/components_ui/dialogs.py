from PySide6.QtWidgets import QMessageBox

class Dialogs:

    parent = None

    @classmethod
    def info(cls, message):
        QMessageBox.information(cls.parent, 'Info', message)

    @classmethod
    def error(cls, message):
        QMessageBox.information(cls.parent, 'Erro', message)
