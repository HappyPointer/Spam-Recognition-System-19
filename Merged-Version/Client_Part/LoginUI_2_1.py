import sys
import traceback
from Popup_Win import *
from qtpy import QtCore
from functools import partial

from LoginAndGetMail2_6 import *
import MainUI3_1
from SettingOperations import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class RunThread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    #在这里我新增了三个属性，以后开发会用到
    _signal = pyqtSignal(str)
    _signal1 = pyqtSignal(str)
    my_serv=None
    my_rulelist=[]
    my_mailadress=None
    my_intensity=''

    def __init__(self, parent=None,serv=None,rulelist=[],mailadress=None,intensity=''):
        super(RunThread, self).__init__()
        self.my_serv=serv
        self.my_rulelist=rulelist
        self.my_mailadress=mailadress
        self.my_intensity=intensity

    def __del__(self):
        self.wait()

    def run(self):
        #设置初始列表长度为
        #根据该函数获取邮箱内邮件 并获取邮件对应的判断结果
        print(self.my_intensity)
        response_result_list = checkAndJudgeOldMail(self.my_serv,self.my_intensity,self.my_rulelist)
        #此处会把邮箱内的邮件以及他们的判断结果作为信号发送

        self._signal.emit(str(response_result_list))
        #更新列表长度
        len_list=getMailNum(self.my_serv)
        while True:
            #进入循环，不断接收邮件
            time.sleep(4)
            email_list=getSomeMail(self.my_serv,len_list)
            len_list = getMailNum(self.my_serv)
            if email_list:
                #若果发现邮件列表增长，那么将增长的部分发送至judgenewemail函数进行判断
                response_result_list=judgeNewMail(self.my_intensity,email_list,self.my_rulelist)
                # for i in email_list:
                    # try:
                    #     # win = PopupWin()
                    #     print("win")
                    #     win.show(type=i[1], subject=i[0][0][0], sender=i[0][0][1],
                    #              body=i[0][1]).showAnimation()
                    #     print("win.show")
                    # except Exception as e:
                    #     print(e)
                self._signal1.emit(str(response_result_list))
                # 将邮件主体和判断结果作为信号发送
                self._signal.emit(str(response_result_list))
                #更新列表长度
            else:
                pass

