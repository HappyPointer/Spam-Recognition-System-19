# encoding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DetailedMailWin(QWidget):
    def __init__(self, dic):
        super(DetailedMailWin, self).__init__()
        self.emailInfo = dic
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


if __name__ == "__main__":
    import sys

    dic = eval("{'sender': '10000@qq.com', 'text': '邮箱亲爱的邮箱用户你的邮箱已经成功开通了欢迎你的到来现在你可以开始使"
               "用邮箱了如果这是你第一次使用下面这些指引或许能帮到你别名邮箱你的邮箱可以有不同的名字你可以给你的邮箱设置一个"
               "英文别名它方便记忆且不会透露你的号收取其他邮箱无需东奔西走让所有邮件归于一处如果你有等其他邮箱可以直接搬过来"
               "在我们这里收发邮件移动的邮箱移动的邮箱随时随地常联系你还可以通过手机或平板电脑随时随地访问邮箱', "
               "'type': '星标邮件?'}")

    app = QApplication(sys.argv)
    ui = DetailedMailWin(dic)
    ui.show()
    sys.exit(app.exec_())