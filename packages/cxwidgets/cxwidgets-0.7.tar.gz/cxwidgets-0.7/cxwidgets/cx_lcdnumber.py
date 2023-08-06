from cxwidgets.aQt.QtWidgets import QLCDNumber
from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
import pycx4.qcda as cda
from .menus.general_cm import CXGeneralCM


class CXLCDNumber(QLCDNumber):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()

        self.context_menu = None

    def contextMenuEvent(self, event):
        self.context_menu = CXGeneralCM(self)
        self.context_menu.popup(event.globalPos())

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.DChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    def cs_update(self, chan):
        self.display(chan.val)

    @pyqtSlot(float)
    def setCname(self, cname):
        self._cname = cname
        self.cx_connect()

    def getCname(self):
        return self._cname

    cname = pyqtProperty(str, getCname, setCname)
