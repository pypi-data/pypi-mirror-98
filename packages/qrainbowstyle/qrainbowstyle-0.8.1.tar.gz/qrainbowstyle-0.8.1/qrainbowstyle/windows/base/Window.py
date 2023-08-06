import qrainbowstyle
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy, QDialog
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt, QMetaObject, QEvent, QSize, Signal

from .Titlebar import Titlebar


class FramelessWindowBase(QDialog):
    closeClicked = Signal()
    minimizeClicked = Signal()

    def __init__(self, parent):
        super(FramelessWindowBase, self).__init__(parent)
        self.__rect = QApplication.instance().desktop().availableGeometry(self)

        self.__resizingEnabled = True
        self.__contentWidgets = []

        self.setMouseTracking(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setWindowFlags(Qt.Window
                            | Qt.FramelessWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint
                            | Qt.WindowCloseButtonHint)

        self.__centralWidget = QWidget(self)
        self.__centralWidget.setObjectName("centralWidget")
        self.__centralWidget.setContentsMargins(2.5, 2.5, 2.5, 2.5)
        self.__centralWidget.setMouseTracking(True)

        self.__centralLayout = QVBoxLayout(self.__centralWidget)
        self.__centralLayout.setAlignment(Qt.AlignBottom)
        self.__centralLayout.setSpacing(3)
        self.__centralLayout.setContentsMargins(0, 0, 0, 0)

        self.__bar = Titlebar(self)
        self.__bar.showRestoreButton(False)
        self.__bar.showMinimizeButton(False)
        self.__bar.showMaximizeButton(False)
        self.__centralLayout.addWidget(self.__bar)
        self.__centralLayout.setAlignment(self.__bar, Qt.AlignVCenter)

        self.__centralLayout.addSpacing(3)

        self.__contentWidget = QWidget(self)
        self.__contentWidget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding)
        self.__contentWidget.setContentsMargins(0, 0, 0, 0)
        self.__contentWidgetLayout = QVBoxLayout(self.__contentWidget)
        self.__contentWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.__centralLayout.addWidget(self.__contentWidget)

        self.__centralWidget.setLayout(self.__centralLayout)
        self.__contentWidget.setAutoFillBackground(True)

        self.__bar.minimizeClicked.connect(self.minimizeClicked.emit)
        self.__bar.closeClicked.connect(self.closeClicked.emit)
        self.closeClicked.connect(self.close)

        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__main_layout)
        self.__main_layout.addWidget(self.__centralWidget)

        QMetaObject.connectSlotsByName(self)
        self.showSizeControl(True)
        self.resize(QSize(self.__rect.width() / 2, self.__rect.height() / 2))

    def showWindowShadow(self, value: bool):
        pass

    def setEdgeSnapping(self, value: bool):
        pass

    def showBordersOnMaximize(self, value: bool):
        pass

    def setResizingEnabled(self, value: bool):
        """Enable window resizing

        Args:
            value (bool): Enable or disable window resizing
        """
        self.__resizingEnabled = value

    def addMenu(self, menu):
        self.__bar.addMenu(menu)

    def titlebar(self):
        return self.__bar

    def showSizeControl(self, value: bool):
        self.__bar.showMaximizeButton(value)
        self.__bar.showMinimizeButton(value)

    def isResizingEnabled(self) -> bool:
        """Return if window allows resizing

        Returns:
            value (bool): Window allow resizing.
        """
        return self.__resizingEnabled

    def setTitlebarHeight(self, height: int):
        """Set titlebar height.

        Args:
            height (int): Titlebar height.
        """
        self.__bar.setTitlebarHeight(height)

    def addContentWidget(self, widget: QWidget):
        """Add master widget to window.

        Args:
            widget (QWidget): Content widget.
        """
        self.__contentWidgets.append(widget)
        self.__contentWidgetLayout.addWidget(widget)

    def insertContentWidget(self, index, widget: QWidget):
        """Insert master widget to window at pos.

        Args:
            index (int): Index
            widget (QWidget): Content widget.
        """
        self.__contentWidgets.insert(index, widget)
        self.__contentWidgetLayout.insertWidget(index, widget)

    def setWindowIcon(self, icon: QIcon) -> None:
        self.__bar.setWindowIcon(icon)
        super().setWindowIcon(icon)

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() == Qt.WindowMaximized:
                self.__bar.showRestoreButton(True)
                if not qrainbowstyle.USE_DARWIN_BUTTONS:
                    self.__bar.showMaximizeButton(False)

            elif self.windowState() == Qt.WindowNoState:
                self.__bar.showRestoreButton(False)
                self.__bar.showMaximizeButton(True)
        return super().changeEvent(event)
