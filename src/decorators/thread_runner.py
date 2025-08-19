from PySide6.QtCore import QObject, QThread, Signal

class Worker(QObject):
    finished = Signal(object)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.__result = {}

    def run(self):
        self.__result = self.fn(*self.args, **self.kwargs)
        self.finished.emit(self.__result)

    def get_result(self):
        return self.__result


class ThreadRunner:
    """
    Encapsula QThread + Worker em uma interface simples
    """

    def __init__(self, fn, *args, callback=None, **kwargs):
        self.thread = QThread()
        self.worker = Worker(fn, *args, **kwargs)
        self.worker.moveToThread(self.thread)

        # Conexões
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        if callback:
            self.worker.finished.connect(callback)

    def start(self):
        self.thread.start()
