class HistoryTable(list):
    def last(self):
        return self.__getitem__(-1)

    def first(self):
        return self.__getitem__(0)

    def get(self, pos=0):
        return self.__getitem__(pos)

    def length(self):
        return self.__len__()