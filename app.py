from PyQt5 import QtWidgets
import sys
#from form_Principal import formPrincipal
from form_Login_App import formLoginApp

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        janela = formLoginApp()
        #janela = formPrincipal()
        janela.show()
        sys.exit(app.exec_())