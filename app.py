from PyQt5 import QtWidgets
import sys
#from form_principal import formPrincipal
from form_Login import formLogin

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        janela = formLogin()
        janela.show()
        sys.exit(app.exec_())