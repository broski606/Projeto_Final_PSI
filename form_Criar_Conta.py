from PyQt5 import QtWidgets
from Interfaces.formCriarConta import Ui_MainWindow
from form_Principal import formPrincipal
from form_Login import formLogin

class formCriarConta(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Definir os forms
        self.form_Principal = formPrincipal(self)
        self.form_Login = formLogin(self)

        #Definir os botões
        self.pushButton_Criar_Conta.clicked.connect('''Criar_Conta''')

    #Métodos
    def mostrar_form_Login(self):
        self.hide()
        self.form_Login.show()
        #self.form_Principal.listagemStock()