from PyQt5.QtCore import QObject, pyqtSlot


class IndexChangedSlot(QObject):

    def __init__(self, callback, parent=None):
        super(IndexChangedSlot, self).__init__()
        self.index = 0
        self.callback = callback

    @pyqtSlot(int)
    def notifyIndexChanged(self,index):
        self.index = index
        self.callback()
