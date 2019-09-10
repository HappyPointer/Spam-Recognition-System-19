"""
作者：蔡夏菁，郭振东，何颖智，丁婧伊
描述：登录界面文件
创建日期：2019-8-26
最后修改日期：2019-9-10
"""

import sys
import SettingOperations
from ChangeThemeWin import ChangeThemeWin
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Popup_Win import *
from PaintQSlider import PaintQSlider
import re
import chardet

import LoginAndGetMail2_6
import ListFuncLib
import DetailedMailWin

# 辅助显示任务栏图标
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class MainUI(QWidget):
    """
    作者：蔡夏菁，丁婧伊，何颖智，郭振东
    描述：创建主界面窗口
    """
    # 存储所有的邮件信息，列表中存储字典数据，字典包括三个 key : sender, text, type
    mailContent = []
    # 记录当前邮件预览界面中已经显示的邮件数量
    mailWidgetCount = 0
    # 记录当前 mailList 是否处在加载状态中
    mailLoadingState = True
    # 信号，发射主题编号
    _themeSignal = pyqtSignal(str)

    def __init__(self):
        """
        作者：蔡夏菁
        描述：初始化主界面窗口
        """
        super().__init__()
        self.changeWin = ChangeThemeWin()
        self.changeWin._signal.connect(self.changeTheme)
        self.initMainUI()


    def initMainUI(self):
        """
        作者：蔡夏菁，丁婧伊，何颖智
        描述：初始化主界面窗口
        """
        # 解决点击控件和窗口拖拽事件冲突造成的系统崩溃
        # 添加bool变量确定鼠标是否按在QWidget界面
        self.isPressedWidget = False
        # 设置widget组件的大小(w,h)
        self.resize(1000, 700)
        # 设置widget大小不可变
        self.setMinimumSize(1000, 700)
        self.setMaximumSize(1000, 700)
        # 设置widget的ObjectName
        self.setObjectName("MainUI")
        # 设置widget组件的位置居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # 给widget组件设置标题
        self.setWindowTitle('圆桌清道夫')
        # 隐藏边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        # logo设置
        self.logoPixmap = QPixmap("./pic/logo.png")
        self.logopic = QIcon()
        self.logopic.addPixmap(self.logoPixmap)
        self.setWindowIcon(self.logopic)

        # 设置默认背景图，写在MainUI中
        self.palette = QPalette()
        self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("/mountain.jpg")))
        self.setPalette(self.palette)

        # 美化主界面
        with open("./scrollbar/MainWin.qss", "rb")as fp:
            content = fp.read()
            encoding = chardet.detect(content) or {}
            content = content.decode(encoding.get("encoding") or "utf-8")
        self.setStyleSheet(content)

        # 设置字体信息
        # 用于左侧选择栏的字体
        fontleft = QFont()
        # 字体
        fontleft.setFamily('微软雅黑')
        # 加粗
        fontleft.setBold(True)
        # 大小
        fontleft.setPointSize(15)
        fontleft.setWeight(75)

        # 左侧共三个按钮
        # 消息按钮，初始默认为按下
        self.btnleft_Message = QPushButton(self)
        self.btnleft_Message.setGeometry(0, 100, 250, 75)
        self.btnleft_Message.setText("      邮件")
        self.icon1 = QIcon()
        self.icon1.addPixmap(QPixmap("pic\Message.png"), QIcon.Normal, QIcon.Off)
        self.btnleft_Message.setIcon(self.icon1)
        self.btnleft_Message.setIconSize(QSize(50, 80))
        self.btnleft_Message.setObjectName("btnleft_Message")
        self.btnleft_Message.setFont(fontleft)
        self.btnleft_Message.clicked.connect(self.Shift_Main)

        # 过滤器按钮，实现过滤器功能
        self.btnleft_Filter = QPushButton(self)
        self.btnleft_Filter.setGeometry(0, 175, 250, 75)
        self.btnleft_Filter.setText("   过滤器")
        self.icon2 = QIcon()
        self.icon2.addPixmap(QPixmap("pic\Filter.png"), QIcon.Normal, QIcon.Off)
        self.btnleft_Filter.setIcon(self.icon2)
        self.btnleft_Filter.setIconSize(QSize(50,80))
        self.btnleft_Filter.setObjectName("btnleft_Filter")
        self.btnleft_Filter.setFont(fontleft)
        self.btnleft_Filter.clicked.connect(self.Shift_Filter)

        # 设置按钮，用于设置界面以及部分功能
        self.btnleft_Setting = QPushButton(self)
        self.btnleft_Setting.setGeometry(0, 250, 250, 75)
        self.btnleft_Setting.setText("      设置")
        self.icon3 = QIcon()
        self.icon3.addPixmap(QPixmap("pic\Setting.png"), QIcon.Normal, QIcon.Off)
        self.btnleft_Setting.setIcon(self.icon3)
        self.btnleft_Setting.setIconSize(QSize(50,80))
        self.btnleft_Setting.setObjectName("btnleft_Setting")
        self.btnleft_Setting.setFont(fontleft)
        self.btnleft_Setting.clicked.connect(self.Shift_Setting)

        # 右侧布局
        # 右侧消息框背景
        self.backgroundRight = QLabel(self)
        self.backgroundRight.setGeometry(QRect(250, 40, 750, 660))
        self.backgroundRight.setObjectName("backgroundRight")

        # 设置关闭按钮
        self.closebtn = QPushButton('×', self)
        self.closebtn.setGeometry(950, 0, 50, 40)
        self.closebtn.setObjectName("closebtn")
        self.closebtn.setFont(fontleft)
        self.closebtn.clicked.connect(self.hide)

        # 设置最小化按钮
        self.minimize = QPushButton('-', self)
        self.minimize.setGeometry(900, 0, 50, 40)
        self.minimize.setObjectName("minimize")
        self.minimize.setFont(fontleft)
        self.minimize.clicked.connect(self.showMinimized)

        # 设置换肤按钮
        self.changeThemebtn = QPushButton(self)
        self.changeThemebtn.setGeometry(850, 0, 50, 40)
        self.iconCloth = QIcon()
        self.iconCloth.addPixmap(QPixmap("pic\shirt.png"), QIcon.Normal, QIcon.Off)
        self.changeThemebtn.setIcon(self.iconCloth)
        self.changeThemebtn.setIconSize(QSize(25, 20))
        self.changeThemebtn.setObjectName("changeThemebtn")
        self.changeThemebtn.setFont(fontleft)
        self.changeThemebtn.clicked.connect(self.changeThemeWidget)

        # 右侧主界面布局
        # 创建主界面布局
        # 显示垃圾邮件信息
        self.Message_Receive = QFrame(self)
        self.Message_Receive.setGeometry(250, 40, 700, 660)
        self.vbox1 = QVBoxLayout(self.Message_Receive)

        self.mailList = QListWidget(self.Message_Receive)
        self.mailList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.vbox1.addWidget(self.mailList)

        # 添加加载中提示
        item = QListWidgetItem()  # 创建QListWidgetItem对象
        item.setSizeHint(QSize(670, 635))  # 设置QListWidgetItem大小
        widget = ListFuncLib.createWaitingItem()  # 创建等待中 Widget

        self.mailList.addItem(item)  # 添加item
        self.mailList.setItemWidget(item, widget)  # 为item设置等待中widget
        self.mailList.setEnabled(False)

        self.mailList.itemDoubleClicked.connect(self.showDetailedMail)

        # 右侧过滤器布局
        # 显示过滤器信息
        # 创建过滤器及其窗体信息
        self.FilterFrame = QFrame(self)
        self.FilterFrame.setGeometry(250, 40, 700, 660)
        self.formLayout1 = QFormLayout(self.FilterFrame)

        # 用于过滤器设置界面的字体
        font_filter=QFont()
        font_filter.setFamily('微软雅黑')
        font_filter.setPointSize(10)

        # 用于说明栏的字体
        font_tip = QFont()
        font_tip.setFamily("微软雅黑")
        font_tip.setItalic(True)
        font_tip.setPointSize(11)

        # 用于按钮的字体
        font_button = QFont()
        font_button.setFamily('微软雅黑')
        font_button.setPointSize(10)

        # 设置标签
        self.addresser2 = QLabel(self)
        self.addresser2.setText("发件人")
        self.addresser2.setFont(font_filter)
        self.word_detect = QLabel(self)
        self.word_detect.setText("包含字词")
        self.word_detect.setFont(font_filter)
        self.tip1 = QLabel(self)
        self.tip1.setText("请输入至少一条邮件过滤条目")
        self.tip1.setStyleSheet("text-decoration:underline;")
        self.tip1.setFont(font_tip)
        self.tip2 = QLabel(self)
        self.tip2.setText("请选择此邮件类别")
        self.tip2.setStyleSheet("text-decoration:underline;")
        self.tip2.setFont(font_tip)
        self.linePixmap = QPixmap("./pic/line.png")
        self.deco0 = QLabel(self)
        self.deco0.setPixmap(self.linePixmap)
        self.deco1 = QLabel(self)
        self.deco1.setPixmap(self.linePixmap)

        # 设置文本框
        self.addresser2_text = QLineEdit(self)
        self.word_detect_text = QLineEdit(self)

        # 设置单选按钮
        self.spam_mail_button = QRadioButton("设置为垃圾邮件", self)
        self.normal_mail_button = QRadioButton("设置为为正常邮件", self)
        self.star_mail_button = QRadioButton("标记该类邮件", self)

        self.spam_mail_button.setFont(font_filter)
        self.normal_mail_button.setFont(font_filter)
        self.star_mail_button.setFont(font_filter)

        self.ButtonGroup = QButtonGroup(self)
        self.ButtonGroup.addButton(self.spam_mail_button, 1)
        self.ButtonGroup.addButton(self.normal_mail_button, 2)
        self.ButtonGroup.addButton(self.star_mail_button, 3)

        # 初始化单选按钮结果
        self.info = ""

        # 设置按钮
        self.Filter_create_button = QPushButton("创建过滤规则", self)
        self.Filter_create_button.setFont(font_button)
        self.Filter_create_button.setFixedSize(120, 30)
        self.Filter_create_button.setCursor(QCursor(Qt.PointingHandCursor))
        # 设置按钮样式
        self.Filter_create_button.setStyleSheet("QPushButton{color:white}"
                                                "QPushButton{background-color:rgb(1,114,171)}"
                                                "QPushButton:hover{background-color:rgb(3,96,142)}"
                                                "QPushButton{border:none;}"
                                                "QPushButton{border:2px}"
                                                "QPushButton{border-radius:10px}"
                                                "QPushButton{padding:2px 4px}")

        # 过滤器界面布局
        self.formLayout1.setVerticalSpacing(15)
        self.formLayout1.addRow(self.deco0)
        self.formLayout1.addRow(self.tip1)
        self.formLayout1.addRow(self.addresser2, self.addresser2_text)
        self.formLayout1.addRow(self.word_detect, self.word_detect_text)
        self.formLayout1.addRow(self.deco1)
        self.formLayout1.addRow(self.tip2)
        self.formLayout1.addRow(self.spam_mail_button)
        self.formLayout1.addRow(self.normal_mail_button)
        self.formLayout1.addRow(self.star_mail_button)
        self.formLayout1.addRow(self.Filter_create_button)

        # 设置该窗口初始化时不可见
        self.FilterFrame.setVisible(False)

        # 右侧设置界面布局
        # 显示设置信息
        self.SettingFrame = QFrame(self)
        self.SettingFrame.setGeometry(250, 40, 700, 660)
        self.formLayout2 = QFormLayout(self.SettingFrame)

        # 创建QListWidget以显示信息
        self.listWidget_filter = QListWidget(self.SettingFrame)
        self.listWidget_filter.setGeometry(QRect(0, 250, 700, 370))
        self.listWidget_filter.setStyleSheet("QListWidget{border-top:1px solid gray;}"
                                             "QListWidget{background-color:rgb(255,255,255,100)}")
        self.listWidget_filter.setFont(font_filter)
        self.listWidget_filter.setAttribute(Qt.WA_MacShowFocusRect, 0)

        # 设置该窗口初始化时不可见
        self.SettingFrame.setVisible(False)

        # 2019/9/2 15:20 丁婧伊 设置界面加上过滤强度的选择
        # 获取本地文件存储的过滤强度

        # 字体设置
        font_slider = QFont()
        font_slider.setFamily("微软雅黑")
        font_slider.setPointSize(10)

        # 初始化过滤强度标签
        self.intensity_label = QLabel(self)
        self.intensity_label.setText("设置过滤强度：")
        self.intensity_label.setFont(font_slider)
        self.final_intensity_label = QLabel(self)
        self.final_intensity_label.setText('')
        self.final_intensity_label.setFont(font_slider)

        # 存放滑块的widget
        self.sliderWidget = QWidget(self)
        # sliderWidget中的布局
        self.sliderLayout = QVBoxLayout(self.sliderWidget)
        # 过滤强度滑块，设置滑块的最大最小值
        self.intensity_slider = PaintQSlider(Qt.Horizontal, self.sliderWidget, minimumHeight=90)
        self.sliderLayout.addWidget(self.intensity_slider)
        self.intensity_slider.setMinimum(1)
        self.intensity_slider.setMaximum(100)
        self.formLayout2.addRow(self.sliderWidget)

        # 确定按钮
        self.setting_ok_button = QPushButton(self)
        self.setting_ok_button.setText("保存")
        self.setting_ok_button.setFont(font_slider)
        self.setting_ok_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.setting_ok_button.setFixedSize(100, 30)
        self.setting_ok_button.setStyleSheet("QPushButton{color:white}"
                                             "QPushButton{background-color:rgb(1,114,171)}"
                                             "QPushButton:hover{background-color:rgb(3,96,142)}"
                                             "QPushButton{border:none;}"
                                             "QPushButton{border:2px}"
                                             "QPushButton{border-radius:10px}"
                                             "QPushButton{padding:2px 4px}")

        self.formLayout2.setSpacing(15)
        self.formLayout2.addRow(self.intensity_label, self.final_intensity_label)
        self.formLayout2.addRow(self.intensity_slider)
        self.formLayout2.addRow(self.setting_ok_button)

        # 系统托盘设置
        # 在系统托盘处显示图标
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.logopic)

        # 设置系统托盘图标的菜单
        # 设定显示和退出两个选项
        self.op1 = QAction('&显示(Show)', triggered=self.show)
        self.op2 = QAction('&退出(Exit)', triggered=self.quitApp)

        # 创建菜单并添加选项
        self.trayMenu = QMenu()
        self.trayMenu.addAction(self.op1)
        self.trayMenu.addAction(self.op2)
        self.tray.setContextMenu(self.trayMenu)

        # 设置后台运行时的提示信息
        self.tray.showMessage('圆桌清道夫', '已在后台运行', icon=0)
        # 鼠标双击点击或左键单击点击会唤出主界面
        self.tray.activated.connect(self.act)

    def Shift_Main(self):
        """
        作者：蔡夏菁
        描述：左侧邮件按钮槽函数，用于切换至邮件界面
        """
        self.FilterFrame.setVisible(False)
        self.SettingFrame.setVisible(False)
        self.Message_Receive.setVisible(True)

    def Shift_Filter(self):
        """
        作者：蔡夏菁
        描述：左侧过滤器按钮槽函数，用于切换至过滤器界面
        """
        self.FilterFrame.setVisible(True)
        self.SettingFrame.setVisible(False)
        self.Message_Receive.setVisible(False)

    # 切换至设置界面
    def Shift_Setting(self):
        """
        作者：蔡夏菁
        描述：左侧设置按钮槽函数之一，用于切换至设置界面
        """
        self.FilterFrame.setVisible(False)
        self.SettingFrame.setVisible(True)
        self.Message_Receive.setVisible(False)
        # 将设置界面过滤规则信息清空以便重载
        self.listWidget_filter.clear()

    def quitApp(self):
        """
        作者：蔡夏菁
        描述：右下角托盘菜单退出选项槽函数，用于退出程序
        """
        self.show()
        re = QMessageBox.question(self, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            # 关闭窗体程序
            QCoreApplication.instance().quit()
            # 在应用程序全部关闭后，TrayIcon其实还不会自动消失，
            # 直到你的鼠标移动到上面去后，才会消失，
            # 这是个问题，（如同你terminate一些带TrayIcon的应用程序时出现的状况），
            # 这种问题的解决是通过在程序退出前将其setVisible(False)来完成的。
            self.tray.setVisible(False)

    def act(self, reason):
        """
        作者：蔡夏菁
        描述：右下角图标槽函数，用于显示主界面
        """
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            self.show()

    def mousePressEvent(self, event):
        """
        作者：蔡夏菁，丁婧伊
        描述：重写鼠标点击事件，用于拖拽窗口，可避免事件冲突引起的程序终止
        """
        # 判断点击时鼠标不在控件上
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            # 当前鼠标按下的即是QWidget而非界面上布局的其他控件
            self.isPressedWidget = True

    def mouseMoveEvent(self, QMouseEvent):
        """
        作者：蔡夏菁，丁婧伊
        描述：重写鼠标移动窗口事件，用于拖拽窗口，可避免事件冲突引起的程序终止
        """
        # 当前鼠标按下的是QWidget而非界面上布局的其他控件
        if self.isPressedWidget:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
                QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        """
        作者：蔡夏菁，丁婧伊
        描述：重写鼠标释放事件，用于拖拽窗口，可避免事件冲突引起的程序终止
        """
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.isPressedWidget = False


    def email_receive(self, Msg):
        '''
        作者：何颖智
        描述：收到新的邮件，经过文本处理后触发该函数，该函数获取邮件内容并将它们加入到邮件预览列表中
        '''
        # message[0][0][0][2]为发件人，message[0][0][1]为信件内容，message[0][1]为处理结果
        msg = eval(Msg)
        for message in msg:
            #在此处获取邮件的发送人
            sender=message[0][0][1]
            #在此处获取邮件的主体
            content=message[0][1]
            #获取邮件对应的判断结果
            type=message[1]

            mailInfo = {
                        'sender': sender,
                        'text': content,
                        'type': type
                        }
            print(mailInfo)
            self.mailContent.append(mailInfo)

        # 如果是第一次调用该函数，我们还需要去除等待中提示部件
        if self.mailLoadingState:
            self.mailList.takeItem(0)
            self.mailList.setEnabled(True)
            self.mailLoadingState = False

        self.refreshMailList()  # 更新邮件预览部件

    def refreshMailList(self):
        '''
        作者：何颖智
        描述：该函数将更新邮件预览部件
        '''
        if self.mailWidgetCount < len(self.mailContent):  # 邮件预览部件需要被更新
            for i in range(self.mailWidgetCount, len(self.mailContent)):
                mailInfo = self.mailContent[i]
                item = QListWidgetItem()  # 创建QListWidgetItem对象
                item.setSizeHint(QSize(200, 150))  # 设置QListWidgetItem大小
                widget = ListFuncLib.createSingleItem(mailInfo['sender'], mailInfo['text'], mailInfo['type'])
                self.mailList.insertItem(0, item) # 添加item
                self.mailList.setItemWidget(item, widget)  # 为item设置widget

                self.mailWidgetCount += 1

    def showDetailedMail(self):
        '''
        作者：何颖智
        描述：该函数将创建一个 DetailedMailWin 窗口对象，并将这个窗口显示出来
        '''
        # 找到选中邮件再列表中的下标位置
        index = len(self.mailList) - self.mailList.currentRow() - 1
        emialInfoDic = self.mailContent[index]
        # 创建窗口对象
        self.ui = DetailedMailWin.DetailedMailWin(emialInfoDic)
        self.ui.show()

    def changeThemeWidget(self):
        # 跳转出更换皮肤的Widget
        try:
            self.changeWin.show()
        except:
            traceback.print_exc()

    def changeTheme(self, num):
        # 更换皮肤
        self.palette = QPalette()
        # 文件名
        fileName = ""
        if num == 1:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/mountain.jpg")))
            fileName = "./pic/mountain.jpg"
        elif num == 2:
            # 到底使用哪张作为背景？
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/new8_1.jpg")))
            fileName = "./pic/new8_1.jpg"
        elif num == 3:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/cat.jpg")))
            fileName = "./pic/cat.jpg"
        elif num == 4:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/sandstone.jpg")))
            fileName = "./pic/sandstone.jpg"
        elif num == 5:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/pink.jpg")))
            fileName = "./pic/pink.jpg"
        elif num == 6:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/dandelion.jpg")))
            fileName = "./pic/dandelion.jpg"
        elif num == 7:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/cloud.jpg")))
            fileName = "./pic/cloud.jpg"
        elif num == 8:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/sci_fi.jpg")))
            fileName = "./pic/sci_fi.jpg"
        elif num == 9:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/massEnergy.jpg")))
            fileName = "./pic/massEnergy.jpg"
        elif num == 10:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/earth.jpg")))
            fileName = "./pic/earth.jpg"
        elif num == 11:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/mountainAndCloud.jpg")))
            fileName = "./pic/mountainAndCloud.jpg"
        elif num == 12:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/blue.png")))
            fileName = "./pic/blue.png"
        elif num == 13:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/AvocadoGreen.png")))
            fileName = "./pic/AvocadoGreen.png"
        elif num == 14:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/grey.png")))
            fileName = "./pic/grey.png"
        elif num == 15:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/black.png")))
            fileName = "./pic/black.png"
        elif num == 16:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/orange.png")))
            fileName = "./pic/orange.png"
        elif num == 17:
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/red.png")))
            fileName = "./pic/red.png"
        else:
            # 默认皮肤
            self.palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./pic/mountain.jpg")))
            fileName = "./pic/mountain.jpg"
        self.setPalette(self.palette)
        # 发射信号，将存储在文件中写在mainui中
        try:
            self._themeSignal.emit(fileName)
        except:
            traceback.print_exc()






