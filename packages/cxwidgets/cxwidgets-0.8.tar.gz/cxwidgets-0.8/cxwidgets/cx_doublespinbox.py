from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty, Qt
import pycx4.qcda as cda
from .pdoublespinbox import PDoubleSpinBox
from .menus.doublespinbox_cm import CXDoubleSpinboxCM

class CXDoubleSpinBox(PDoubleSpinBox):
    """Inherit: QDoubleSpinbox -> PDoubleSpinbox -> CXDoubleSpinBox.
       It is a double spinbox connected to CX channel.
       Gives some CX info and widget settings control over context menu.
       CX Channel created with data type corresponding to double.
       CX Channel is privately created in order to avoid any interference.

       When value set - it's send to CX (set considered by done signal of PDoubleSpinbox).
       When CX updates value - it's set to spinbox value.

       attributes:
           cname - cx channel name. When changed

    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()
        self.done.connect(self.cs_send)

    def contextMenuEvent(self, event):
        self.context_menu = CXDoubleSpinboxCM(self)
        self.context_menu.popup(event.globalPos())

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.DChan(self._cname, private=True, get_curval=True)
        self.chan.valueChanged.connect(self.cs_update)

    @pyqtSlot(float)
    def cs_send(self, value):
        if self.chan is None:
            return
        if value == self.chan.val:
            return
        self.chan.setValue(value)

    def cs_update(self, chan):
        if self.value() == chan.val:
            return
        self.setValue(chan.val)

    @pyqtSlot(str)
    def setCname(self, cname):
        if self._cname == cname:
            return
        self._cname = cname
        self.cx_connect()

    def getCname(self):
        return self._cname

    cname = pyqtProperty(str, getCname, setCname)

