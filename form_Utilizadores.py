from PyQt5 import QtWidgets
from Interfaces.formUtilizadores import Ui_MainWindow

class formUtilizadores(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal = None):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Principal = formPrincipal
        # Avoid circular import: use the login form instance from formPrincipal if provided
        self.form_Login = formPrincipal.form_Login if formPrincipal is not None else None

        #Definir os botões
        self.pushButton_Voltar.clicked.connect(self.Voltar)
        self.pushButton_Logout.clicked.connect(self.mostrar_form_login)
        
    #Métodos
    def Voltar(self):
        self.close()
        self.form_Principal.show()
        self.form_Principal.ListagemStock()
    
    def mostrar_form_login(self):
        self.hide()
        self.form_Login.show()
        self.form_Login.lineEdit_Palavra_Passe.setText("")

    def ListagemUtilizadores(self):
        pass