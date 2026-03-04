from PyQt5 import QtWidgets
from Interfaces.formCriarConta import Ui_MainWindow
import bcrypt
from base_dados import operacao_DML, ligacao_BD

class formCriarConta(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, login_form=None):
        super().__init__()
        self.setupUi(self)

        #Definir os forms
        # login_form is passed by quem cria o form, evita import circular
        self.form_Login = login_form

        #Definir os botões
        self.pushButton_Criar_Conta.clicked.connect(self.criar_Conta)

    #Métodos
    def mostrar_form_Login(self):
        if self.form_Login:
            self.hide()
            self.form_Login.show()

    def criar_Conta(self):
        username = self.lineEdit_Nome_Utilizador.text()
        email = self.lineEdit_Email.text()
        pw = self.lineEdit_Palavra_Passe.text() #palavra-passe que está na caixa de texto ou atribuir diretamente
        salt = bcrypt.gensalt() #gerar salt
        hash_pw = bcrypt.hashpw(pw.encode('utf-8'), salt) #criar o hash para a palavra-passe
        hash_pw_str = hash_pw.decode('utf-8') #converter hash (bytes) em string
        conn = ligacao_BD()
        try:
            comando_sql = f"INSERT INTO Utilizador(nome, email, password) VALUES ('{username}', '{email}', '{hash_pw_str}')"
            operacao_DML(conn, comando_sql)
            QtWidgets.QMessageBox.information(self,"Sucesso","Conta criada com sucesso!")
            self.mostrar_form_Login()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")
