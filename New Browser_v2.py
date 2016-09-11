# -*- coding: utf-8 -*-
import sys, re, urllib.request
from PyQt5 import QtCore, QtWebEngineWidgets, QtWidgets, QtGui

class MainVindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainVindow, self).__init__(parent)
        self.resize(900, 400)
        self.windowView()

    def windowView(self):
        self.menu_bar = self.menuBar()
        self.menuEngine()
        self.progr = QtWidgets.QProgressBar()
        self.statusBar().addPermanentWidget(self.progr)
        self.progr.setTextVisible(False)
        self.progr.setVisible(False)

        self.widgett = TabWidget(self, "https://mail.ru")
        self.widgett.setTabsClosable(True)
        self.widgett.setMovable(True)
        self.setCentralWidget(self.widgett)
        self.setWindowIcon(QtGui.QIcon("images/WebBro.png"))


    def menuEngine(self):
        podmenu1 = self.menu_bar.addMenu("File")
        self.history = self.menu_bar.addMenu("History")
        self.allHistory = QtWidgets.QAction("All History", self)
        self.history.addAction(self.allHistory)
        self.historyView()

        podmenu3 = self.menu_bar.addMenu("Help")

        exitt = QtWidgets.QAction("Exit", self)
        exitt.setShortcut('Ctrl+Q')
        exitt.setStatusTip("Exit browser")
        #self.connect(exitt, QtCore.PYQT_SIGNAL("triggered()"), QtCore.PYQT_SLOT("close()"))
        exitt.triggered.connect(lambda: self.close())

        about = QtWidgets.QAction("About", self)
        about.setIconVisibleInMenu(True)
        about.setIcon(QtGui.QIcon("images/WebBro.png"))
        about.triggered.connect(lambda: self.aboutView())

        podmenu1.addAction(exitt)
        podmenu3.addAction(about)

    def historyView(self):
        self.modHistoryWindow = QtWidgets.QWidget(self, QtCore.Qt.Window)
        self.modHistoryWindow.setWindowIcon(QtGui.QIcon("images/WebBro.png"))
        self.modHistoryWindow.setWindowTitle("History")
        self.modHistoryWindow.resize(500, 300)
        self.hbox = QtWidgets.QHBoxLayout(self.modHistoryWindow)

    def aboutView(self):
        mod_window = QtWidgets.QWidget(self, QtCore.Qt.Window)
        mod_window.setWindowIcon(QtGui.QIcon("images/WebBro.png"))
        mod_window.setWindowTitle("About")
        mod_window.setFixedSize(500, 332)
        horLayout = QtWidgets.QHBoxLayout(mod_window)
        localHtmls = QtWebEngineWidgets.QWebEngineView()

        #localHtmls.page().acceptNavigationRequest(QtCore.QUrl())
        #localHtmls.page().load(QtCore.QUrl("file://about.html"))
        localHtmls.load(QtCore.QUrl("Html/about.html"))

        horLayout.addWidget(localHtmls)
        #localHtmls.linkClicked.connect(self.clicks)
        mod_window.show()
    def clicks(self, url):
        self.widgett.addTabb(url)

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, this, url, parent=None):
        super(TabWidget, self).__init__(parent)
        self.this = this
        self.webHistoryList = []
        self.setIconSize(QtCore.QSize(16, 16))
        self.addTabb( url)
        self.tabCloseRequested.connect(lambda ind: self.closeTab(ind))

    def closeTab(self, ind):
        obj = self.widget(ind)
        self.removeTab(ind)
        obj.deleteLater()

    def addTabb(self, urll="Html/start.html"):
        input_tab = QtWidgets.QTabWidget()
        super().addTab(input_tab, " ")

        contV = QtWidgets.QVBoxLayout(input_tab)
        contH = QtWidgets.QHBoxLayout()
        contV.addLayout(contH)

        button = QtWidgets.QPushButton("->")
        button2 = QtWidgets.QPushButton("<-")
        button3 = QtWidgets.QPushButton("ReLoad")
        button4 = QtWidgets.QPushButton(" + ")
        button3.setStatusTip("Reload")
        button2.setStatusTip("BacK")
        button.setStatusTip("Go")

        contH.addWidget(button3)
        contH.addWidget(button2)
        contH.addWidget(button)

        textLine = QtWidgets.QLineEdit()
        contH.addWidget(textLine)
        contH.addWidget(button4)
        web = self.createWeb(urll)
        contV.addWidget(web)

        self.engineTab(button, button2, button3, button4, textLine, web)
        indexx = self.indexOf(web.parent())
        self.setCurrentIndex(indexx)
        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.setStyleSheet("QTabBar::tab { width: 100px; height: 25px; }")
        self.setElideMode(QtCore.Qt.ElideRight)

    def createWeb(self, url):
        web = WebView(url)
        return web

    def creteWebList(self, item):
        nesovpad = True
        if len(self.webHistoryList) == 0:
            self.webHistoryList.append(item)
            nesovpad = False
        else:
            for i in self.webHistoryList:
                if i == item:
                    nesovpad = False
                    break
        if nesovpad:
            self.webHistoryList.append(item)

    def engineTab(self, but, but2, but3, but4, texT, web=None):
        def statusChanged(link):
            self.this.statusBar().showMessage(link)
        def urlChanged():
            text = texT.text()
            web.setUrl(QtCore.QUrl(text))
        def reload():
            web.setUrl(QtCore.QUrl(texT.text()))
        def back():
            page = web.page()
            history = page.history()
            history.back()
        def next():
            page = web.page()
            history = page.history()
            history.forward()

        def iconCangedd(icon):
            i = self.indexOf(web.parent())
            print('url', icon)
            self.setTabIcon(i, icon)
        def linkChanged(link):
            try:
                texT.setText(link.toString())
                i = self.indexOf(web.parent())
                link = link.toString()
                result = re.split(r'/', link)
                url = "https://www.google.com/s2/favicons?domain=" + result[2]
                data = urllib.request.urlopen(url).read()
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data)
                icon = QtGui.QIcon(pixmap)
                self.setTabIcon(i, icon)
            except:
                self.setTabIcon(i, QtGui.QIcon("images/WebBro.png"))
            self.creteWebList(link)
        def loadProgress(set):
            if set != 100:
                self.this.progr.setValue(set)
                self.this.progr.setVisible(True)
            else:
                self.this.progr.setVisible(False)
        def loadProgressEnd(set):
            if set:
                self.this.progr.setVisible(False)
        def indexChanged(ind):
            text = self.tabText(ind)
            self.this.setWindowTitle(text)
        def titleChangedd(title):
            i = self.indexOf(web.parent())
            self.this.setWindowTitle(title)
            self.setTabText(i, title)
        def historyEngineView():
            for j in range(self.this.hbox.count()):
                self.this.hbox.itemAt(j).widget().deleteLater()
            tableHistor = QtWidgets.QTableWidget(len(self.webHistoryList), 1)
            header = tableHistor.horizontalHeader()
            header.setStretchLastSection(True)

            tableHistor.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("  URL  "))
            self.this.hbox.addWidget(tableHistor)
            tableHistor.verticalHeader().hide()

            i = 0
            for j in self.webHistoryList:
                tableHistor.setItem(i, 0, QtWidgets.QTableWidgetItem(j))
                i += 1
            tableHistor.itemDoubleClicked.connect(lambda item: self.addTabb(item.text()))
            self.this.modHistoryWindow.show()


        self.this.history.triggered.connect(lambda: historyEngineView())
        web.titleChanged.connect(lambda title: titleChangedd(title))
        web.urlChanged.connect(lambda url: linkChanged(url))
        web.loadProgress.connect(lambda progr: loadProgress(progr))
        web.page().linkHovered.connect(statusChanged)

        but4.clicked.connect(lambda : self.addTabb())
        but3.clicked.connect(reload)
        but2.clicked.connect(back)
        but.clicked.connect(next)
        texT.returnPressed.connect(urlChanged)

        self.currentChanged.connect(lambda ind: indexChanged(ind))
        # web.iconChanged.connect(lambda icon: iconCangedd(icon))

class WebView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, url, parent=None):
        super(WebView, self).__init__(parent)
        self.load(QtCore.QUrl(url))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainVindow()
    window.show()
    sys.exit(app.exec_())
