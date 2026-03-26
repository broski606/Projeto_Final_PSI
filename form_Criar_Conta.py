from PyQt5 import QtWidgets
from Interfaces.formCriarConta import Ui_MainWindow
import bcrypt
from base_dados import operacao_DML, ligacao_BD

class formCriarConta(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, login_form=None):
        super().__init__()
        self.setupUi(self)
        self.lineEdit_Palavra_Passe.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_Confirmar_Palavra_Passe.setEchoMode(QtWidgets.QLineEdit.Password)

        self.senhas_visiveis = False

        #Definir os forms
        # login_form is passed by quem cria o form, evita import circular
        self.form_Login = login_form

        #Definir os botões
        self.pushButton_Criar_Conta.clicked.connect(self.criar_Conta)
        self.pushButton_Toggle_Palavra_Passe.clicked.connect(self.toggle_password_visibility)

    #Métodos
    def mostrar_form_Login(self):
        if self.form_Login:
            self.hide()
            self.form_Login.show()

    def toggle_password_visibility(self):
        self.senhas_visiveis = not self.senhas_visiveis
        modo = QtWidgets.QLineEdit.Normal if self.senhas_visiveis else QtWidgets.QLineEdit.Password
        self.lineEdit_Palavra_Passe.setEchoMode(modo)
        self.lineEdit_Confirmar_Palavra_Passe.setEchoMode(modo)

    def criar_Conta(self):
        username = self.lineEdit_Nome_Utilizador.text().strip()
        email = self.lineEdit_Email.text().strip()
        pw = self.lineEdit_Palavra_Passe.text()
        pw_confirm = self.lineEdit_Confirmar_Palavra_Passe.text()

        if not username or not email or not pw or not pw_confirm:
            QtWidgets.QMessageBox.warning(self, "Atenção", "Preencha todos os campos obrigatórios.")
            return

        if pw != pw_confirm:
            QtWidgets.QMessageBox.warning(self, "Atenção", "As palavras-passe não coincidem.")
            return

        salt = bcrypt.gensalt()
        hash_pw = bcrypt.hashpw(pw.encode('utf-8'), salt)
        hash_pw_str = hash_pw.decode('utf-8')

        conn = ligacao_BD()
        try:
            comando_sql = f"INSERT INTO Utilizador(nome, email, password) VALUES ('{username}', '{email}', '{hash_pw_str}')"
            operacao_DML(conn, comando_sql)
            QtWidgets.QMessageBox.information(self, "Sucesso", "Conta criada com sucesso!")
            self.mostrar_form_Login()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")

