from PyQt5 import QtWidgets
from Interfaces.formCategorias import Ui_MainWindow
from form_CriarAlterar_Categoria import formCriarAlterarCategoria
from base_dados import ligacao_BD, listagem_BD, operacao_DML

from PyQt5.QtGui import QStandardItemModel, QStandardItem


class formCategorias(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, formPrincipal):
        super().__init__()
        self.setupUi(self)
        # Definição dos forms
        self.form_Principal = formPrincipal
        self.form_Login = formPrincipal.form_Login if formPrincipal is not None else None
        self.form_Criar_Alterar_Categoria = formCriarAlterarCategoria(self)

        # Definição dos botões
        self.pushButton_Voltar.clicked.connect(self.Voltar)
        self.pushButton_Logout.clicked.connect(self.mostrar_form_login)
        self.pushButton_Desativar.clicked.connect(self.DesativarCategoria)
        self.pushButton_Pesquisar.clicked.connect(self.ListagemCategorias)
        self.pushButton_Limpar.clicked.connect(self.LimparFiltro)
        self.pushButton_Alterar.clicked.connect(self.alterar)
        self.pushButton_Criar.clicked.connect(self.novo)

    # Métodos
    # Mostrar formulários
    def Voltar(self):
        self.close()
        self.form_Principal.show()
        self.form_Principal.inicializar()

    def mostrar_form_login(self):
        self.hide()
        self.form_Login.show()
        self.form_Login.lineEdit_Palavra_Passe.setText("")

    # Pesquisa e filtros
    def LimparFiltro(self):
        self.lineEdit.setText("")
        self.radioButton_2.setChecked(False)  # Inativo
        self.radioButton_3.setChecked(True)  # Ativo
        self.ListagemCategorias()

    def ListagemCategorias(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD != -1:
                filtro = self.lineEdit.text().strip()
                ativo_checked = self.radioButton_3.isChecked()
                inativo_checked = self.radioButton_2.isChecked()

                # montar query conforme opções de filtro
                if filtro and ativo_checked:
                    cmd_sql = (
                        "SELECT id, designacao FROM Categoria "
                        f"WHERE designacao LIKE '%{filtro}%' AND ativo = 1 ORDER BY designacao ASC;"
                    )
                elif filtro and inativo_checked:
                    cmd_sql = (
                        "SELECT id, designacao FROM Categoria "
                        f"WHERE designacao LIKE '%{filtro}%' AND ativo = 0 ORDER BY designacao ASC;"
                    )
                elif ativo_checked:
                    cmd_sql = "SELECT id, designacao FROM Categoria WHERE ativo = 1 ORDER BY designacao ASC;"
                elif inativo_checked:
                    cmd_sql = "SELECT id, designacao FROM Categoria WHERE ativo = 0 ORDER BY designacao ASC;"
                elif filtro:
                    cmd_sql = (
                        "SELECT id, designacao FROM Categoria "
                        f"WHERE designacao LIKE '%{filtro}%' ORDER BY designacao ASC;"
                    )
                else:
                    cmd_sql = "SELECT id, designacao FROM Categoria WHERE ativo = 1 ORDER BY designacao ASC;"

                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["Id", "Designação"])
                for linha in dados:
                    modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                self.tableView.setModel(modelo)

                self.tableView.resizeColumnsToContents()
                self.tableView.verticalHeader().setVisible(False)
                self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                self.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                self.tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Ocorreu um erro:{e}")

    # Criar / Alterar / Desativar
    def alterar(self):
        selecao = self.tableView.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "É necessário selecionar o registo a alterar!")
            return

        self.hide()
        self.form_Criar_Alterar_Categoria.show()
        self.form_Criar_Alterar_Categoria.inicializar(selecao, "alterar")

    def novo(self):
        self.hide()
        self.form_Criar_Alterar_Categoria.show()
        self.form_Criar_Alterar_Categoria.inicializar(None, "novo")

    def DesativarCategoria(self):
        selecionados = self.tableView.selectionModel().selectedRows()
        if selecionados:
            linha = selecionados[0].row()
            modelo = self.tableView.model()
            id_cat = modelo.data(modelo.index(linha, 0))
            design = modelo.data(modelo.index(linha, 1))

            conn_BD = ligacao_BD()
            if conn_BD and conn_BD != -1:
                resposta = QtWidgets.QMessageBox.question(
                    self,
                    "Questão",
                    f"Tem certeza de que deseja desativar a categoria com identificador {id_cat} e designação '{design}'?"
                )
                if resposta == QtWidgets.QMessageBox.Yes:
                    cmd_sql = "UPDATE Categoria SET ativo = 0 WHERE id = %s;"
                    num_registos = operacao_DML(conn_BD, cmd_sql, (id_cat,))
                    if num_registos > 0:
                        QtWidgets.QMessageBox.information(self, "Sucesso", "A categoria foi desativada com sucesso!")
                        self.ListagemCategorias()
                    else:
                        QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum registo foi alterado !")
                else:
                    QtWidgets.QMessageBox.warning(self, "Aviso", "A desativação da categoria foi cancelada!")
        else:
            QtWidgets.QMessageBox.warning(self, "Aviso", "É necessário selecionar a linha da tabela que contém a categoria a desativar!")
