from PyQt5 import QtWidgets
from Interfaces.formLojas import Ui_MainWindow
from base_dados import ligacao_BD, listagem_BD, operacao_DML
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class formLojas(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Principal = formPrincipal
        self.form_Login = formPrincipal.form_Login if formPrincipal is not None else None

        #Definir os botões
        self.pushButton_Voltar.clicked.connect(self.Voltar)
        self.pushButton_Logout.clicked.connect(self.mostrar_form_login)
        self.pushButton_Desativar.clicked.connect(self.DesativarLoja)
        self.pushButton_Pesquisar.clicked.connect(self.ListagemLojas)
        self.pushButton_Limpar.clicked.connect(self.LimparFiltro)
        
    #Métodos
    #Mostrar Formulários
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
        #self.lineEdit.clear()
        self.ListagemLojas()

    def ListagemLojas(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text()
                if len(filtro) > 0:
                    cmd_sql = f"SELECT id, nome, nif, morada, email, telefone FROM Loja WHERE nome LIKE '%{filtro}%' OR email LIKE '%{filtro}%' OR morada LIKE '%{filtro}%' OR nif LIKE '%{filtro}%' ORDER BY nome ASC;"
                else:
                    cmd_sql = "SELECT id, nome, nif, morada, email, telefone FROM Loja WHERE ativo = 1 ORDER BY nome ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["id", "nome", "nif", "morada", "email", "telefone"])
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
    
    #Criar(Ainda não é para implementar) alterar(Ainda não é para implementar) e apagar(Implementar já)
    '''def alterar(self):
        selecao = self.tableView.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "É necessário selecionar o registo a alterar!")
            return
        
        self.hide()
        self.form_Criar_Alterar_Produto.show()
        self.form_Criar_Alterar_Produto.inicializar(selecao, "alterar")'''

    '''def novo(self):
        self.hide()
        self.form_Criar_Alterar_Produto.show()
        self.form_Criar_Alterar_Produto.inicializar(None, "novo")'''

    def DesativarLoja(self):
        selecionados = self.tableView.selectionModel().selectedRows()
        if selecionados:
            linha = selecionados[0].row() # primeira linha selecionada
            modelo = self.tableView.model()
            id_loja = modelo.data(modelo.index(linha, 0)) # Primeiro item da linha (identificador)
            nome_loja = modelo.data(modelo.index(linha, 1))

            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                resposta = QtWidgets.QMessageBox.question(
                    self,
                    "Questão",
                    f"Tem certeza de que deseja desativar a loja com identificador {id_loja} e designação '{nome_loja}'?"
                )
                if resposta == QtWidgets.QMessageBox.Yes:
                        # Desativar a loja em vez de eliminar
                        cmd_sql = "UPDATE Loja SET ativo = 0 WHERE id = %s;"
                        num_registos= operacao_DML(conn_BD,cmd_sql,(id_loja,))
                        if num_registos > 0:
                            QtWidgets.QMessageBox.information(self, "Sucesso", "A loja foi desativada com sucesso!")
                            self.ListagemLojas()
                        else:
                            QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum registo foi alterado !")
                else:
                        QtWidgets.QMessageBox.warning(self, "Aviso", "A desativação da loja foi cancelada!")
        else:
            QtWidgets.QMessageBox.warning(self,"Aviso","É necessário selecionar a linha da tabela que contém o loja a desativar!")