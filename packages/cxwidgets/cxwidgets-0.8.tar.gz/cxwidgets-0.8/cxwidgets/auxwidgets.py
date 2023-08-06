# auxiliary widgets common for some programs

from cxwidgets.aQt.QtWidgets import QWidget, QGridLayout, QFrame

# colors from bolkhov's apps
#FFC0CB  - red
#EDED6D  - yellow
#0000FF  - wierd
#4682B4  - old
#B03060  - hardware problem
#8B8B00  - software problem
#FFA500  - changed by other op
#C0E6E6  - data never read
#00FF00  - alarm just gone
#D8E3D5  - was changed programmatically
#404040  - not found


class HLine(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        h = kwargs.get('h', 3)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)
        self.setMidLineWidth(h)


class VLine(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        h = kwargs.get('h', 3)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)
        self.setMidLineWidth(h)


class BaseGridW(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(2, 2, 2, 2)
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(1)
        self.setLayout(self.grid)


class BaseFrameGridW(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(2, 2, 2, 2)
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(1)
        self.setLayout(self.grid)

        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setLineWidth(3)
        self.setMidLineWidth(3)
