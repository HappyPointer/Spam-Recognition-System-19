import sys
import test3
import MainUI0_9
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class LoginUI(QWidget):
    def __init__(self):
        # 初始化————init__
        super().__init__()
        self.initLoginUI()

    def initLoginUI(self):
        # 设置widget组件的大小(w,h)
        self.resize(500, 400)
        # 设置widget大小不可变
        self.setMinimumSize(500, 400)
        self.setMaximumSize(500, 400)
        # 设置widget组件的位置居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # 给widget组件设置标题
        self.setWindowTitle('登录')
        # 隐藏边框
        self.setWindowFlag(Qt.FramelessWindowHint)

        # 设置字体信息
        # 字体一
        font1 = QFont()
        # 字体
        font1.setFamily('微软雅黑')
        # 加粗
        font1.setBold(True)
        # 大小
        font1.setPointSize(20)
        font1.setWeight(75)

        # 字体二
        font2 = QFont()
        # 大小
        font2.setPointSize(15)
        font2.setWeight(75)

        # 背景颜色设置
        self.background1 = QLabel(self)
        self.background1.setGeometry(QRect(0, 0, 500, 200))
        self.background1.setStyleSheet('background-color: rgb(255,71,71)')

        self.background2 = QLabel(self)
        self.background2.setGeometry(QRect(0, 200, 500, 200))
        self.background2.setStyleSheet('background-color: white')

        # 设置关闭按钮
        self.closebtn = QPushButton('×', self)
        self.closebtn.setGeometry(450, 0, 50, 40)
        self.closebtn.setStyleSheet("QPushButton{color:white}"
                                    "QPushButton:hover{color:black}"
                                    "QPushButton{background-color:rgb(255,71,71)}"
                                    "QPushButton{border:none;}")
        self.closebtn.setFont(font2)
        self.closebtn.clicked.connect(QCoreApplication.quit)

        # 设置最小化按钮
        self.minimize = QPushButton('-', self)
        self.minimize.setGeometry(400, 0, 50, 40)
        self.minimize.setStyleSheet("QPushButton{color:white}"
                                    "QPushButton:hover{color:black}"
                                    "QPushButton{background-color:rgb(255,71,71)}"
                                    "QPushButton{border:none;}")
        self.minimize.setFont(font2)
        self.minimize.clicked.connect(self.showMinimized)

        # 设置登录按钮
        self.login = QPushButton('登录', self)
        # 给按钮设置位置(x,y,w,h)
        self.login.setGeometry(150, 350, 200, 30)
        # 设置按钮样式
        self.login.setStyleSheet("QPushButton{color:white}"
                                 "QPushButton:hover{color:black}"
                                 "QPushButton{background-color:rgb(255,71,71)}"
                                 "QPushButton{border:2px}"
                                 "QPushButton{border-radius:10px}"
                                 "QPushButton{padding:2px 4px}")
        # 点击按钮触发事件
        self.login.clicked.connect(self.clickbtn1)

        # 设置标题
        self.title = QLabel(self)
        self.title.setGeometry(QRect(170, 50, 200, 75))
        self.title.setFont(font1)
        self.title.setStyleSheet('color:white')
        self.title.setText('圆桌清道夫')
        self.title.setObjectName('label')

        # 设置账号输入框
        self.account = QLineEdit(self)
        self.account.resize(200, 30)
        self.account.move(150, 230)
        self.account.setPlaceholderText("请输入邮箱账号")
        self.account.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        # 设置密码输入框
        self.password = QLineEdit(self)
        self.password.setContextMenuPolicy(Qt.NoContextMenu)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.resize(200, 30)
        self.password.move(150, 280)
        self.password.setPlaceholderText("请输入授权码")
        self.password.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px")

        # show()方法在屏幕上显示出组件
        self.show()

    # 点击鼠标触发函数
    def clickbtn1(self):
        # 打印出输入框的信息
        textboxValue1 = self.account.text()
        textboxValue2 = self.password.text()
        if textboxValue1 == '' or textboxValue2 == '':
            QMessageBox.question(self, "提示", '请正确输入邮箱账号及授权码', QMessageBox.Ok, QMessageBox.Ok)
        else:
            MessageReturn = test3.logIn(textboxValue1, textboxValue2)
            # 获取返回信息
            QMessageBox.question(self, "提示", MessageReturn[0], QMessageBox.Ok, QMessageBox.Ok)
            if MessageReturn[0]=='登陆成功！':
                test3.getAllMail(MessageReturn[1])
                # 转到主界面
                MainUI.show()
                MainUI.tray.show()
                self.close()


        # 清空输入框信息
        self.account.setText('')
        self.password.setText('')

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


# 主函数
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 关闭所有窗口,也不关闭应用程序
    QApplication.setQuitOnLastWindowClosed(False)
    MainUI = MainUI0_9.MainUI()
    gui = LoginUI()

    sys.exit(app.exec_())
