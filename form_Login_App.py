from PyQt5 import QtWidgets
from Interfaces.formLogin import Ui_MainWindow
from form_Principal import formPrincipal
from form_Criar_Conta import formCriarConta

class formLoginApp(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Definir os forms
        self.form_Principal = formPrincipal()
        self.form_Criar_Conta = formCriarConta(self)

        #Definir os botões
        self.pushButton_Criar_Conta.clicked.connect(self.mostrar_form_Criar_Conta)
        self.pushButton_Entrar.clicked.connect(self.mostrar_form_Principal)

    #Métodos
    def mostrar_form_Principal(self):
        self.hide()
        self.form_Principal.show()
        self.form_Principal.ListagemStock()
    
    def mostrar_form_Criar_Conta(self):
        self.hide()
        self.form_Criar_Conta.show()