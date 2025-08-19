from PySide6.QtCore import QObject, Signal

class BaseController(QObject):

    progress = Signal(object)
    error = Signal(object)

    def __init__(self):
        super().__init__()
        self.__result_error = False

    def update_progress(self, message, progress=0):
        self.progress.emit((progress, message))

    def raise_error(self, message=''):
        self.__result_error = str(message)
        self.error.emit(str(message))

    def is_error(self):
        return self.__result_error
