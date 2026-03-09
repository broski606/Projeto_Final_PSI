from PyQt5 import QtWidgets
from Interfaces.formEntradasDeMaterial import Ui_MainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from form_CriarAlterar_Encomenda_Armazem import formCriarAlterarEncomendaArmazem

class formEntradasDeMaterial(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Principal = formPrincipal
        self.form_Login = formPrincipal.form_Login if formPrincipal is not None else None
        self.form_CriarAlterar_Encomenda_Armazem = formCriarAlterarEncomendaArmazem(self)

        #Definir os botões
        self.pushButton_Voltar.clicked.connect(self.Voltar)
        self.pushButton_Logout.clicked.connect(self.mostrar_form_login)
        self.pushButton_Pesquisar.clicked.connect(self.listagemEncomenda)
        self.pushButton_Limpar.clicked.connect(self.LimparFiltro)
        self.pushButton_Criar.clicked.connect(self.criarEncomenda)
        self.pushButton_Alterar.clicked.connect(self.alterarEncomenda)
        
    #Métodos
    def Voltar(self):
        self.close()
        self.form_Principal.show()
        self.form_Principal.inicializar()
    
    def mostrar_form_login(self):
        self.hide()
        self.form_Login.show()
        self.form_Login.lineEdit_Palavra_Passe.setText("")

    #Listagens e Filtros
    def LimparFiltro(self):
        self.lineEdit.setText("")

        #self.radioButton.setAutoExclusive(False)
        #self.radioButton_2.setAutoExclusive(False)
        #
        #self.radioButton.setChecked(False)
        #self.radioButton_2.setChecked(False)
        #
        #self.radioButton.setAutoExclusive(True)
        #self.radioButton_2.setAutoExclusive(True)

        self.listagemEncomenda()
    
    def listagemDetalhesEncomenda(self, selecao):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                selecao = self.tableView.selectionModel().selectedRows()
                if selecao:
                    linha = selecao[0].row() # primeira linha selecionada
                    modelo = self.tableView.model()
                    nEncomendaArmazem = modelo.data(modelo.index(linha, 0)) # Primeiro item da linha (identificador)
                    cmd_sql = f"SELECT Produto.Designacao, DetalheEncomendaArmazem.Quantidade, DetalheEncomendaArmazem.precoUnitario, DetalheEncomendaArmazem.precoUnitario * DetalheEncomendaArmazem.Quantidade AS Total FROM DetalheEncomendaArmazem JOIN Produto ON Produto.id = DetalheEncomendaArmazem.idProduto WHERE nEncomendaArmazem = {nEncomendaArmazem} ORDER BY DetalheEncomendaArmazem.idProduto ASC;"
                    dados = listagem_BD(conn_BD, cmd_sql)
                    modelo = QStandardItemModel()
                    self.tableView_2.verticalHeader().setVisible(False)
                    modelo.setHorizontalHeaderLabels(["Id. Artigo","Designação", "Quantidade", "Preço Unit.", "Total"])
                    for linha in dados:
                        modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                    self.tableView_2.setModel(modelo)
                    self.tableView_2.resizeColumnsToContents()
                else:
                    return
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

    def listagemEncomenda(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text()
                if len(filtro) > 0:
                    cmd_sql = f"SELECT nEncomendaArmazem, Utilizador.nome, Fornecedor.nome, dataEncomenda, dataEntrega FROM EncomendaArmazem, Utilizador, Fornecedor WHERE EncomendaArmazem.idUtilizador = Utilizador.id AND EncomendaArmazem.idFornecedor = Fornecedor.id AND (Utilizador.nome LIKE '%{filtro}%' OR Fornecedor.nome LIKE '%{filtro}%') AND EncomendaArmazem.ativo = 1 ORDER BY EncomendaArmazem.dataEncomenda DESC;"
                else:
                    cmd_sql = "SELECT nEncomendaArmazem, Utilizador.nome, Fornecedor.nome, dataEncomenda, dataEntrega FROM EncomendaArmazem, Utilizador, Fornecedor WHERE EncomendaArmazem.idUtilizador = Utilizador.id AND EncomendaArmazem.idFornecedor = Fornecedor.id AND EncomendaArmazem.ativo = 1 ORDER BY EncomendaArmazem.dataEncomenda DESC;"
                #if len(filtro) == 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == False: #Cábula: radioButton1 - Entregues e radioButton2 - Por entregar
                #    cmd_sql = f"SELECT encomenda.nEncomendaArmazem, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id ORDER BY encomenda.dataEncomenda DESC;"
                #
                #elif len(filtro) > 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == False:
                #    cmd_sql = f"SELECT encomenda.nEncomendaArmazem, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' ORDER BY encomenda.dataEncomenda DESC;"
                #
                #elif len(filtro) > 0 and self.radioButton.isChecked() == True and self.radioButton_2.isChecked() == False:
                #    cmd_sql = f"SELECT encomenda.nEncomendaArmazem, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' AND encomenda.dataEntrega IS NOT NULL ORDER BY encomenda.dataEncomenda DESC;"
                #
                #elif len(filtro) > 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == True:
                #    cmd_sql = f"SELECT encomenda.nEncomendaArmazem, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' AND encomenda.dataEntrega IS NULL ORDER BY encomenda.dataEncomenda DESC;"
                #
                #elif len(filtro) == 0 and self.radioButton.isChecked() == True and self.radioButton_2.isChecked() == False:
                #    cmd_sql = f"SELECT encomenda.nEncomendaArmazem, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND encomenda.dataEntrega IS NOT NULL ORDER BY encomenda.dataEncomenda DESC;"
                #
                #elif len(filtro) == 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == True:
                #    cmd_sql = f"SELECT encomenda.nEncomendaArmazem, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND encomenda.dataEntrega IS NULL ORDER BY encomenda.dataEncomenda DESC;"
                
                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                self.tableView.verticalHeader().setVisible(False)
                modelo.setHorizontalHeaderLabels(["Nº Encomenda", "Utilizador", "Fornecedor", "Data Encomenda", "Data Entrega"])
                for linha in dados:
                    modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                self.tableView.setModel(modelo)

                #Chamar a atualização dos detalhes da encomenda
                self.tableView.selectionModel().selectionChanged.connect(self.listagemDetalhesEncomenda)
                
                self.tableView.resizeColumnsToContents()
                # Selecionar apenas linhas inteiras
                self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                self.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                self.tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

    def criarEncomenda(self):
        self.hide()
        self.form_CriarAlterar_Encomenda_Armazem.show()
        self.form_CriarAlterar_Encomenda_Armazem.inicializar(None, "novo")

    def alterarEncomenda(self):
        selecao = self.tableView.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione uma encomenda para alterar.")
            return
        self.hide()
        self.form_CriarAlterar_Encomenda_Armazem.show()
        self.form_CriarAlterar_Encomenda_Armazem.inicializar(selecao, "alterar")