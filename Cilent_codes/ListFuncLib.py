import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re

def createSingleItem(sender, text, type):
    # 尽可能的去掉邮件主体内部含有的换行符之类
    text = re.sub('\n', '  ', text)
    text = re.sub('\r', '  ', text)
    text = text.strip()
    if len(text) == 0:
        text = '内容无法显示'

    # 创建 Qwidge 对象，该对象将被返回
    widget = QWidget()

    widget.setObjectName('widget')
    widget.setStyleSheet("QWidget#widget{border-image:url(./pic/ItemBackground.png)}")

    # 总体横向布局
    layout_main = QHBoxLayout()
    map_type = QLabel(widget)  # 组件右侧的图标显示
    map_type.setFixedSize(70, 70)

    if type == "垃圾邮件":
        maps = QPixmap('./pic/spam_icon.png').scaled(70, 70)
    elif type == "星标邮件":
        maps = QPixmap('./pic/star_icon.png').scaled(70, 70)
    elif type == "正常邮件":
        maps = QPixmap('./pic/normal_icon.png').scaled(70, 70)
    else:
        print("Type error!")
        maps = QPixmap('./pic/timeout_icon.png').scaled(70, 70)

    map_type.setPixmap(maps)

    font_microB = QFont()
    font_microB.setFamily('微软雅黑')

    # 右边的纵向布局
    layout_text = QVBoxLayout()
    senderLabel = QLabel("发件人： " + sender)
    senderLabel.setFont(font_microB)
    senderLabel.setFixedSize(400, 50)
    textLabel = QLabel()
    textLabel.setFont(font_microB)
    textLabel.setFixedSize(400, 120)
    textLabel.setAlignment(Qt.AlignTop)
    textLabel.setWordWrap(True)
    elidfont = QFontMetrics(font_microB)
    textLabel.setText(elidfont.elidedText(text, Qt.ElideRight, textLabel.width()*2.7))

    layout_text.addWidget(senderLabel)
    layout_text.addWidget(textLabel)

    # 向总体布局中添加组件
    layout_main.addLayout(layout_text)  # 添加左侧文本 Layout
    layout_main.addWidget(map_type)  # 添加组件右侧的图标

    widget.setLayout(layout_main)  # 将总体布局设置给 wight
    return widget  # 返回 widget