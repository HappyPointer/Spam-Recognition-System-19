import sys
import time
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation
from PyQt5.QtWidgets import QApplication


class PopupWin(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self._init()

    def _init(self):
        # 设置widget大小
        self.resize(450, 200)
        # 隐藏任务栏，去掉边框，顶层显示
        self.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 设置样式表
        self.setStyleSheet("QWidget#widgetTitle {\n"
                           "    background-color: rgb(76, 169, 106);\n"
                           "}\n"
                           "QWidget#widgetBottom {\n"
                           "    border-top-style: solid;\n"
                           "    border-top-width: 2px;\n"
                           "    border-top-color: rgb(185, 218, 201);\n"
                           "}\n"
                           "QLabel#labelTitle {\n"
                           "    color: rgb(255, 255, 255);\n"
                           "}\n"
                           "QLabel#labelContent {\n"
                           "    padding: 5px;\n"
                           "}\n"
                           "QPushButton {\n"
                           "    border: none;\n"
                           "    background: transparent;\n"
                           "}\n"
                           "QPushButton#buttonClose {\n"
                           "    font-family: \"webdings\";\n"
                           "    color: rgb(255, 255, 255);\n"
                           "}\n"
                           "QPushButton#buttonClose:hover {\n"
                           "    background-color: rgb(212, 64, 39);\n"
                           "}\n"
                           "QPushButton#buttonView {\n"
                           "    color: rgb(255, 255, 255);\n"
                           "    border-radius: 5px;\n"
                           "    border: solid 1px rgb(76, 169, 106);\n"
                           "    background-color: rgb(76, 169, 106);\n"
                           "}\n"
                           "QPushButton#buttonView:hover {\n"
                           "    color: rgb(0, 0, 0);\n"
                           "}")
        # 设置横着的布局，总体布局
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        # 设置布局内预留的空白边框宽度
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        # 设置布局内各个空间横向和纵向的间距6px
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        # 标题栏
        self.widgetTitle = QtWidgets.QWidget(self)
        self.widgetTitle.setMinimumSize(QtCore.QSize(0, 26))
        self.widgetTitle.setObjectName("widgetTitle")
        # 竖着的布局
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout(self.widgetTitle)
        # 设置布局内预留的空白边框宽度
        self.horizontalLayout_1.setContentsMargins(10, 0, 0, 0)
        # 设置布局内各个空间横向和纵向的间距0px
        self.horizontalLayout_1.setSpacing(0)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        # 标题栏标签
        self.labelTitle = QtWidgets.QLabel(self.widgetTitle)
        self.labelTitle.setText("新邮件")
        self.labelTitle.setObjectName("labelTitle")
        # 竖着的布局增加标题栏标签
        self.horizontalLayout_1.addWidget(self.labelTitle)
        # 添加空白区宽40px、高20px，宽度尽可能扩大，高度尽可能缩小
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_1.addItem(spacerItem)
        # 关闭按钮
        self.buttonClose = QtWidgets.QPushButton(self.widgetTitle)
        self.buttonClose.setText("r")
        self.buttonClose.setMinimumSize(QtCore.QSize(30, 30))
        self.buttonClose.setMaximumSize(QtCore.QSize(30, 30))
        self.buttonClose.setObjectName("buttonClose")
        # 竖着的布局增加关闭按钮
        self.horizontalLayout_1.addWidget(self.buttonClose)
        # 横着的布局添加竖着的布局的标题栏在上面
        self.verticalLayout.addWidget(self.widgetTitle)
        # 增加放新邮件内容的窗口
        self.mailInfo = QtWidgets.QWidget(self)
        # 430 140
        self.mailInfo.resize(420, 130)
        self.mailInfo.setObjectName("mailInfo")
        # 在邮件内容窗体中添加竖着的布局
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.mailInfo)
        # 设置布局内预留的空白边框宽度
        self.horizontalLayout_2.setContentsMargins(10, 0, 0, 0)
        # 设置布局内各个空间横向和纵向的间距0px
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # 邮件图标（正常邮件，垃圾邮件，星标邮件）
        self.mailPicLabel = QtWidgets.QLabel(self)
        self.mailPicLabel.setMinimumSize(100, 100)
        self.mailPicLabel.setMaximumSize(100, 100)
        # 普通邮件图标
        self.normalPic = QtGui.QPixmap("D:/大学/大三/实训/小组资料/normalMail")
        # 垃圾邮件图标
        self.junkPic = QtGui.QPixmap("D:/大学/大三/实训/小组资料/junkMail.png")
        # 星标邮件图标
        self.starPic = QtGui.QPixmap("D:/大学/大三/实训/小组资料/starMail.png")
        # 默认邮件图标
        self.defaultPic = QtGui.QPixmap("D:/大学/大三/实训/小组资料/defaultMail2.png")
        # 让图片自适应label大小
        self.mailPicLabel.setScaledContents(True)
        self.mailPicLabel.setObjectName("mailPicLabel")
        self.horizontalLayout_2.addWidget(self.mailPicLabel)
        self.mailInfoWidget = QtWidgets.QWidget(self)
        # 添加装载邮件信息的布局
        self.mailInfoLayout = QtWidgets.QVBoxLayout(self.mailInfoWidget)
        # 设置布局内预留的空白边框宽度
        self.mailInfoLayout.setContentsMargins(0, 0, 0, 0)
        # 设置布局内各个空间横向和纵向的间距6px
        self.mailInfoLayout.setSpacing(6)
        self.mailInfoLayout.setObjectName("mailInfoLayout")
        # 主题标签
        self.subject = QtWidgets.QLabel(self)
        self.subject.setText("")
        self.subject.setWordWrap(True)  # 自动换行
        self.subject.setObjectName("subject")
        self.mailInfoLayout.addWidget(self.subject)
        # 发件人标签
        self.sender = QtWidgets.QLabel(self)
        self.sender.setText("")
        self.sender.setWordWrap(True)  # 自动换行
        self.sender.setObjectName("sender")
        self.mailInfoLayout.addWidget(self.sender)
        # 邮件内容标签
        self.body = QtWidgets.QLabel(self)
        self.body.setText("")
        # self.body.setWordWrap(True)  # 自动换行
        self.body.setObjectName("body")
        self.mailInfoLayout.addWidget(self.body)
        self.horizontalLayout_2.addWidget(self.mailInfoWidget)
        self.verticalLayout.addWidget(self.mailInfo)
        self.verticalLayout.setObjectName("verticalLayout")
        # 底部的widget
        self.widgetBottom = QtWidgets.QWidget(self)
        self.widgetBottom.setObjectName("widgetBottom")
        # 底部竖着的布局
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widgetBottom)
        # 设置布局内预留的空白边框宽度
        self.horizontalLayout.setContentsMargins(0, 5, 5, 5)
        # 设置布局内各个空间横向和纵向的间距0px
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # 添加空白区宽170px、高20px，宽度尽可能扩大，高度尽可能缩小
        spacerItem1 = QtWidgets.QSpacerItem(170, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        # 查看按钮
        self.buttonView = QtWidgets.QPushButton(self.widgetBottom)
        self.buttonView.setText("查看")
        self.buttonView.setObjectName("buttonView")
        self.buttonView.setMinimumSize(QtCore.QSize(80, 30))
        # 设置光标（手指）
        self.buttonView.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonView.setObjectName("buttonView")
        self.horizontalLayout.addWidget(self.buttonView)
        self.verticalLayout.addWidget(self.widgetBottom)
        # 两个空间1:1
        self.verticalLayout.setStretch(1, 1)

        # 信号：点击关闭按钮 槽函数：以动画形式关闭窗口
        self.buttonClose.clicked.connect(self.onclose)
        # 鼠标是否在窗口的标志
        self.mouseIsInWidget = False
        # 是否在显示标志
        self.isShow = True
        # 超时标志
        self.isTimeOut = False
        # 页面停留时间是5s(ok)
        self.timeout = 5000
        # 计时器, 计时开始后每1秒进入一次关闭动画的函数
        # 2019/9/6 14:48 debug
        self.timer = QTimer(self, timeout=self.closeAnimation)
        # 获取桌面
        self.deskTop = QApplication.instance().desktop()
        # 获取窗口开始位置
        self.startPos = QPoint(self.deskTop.screenGeometry().width() - self.width() - 5,
                               self.deskTop.screenGeometry().height())
        # 获取窗口弹出结束位置
        self.endPos = QPoint(self.deskTop.screenGeometry().width() - self.width() - 5,
                             self.deskTop.availableGeometry().height() - self.height() - 5)
        # 初始化位置到右下角
        # 2019/9/6 14:42 debug
        self.move(self.startPos)
        # 添加动画（b'pos'是弹出, b'windowOpacity'是渐隐）
        self.animation = QPropertyAnimation(self, b'pos')
        # 2019/9/6 14:46 debug
        self.animation.finished.connect(self.animationEnd)
        # 设置动画持续时间1s
        self.animation.setDuration(1000)

    def onclose(self):
        # 点击关闭按钮时
        self.isShow = False
        # 按下关闭按钮后0.1s启动弹回动画
        QTimer.singleShot(100, self.closeAnimation)

    def show(self, type, subject, sender, body):
        """type： 正常邮件，垃圾邮件，星标邮件"""
        # 停止计时器，防止第二个弹窗弹出时之前的定时器出现问题
        self.timer.stop()
        # 先隐藏
        self.hide()
        # 初始化位置到右下角
        self.move(self.startPos)
        # 调用父类方法
        super(PopupWin, self).show()
        # 根据邮件种类切换图标
        if type == "正常邮件":
            self.mailPicLabel.setPixmap(self.normalPic)
        elif type == "垃圾邮件":
            self.mailPicLabel.setPixmap(self.junkPic)
        elif type == "星标邮件":
            self.mailPicLabel.setPixmap(self.starPic)
        else:
            self.mailPicLabel.setPixmap(self.defaultPic)
        self.subject.setText(subject)
        self.sender.setText(sender)
        # body长度
        try:
            bodyLen = len(body)
            if (bodyLen > 40):
                # 只读取前50个字符, 每20个字符添加一个\n
                bodyStr = body[0: 20] + '\n' + body[20: 40] + '...'
            elif (bodyLen > 20 and bodyLen <= 40):
                bodyStr = body[0: 20] + '\n' + body[20: bodyLen] + '...'
            else:
                bodyStr = body
            self.body.setText(bodyStr)
        except Exception as e:
            traceback.print_exc()
        return self

    def showAnimation(self):
        # 显示动画
        self.isShow = True
        # 先停止之前的动画，重新开始
        self.animation.stop()
        # 设置动画起始和停止的位置
        # 2019/9/6 14:44 debug
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self.endPos)
        # 开始动画
        self.animation.start()
        # 弹出5秒后，如果没有焦点则弹回去
        self.timer.start(self.timeout)

    def closeAnimation(self):
        self.timer.start()
        # 关闭动画
        # 如果鼠标点击了closeButton并停留其上，则执行下面的操作
        if self.isShow:
            # print("没有点击关闭按钮")
            if self.mouseIsInWidget:
                # 如果弹出后倒计时5秒后鼠标还在窗体里，则鼠标移开后后需要主动触发关闭
                self.isTimeOut = True
                return
        # 计时器停止
        self.timer.stop()
        # 不再show
        self.isShow = False
        self.animation.stop()
        # 设置动画起始和停止的位置
        # 2019/9/6 14:43 debug
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self.startPos)
        self.animation.start()
        # 动画结束, 关闭当前窗口并清理
        self.animation.finished.connect(self.animationEnd)

    def animationEnd(self):
        # 动画结束，关闭窗口并清理
        if not self.isShow:
            # 关闭窗口
            self.close()
            # 停止计时器
            self.timer.stop()

    def enterEvent(self, event):
        # 鼠标进入窗口
        super().enterEvent(event)
        self.mouseIsInWidget = True

    def leaveEvent(self, event):
        # 鼠标离开窗口
        super().leaveEvent(event)
        self.mouseIsInWidget = False

