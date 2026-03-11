from PyQt5 import QtWidgets
import bcrypt
from Interfaces.formCriarAlterarUtilizador import Ui_MainWindow
from base_dados import ligacao_BD, consultaUmValor, operacao_DML
from funcoes_gerais import verificar_tipo_dados


class formCriarAlterarUtilizador(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, formUtilizadores):
        super().__init__()
        self.setupUi(self)
        # modo de funcionamento ("novo" ou "alterar")
        self.modo_funcionamento = None

        # formulário pai para voltar e atualizar
        self.form_Utilizadores = formUtilizadores

        # ligar botões
        self.pushButton_Voltar.clicked.connect(self.voltar)
        self.pushButton_CriarAlterar.clicked.connect(self.gravar)

    def gravar(self):
        if self.modo_funcionamento == "novo":
            try:
                id_val = self.lineEdit_Id.text()
                nome = self.lineEdit_Nome.text()
                email = self.lineEdit_Email.text()
                pw = self.lineEdit_PalavraPasse.text()
                admin = self.checkBox_Admin.isChecked()
                ativo = self.checkBox.isChecked()

                # validações básicas
                if len(id_val) == 0 or len(nome) == 0 or len(email) == 0 or len(pw) == 0:
                    QtWidgets.QMessageBox.critical(self, "Aviso", "Campos por preencher")
                    return

                tipoDados_id = verificar_tipo_dados(id_val)
                if tipoDados_id != "inteiro":
                    QtWidgets.QMessageBox.critical(self, "Aviso", "Inserir valor inteiro no campo id")
                    return

                # encriptar palavra-passe
                salt = bcrypt.gensalt()
                hash_pw = bcrypt.hashpw(pw.encode("utf-8"), salt).decode("utf-8")

                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self, "Erro", "A ligação à BD não está estabelecida")
                    return

                # verificar se id ou email já existem
                cmd_sql = "SELECT COUNT(*) FROM Utilizador WHERE id = %s OR email = %s;"
                numRegistos = consultaUmValor(conn_BD, cmd_sql, (id_val, email,))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Ocorreu um erro ao verificar a existência do utilizador")
                    return
                elif numRegistos > 0:
                    QtWidgets.QMessageBox.critical(self, "Aviso", f"Já existe um utilizador com email {email} ou com id {id_val} introduzidos")
                    return

                cmd_sql = "INSERT INTO Utilizador (id, nome, email, password, admin, ativo) VALUES (%s, %s, %s, %s, %s, %s);"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (id_val, nome, email, hash_pw, admin, ativo))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Ocorreu um erro ao inserir o registo")
                    return

                resposta = QtWidgets.QMessageBox.question(
                    self,
                    "Confirmação",
                    "Utilizador inserido com sucesso!\n Pretende inserir dados de um novo utilizador?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                )
                if resposta == QtWidgets.QMessageBox.Yes:
                    self.inicializar(selecao=None, modo_funcionamento="novo")
                    return
                else:
                    self.voltar()

                conn_BD.close()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erro", f"Erro: {e}")
                return

        elif self.modo_funcionamento == "alterar":
            try:
                id_val = self.lineEdit_Id.text()
                nome = self.lineEdit_Nome.text()
                email = self.lineEdit_Email.text()
                pw = self.lineEdit_PalavraPasse.text()
                admin = self.checkBox_Admin.isChecked()
                ativo = self.checkBox.isChecked()

                if len(nome) == 0 or len(email) == 0:
                    QtWidgets.QMessageBox.critical(self, "Aviso", "Nome e email por preencher")
                    return

                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self, "Erro", "A ligação à BD não está estabelecida")
                    return

                # verificar existencia por id
                cmd_sql = "SELECT COUNT(*) FROM Utilizador WHERE id = %s;"
                numRegistosId = consultaUmValor(conn_BD, cmd_sql, (id_val,))

                # verificar duplicação de email em outro id
                cmd_sql = "SELECT COUNT(*) FROM Utilizador WHERE email = %s AND id <> %s;"
                numRegistosEmail = consultaUmValor(conn_BD, cmd_sql, (email, id_val))

                if numRegistosId == -1 or numRegistosEmail == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Ocorreu um erro ao verificar a existência do utilizador")
                    return
                elif numRegistosId == 0:
                    QtWidgets.QMessageBox.critical(self, "Aviso", f"Não foi possível encontrar o utilizador com identificador {id_val}!")
                    return
                elif numRegistosEmail > 0:
                    QtWidgets.QMessageBox.critical(self, "Aviso", f"Já existe outro utilizador com o email '{email}' introduzido")
                    return

                # apenas atualizar password se o campo não estiver vazio
                if pw:
                    salt = bcrypt.gensalt()
                    hash_pw = bcrypt.hashpw(pw.encode("utf-8"), salt).decode("utf-8")
                    cmd_sql = "UPDATE Utilizador SET nome = %s, email = %s, password = %s, admin = %s, ativo = %s WHERE id = %s;"
                    params = (nome, email, hash_pw, admin, ativo, id_val)
                else:
                    cmd_sql = "UPDATE Utilizador SET nome = %s, email = %s, admin = %s, ativo = %s WHERE id = %s;"
                    params = (nome, email, admin, ativo, id_val)

                numRegistos = operacao_DML(conn_BD, cmd_sql, params)
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Ocorreu um erro ao alterar o registo")
                    return

                QtWidgets.QMessageBox.information(self, "Confirmação", "Utilizador alterado com sucesso!")

                self.close()
                self.form_Utilizadores.show()
                self.form_Utilizadores.ListagemUtilizadores()
                conn_BD.close()

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erro", f"Erro: {e}")
                return

    def inicializar(self, selecao, modo_funcionamento):
        self.modo_funcionamento = modo_funcionamento
        if modo_funcionamento == "novo":
            self.lineEdit_Id.setEnabled(True)
            self.lineEdit_Id.setText("")
            self.lineEdit_Nome.setText("")
            self.lineEdit_Email.setText("")
            self.lineEdit_PalavraPasse.setText("")
            self.checkBox_Admin.setChecked(False)
            self.checkBox.setChecked(True)

            try:
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self, "Erro", "A ligação à BD não está estabelecida")
                    return

                cmd_sql = "SELECT MAX(id)+1 FROM Utilizador;"
                proximo_id = consultaUmValor(conn_BD, cmd_sql)
                if proximo_id == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Ocorreu um erro ao obter o próximo id")
                    return
                self.lineEdit_Id.setText(str(proximo_id))
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erro", f"Ocorreu um erro:{e}")
            finally:
                if conn_BD:
                    conn_BD.close()

        elif modo_funcionamento == "alterar":
            linha = selecao[0].row()
            modelo = self.form_Utilizadores.tableView.model()
            self.lineEdit_Id.setText(modelo.data(modelo.index(linha, 0)))
            self.lineEdit_Nome.setText(modelo.data(modelo.index(linha, 1)))
            self.lineEdit_Email.setText(modelo.data(modelo.index(linha, 2)))
            # admin column is 3
            admin_val = modelo.data(modelo.index(linha, 3))
            self.checkBox_Admin.setChecked(True if admin_val in ("Sim", "1", 1, True) else False)
            self.checkBox.setChecked(True)
            self.lineEdit_PalavraPasse.setText("")
            self.lineEdit_Id.setEnabled(False)

    def voltar(self):
        self.close()
        self.form_Utilizadores.show()
        self.form_Utilizadores.ListagemUtilizadores()
