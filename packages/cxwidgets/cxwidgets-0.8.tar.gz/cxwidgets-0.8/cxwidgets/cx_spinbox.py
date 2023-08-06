from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
import pycx4.qcda as cda
from .pspinbox import PSpinBox
from .menus.spinbox_cm import CXSpinboxCM


class CXSpinBox(PSpinBox):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._cname = kwargs.get('cname', None)
        self.chan = None

        self.cx_connect()
        self.done.connect(self.cs_send)
        self.context_menu = None

        self._hardmin = 0
        self._hardmax = 0

    def contextMenuEvent(self, event):
        self.context_menu = CXSpinboxCM(self)
        self.context_menu.popup(event.globalPos())

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.IChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    @pyqtSlot(int)
    def cs_send(self, value):
        if self.chan is None:
            return
        if int(value) == self.chan.val:
            return
        self.chan.setValue(value)

    def cs_update(self, chan):
        if int(self.value()) == chan.val:
            return
        self.setValue(chan.val)
        if chan.rflags != 0:
            print(chan.rflags_text())
            pass

    @pyqtSlot(str)
    def set_cname(self, cname):
        if self._cname == cname:
            return
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = pyqtProperty(str, get_cname, set_cname)

    @pyqtSlot(int)
    def set_hardmin(self, value):
        self._hardmin = value

    def get_hardmin(self):
        return self._hardmin

    hardmin = pyqtProperty(int, get_hardmin, set_hardmin)

    @pyqtSlot(int)
    def set_hardmax(self, value):
        self._hardmax = value

    def get_hardmax(self):
        return self._hardmax

    hardmax = pyqtProperty(int, get_hardmax, set_hardmax)