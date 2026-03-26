from PyQt5 import QtWidgets
from Interfaces.formFornecedores import Ui_MainWindow
from form_CriarAlterar_Fornecedor import formCriarAlterarFornecedor
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class formFornecedores(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Principal = formPrincipal
        self.form_Login = formPrincipal.form_Login if formPrincipal is not None else None
        self.form_Criar_Alterar_Fornecedor = formCriarAlterarFornecedor(self)

        #Definir os botões
        self.pushButton_Voltar.clicked.connect(self.Voltar)
        self.pushButton_Logout.clicked.connect(self.mostrar_form_login)
        self.pushButton_Desativar.clicked.connect(self.DesativarFornecedor)
        self.pushButton_Pesquisar.clicked.connect(self.ListagemFornecedores)
        self.pushButton_Limpar.clicked.connect(self.LimparFiltro)
        self.pushButton_Alterar.clicked.connect(self.alterar)
        self.pushButton_Criar.clicked.connect(self.novo)

    #Métodos
    #Mostar Formulários
    def Voltar(self):
        self.close()
        self.form_Principal.show()
        self.form_Principal.inicializar()
    
    def mostrar_form_login(self):
        self.hide()
        self.form_Login.show()
        self.form_Login.lineEdit_Palavra_Passe.setText("")
    
    #Pesquisa e Filtros
    def LimparFiltro(self):
        self.lineEdit.setText("") 
        self.radioButton_2.setChecked(False)  # Inativo
        self.radioButton_3.setChecked(True)  # Ativo
        self.ListagemFornecedores()

    def ListagemFornecedores(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text().strip()
                ativo_checked = self.radioButton_3.isChecked()
                inativo_checked = self.radioButton_2.isChecked()

                # Montar query usando apenas if statements (sem lógica dinâmica complexa)
                if filtro and ativo_checked:
                    cmd_sql = f"SELECT id, nome, nif, morada, telefone, email FROM Fornecedor WHERE (nome LIKE '%{filtro}%' OR email LIKE '%{filtro}%' OR morada LIKE '%{filtro}%' OR nif LIKE '%{filtro}%') AND ativo = 1 ORDER BY nome ASC;"
                elif filtro and inativo_checked:
                    cmd_sql = f"SELECT id, nome, nif, morada, telefone, email FROM Fornecedor WHERE (nome LIKE '%{filtro}%' OR email LIKE '%{filtro}%' OR morada LIKE '%{filtro}%' OR nif LIKE '%{filtro}%') AND ativo = 0 ORDER BY nome ASC;"
                elif ativo_checked:
                    cmd_sql = "SELECT id, nome, nif, morada, telefone, email FROM Fornecedor WHERE ativo = 1 ORDER BY nome ASC;"
                elif inativo_checked:
                    cmd_sql = "SELECT id, nome, nif, morada, telefone, email FROM Fornecedor WHERE ativo = 0 ORDER BY nome ASC;"
                elif filtro:
                    cmd_sql = f"SELECT id, nome, nif, morada, telefone, email FROM Fornecedor WHERE nome LIKE '%{filtro}%' OR email LIKE '%{filtro}%' OR morada LIKE '%{filtro}%' OR nif LIKE '%{filtro}%' ORDER BY nome ASC;"
                else:
                    cmd_sql = "SELECT id, nome, nif, morada, telefone, email FROM Fornecedor WHERE ativo = 1 ORDER BY nome ASC;"

                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["Id", "Nome", "NIF", "Morada", "Telefone", "Email"])
                for linha in dados:
                    modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                self.tableView.setModel(modelo)
                
                self.tableView.resizeColumnsToContents()
                # Selecionar apenas linhas inteiras
                self.tableView.verticalHeader().setVisible(False)
                self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                self.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                self.tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

    # Criar / Alterar / Desativar
    def alterar(self):
        selecao = self.tableView.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "É necessário selecionar o registo a alterar!")
            return

        self.hide()
        self.form_Criar_Alterar_Fornecedor.show()
        self.form_Criar_Alterar_Fornecedor.inicializar(selecao, "alterar")

    def novo(self):
        self.hide()
        self.form_Criar_Alterar_Fornecedor.show()
        self.form_Criar_Alterar_Fornecedor.inicializar(None, "novo")

    def DesativarFornecedor(self):
        selecionados = self.tableView.selectionModel().selectedRows()
        if selecionados:
            linha = selecionados[0].row() # primeira linha selecionada
            modelo = self.tableView.model()
            id_fornecedor = modelo.data(modelo.index(linha, 0)) # Primeiro item da linha (identificador)
            nome_fornecedor = modelo.data(modelo.index(linha, 1))

            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                resposta = QtWidgets.QMessageBox.question(
                    self,
                    "Questão",
                    f"Tem certeza de que deseja desativar o fornecedor com identificador {id_fornecedor} e designação '{nome_fornecedor}'?"
                )
                if resposta == QtWidgets.QMessageBox.Yes:
                        # Desativar o fornecedor em vez de eliminar
                        cmd_sql = "UPDATE Fornecedor SET ativo = 0 WHERE id = %s;"
                        num_registos= operacao_DML(conn_BD,cmd_sql,(id_fornecedor,))
                        if num_registos > 0:
                            QtWidgets.QMessageBox.information(self, "Sucesso", "O fornecedor foi desativado com sucesso!")
                            self.ListagemFornecedores()
                        else:
                            QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum registo foi alterado !")
                else:
                        QtWidgets.QMessageBox.warning(self, "Aviso", "A desativação do fornecedor foi cancelada!")
        else:
            QtWidgets.QMessageBox.warning(self,"Aviso","É necessário selecionar a linha da tabela que contém o fornecedor a desativar!")