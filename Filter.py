from PyQt5.QtCore import pyqtSignal,QObject


class Filter(QObject):
    filterQueryError = pyqtSignal(name="queryError")

    def __init__(self, query):
        super().__init__()
        self.searchContents = []
        self.status = None
        self.score = []
        self.tags = []
        self.readStatus=None
        self.query = query

    def isEmpty(self):
        if (self.searchContents == []) and (self.status is None) and (self.score == []) and (self.tags == []):
            return True
        else:
            return False

    def getSearchContentSql(self, colList):
        cols = "||".join(f"ifnull(`{col}`,0)" for col in colList)
        filterSql = cols + " like '%" + self.searchContents[0] + "%' "
        if len(self.searchContents) > 1:
            for i in range(len(self.searchContents)):
                if self.searchContents[i] != '':
                    filterSql += " or " + cols + " like '%" + self.searchContents[i] + "%' "
        filterSql += " COLLATE NOCASE "
        return filterSql

    def getTagFilterSql(self):
        bookIds = []
        tags = "'" + "', '".join(self.tags) + "'"
        bookSql = f"select DISTINCT book_id from book_tag where tag_id in (select tag_id from tags where tag_name in ({tags}))"
        print(bookSql)
        if self.query.exec(bookSql):
            while self.query.next():
                bookIds.append(self.query.value(0))
        else:
            self.searchContents.emit()
        if bookIds:
            return f" book_id in ({', '.join(map(str,bookIds))}) "
        return " 1=2 "

    def printAll(self):
        print(f"search content:{self.searchContents}")
        print(f"status:{self.status}")
        print(f"readStatus:{self.readStatus}")
        print(f"score:{self.score}")
        print(f"tags:{self.tags}")
        print(f"tag sql:"+self.getTagFilterSql())

