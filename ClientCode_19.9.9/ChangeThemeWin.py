"""
说明：换肤窗口，为用户提供多种个性装扮。当用户点击主界面MainUI中右上角的换肤图标时跳出本窗口，
用户点击本窗口中的任意主题并确认即可换肤
作者：71117205丁婧伊
创建时间：2019/9/8 8:23pm
最后一次修改时间：2019/9/10 9:35am
"""
import sys
import traceback
from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QPushButton, QApplication, QScrollArea, QVBoxLayout, \
    QMessageBox
from qtpy import QtCore


# 更换皮肤的窗口，提供多种可更换装扮
class ChangeThemeWin(QWidget):
    # 点击皮肤，然后确认更换后发射的信号量，发射的int变量是第几个主题
    _signal = pyqtSignal(int)

    # 构造函数
    def __init__(self):
        super().__init__()
        self.initMainUI()

    # 初始化函数，修改窗体属性，添加窗体控件
    def initMainUI(self):
        # 添加bool变量确定鼠标是否按在QWidget界面，解决点击控件与拖拽页面事件冲突
        self.isPressedWidget = False
        # 设置widget组件的大小
        self.resize(800, 560)
        self.setMinimumSize(800, 560)
        self.setMaximumSize(800, 560)
        # 设置窗体名称和图标
        self.setWindowTitle('个性装扮')
        self.logoPixmap = QPixmap("./pic/shirt.png")
        self.logopic = QIcon()
        self.logopic.addPixmap(self.logoPixmap)
        self.setWindowIcon(self.logopic)
        # 设置窗体的ObjectName
        self.setObjectName("ChangeThemeWin")
        # 设置widget组件的位置居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # 隐藏边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 设置样式表
        self.setStyleSheet(
            "QWidget#themeWidget {\n"
            "    background-color: white;\n"
            "}\n"
            "QWidget#scroll_contents {\n"
            "    background-color: white;\n"
            "}\n"
            "QWidget#widgetTitle {\n"
            "    background-color: rgb(166, 166, 250);\n"
            "}\n"
            "QLabel#themeTitleLabel{ \n"
            "   color: white;\n"
            "}\n"
            "QPushButton#closeButton{\n"
            "   border: none;\n"
            "   color: white;\n"
            "   background: transparent;\n"
            "}\n"
            "QPushButton#closeButton:hover {\n"
            "    background-color: rgba(255, 0, 0, 100%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn1{\n"
            "   border-image: url(pic/mountain_small.jpg);"
            "}\n"
            "QPushButton#clothBtn1:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn2{\n"
            "   border-image: url(pic/mountainAndStars_small.jpg);"
            "}\n"
            "QPushButton#clothBtn2:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn3{\n"
            "   border-image: url(pic/cat_small.jpg);"
            "}\n"
            "QPushButton#clothBtn3:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn4{\n"
            "   border-image: url(pic/sandstone_small.jpg);"
            "}\n"
            "QPushButton#clothBtn4:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn5{\n"
            "   border-image: url(pic/pink_small.jpg);"
            "}\n"
            "QPushButton#clothBtn5:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn6{\n"
            "   border-image: url(pic/dandelion_small.jpg);"
            "}\n"
            "QPushButton#clothBtn6:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn7{\n"
            "   border-image: url(pic/cloud_small.jpg);"
            "}\n"
            "QPushButton#clothBtn7:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn8{\n"
            "   border-image: url(pic/sci_fi_small.jpg);"
            "}\n"
            "QPushButton#clothBtn8:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn9{\n"
            "   border-image: url(pic/mass_energy_small.jpg);"
            "}\n"
            "QPushButton#clothBtn9:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn10{\n"
            "   border-image: url(pic/earth_small.jpg);"
            "}\n"
            "QPushButton#clothBtn10:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn11{\n"
            "   border-image: url(pic/mountainAndCloud_small.jpg);"
            "}\n"
            "QPushButton#clothBtn11:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn12{\n"
            "   border-image: url(pic/blue.png);"
            "}\n"
            "QPushButton#clothBtn12:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn13{\n"
            "   border-image: url(pic/AvocadoGreen.png);"
            "}\n"
            "QPushButton#clothBtn13:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn14{\n"
            "   border-image: url(pic/grey.png);"
            "}\n"
            "QPushButton#clothBtn14:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn15{\n"
            "   border-image: url(pic/black.png);"
            "}\n"
            "QPushButton#clothBtn15:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn16{\n"
            "   border-image: url(pic/orange.png);"
            "}\n"
            "QPushButton#clothBtn16:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
            "QPushButton#clothBtn17{\n"
            "   border-image: url(pic/red.png);"
            "}\n"
            "QPushButton#clothBtn17:hover {\n"
            "    background-color: rgba(255, 255, 255, 50%);\n"
            "    color: white\n"
            "}\n"
        )
        # 标题栏窗体
        self.widgetTitle = QWidget(self)
        self.widgetTitle.setGeometry(0, 0, 800, 35)
        self.widgetTitle.setObjectName("widgetTitle")
        # 标题栏标签
        self.themeTitleLabel = QLabel(self)
        self.themeTitleLabel.setGeometry(10, 0, 80, 35)
        self.themeTitleLabel.setText("个性装扮")
        self.themeTitleLabel.setObjectName("themeTitleLabel")
        # 关闭按钮
        self.closeButton = QPushButton("×", self)
        self.closeButton.setGeometry(765, 0, 35, 35)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.clicked.connect(self.close)
        # 将皮肤窗体放在可滚动区域中
        self.themeWidget = QWidget(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(0, 35, 800, 525)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_bar = self.scroll_area.verticalScrollBar()
        # 设置窗体，控制滚动区域的大小
        self.scroll_contents = QWidget()
        self.scroll_contents.setGeometry(0, 35, 800, 1000)
        self.scroll_contents.setObjectName("scroll_contents")
        self.scroll_contents.setMinimumSize(770, 1000)
        # 主题1 按钮
        self.clothBtn1 = QPushButton(self.scroll_contents)
        self.clothBtn1.resize(150, 120)
        self.clothBtn1.move(30, 50)
        self.clothBtn1.setText("主题1")
        self.clothBtn1.setObjectName("clothBtn1")
        self.clothBtn1.clicked.connect(partial(self.changeCloth, 1))
        # 主题2 按钮
        self.clothBtn2 = QPushButton(self.scroll_contents)
        self.clothBtn2.resize(150, 120)
        self.clothBtn2.move(230, 50)
        self.clothBtn2.setText("主题2")
        self.clothBtn2.setObjectName("clothBtn2")
        self.clothBtn2.clicked.connect(partial(self.changeCloth, 2))
        # 主题3 按钮
        self.clothBtn3 = QPushButton(self.scroll_contents)
        self.clothBtn3.resize(150, 120)
        self.clothBtn3.move(420, 50)
        self.clothBtn3.setText("主题3")
        self.clothBtn3.setObjectName("clothBtn3")
        self.clothBtn3.clicked.connect(partial(self.changeCloth, 3))
        # 主题4 按钮
        self.clothBtn4 = QPushButton(self.scroll_contents)
        self.clothBtn4.resize(150, 120)
        self.clothBtn4.move(610, 50)
        self.clothBtn4.setText("主题4")
        self.clothBtn4.setObjectName("clothBtn4")
        self.clothBtn4.clicked.connect(partial(self.changeCloth, 4))
        # 主题5 按钮
        self.clothBtn5 = QPushButton(self.scroll_contents)
        self.clothBtn5.resize(150, 120)
        self.clothBtn5.move(30, 210)
        self.clothBtn5.setText("主题5")
        self.clothBtn5.setObjectName("clothBtn5")
        self.clothBtn5.clicked.connect(partial(self.changeCloth, 5))
        # 主题6 按钮
        self.clothBtn6 = QPushButton(self.scroll_contents)
        self.clothBtn6.resize(150, 120)
        self.clothBtn6.move(230, 210)
        self.clothBtn6.setText("主题6")
        self.clothBtn6.setObjectName("clothBtn6")
        self.clothBtn6.clicked.connect(partial(self.changeCloth, 6))
        # 主题7 按钮
        self.clothBtn7 = QPushButton(self.scroll_contents)
        self.clothBtn7.resize(150, 120)
        self.clothBtn7.move(420, 210)
        self.clothBtn7.setText("主题7")
        self.clothBtn7.setObjectName("clothBtn7")
        self.clothBtn7.clicked.connect(partial(self.changeCloth, 7))
        # 主题8 按钮
        self.clothBtn8 = QPushButton(self.scroll_contents)
        self.clothBtn8.resize(150, 120)
        self.clothBtn8.move(610, 210)
        self.clothBtn8.setText("主题8")
        self.clothBtn8.setObjectName("clothBtn8")
        self.clothBtn8.clicked.connect(partial(self.changeCloth, 8))
        # 主题9 按钮
        self.clothBtn9 = QPushButton(self.scroll_contents)
        self.clothBtn9.resize(150, 120)
        self.clothBtn9.move(30, 370)
        self.clothBtn9.setText("主题9")
        self.clothBtn9.setObjectName("clothBtn9")
        self.clothBtn9.clicked.connect(partial(self.changeCloth, 9))
        # 主题10 按钮
        self.clothBtn10 = QPushButton(self.scroll_contents)
        self.clothBtn10.resize(150, 120)
        self.clothBtn10.move(230, 370)
        self.clothBtn10.setText("主10")
        self.clothBtn10.setObjectName("clothBtn10")
        self.clothBtn10.clicked.connect(partial(self.changeCloth, 10))
        # 主题11 按钮
        self.clothBtn11 = QPushButton(self.scroll_contents)
        self.clothBtn11.resize(150, 120)
        self.clothBtn11.move(420, 370)
        self.clothBtn11.setText("主题11")
        self.clothBtn11.setObjectName("clothBtn11")
        self.clothBtn11.clicked.connect(partial(self.changeCloth, 11))
        # 主题12 按钮
        self.clothBtn12 = QPushButton(self.scroll_contents)
        self.clothBtn12.resize(150, 120)
        self.clothBtn12.move(610, 370)
        self.clothBtn12.setText("主题12")
        self.clothBtn12.setObjectName("clothBtn12")
        self.clothBtn12.clicked.connect(partial(self.changeCloth, 12))
        # 主题13 按钮
        self.clothBtn13 = QPushButton(self.scroll_contents)
        self.clothBtn13.resize(150, 120)
        self.clothBtn13.move(30, 530)
        self.clothBtn13.setText("主题13")
        self.clothBtn13.setObjectName("clothBtn13")
        self.clothBtn13.clicked.connect(partial(self.changeCloth, 13))
        # 主题14 按钮
        self.clothBtn14 = QPushButton(self.scroll_contents)
        self.clothBtn14.resize(150, 120)
        self.clothBtn14.move(230, 530)
        self.clothBtn14.setText("主题14")
        self.clothBtn14.setObjectName("clothBtn14")
        self.clothBtn14.clicked.connect(partial(self.changeCloth, 14))
        # 主题15 按钮
        self.clothBtn15 = QPushButton(self.scroll_contents)
        self.clothBtn15.resize(150, 120)
        self.clothBtn15.move(420, 530)
        self.clothBtn15.setText("主题15")
        self.clothBtn15.setObjectName("clothBtn15")
        self.clothBtn15.clicked.connect(partial(self.changeCloth, 15))
        # 主题16 按钮
        self.clothBtn16 = QPushButton(self.scroll_contents)
        self.clothBtn16.resize(150, 120)
        self.clothBtn16.move(610, 530)
        self.clothBtn16.setText("主题16")
        self.clothBtn16.setObjectName("clothBtn16")
        self.clothBtn16.clicked.connect(partial(self.changeCloth, 16))
        # 主题17 按钮
        self.clothBtn17 = QPushButton(self.scroll_contents)
        self.clothBtn17.resize(150, 120)
        self.clothBtn17.move(30, 690)
        self.clothBtn17.setText("主题17")
        self.clothBtn17.setObjectName("clothBtn17")
        self.clothBtn17.clicked.connect(partial(self.changeCloth, 17))
        # 将可滚动区域放入设置好的窗体中
        self.scroll_area.setWidget(self.scroll_contents)
        self.scroll_area.installEventFilter(self)

    # 槽函数，当用户点击任意一个皮肤时跳出确认是否更换皮肤的提示框，如果用户点击确认，则发射皮肤编号给MainUI更换皮肤
    def changeCloth(self, num):
        try:
            re = QMessageBox.question(self, "提示", "更换皮肤", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)
            if re == QMessageBox.Yes:
                # 如果确认更换，发射用户选择的皮肤编号
                self._signal.emit(num)
        except Exception as e:
            traceback.print_exc()

    # 用户按住鼠标事件, 获取拖拽前鼠标相对窗口的位置
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            # 获取鼠标相对窗口的位置
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            # 当前鼠标点击的是窗体而不是控件
            self.isPressedWidget = True

    # 鼠标移动事件，窗体随鼠标拖拽而移动
    def mouseMoveEvent(self, QMouseEvent):
        if self.isPressedWidget:
            # 当前鼠标点击的是窗体而不是控件
            if Qt.LeftButton and self.m_flag:
                # 更改窗口位置
                self.move(QMouseEvent.globalPos() - self.m_Position)
                QMouseEvent.accept()

    # 用户松开鼠标事件
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.isPressedWidget = False