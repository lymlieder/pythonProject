# from cefpython3 import cefpython as cef
# import platform
# import sys
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView


# 创建主窗口
class MainWindow(QMainWindow):

    homePageUrl = "https://yayin.shandongyayin.com/dist/index.html#/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle('山东亚银 客户管理端')
        # 设置窗口大小900*600
        self.resize(2600, 1400)
        self.show()

        # 创建tabWidget（多标签页面）
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_Tab)
        self.setCentralWidget(self.tabWidget)

        # 第一个tab页面
        self.webView = WebEngineView(self)  # self必须要有，是将主窗口作为参数，传给浏览器
        self.webView.load(QUrl(self.homePageUrl))
        self.create_tab(self.webView)
        # self.setCentralWidget(self.webView)

        # 使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(32, 32))
        # 添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        #3a7d421fe8e211034238988ad30ee39967bcfa3c
        # url_head = "https://public.shandongyayin.com/desktop/"
        url_head = QFileInfo(__file__).absolutePath() + "/icons/"
        # QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon(url_head + 'backward.png'), 'backward', self)
        # back_button = QAction("test", 'backward', self)
        next_button = QAction(QIcon(url_head + 'forward.png'), 'forward', self)
        stop_button = QAction(QIcon(url_head + 'stop.png'), 'stop', self)
        reload_button = QAction(QIcon(url_head + 'reload.png'), 'reload', self)
        homepage_button = QAction(QIcon(url_head + 'homepage.png'), 'homepage', self)

        # 绑定事件
        back_button.triggered.connect(self.webView.back)
        next_button.triggered.connect(self.webView.forward)
        stop_button.triggered.connect(self.webView.stop)
        reload_button.triggered.connect(self.webView.reload)
        homepage_button.triggered.connect(self.go_to_home_page)

        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)
        navigation_bar.addSeparator()
        navigation_bar.addAction(homepage_button)

        # 添加URL地址栏
        # self.urlbar = QLineEdit()
        # # 让地址栏能响应回车按键信号
        # self.urlbar.returnPressed.connect(self.navigate_to_url)
        #
        # navigation_bar.addSeparator()
        # navigation_bar.addWidget(self.urlbar)

        # 让浏览器相应url地址的变化
        # self.webView.urlChanged.connect(self.renew_urlbar)

    # 导航到首页
    def go_to_home_page(self):
        q = QUrl(self.homePageUrl)
        self.webview.setUrl(q)

    # 显示地址
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.webview.setUrl(q)

    # 响应输入的地址
    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # 创建tab页面
    def create_tab(self, webview):
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.setCurrentWidget(self.tab)

        # 渲染到页面
        self.Layout = QHBoxLayout(self.tab)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.addWidget(webview)

    # 关闭tab页面
    def close_Tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()  # 当只有1个tab时，关闭主窗口


# 创建浏览器，重写重写createwindow方法实现页面连接的点击跳转
class WebEngineView(QWebEngineView):

    def __init__(self, mainwindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.create_tab(new_webview)
        return new_webview


# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 创建主窗口
    browser = MainWindow()
    browser.show()
    # 运行应用，并监听事件
    sys.exit(app.exec_())

# def main():
# check_versions()
# sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
# cef.Initialize()
# cef.CreateBrowserSync(url="https://www.baidu.com/",
#                       window_title="Hello World!")
# cef.MessageLoop()
# cef.Shutdown()


# def check_versions():
#     ver = cef.GetVersion()
#     print("[hello_world.py] CEF Python {ver}".format(ver=ver["version"]))
#     print("[hello_world.py] Chromium {ver}".format(ver=ver["chrome_version"]))
#     print("[hello_world.py] CEF {ver}".format(ver=ver["cef_version"]))
#     print("[hello_world.py] Python {ver} {arch}".format(
#            ver=platform.python_version(),
#            arch=platform.architecture()[0]))
#     assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


# if __name__ == '__main__':
# main()

"""
将cefpython3嵌入到PyQt5中，往输入框中输入URL地址，点击查询，创建浏览器并加载HTML内容显示
"""
# from PyQt5 import QtWidgets
# from cefpython3 import cefpython as cef
# import sys
#
# # 浏览器内容窗口
# class CefBrowser(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         self.browser = None
#         super().__init__(parent)
#
#     def create_browser(self, window_info, url):
#         self.browser = cef.CreateBrowserSync(window_info, url=url)
#
#     def embedBrowser(self, url):
#         window_info = cef.WindowInfo()
#         # void window_info.SetAsChild(int parentWindowHandle, list windowRect), windowRect~[left,top,right,bottom]
#         window_info.SetAsChild(int(self.winId()), [0, 0, self.width(), self.height()])
#         cef.PostTask(cef.TID_UI, self.create_browser, window_info, url)
#
# # Qt主窗口
# class BrowserWindow:
#     def setUI(self, MainWindow):
#         MainWindow.resize(800, 600)
#         MainWindow.setWindowTitle("cefpython3-PyQt5")
#
#         # URL输入框、查询按钮、浏览器控件
#         self.le_search = QtWidgets.QLineEdit()
#         self.le_search.setPlaceholderText("输入网址...")
#         self.btn_search = QtWidgets.QPushButton()
#         self.btn_search.setText("查询")
#         self.browser_widget = CefBrowser()
#
#         # 设置布局方式：栅栏式
#         self.main_layout = QtWidgets.QGridLayout(MainWindow)
#         self.main_layout.addWidget(self.le_search, 0, 0, 1, 1)
#         self.main_layout.addWidget(self.btn_search, 0, 1, 1, 1)
#         self.main_layout.addWidget(self.browser_widget, 1, 0, 8, 2)
#
#         # 信号和槽函数
#         self.signal_slots()
#
#     def signal_slots(self):
#         # 绑定`查询`按钮的点击事件
#         self.btn_search.clicked.connect(self.slot_load_url)
#
#     def slot_load_url(self):
#         """获取输入框的URL，判断是否已存在browser对象，如果存在则LoadUrl否则开始创建浏览器"""
#         if self.le_search.text():
#             if self.browser_widget.browser:
#                 self.browser_widget.browser.LoadUrl(self.le_search.text())
#             else:
#                 self.browser_widget.embedBrowser(self.le_search.text())
#
#     def show(self):
#         """创建和显示应用窗口，循环监听处理"""
#         app = QtWidgets.QApplication([])
#         widget = QtWidgets.QWidget()
#         main_window = BrowserWindow()
#         main_window.setUI(widget)
#         widget.show()
#         app.exec_()
#
#
# if __name__ == "__main__":
#     sys.excepthook = cef.ExceptHook
#     # bool cef.Initialize(settings={...},switches={...})
#     cef.Initialize(settings={"multi_threaded_message_loop": True})
#     BrowserWindow().show()
#     # cef.Shutdown()
#     while(1 == 1):
#         s = 1
