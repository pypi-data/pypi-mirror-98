from cxwidgets.aQt.QtWidgets import QProgressBar
from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
import pycx4.qcda as cda
from .menus.general_cm import CXGeneralCM


class CXProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
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
        self.chan = cda.IChan(self._cname, private=True, on_update=True)
        self.chan.valueChanged.connect(self.cs_update)

    def cs_update(self, chan):
        if self.value() != chan.val:
            self.setValue(chan.val)

    @pyqtSlot(str)
    def set_cname(self, cname):
        if self._cname == cname:
            return
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = pyqtProperty(str, get_cname, set_cname)
