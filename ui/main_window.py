import os
import typing
import webbrowser
import pelican.contents
import threadpool
from PySide2 import QtWidgets, QtCore, QtGui
from .source.main_window import Ui_MainWindow
import core
import settings


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.showMaximized()
        self.pelican = core.Reader()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setHorizontalHeaderLabels(["编号", "分类", "标题", "日期", "图片库", "已发布"])
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

    def reload(self):
        self.thread_pool.putRequest(threadpool.WorkRequest(self.read_articles))

    def preview(self):
        def wrapper():
            self.pelican.write()
            webbrowser.get().open('http://localhost')

        self.thread_pool.putRequest(threadpool.WorkRequest(wrapper))

    def deploy(self):
        print('deploy')

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
