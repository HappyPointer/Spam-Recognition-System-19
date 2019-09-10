import sys
import traceback
from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QPushButton, QApplication, QScrollArea, QVBoxLayout, \
    QMessageBox
from qtpy import QtCore


class ChangeThemeWin(QWidget):

    _signal = pyqtSignal(int)

    def __init__(self):
        # 初始化————init__
        super().__init__()
        self.initMainUI()

    def initMainUI(self):
        # 添加bool变量确定鼠标是否按在QWidget界面
        self.isPressedWidget = False
        # 设置widget组件的大小(w,h)
        self.resize(800, 560)
        # 设置widget大小不可变
        self.setMinimumSize(800, 560)
        self.setMaximumSize(800, 560)
        # 设置widget的ObjectName
        self.setObjectName("ChangeThemeWin")
        # 设置widget组件的位置居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # 隐藏边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 设置样式表,到时候统一整合在一个qss文件中
        # themeWidget 为什么设置皮肤不好使？
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
        # 标题栏
        self.widgetTitle = QWidget(self)
        self.widgetTitle.setGeometry(0, 0, 800, 35)
        self.widgetTitle.setObjectName("widgetTitle")
        # 标题栏名字
        self.themeTitleLabel = QLabel(self)
        self.themeTitleLabel.setGeometry(10, 0, 80, 35)
        self.themeTitleLabel.setText("个性装扮")
        self.themeTitleLabel.setObjectName("themeTitleLabel")
        #关闭按钮
        self.closeButton = QPushButton("×", self)
        self.closeButton.setGeometry(765, 0, 35, 35)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.clicked.connect(self.close)
        # 放各种主题皮肤的窗口
        self.themeWidget = QWidget(self)
        # 可滚动区域
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(0, 35, 800, 525)
        self.scroll_area.setWidgetResizable(True)
        # 滚动条
        self.scroll_bar = self.scroll_area.verticalScrollBar()
        # 可滚动区域中的widget
        self.scroll_contents = QWidget()
        self.scroll_contents.setGeometry(0, 35, 800, 1000)
        self.scroll_contents.setObjectName("scroll_contents")
        # 为什么大小会变？
        self.scroll_contents.setMinimumSize(770, 1000)

        # 更换皮肤按钮
        self.clothBtn1 = QPushButton(self.scroll_contents)
        self.clothBtn1.resize(150, 120)
        self.clothBtn1.move(30, 50)
        self.clothBtn1.setText("主题1")
        self.clothBtn1.setObjectName("clothBtn1")
        self.clothBtn1.clicked.connect(partial(self.changeCloth, 1))

        self.clothBtn2 = QPushButton(self.scroll_contents)
        self.clothBtn2.resize(150, 120)
        self.clothBtn2.move(230, 50)
        self.clothBtn2.setText("主题2")
        self.clothBtn2.setObjectName("clothBtn2")
        self.clothBtn2.clicked.connect(partial(self.changeCloth, 2))

        self.clothBtn3 = QPushButton(self.scroll_contents)
        self.clothBtn3.resize(150, 120)
        self.clothBtn3.move(420, 50)
        self.clothBtn3.setText("主题3")
        self.clothBtn3.setObjectName("clothBtn3")
        self.clothBtn3.clicked.connect(partial(self.changeCloth, 3))

        self.clothBtn4 = QPushButton(self.scroll_contents)
        self.clothBtn4.resize(150, 120)
        self.clothBtn4.move(610, 50)
        self.clothBtn4.setText("主题4")
        self.clothBtn4.setObjectName("clothBtn4")
        self.clothBtn4.clicked.connect(partial(self.changeCloth, 4))

        self.clothBtn5 = QPushButton(self.scroll_contents)
        self.clothBtn5.resize(150, 120)
        self.clothBtn5.move(30, 210)
        self.clothBtn5.setText("主题5")
        self.clothBtn5.setObjectName("clothBtn5")
        self.clothBtn5.clicked.connect(partial(self.changeCloth, 5))

        self.clothBtn6 = QPushButton(self.scroll_contents)
        self.clothBtn6.resize(150, 120)
        self.clothBtn6.move(230, 210)
        self.clothBtn6.setText("主题6")
        self.clothBtn6.setObjectName("clothBtn6")
        self.clothBtn6.clicked.connect(partial(self.changeCloth, 6))

        self.clothBtn7 = QPushButton(self.scroll_contents)
        self.clothBtn7.resize(150, 120)
        self.clothBtn7.move(420, 210)
        self.clothBtn7.setText("主题7")
        self.clothBtn7.setObjectName("clothBtn7")
        self.clothBtn7.clicked.connect(partial(self.changeCloth, 7))

        self.clothBtn8 = QPushButton(self.scroll_contents)
        self.clothBtn8.resize(150, 120)
        self.clothBtn8.move(610, 210)
        self.clothBtn8.setText("主题8")
        self.clothBtn8.setObjectName("clothBtn8")
        self.clothBtn8.clicked.connect(partial(self.changeCloth, 8))

        self.clothBtn9 = QPushButton(self.scroll_contents)
        self.clothBtn9.resize(150, 120)
        self.clothBtn9.move(30, 370)
        self.clothBtn9.setText("主题9")
        self.clothBtn9.setObjectName("clothBtn9")
        self.clothBtn9.clicked.connect(partial(self.changeCloth, 9))

        self.clothBtn10 = QPushButton(self.scroll_contents)
        self.clothBtn10.resize(150, 120)
        self.clothBtn10.move(230, 370)
        self.clothBtn10.setText("主10")
        self.clothBtn10.setObjectName("clothBtn10")
        self.clothBtn10.clicked.connect(partial(self.changeCloth, 10))

        self.clothBtn11 = QPushButton(self.scroll_contents)
        self.clothBtn11.resize(150, 120)
        self.clothBtn11.move(420, 370)
        self.clothBtn11.setText("主题11")
        self.clothBtn11.setObjectName("clothBtn11")
        self.clothBtn11.clicked.connect(partial(self.changeCloth, 11))

        self.clothBtn12 = QPushButton(self.scroll_contents)
        self.clothBtn12.resize(150, 120)
        self.clothBtn12.move(610, 370)
        self.clothBtn12.setText("主题12")
        self.clothBtn12.setObjectName("clothBtn12")
        self.clothBtn12.clicked.connect(partial(self.changeCloth, 12))

        self.clothBtn13 = QPushButton(self.scroll_contents)
        self.clothBtn13.resize(150, 120)
        self.clothBtn13.move(30, 530)
        self.clothBtn13.setText("主题13")
        self.clothBtn13.setObjectName("clothBtn13")
        self.clothBtn13.clicked.connect(partial(self.changeCloth, 13))

        self.clothBtn14 = QPushButton(self.scroll_contents)
        self.clothBtn14.resize(150, 120)
        self.clothBtn14.move(230, 530)
        self.clothBtn14.setText("主题14")
        self.clothBtn14.setObjectName("clothBtn14")
        self.clothBtn14.clicked.connect(partial(self.changeCloth, 14))

        self.clothBtn15 = QPushButton(self.scroll_contents)
        self.clothBtn15.resize(150, 120)
        self.clothBtn15.move(420, 530)
        self.clothBtn15.setText("主题15")
        self.clothBtn15.setObjectName("clothBtn15")
        self.clothBtn15.clicked.connect(partial(self.changeCloth, 15))

        self.clothBtn16 = QPushButton(self.scroll_contents)
        self.clothBtn16.resize(150, 120)
        self.clothBtn16.move(610, 530)
        self.clothBtn16.setText("主题16")
        self.clothBtn16.setObjectName("clothBtn16")
        self.clothBtn16.clicked.connect(partial(self.changeCloth, 16))

        self.clothBtn17 = QPushButton(self.scroll_contents)
        self.clothBtn17.resize(150, 120)
        self.clothBtn17.move(30, 690)
        self.clothBtn17.setText("主题17")
        self.clothBtn17.setObjectName("clothBtn17")
        self.clothBtn17.clicked.connect(partial(self.changeCloth, 17))

        self.scroll_area.setWidget(self.scroll_contents)
        self.scroll_area.installEventFilter(self)

    def changeCloth(self, num):
        try:
            # 跳出弹框确认是否更换皮肤
            re = QMessageBox.question(self, "提示", "更换皮肤", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)
            if re == QMessageBox.Yes:
                # 发射信号
                self._signal.emit(num)
        except:
            traceback.print_exc()

    def mousePressEvent(self, event):
        # 判断点击时鼠标不在控件上
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            # 当前鼠标按下的即是QWidget而非界面上布局的其他控件
            self.isPressedWidget = True

    def mouseMoveEvent(self, QMouseEvent):
        # 当前鼠标按下的是QWidget而非界面上布局的其他控件
        if self.isPressedWidget:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
                QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.isPressedWidget = False

if __name__ == '__main__':
    # 主函数
    app = QApplication(sys.argv)
    win = ChangeThemeWin()
    win.show()
    sys.exit(app.exec_())


