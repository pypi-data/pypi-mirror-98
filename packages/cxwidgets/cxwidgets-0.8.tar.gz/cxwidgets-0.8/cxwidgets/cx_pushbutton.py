from cxwidgets.aQt.QtWidgets import QPushButton
from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
import pycx4.qcda as cda
from .menus.general_cm import CXGeneralCM


class CXPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self._cname = kwargs.get('cname', '')
        self.chan = None
        self.cx_connect()
        self.clicked.connect(self.cs_send)
        self.context_menu = None

    def contextMenuEvent(self, event):
        self.context_menu = CXGeneralCM(self)
        self.context_menu.popup(event.globalPos())

    def cx_connect(self):
        if self._cname == '':
            self.chan = None
            return
        self.chan = cda.IChan(self._cname, private=True, on_update=True)

    @pyqtSlot()
    def cs_send(self):
        if self.chan is None:
            return
        self.chan.setValue(1)

    @pyqtSlot(str)
    def set_cname(self, cname):
        if self._cname == cname:
            return
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = pyqtProperty(str, get_cname, set_cname)



