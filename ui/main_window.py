import os
import typing
import webbrowser
import pelican.contents
import threadpool
from PySide2 import QtWidgets, QtCore, QtGui
from .source.main_window import Ui_MainWindow
import core
import settings


class Table(QtWidgets.QTableWidget):
    def __init__(self, parent):
        super(Table, self).__init__(parent)
        self.setShowGrid(False)
        self.setColumnCount(6)
        for index, column_name in enumerate(settings.HEADERS):
            self.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(column_name))


class ButtonList(QtWidgets.QVBoxLayout):
    def __init__(self):
        super(ButtonList, self).__init__()
        buttons = [QtWidgets.QPushButton(text) for text in ['adf', 'asdf']]
        self.button1 = QtWidgets.QPushButton("asdfga")
        QtCore.QObject.connect(self.button1,QtCore.SIGNAL('clicked()'), MainWindow.upload_photos)
        self.addWidget(self.button1)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.showMaximized()
        self.left_layout = ButtonList()
        self.right_layout = QtWidgets.QVBoxLayout()
        self.layout().addChildLayout(self.left_layout)
        self.layout().addChildLayout(self.right_layout)

        self.tableWidget = Table(self)
        self.pelican = core.Pelican()
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)
        self.thread_pool = threadpool.ThreadPool(2)
        self.thread_pool.putRequest(threadpool.WorkRequest(self.read_articles))
        self.thread_pool.putRequest(threadpool.WorkRequest(self.pelican.serve))
        self.articles = []

    def read_articles(self):
        self.pelican.read(local=True)
        self.articles = self.pelican.articles_generator.articles
        self.articles.sort(key=lambda article: -int(article.metadata['permalink']))
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()
        for row_index, article in enumerate(self.articles):
            values = settings.get_fields(article)
            values = [values[header] for header in settings.HEADERS]
            self.tableWidget.insertRow(row_index)
            for col_index, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(value)
                self.tableWidget.setItem(row_index, col_index, item)

    def edit(self):
        item: typing.List[QtWidgets.QTableWidgetItem] = self.tableWidget.selectedItems()
        permalink = item[0].text()
        article: pelican.contents.Article = [art for art in self.articles if art.metadata['permalink'] == permalink][0]
        command = f'\"{settings.EDITOR_PATH}\" "{article.source_path}"'
        os.popen(command)

    def create_article(self):
        self.tableWidget.setColumnCount(5)

    def read(self):
        self.thread_pool.putRequest(threadpool.WorkRequest(self.read_articles))

    def write(self):
        pass

    def preview(self):
        """
        开始本地预览
        :return:
        """

        def wrapper():
            self.pelican.write()
            webbrowser.get().open('http://localhost')

        self.thread_pool.putRequest(threadpool.WorkRequest(wrapper))

    def deploy(self):
        """
        将博客上传至github
        :return:
        """

        def wrapper():
            self.pelican.deploy()

        self.thread_pool.putRequest(threadpool.WorkRequest(wrapper))

    def upload_photos(self):
        print('upload')

    def get_fields(article: pelican.contents.Article):
        storage = article.metadata['storage']
        gallery = article.metadata['gallery'] if article.metadata['gallery'] else 'default'
        return {
            '编号': article.metadata['permalink'],
            '分类': article.metadata['category'],
            '标题': article.title,
            '日期': article.date.strftime('%y-%m-%d'),
            '图片库': f'{storage}:{gallery}',
            '已发布': article.status,
        }

    def open_explorer(self):
        pass

    def open_album(self):
        """
        在文件管理器中打开图片库
        :return:
        """
        pass
