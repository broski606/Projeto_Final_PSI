from PyQt5 import QtWidgets
from Interfaces.formCriarAlterarCategoria import Ui_MainWindow
from base_dados import ligacao_BD, consultaUmValor, operacao_DML
from funcoes_gerais import verificar_tipo_dados


class formCriarAlterarCategoria(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, formCategorias):
        super().__init__()
        self.setupUi(self)
        # variáveis de controlo
        self.modo_funcionamento = None

        # referir o formulário pai
        self.form_Categorias = formCategorias

        # botões
        self.pushButton_Voltar.clicked.connect(self.voltar)
        self.pushButton_CriarAlterar.clicked.connect(self.gravar)

    def gravar(self):
        if self.modo_funcionamento == "novo":
            try:
                id_val = self.lineEdit_Id.text()
                designacao = self.lineEdit_Id_2.text()
                ativo = self.checkBox.isChecked()

                if len(id_val) == 0 or len(designacao) == 0:
                    QtWidgets.QMessageBox.critical(self, "Aviso", "Campos por preencher")
                    return

                tipoDados_id = verificar_tipo_dados(id_val)
                if tipoDados_id != "inteiro":
                    QtWidgets.QMessageBox.critical(self, "Aviso", "Inserir valor inteiro no campo id")
                    return

                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self, "Erro", "A ligação à BD não está estabelecida")
                    return

                cmd_sql = "SELECT COUNT(*) FROM Categoria WHERE id = %s OR designacao = %s;"
                numRegistos = consultaUmValor(conn_BD, cmd_sql, (id_val, designacao,))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Ocorreu um erro ao verificar a existência da categoria")
                    return
                elif numRegistos > 0:
                    QtWidgets.QMessageBox.critical(self, "Aviso", f"Já existe uma categoria com designação '{designacao}' ou com id {id_val} introduzidos")
                    return

                cmd_sql = "INSERT INTO Categoria (id, designacao, ativo) VALUES (%s, %s, %s);"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (id_val, designacao, ativo))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Ocorreu um erro ao inserir o registo")
                    return

                resposta = QtWidgets.QMessageBox.question(
                    self,
                    "Confirmação",
                    "Categoria inserida com sucesso!\n Pretende inserir dados de uma nova categoria?",
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
                designacao = self.lineEdit_Id_2.text()
                ativo = self.checkBox.isChecked()

                if len(designacao) == 0:
                    QtWidgets.QMessageBox.critical(self, "Aviso", "Designação por preencher")
                    return

                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self, "Erro", "A ligação à BD não está estabelecida")
                    return

                # verificar existência por id
                cmd_sql = "SELECT COUNT(*) FROM Categoria WHERE id = %s;"
                numRegistosId = consultaUmValor(conn_BD, cmd_sql, (id_val,))

                # verificar duplicação de designação em outro id
                cmd_sql = "SELECT COUNT(*) FROM Categoria WHERE designacao = %s AND id <> %s;"
                numRegistosDesign = consultaUmValor(conn_BD, cmd_sql, (designacao, id_val))

                if numRegistosId == -1 or numRegistosDesign == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Ocorreu um erro ao verificar a existência da categoria")
                    return
                elif numRegistosId == 0:
                    QtWidgets.QMessageBox.critical(self, "Aviso", f"Não foi possível encontrar a categoria com identificador {id_val}!")
                    return
                elif numRegistosDesign > 0:
                    QtWidgets.QMessageBox.critical(self, "Aviso", f"Já existe outra categoria com a designação '{designacao}' introduzida")
                    return

                cmd_sql = "UPDATE Categoria SET designacao = %s, ativo = %s WHERE id = %s;"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (designacao, ativo, id_val,))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Ocorreu um erro ao alterar o registo")
                    return

                QtWidgets.QMessageBox.information(self, "Confirmação", "Categoria alterada com sucesso!")

                self.close()
                self.form_Categorias.show()
                self.form_Categorias.ListagemCategorias()
                conn_BD.close()

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erro", f"Erro: {e}")
                return

    def inicializar(self, selecao, modo_funcionamento):
        self.modo_funcionamento = modo_funcionamento
        if modo_funcionamento == "novo":
            self.lineEdit_Id.setEnabled(True)
            self.lineEdit_Id.setText("")
            self.lineEdit_Id_2.setText("")
            self.checkBox.setChecked(True)

            try:
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self, "Erro", "A ligação à BD não está estabelecida")
                    return

                cmd_sql = "SELECT MAX(id)+1 FROM Categoria;"
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
            modelo = self.form_Categorias.tableView.model()
            self.lineEdit_Id.setText(modelo.data(modelo.index(linha, 0)))
            self.lineEdit_Id_2.setText(modelo.data(modelo.index(linha, 1)))
            self.checkBox.setChecked(True)
            self.lineEdit_Id.setEnabled(False)

    def voltar(self):
        self.close()
        self.form_Categorias.show()
        self.form_Categorias.ListagemCategorias()
