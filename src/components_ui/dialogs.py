from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Signal, Slot, QEventLoop

class Dialogs(QObject):

    _instance = None
    request_message = Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent
        self.request_message.connect(self._show_dialog)
        Dialogs._instance = self
        self._event_loop = None
        self._response = None

    @classmethod
    def setup(cls, parent):
        if cls._instance is None:
            cls._instance = Dialogs(parent)
        return cls._instance

    @classmethod
    def info(cls, message, title='Information'):
        if cls._instance is None:
            raise RuntimeError('MessageDialog não foi inicializado. Chame setup().')

        loop = QEventLoop()
        cls._instance._event_loop = loop
        cls._instance.request_message.emit('info', title, message)
        loop.exec()

    @classmethod
    def error(cls, message):
        QMessageBox.information(cls.parent, 'Erro', message)

    @Slot(str, str, str)
    def _show_dialog(self, tipo, title, text):
        if tipo == 'info':
            QMessageBox.information(self._parent, title, text)
            self._response = True
        self._event_loop.quit()