class DeleteButton(QPushButton):

    def setrow(self, row):
        self.row = row


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

        #初始化info
        self.info=''

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
            print('login[[[[[[[[[[[[[[[[[[[[[[[[')
            MessageReturn = logIn(textboxValue1, textboxValue2)
            print(']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
            # 获取返回信息
            QMessageBox.question(self, "提示", MessageReturn[0], QMessageBox.Ok, QMessageBox.Ok)
            if MessageReturn[0]=='登陆成功！':
                temp = Setting_Operations()
                intensity = temp.getIntensity(MessageReturn[2])
                self.user_thread(MessageReturn[1], MessageReturn[2],MainUI,intensity)
                # 转到主界面
                MainUI.show()
                MainUI.tray.show()
                print(555555555555555555555)
                # 设置连接信号槽函数
                MainUI.intensity_slider.valueChanged.connect(self.valueChange)
                MainUI.intensity_slider.sliderMoved.connect(self.valueChange)
                MainUI.setting_ok_button.clicked.connect(self.confirmChange)
                print(66666666666666666666666)
                MainUI.Filter_create_button.clicked.connect(self.Filter_create)
                MainUI.ButtonGroup.buttonClicked.connect(self.BGclicked)
                print(77777777777777777777)
                MainUI.btnleft_Setting.clicked.connect(self.Reload_filter_message)
                print(88888888888888888888)
                # 初始化时从文件中读取用户的过滤强度

                if (intensity == "low"):
                    intensity_chinese = "低强度"
                elif (intensity == "high"):
                    intensity_chinese = "高强度"
                elif (intensity == "medium"):
                    intensity_chinese = "中强度"
                else:
                    intensity_chinese = "默认强度"
                # 初始化过滤强度标签
                MainUI.final_intensity_label.setText(intensity_chinese)
                # 初始化过滤强度滑块位置
                if (intensity_chinese == "低强度"):
                    MainUI.intensity_slider.setValue(15)
                elif (intensity_chinese == "中强度"):
                    MainUI.intensity_slider.setValue(50)
                elif (intensity_chinese == "高强度"):
                    MainUI.intensity_slider.setValue(85)
                else:
                    # 默认强度
                    MainUI.intensity_slider.setValue(50)
                print(999999999999999999999)
                self.setVisible(False)

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

    # 创建线程
    def user_thread(self,serv,mailadress,MainUI,intensity):
        # dic_list = [{'id': 1, 'owner': 'a1', 'sender': '', 'key_word': '才寻鲲', 'type': 'black'}]
        dic={}
        #向服务器请求过滤配置
        print(11111)
        try:
            dic=send_client('request-info',mailadress)
        except:
            traceback.print_exc()
            print('请求用户已有规则失败，网络错误！')
            dic={'content':[]}
        print('2')
        #创建一个新的线程对象
        print(dic['content'])
        self.thread = RunThread(None,serv,dic['content'],mailadress,intensity)
        #将信号的目的地连接至mainUI函数的emailreceive函数
        self.thread._signal.connect(MainUI.email_receive)
        self.thread._signal1.connect(self.popUp)
        #启动该线程
        self.thread.start()

    # 创建过滤器事件
    def Filter_create(self):
        # 读取输入数据
        textboxValue1 = MainUI.addresser2_text.text()
        textboxValue2 = MainUI.word_detect_text.text()
        if textboxValue1 == "" and textboxValue2 == "":
            QMessageBox.question(MainUI, "提示", '输入发件人信息或包含字词信息不能为空', QMessageBox.Ok, QMessageBox.Ok)
        elif self.info == "":
            QMessageBox.question(MainUI, "提示", '请选择过滤条件', QMessageBox.Ok, QMessageBox.Ok)
        else:
            # 此处应将用户要求交予逻辑程序部分处理
            rule_dic_list=[]
            rule_dic={'id':None,'owner':self.thread.my_mailadress,'sender':textboxValue1,'key_word':textboxValue2,'type':self.info}
            rule_dic_list.append(rule_dic)
            try:
                send_client('post',rule_dic_list)
                self.thread.my_rulelist.append(rule_dic)
                QMessageBox.information(MainUI, "提示", '操作成功', QMessageBox.Ok, QMessageBox.Ok)
            except:
                QMessageBox.information(MainUI, "提示", '操作失败', QMessageBox.Ok, QMessageBox.Ok)
                traceback.print_exc()
                pass


        # MainUI.spam_mail_button.setCheckable(False)
        # MainUI.spam_mail_button.setCheckable(True)
        # MainUI.normal_mail_button.setCheckable(False)
        # MainUI.normal_mail_button.setCheckable(True)
        # MainUI.star_mail_button.setCheckable(False)
        # MainUI.star_mail_button.setCheckable(True)
        MainUI.addresser2_text.setText("")
        MainUI.word_detect_text.setText("")

        # 刷新已有过滤器信息操作


    def Reload_filter_message(self):
        # 创建说明栏
        print(456465464654654654654564)
        MainUI.widget_filter = QWidget()
        MainUI.layout_filter = QHBoxLayout()
        MainUI.filter_item = QListWidgetItem()
        MainUI.filter_item.setSizeHint(QSize(670, 40))

        MainUI.filter_rule = QLabel(MainUI)
        MainUI.filter_rule.setText("收信规则")
        MainUI.filter_rule.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        MainUI.filter_operation = QLabel(MainUI)
        MainUI.filter_operation.setText("操作")
        MainUI.filter_operation.setAlignment(Qt.AlignTop | Qt.AlignRight)

        MainUI.layout_filter.addWidget(MainUI.filter_rule)
        MainUI.layout_filter.addWidget(MainUI.filter_operation)
        MainUI.widget_filter.setLayout(MainUI.layout_filter)

        MainUI.listWidget_filter.addItem(MainUI.filter_item)
        MainUI.listWidget_filter.setItemWidget(MainUI.filter_item, MainUI.widget_filter)

        num = -1
        # 循环创建需要添加的过滤规则信息
        MainUI.operationbtn_list = []
        MainUI.argList = []

        for i in self.thread.my_rulelist:

            MainUI.filter_additem = QListWidgetItem()
            MainUI.filter_additem.setSizeHint(QSize(670, 80))

            MainUI.filter_message = QLabel(MainUI)
            rule_str='包含：'
            # rule_str=rule_str+i['key_word']+'，发件人为：'+i['sender']+'时，该邮件会被识别为：'+i['type']

            # 用于过滤规则的字体
            font3 = QFont()
            font3.setFamily('微软雅黑')
            font3.setPointSize(9)
            elidfont = QFontMetrics(font3)
            str_1 = elidfont.elidedText(i['key_word'], Qt.ElideRight, 120)
            str_2 = elidfont.elidedText(i['sender'], Qt.ElideRight, 100)
            rule_str = rule_str + str_1 + '，发件人为：' + str_2 + '时，该邮件会被识别为：' + i['type']

            # elidfont = QFontMetrics(font3)
            # MainUI.filter_message.setText(elidfont.elidedText(rule_str, Qt.ElideRight, MainUI.filter_message.width() * 0.9))
            MainUI.filter_message.setText(rule_str)
            num += 1
            MainUI.operationbtn_list.append(QPushButton('删除', MainUI))
            # opr = MainUI.operationbtn_list[num]
            # opr.setrow(num)
            MainUI.operationbtn_list[num].setFixedSize(32, 25)
            MainUI.operationbtn_list[num].setStyleSheet("QPushButton{color:blue}"
                                     "QPushButton:hover{color:black}"
                                     "QPushButton{background-color:rgb(255,255,255,0)}"
                                     "QPushButton{border:none;}")
            MainUI.operationbtn_list[num].setCursor(QCursor(Qt.PointingHandCursor))
            # MainUI.operation = QPushButton('删除', MainUI)
            # MainUI.operation.setFixedSize(32, 25)
            # MainUI.operation.setStyleSheet("QPushButton{color:blue}"
            #                          "QPushButton:hover{color:black}"
            #                          "QPushButton{background-color:rgb(255,255,255,0)}"
            #                          "QPushButton{border:none;}")
            # MainUI.operation.setCursor(QCursor(Qt.PointingHandCursor))

            MainUI.layout_filter1 = QHBoxLayout()
            MainUI.layout_filter1.addWidget(MainUI.filter_message)
            # MainUI.layout_filter1.addWidget(MainUI.operation)
            MainUI.layout_filter1.addWidget(MainUI.operationbtn_list[num])
            MainUI.widget_filter1 = QWidget()
            MainUI.widget_filter1.setLayout(MainUI.layout_filter1)

            MainUI.listWidget_filter.addItem(MainUI.filter_additem)
            MainUI.listWidget_filter.setItemWidget(MainUI.filter_additem, MainUI.widget_filter1)
            MainUI.operationbtn_list[num].clicked.connect(partial(self.filter_delete,num))
        #     MainUI.argList.append(len(MainUI.argList))
        #     # MainUI.operationbtn_list[num].clicked.connect(lambda: self.filter_delete(MainUI, opr.row))
        #
        # for num in MainUI.argList:
        #     print('num value is : ' + str(num))
        #     MainUI.operationbtn_list[num].clicked.connect(lambda index=num:  self.filter_delete(MainUI, index))

            MainUI.operationbtn_list[num].clicked.connect(self.Reload_filter_message)


        # 删除ListWidget中的某一行

    def filter_delete(self,n):
        # 清空原有的过滤规则信息
        # print(MainUI.listWidget_filter.currentRow())
        rule_list=[]
        print(self.thread.my_rulelist)
        print(n)
        rule_list.append(self.thread.my_rulelist[n])

        send_client('delete',rule_list)
        del self.thread.my_rulelist[n]
        MainUI.listWidget_filter.clear()

    #创建单选按钮事件
    def BGclicked(self):
        # 读取点击的按钮
        if MainUI.ButtonGroup.checkedId() == 1:
            self.info = 'black'
        elif MainUI.ButtonGroup.checkedId() == 2:
            self.info = 'white'
        elif MainUI.ButtonGroup.checkedId() == 3:
            self.info = 'star'
        else:
            self.info = ""

    # 槽函数，确认设置界面中的修改
    def confirmChange(self):
        # 弹窗
        re1 = QMessageBox.question(MainUI, "提示", '确认要修改吗？', QMessageBox.Yes | QMessageBox.No)
        # 确认修改
        if re1 == QMessageBox.Yes:
            # 获取用户设置的强度
            intensity = MainUI.final_intensity_label.text()
            # 修改本地过滤强度
            temp = Setting_Operations()

            result = temp.setIntensity(intensity,self.thread.my_mailadress) # 判断是否修改成功
            if(result):
                self.thread.my_intensity=result
                re2 = QMessageBox.question(MainUI, "提示", "修改成功！", QMessageBox.Yes)
                # 这里向逻辑线程传递改变过滤强度的信息

            else:
                r2 = QMessageBox.question(MainUI, "提示", "修改失败！请重试", QMessageBox.Yes)

    # 槽函数，改变过滤强度标签的值
    def valueChange(self):
        # 获取滑块位置并更改当前过滤强度label
        # 低强度:1-33，中强度:34-66，高强度:67-100
        slider_value = MainUI.intensity_slider.value()
        if (slider_value >= 1 and slider_value <= 33):
            MainUI.final_intensity_label.setText("低强度")
        elif (slider_value >= 34 and slider_value <= 66):
            MainUI.final_intensity_label.setText("中强度")
        else:
            MainUI.final_intensity_label.setText("高强度")

    def popUp(self, Msg):
        # 跳出弹框的槽函数
        email_list=eval(Msg)
        for i in email_list:
            sender=i[0][0][1]
            subject=i[0][0][0]
            body=i[0][1]
            type=i[1]
        print("type:", type)
        win.show(type, subject, sender, body).showAnimation()

    def onView(self):
        # 弹出框中点击‘查看’按钮，显示主页面
        MainUI.show()

if __name__ == '__main__':
# 主函数
    try:
        app = QApplication(sys.argv)
        # 创建PopupWin对象
        # 关闭所有窗口,也不关闭应用程序
        QApplication.setQuitOnLastWindowClosed(False)
        MainUI = MainUI3_1.MainUI()
        print(1)
        gui = LoginUI()
        win = PopupWin()
        win.buttonView.clicked.connect(gui.onView)
        win.buttonView.clicked.connect(MainUI.showNormal)
        sys.exit(app.exec_())
    except Exception as e:
        traceback.print_exc()
    finally:
        gui.thread.my_serv.close()
        gui.thread.my_serv.logout()
        print('成功登出！')

