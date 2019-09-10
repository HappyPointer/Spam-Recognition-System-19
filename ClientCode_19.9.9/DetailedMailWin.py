# encoding=utf-8

# 该 py 文件定义 DetailedMailWin 窗口类，该窗口将用于显示某一封邮件的详情
# 作者：何颖智
# 创建日期：2019-9-5
# 最后修改日期：2019-9-5

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# 显示邮件详情的窗口类，继承了 QWidget 类
class DetailedMailWin(QWidget):
	# 初始化函数
    def __init__(self, dic):
        super(DetailedMailWin, self).__init__()
        self.emailInfo = dic   # 该邮件中包含的所有内容
        self.setObjectName("DetailedMailWindow")
        self.setWindowTitle("邮件详情")
        self.setFixedSize(450, 700)
        logopic = QIcon()
        logopic.addPixmap(QPixmap("./pic/logo.png"))
        self.setWindowIcon(logopic)

        # 窗口主题 layout
        layout_main = QVBoxLayout()

        # 在窗口最上方表明邮件类型使用的字体
        typeFont = QFont()
        typeFont.setFamily('微软雅黑')
        typeFont.setBold(True)
        typeFont.setPointSize(30)
        typeFont.setWeight(75)

        typeLabel = QLabel()  # 在窗口最上方表明邮件类型
        if self.emailInfo['type'] == "垃圾邮件":
            typeLabel.setText('垃圾邮件')
            typeLabel.setFont(typeFont)
            typeLabel.setStyleSheet("color:red;")

        elif self.emailInfo['type'] == "星标邮件":
            typeLabel.setText('星标邮件')
            typeLabel.setFont(typeFont)
            typeLabel.setStyleSheet("color:rgb(255,185,15);")

        elif self.emailInfo['type'] == "正常邮件":
            typeLabel.setText('正常邮件')
            typeLabel.setFont(typeFont)
            typeLabel.setStyleSheet("color:black;")

        else:
            typeLabel.setText('出错了...')
            typeLabel.setFont(typeFont)
            typeLabel.setStyleSheet("color:rgb(105,105,105);")
        layout_main.addWidget(typeLabel)


        # 显示发件人信息一栏使用的字体
        senderFont = QFont()
        senderFont.setFamily('微软雅黑')
        senderFont.setPointSize(15)
        senderFont.setWeight(100)
        # 显示发件人信息
        senderLabel = QLabel()
        senderLabel.setFont(senderFont)
        senderLabel.setText('发件人:\n    ' + self.emailInfo['sender'])
        layout_main.addWidget(senderLabel)


        #  显示邮件正文内容的模块
        textFrame = QFrame()
        textFrame_layout = QVBoxLayout()
        # 用于显示邮件正文内容的文本框
        textBrowser = QTextBrowser()
        textBrowser.setText(self.emailInfo['text'])

        # 文本框上方的文字提示信息
        textTipLabel = QLabel('邮件内容：')
        textFont = QFont()
        textFont.setFamily('微软雅黑')
        textFont.setPointSize(12)
        textFont.setWeight(100)

        textTipLabel.setFont(textFont)

        # 将控件加入到 layout 中
        textFrame_layout.addWidget(textTipLabel)
        textFrame_layout.addWidget(textBrowser)
        textFrame.setLayout(textFrame_layout)

        layout_main.addWidget(textFrame)
        self.setLayout(layout_main)