import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from client import User
from handlers import GuiReceiver

t_chat_app = QtWidgets.QApplication(sys.argv)
t_chat_window = uic.loadUi('forms/t_chat_main.ui')


t_chat_window.show()
sys.exit(t_chat_app.exec_())