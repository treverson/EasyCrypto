from PyQt5.QtCore import QAbstractListModel, Qt


class WebsiteModel(QAbstractListModel):
    """ Model used by Qt to display list of websites

    """
    NameRole = Qt.UserRole + 1

    __roles = {NameRole: b"name"}

    def __init__(self, names):
        super(WebsiteModel, self).__init__()
        self.__names = names

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__names)

    def data(self, QModelIndex, role=None):
        row = QModelIndex.row()
        if role == self.NameRole:
            return self.__names[row]

    def roleNames(self):
        return self.__roles


class ActionModel(QAbstractListModel):
    """ Model used by Qt to display list of actions

    """
    AddressRole = Qt.UserRole + 1

    __roles = {AddressRole: b"address"}

    def __init__(self, addresses):
        super(ActionModel, self).__init__()
        self.__addresses = addresses

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__addresses)

    def data(self, QModelIndex, role=None):
        row = QModelIndex.row()
        if role == self.AddressRole:
            return self.__addresses[row]

    def roleNames(self):
        return self.__roles