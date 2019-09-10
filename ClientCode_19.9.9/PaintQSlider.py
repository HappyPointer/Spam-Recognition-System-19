"""
说明：美化滑动条QSlider，提供蓝色双层圆环样式的滑动条，同时支持美化后的横向和竖向的滑动条
作者：71117205丁婧伊
创建时间：2019/9/9 10:21 pm
最后一次修改时间：2019/9/10 9:00am
"""
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QSlider, QProxyStyle, QStyle, QStyleOptionSlider


# 提供滑动条样式的类
class SliderStyle(QProxyStyle):

    # 重写subControlRect方法，使得滑动条的中间线条变窄
    def subControlRect(self, control, option, subControl, widget=None):
        rect = super(SliderStyle, self).subControlRect(
            control, option, subControl, widget)
        if subControl == QStyle.SC_SliderHandle:
            if option.orientation == Qt.Horizontal:
                # 如果是水平滑块，将高度变为原来的1/3
                radius = int(widget.height() / 3)
                offset = int(radius / 3)
                if option.state & QStyle.State_MouseOver:
                    x = min(rect.x() - offset, widget.width() - radius)
                    x = x if x >= 0 else 0
                else:
                    radius = offset
                    x = min(rect.x(), widget.width() - radius)
                rect = QRect(x, int((rect.height() - radius) / 2),
                             radius, radius)
            else:
                # 如果是竖直滑块，宽度变为原来的1/3
                radius = int(widget.width() / 3)
                offset = int(radius / 3)
                if option.state & QStyle.State_MouseOver:
                    y = min(rect.y() - offset, widget.height() - radius)
                    y = y if y >= 0 else 0
                else:
                    radius = offset
                    y = min(rect.y(), widget.height() - radius)
                rect = QRect(int((rect.width() - radius) / 2),
                             y, radius, radius)
            return rect
        return rect


# 继承滑动条类的自定义滑块类，拥有酷炫的双层圆环样式
class PaintQSlider(QSlider):

    # 构造函数, 使用SliderStyle类提供的样式，滑块条中间的线变窄
    def __init__(self, *args, **kwargs):
        super(PaintQSlider, self).__init__(*args, **kwargs)
        # 设置代理样式,主要用于计算和解决鼠标点击区域
        self.setStyle(SliderStyle())

    # 重写painEvent，为横向和竖向的滑块提供蓝色双层圆环样式
    def paintEvent(self, _):
        option = QStyleOptionSlider()
        self.initStyleOption(option)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 中间圆圈的位置
        rect = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)

        # 画中间蓝色线条
        painter.setPen(QColor(5, 110, 150, 255))
        painter.setBrush(QColor(5, 110, 150, 255))
        if self.orientation() == Qt.Horizontal:
            # 如果是横向的高度减半
            y = self.height() / 2
            painter.drawLine(QPointF(0, y), QPointF(self.width(), y))
        else:
            # 如果是竖向的宽度减半
            x = self.width() / 2
            painter.drawLine(QPointF(x, 0), QPointF(x, self.height()))
        # 画双重圆
        painter.setPen(Qt.NoPen)
        if option.state & QStyle.State_MouseOver:
            # 半透明大圆
            r = rect.height() / 2
            painter.setBrush(QColor(5, 110, 150, 100))
            painter.drawRoundedRect(rect, r, r)
            # 实心小圆(上下左右偏移4)
            rect = rect.adjusted(4, 4, -4, -4)
            r = rect.height() / 2
            painter.setBrush(QColor(5, 110, 150, 255))
            painter.drawRoundedRect(rect, r, r)
            # 绘制文字
            painter.setPen(QColor(5, 110, 150, 255))
            if self.orientation() == Qt.Horizontal:
                # 如果是横向的在上方绘制文字
                x, y = rect.x(), rect.y() - rect.height() - 2
            else:
                # 如果是竖向的在左侧绘制文字
                x, y = rect.x() - rect.width() - 2, rect.y()
            painter.drawText(
                x, y, rect.width(), rect.height(),
                Qt.AlignCenter, str(self.value())
            )
        else:  # 实心圆
            r = rect.height() / 2
            painter.setBrush(QColor(5, 110, 150, 255))
            painter.drawRoundedRect(rect, r, r)