from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QSlider, QWidget, QVBoxLayout, QProxyStyle, QStyle,\
    QStyleOptionSlider


class SliderStyle(QProxyStyle):

    def subControlRect(self, control, option, subControl, widget=None):
        rect = super(SliderStyle, self).subControlRect(
            control, option, subControl, widget)
        if subControl == QStyle.SC_SliderHandle:
            if option.orientation == Qt.Horizontal:
                # 高度1/3
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
                # 宽度1/3
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


class PaintQSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super(PaintQSlider, self).__init__(*args, **kwargs)
        # 设置代理样式,主要用于计算和解决鼠标点击区域
        self.setStyle(SliderStyle())

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
            y = self.height() / 2
            painter.drawLine(QPointF(0, y), QPointF(self.width(), y))
        else:
            x = self.width() / 2
            painter.drawLine(QPointF(x, 0), QPointF(x, self.height()))
        # 画圆
        painter.setPen(Qt.NoPen)
        if option.state & QStyle.State_MouseOver:  # 双重圆
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
            if self.orientation() == Qt.Horizontal:  # 在上方绘制文字
                x, y = rect.x(), rect.y() - rect.height() - 2
            else:  # 在左侧绘制文字
                x, y = rect.x() - rect.width() - 2, rect.y()
            painter.drawText(
                x, y, rect.width(), rect.height(),
                Qt.AlignCenter, str(self.value())
            )
        else:  # 实心圆
            r = rect.height() / 2
            painter.setBrush(QColor(5, 110, 150, 255))
            painter.drawRoundedRect(rect, r, r)