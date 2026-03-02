from PyQt5 import QtWidgets
from Interfaces.formCriarConta import Ui_MainWindow
from form_Principal import formPrincipal

class formCriarConta(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, login_form=None):
        super().__init__()
        self.setupUi(self)

        #Definir os forms
        self.form_Principal = formPrincipal()
        # login_form is passed by quem cria o form, evita import circular
        self.form_Login = login_form

        #Definir os botões
        self.pushButton_Criar_Conta.clicked.connect(self.criar_Conta)

    #Métodos
    def mostrar_form_Login(self):
        if self.form_Login:
            self.hide()
            self.form_Login.show()
        #self.form_Principal.listagemStock()

    def criar_Conta(self):
        print("Criar Conta")