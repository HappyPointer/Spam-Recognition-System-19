import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qtpy import QtCore
import re

import LoginAndGetMail2_3

user_serv=None
user_adress=None

class MainUI(QWidget):



    def __init__(self):
        # 初始化————init__
        super().__init__()
        self.initMainUI()

    def initMainUI(self):
        # 设置widget组件的大小(w,h)
        self.resize(1000, 700)
        # 设置widget大小不可变
        self.setMinimumSize(1000, 700)
        self.setMaximumSize(1000, 700)
        # 设置widget组件的位置居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # 给widget组件设置标题
        self.setWindowTitle('圆桌清道夫')
        # 隐藏边框
        self.setWindowFlag(Qt.FramelessWindowHint)

        #创建子进程


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

        # 左侧布局
        # 左侧按钮栏背景
        self.backgroundLeft = QLabel(self)
        self.backgroundLeft.setGeometry(QRect(0, 0, 250, 700))
        self.backgroundLeft.setStyleSheet('background-color: rgb(1,114,171)')

        # 左侧共三个按钮
        # 消息按钮，初始默认为按下
        self.btnleft_Message = QPushButton(self)
        self.btnleft_Message.setGeometry(0, 100, 250, 75)
        self.btnleft_Message.setText("      邮件")
        self.icon1 = QIcon()
        self.icon1.addPixmap(QPixmap("D:\pic\Message.png"), QIcon.Normal, QIcon.Off)
        self.btnleft_Message.setIcon(self.icon1)
        self.btnleft_Message.setIconSize(QSize(50, 80))
        self.btnleft_Message.setStyleSheet("QPushButton{color:white}"
                                           "QPushButton{background-color:rgb(1,114,171)}"
                                           "QPushButton:hover{background-color:rgb(3,96,142)}"
                                           "QPushButton{border:none;}")
        self.btnleft_Message.setFont(fontleft)
        self.btnleft_Message.clicked.connect(self.Shift_Main)

        # 过滤器按钮，实现过滤器功能
        self.btnleft_Filter = QPushButton(self)
        self.btnleft_Filter.setGeometry(0, 175, 250, 75)
        self.btnleft_Filter.setText("   过滤器")
        self.icon2 = QIcon()
        self.icon2.addPixmap(QPixmap("D:\pic\Filter.png"), QIcon.Normal, QIcon.Off)
        self.btnleft_Filter.setIcon(self.icon2)
        self.btnleft_Filter.setIconSize(QSize(50,80))
        self.btnleft_Filter.setStyleSheet("QPushButton{color:white}"
                                           "QPushButton{background-color:rgb(1,114,171)}"
                                           "QPushButton:hover{background-color:rgb(3,96,142)}"
                                           "QPushButton{border:none;}")
        self.btnleft_Filter.setFont(fontleft)
        self.btnleft_Filter.clicked.connect(self.Shift_Filter)

        # 设置按钮，用于设置界面以及部分功能
        self.btnleft_Setting = QPushButton(self)
        self.btnleft_Setting.setGeometry(0, 250, 250, 75)
        self.btnleft_Setting.setText("      设置")
        self.icon3 = QIcon()
        self.icon3.addPixmap(QPixmap("D:\pic\Setting.png"), QIcon.Normal, QIcon.Off)
        self.btnleft_Setting.setIcon(self.icon3)
        self.btnleft_Setting.setIconSize(QSize(50,80))
        self.btnleft_Setting.setStyleSheet("QPushButton{color:white}"
                                           "QPushButton{background-color:rgb(1,114,171)}"
                                           "QPushButton:hover{background-color:rgb(3,96,142)}"
                                           "QPushButton{border:none;}")
        self.btnleft_Setting.setFont(fontleft)
        self.btnleft_Setting.clicked.connect(self.Shift_Setting)

        # 关于我们，显示项目介绍

        # 可能未来会有更多按钮？

        # 右侧布局
        # 右侧消息框背景
        self.backgroundRight = QLabel(self)
        self.backgroundRight.setGeometry(QRect(250, 0, 750, 700))
        self.backgroundRight.setStyleSheet('background-color: rgb(255, 255, 255)')

        # 设置关闭按钮
        self.closebtn = QPushButton('×', self)
        self.closebtn.setGeometry(950, 0, 50, 40)
        self.closebtn.setStyleSheet("QPushButton{color:black}"
                                    "QPushButton:hover{background-color:rgb(255, 0, 0)}"
                                    "QPushButton:hover{color:white}"
                                    "QPushButton{background-color:rgb(255, 255, 255)}"
                                    "QPushButton{border:none;}")
        self.closebtn.setFont(fontleft)
        self.closebtn.clicked.connect(self.hide)

        # 设置最小化按钮
        self.minimize = QPushButton('-', self)
        self.minimize.setGeometry(900, 0, 50, 40)
        self.minimize.setStyleSheet("QPushButton{color:black}"
                                    "QPushButton:hover{background-color:rgb(225, 225, 225)}"
                                    "QPushButton{background-color:rgb(255, 255, 255)}"
                                    "QPushButton{border:none;}")
        self.minimize.setFont(fontleft)
        self.minimize.clicked.connect(self.showMinimized)

        # 右侧布局一
        # 显示垃圾邮件信息
        # 每接受一条信息就创建一个新的Lable用于显示
        # 创建主界面布局
        self.Message_Receive = QFrame(self)
        self.Message_Receive.setGeometry(250, 40, 700, 660)
        self.vbox1 = QVBoxLayout(self.Message_Receive)
        self.listmodel1 = QStringListModel(self.Message_Receive)
        self.listview1 = QListView(self.Message_Receive)

        # 设置说明栏
        tplt = "{0:{3}^20}\t{1:{3}^20}\t{2:^20}"
        self.item1=[]
        self.item1.append(tplt.format('发件人','主要内容','判断结果',chr(12288)))

        self.listmodel1.setStringList(self.item1)
        self.listview1.setModel(self.listmodel1)
        self.vbox1.addWidget(self.listview1)



        # 右侧布局二
        # 显示过滤器信息
        # 创建过滤器及其窗体信息
        self.FilterFrame = QFrame(self)
        self.FilterFrame.setGeometry(250, 40, 700, 660)
        self.formLayout1 = QFormLayout(self.FilterFrame)

        # 设置标签
        self.addresser2 = QLabel(self)
        self.addresser2.setText("收件人")
        self.word_detect = QLabel(self)
        self.word_detect.setText("包含字词")

        # 设置文本框
        self.addresser2_text = QLineEdit(self)
        self.word_detect_text = QLineEdit(self)

        # 设置单选按钮
        self.spam_mail_button = QRadioButton("设置为垃圾邮件", self)
        self.normal_mail_button = QRadioButton("设置为为正常邮件", self)
        self.star_mail_button = QRadioButton("标记该类邮件", self)

        self.ButtonGroup = QButtonGroup(self)
        self.ButtonGroup.addButton(self.spam_mail_button, 1)
        self.ButtonGroup.addButton(self.normal_mail_button, 2)
        self.ButtonGroup.addButton(self.star_mail_button, 3)

        self.ButtonGroup.buttonClicked.connect(self.BGclicked)

        # 初始化单选按钮结果
        self.info = ""

        # 设置按钮
        self.Filter_create_button = QPushButton("创建过滤器", self)

        # 设置按钮事件
        self.Filter_create_button.clicked.connect(self.Filter_create)

        # 过滤器界面布局
        self.formLayout1.addRow(self.addresser2, self.addresser2_text)
        self.formLayout1.addRow(self.word_detect, self.word_detect_text)
        self.formLayout1.addRow(self.spam_mail_button)
        self.formLayout1.addRow(self.normal_mail_button)
        self.formLayout1.addRow(self.star_mail_button)
        self.formLayout1.addRow(self.Filter_create_button)

        # 设置该窗口初始化时不可见
        self.FilterFrame.setVisible(False)

        # 右侧布局三
        # 显示设置信息
        self.SettingFrame = QFrame(self)
        self.SettingFrame.setGeometry(250, 40, 700, 660)
        self.formLayout2 = QFormLayout(self.SettingFrame)

        # 设置说明栏
        self.Receiving_rules = QLabel(self)
        self.Receiving_rules.setText("        收信规则")
        self.operation = QLabel(self)
        self.operation.setText("                                                   操作")

        # 设置界面布局
        self.formLayout2.addRow(self.Receiving_rules, self.operation)

        # 设置该窗口初始化时不可见
        self.SettingFrame.setVisible(False)

        # 在系统托盘处显示图标
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('d:/pic/SysTray.jpg'))

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

    # 切换至主界面
    def Shift_Main(self):
        self.FilterFrame.setVisible(False)
        self.SettingFrame.setVisible(False)
        self.Message_Receive.setVisible(True)

    # 切换至过滤器界面
    def Shift_Filter(self):
        self.FilterFrame.setVisible(True)
        self.SettingFrame.setVisible(False)
        self.Message_Receive.setVisible(False)

    # 切换至设置界面
    def Shift_Setting(self):
        self.FilterFrame.setVisible(False)
        self.SettingFrame.setVisible(True)
        self.Message_Receive.setVisible(False)
        fliterlist=LoginAndGetMail2_3.showRuleList()
        self.Message_Filter = QLabel(self)
        self.Message_Filter.setText(fliterlist[0])
        self.formLayout2.addRow(self.Message_Filter)


    #创建单选按钮事件
    def BGclicked(self):
        # 读取点击的按钮
        if self.ButtonGroup.checkedId() == 1:
            self.info = '设置为垃圾邮件'
        elif self.ButtonGroup.checkedId() == 2:
            self.info = '设置为正常邮件'
        elif self.ButtonGroup.checkedId() == 3:
            self.info = '设置为星标邮件'
        else:
            self.info = ""

    # 创建过滤器事件
    def Filter_create(self):
        # 读取输入数据
        textboxValue1 = self.addresser2_text.text()
        textboxValue2 = self.word_detect_text.text()
        if textboxValue1 == "" and textboxValue2 == "":
            QMessageBox.question(self, "提示", '输入发件人信息或包含字词信息不能为空', QMessageBox.Ok, QMessageBox.Ok)
        if self.info == "":
            QMessageBox.question(self, "提示", '请选择过滤条件', QMessageBox.Ok, QMessageBox.Ok)
        # 此处应将用户要求交予逻辑程序部分处理

        self.spam_mail_button.setChecked(False)
        self.normal_mail_button.setChecked(False)
        self.star_mail_button.setChecked(False)

    # 退出程序
    def quitApp(self):
        self.show()  # w.hide() #隐藏
        re = QMessageBox.question(self, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            # 关闭窗体程序
            QCoreApplication.instance().quit()
            # 在应用程序全部关闭后，TrayIcon其实还不会自动消失，
            # 直到你的鼠标移动到上面去后，才会消失，
            # 这是个问题，（如同你terminate一些带TrayIcon的应用程序时出现的状况），
            # 这种问题的解决我是通过在程序退出前将其setVisible(False)来完成的。
            self.tray.setVisible(False)

    # 鼠标事件
    def act(self, reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))


    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # message[0][0][0][2]为发件人，message[0][0][1]为信件内容，message[0][1]为处理结果
    def email_receive(self, Msg):
        msg = eval(Msg)
        # print(msg)
        for message in msg:
            # print(message)
            # print(self.item1)
            # self.addresser = ''.join(message[0][0][0][2])
            # self.content = ''.join(message[0][0][1])
            # self.result = ''.join(message[0][1])
            #在此处获取邮件的发送人
            sender=message[0][0][1]
            #在此处获取邮件的主体
            content=message[0][1]
            #尽可能的去掉邮件主体内部含有的换行符之类
            content = re.sub('\n', '', content)
            content = re.sub('\r','',content)
            content = content.strip()
            #在这里获取邮件对应的判断结果
            reslut=message[1]
            #处理邮件内容，截取前三十字
            len_content = len(content)
            if (len_content >= 20):
                content = content[0:20]
                print(content)
            elif len_content==0:
                content='内容无法显示'
            #格式化输出所得到的结果
            tplt = "{0:{3}^30}\t{1:{3}^20}\t{2:{3}^20}"
            # print(tplt.format(sender,content,reslut,chr(12288)))
            #将格式化之后的结果添加到显示列表中
            self.item1.append(tplt.format(sender,content,reslut,chr(12288)))
        #显示显示列表内的内容
        self.listmodel1.setStringList(self.item1)
        self.listview1.setModel(self.listmodel1)







