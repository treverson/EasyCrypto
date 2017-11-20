from PyQt5.QtCore import QObject, pyqtSlot


class WebsiteSlot(QObject):

    @pyqtSlot(int)
    def fun(self,index):
        print(index)