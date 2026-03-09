from PyQt5 import QtWidgets
from Interfaces.formLogin import Ui_MainWindow
from form_Principal import formPrincipal
from form_Criar_Conta import formCriarConta
import bcrypt
from base_dados import operacao_DML, listagem_BD, ligacao_BD

class formLoginApp(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #Setar o lineEdit_Palavra_Passe para modo password
        self.lineEdit_Palavra_Passe.setEchoMode(QtWidgets.QLineEdit.Password)

        #Variável usada para passar o email logado para outros forms
        self.email = None

        #Definir os forms
        self.form_Principal = formPrincipal(self, self.email)
        self.form_Criar_Conta = formCriarConta(self)

        #Definir os botões
        self.pushButton_Criar_Conta.clicked.connect(self.mostrar_form_Criar_Conta)
        self.pushButton_Entrar.clicked.connect(self.verificar_login)

    #Métodos
    def mostrar_form_Principal(self):
        self.hide()
        self.form_Principal.show()
        self.form_Principal.inicializar()
    
    def mostrar_form_Criar_Conta(self):
        self.hide()
        self.form_Criar_Conta.show()
        self.form_Criar_Conta.lineEdit_Email.setText("")
        self.form_Criar_Conta.lineEdit_Palavra_Passe.setText("")
        self.form_Criar_Conta.lineEdit_Nome_Utilizador.setText("")

    def verificar_login(self):
        conn = ligacao_BD()
        try:
            email = self.lineEdit_Email.text()
            self.email = email
            cmd_sql = f"SELECT password, nome FROM Utilizador WHERE email = '{email}' AND ativo = 1;"
            dados = listagem_BD(conn, cmd_sql)

            if not dados:
                QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum utilizador está associado a este email!")
                return
            else:
                pw_bd = dados[0][0] #passe encriptada como vem da base de dados
                nome_utilizador = dados[0][1] #nome do utilizador
                pw_inserida = self.lineEdit_Palavra_Passe.text() #palavra-passe inserida pelo utilizador
                # Verificar se a palavra-passe digitada corresponde ao hash armazenado
                if bcrypt.checkpw(pw_inserida.encode('utf-8'), pw_bd.encode('utf-8')):
                    QtWidgets.QMessageBox.information(self, "Info", f"Login bem-sucedido! Bem-vindo, {nome_utilizador}!")
                    self.mostrar_form_Principal()
                else:
                    QtWidgets.QMessageBox.warning(self, "Aviso", "Password incorreta!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")