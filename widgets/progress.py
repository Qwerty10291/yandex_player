from PyQt5 import QtWidgets, QtCore, QtGui


class ProgressBar(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.progress = 0

        self.gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0),  QtCore.QPointF(100, 100))
        self.gradient.setColorAt(0, QtGui.QColor(15, 30, 242))
        self.gradient.setColorAt(1, QtGui.QColor(3, 252, 227))
        self.background_brush = QtGui.QBrush(QtGui.QColor(27, 30, 32))
        self.progress_brush = QtGui.QBrush(self.gradient)
        self.slider_brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))

        self.size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(self.size_policy)
        self.setFixedHeight(25)

        self.is_pressed = False
        self.is_moved = True
        self.slot = None
    
    def position_signal(self, func):
        self.slot = func

    def set_progress(self, progress:int):
        self.progress = progress
        self.repaint()
    
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.fillRect(event.rect(), self.background_brush)
        self._draw_progress(event, qp)
        self._draw_slider(event, qp)
    
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.gradient.setFinalStop(self.width(), self.height())
        self.progress_brush = QtGui.QBrush(self.gradient)

    def _draw_progress(self, event:QtGui.QPaintEvent, qp:QtGui.QPainter):
        width = event.rect().width() / 100 * self.progress
        rect = QtCore.QRect(0, 0, width, event.rect().height())
        qp.fillRect(rect, self.progress_brush)
    
    def _draw_slider(self, event,  qp:QtGui.QPainter):
        x = int(event.rect().width() / 100 * self.progress)
        width = int(self.rect().width() / 100)
        rect = QtCore.QRect(x - width, 0, width * 2, event.rect().height())
        qp.fillRect(rect, self.slider_brush)
    
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(a0)
        self.is_pressed = True
        progress = int(a0.x() / self.width() * 100)
        self.mouse_change_progress(progress)
    
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(a0)
        self.is_pressed = False
        if self.is_moved:
            progress = int(a0.x() / self.width() * 100)
            self.mouse_change_progress(progress)
            self.is_moved = False
    
    def mouse_change_progress(self, progress):
        self.set_progress(progress)
        if self.slot:
            self.slot(progress)
    
    
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        super().mouseMoveEvent(a0)
        if self.is_pressed:
            x = a0.x()
            progress = int(x / self.width() * 100)
            self.set_progress(progress)
            self.is_moved = True