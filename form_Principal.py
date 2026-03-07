from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Interfaces.formPrincipal import Ui_MainWindow
from form_Utilizadores import formUtilizadores
from form_Lojas import formLojas
from form_Fornecedores import formFornecedores
from form_Entradas_de_Material import formEntradasDeMaterial
from form_Saidas_de_Material import formSaidasDeMaterial
from form_CriarAlterar_Produto import formCriarAlterarProduto
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML

class formPrincipal(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formLogin):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Login = formLogin
        self.form_Utilizadores = formUtilizadores(self)
        self.form_Lojas = formLojas(self)
        self.form_Fornecedores = formFornecedores(self)
        self.form_Entradas_de_Material = formEntradasDeMaterial(self)
        self.form_Saidas_de_Material = formSaidasDeMaterial(self)
        self.form_Criar_Alterar_Produto = formCriarAlterarProduto(self)

        #Definir os botões
        #Pesquisa e Filtros
        self.pushButton_Limpar.clicked.connect(self.LimparFiltro)
        self.pushButton_Pesquisar.clicked.connect(self.ListagemStock)
        self.pushButton_Alterar.clicked.connect(self.alterar)
        self.pushButton_Novo.clicked.connect(self.novo)
        self.pushButton_Desativar.clicked.connect(self.DesativarProduto)

        #Barra de Utilidades
        self.pushButton_Logout.clicked.connect(self.mostrar_form_login)
        self.pushButton_Utilizadores.clicked.connect(self.mostrar_form_Utilizadores)
        self.pushButton_Lojas.clicked.connect(self.mostrar_form_Lojas)
        self.pushButton_Fornercedores.clicked.connect(self.mostrar_form_Fornecedores)
        self.pushButton_Entradas_de_Material.clicked.connect(self.mostrar_form_Entradas_de_Material)
        self.pushButton_Saidas_de_Material.clicked.connect(self.mostrar_form_Saidas_de_Material)
        
    #Métodos
    #Mostrar forms
    def mostrar_form_login(self):
        self.hide()
        self.form_Login.show()
        self.form_Login.lineEdit_Palavra_Passe.setText("")

    def mostrar_form_Utilizadores(self):
        self.hide()
        self.form_Utilizadores.show()
        self.form_Utilizadores.ListagemUtilizadores()

    def mostrar_form_Lojas(self):
        self.hide()
        self.form_Lojas.show()
        self.form_Lojas.ListagemLojas()

    def mostrar_form_Fornecedores(self):
        self.hide()
        self.form_Fornecedores.show()
        self.form_Fornecedores.ListagemFornecedores()
    
    def mostrar_form_Entradas_de_Material(self):
        self.hide()
        self.form_Entradas_de_Material.show()
        self.form_Entradas_de_Material.listagemEncomenda()

    def mostrar_form_Saidas_de_Material(self):
        self.hide()
        self.form_Saidas_de_Material.show()
        self.form_Saidas_de_Material.listagemEncomenda()

    #Pesquisa e Filtros
    def LimparFiltro(self):
        self.lineEdit.setText("") 
        #self.lineEdit.clear()
        self.ListagemStock()

    def ListagemStock(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text()
                if len(filtro) > 0:
                    cmd_sql = f"SELECT Produto.id, Categoria.designacao, Fornecedor.nome, Produto.designacao, Produto.preco, Produto.precoRevenda, Produto.stock FROM Produto, Fornecedor, Categoria WHERE Produto.idCategoria = Categoria.id AND Produto.idFornecedor = Fornecedor.id AND Produto.ativo = 1 AND Produto.designacao LIKE '%{filtro}%' ORDER BY Produto.designacao ASC;"
                    dados = listagem_BD(conn_BD, cmd_sql)
                else:
                    #cmd_sql = "SELECT id, idCategoria, designacao, preco, stock FROM Produto ORDER BY designacao ASC;"
                    cmd_sql = f"SELECT Produto.id, Categoria.designacao, Fornecedor.nome, Produto.designacao, Produto.preco, Produto.precoRevenda, Produto.stock FROM Produto, Fornecedor, Categoria WHERE Produto.idCategoria = Categoria.id AND Produto.idFornecedor = Fornecedor.id AND Produto.ativo = 1 AND Produto.designacao LIKE '%{filtro}%' ORDER BY Produto.designacao ASC;"
                    dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["Id", "Categoria", "Fornecedor", "Designação", "Preço", "Preço de Revenda", "Stock"])
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
        
    #Criar alterar e apagar
    def alterar(self):
        selecao = self.tableView.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "É necessário selecionar o registo a alterar!")
            return
        
        self.hide()
        self.form_Criar_Alterar_Produto.show()
        self.form_Criar_Alterar_Produto.inicializar(selecao, "alterar")

    def novo(self):
        self.hide()
        self.form_Criar_Alterar_Produto.show()
        self.form_Criar_Alterar_Produto.inicializar(None, "novo")

    def DesativarProduto(self):
        selecionados = self.tableView.selectionModel().selectedRows()
        if selecionados:
            linha = selecionados[0].row() # primeira linha selecionada
            modelo = self.tableView.model()
            id_produto = modelo.data(modelo.index(linha, 0)) # Primeiro item da linha (identificador)
            nome_produto = modelo.data(modelo.index(linha, 3))

            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                cmd_sql = "SELECT COUNT(*) FROM DetalheEncomendaArmazem WHERE idProduto = %s;"
                num_registos = consultaUmValor(conn_BD,cmd_sql,(id_produto,))
                if num_registos == 0:
                    # Verificar também nas encomendas de loja
                    cmd_sql = "SELECT COUNT(*) FROM DetalheEncomendaLoja WHERE idProduto = %s;"
                    num_registos = consultaUmValor(conn_BD,cmd_sql,(id_produto,))

                if num_registos == 0:
                    resposta = QtWidgets.QMessageBox.question(
                        self,
                        "Questão",
                        f"Tem certeza de que deseja desativar o produto com identificador {id_produto} e designação '{nome_produto}'?"
                    )
                    if resposta == QtWidgets.QMessageBox.Yes:
                            # Desativar o produto em vez de eliminar
                            cmd_sql = "UPDATE Produto SET ativo = 0 WHERE id = %s;"
                            num_registos= operacao_DML(conn_BD,cmd_sql,(id_produto,))
                            if num_registos > 0: 
                                QtWidgets.QMessageBox.information(self, "Sucesso", "O produto foi desativado com sucesso!")
                                self.ListagemStock()
                            else:
                                QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum registo foi alterado !")
                    else:
                            QtWidgets.QMessageBox.warning(self, "Aviso", "A desativação do produto foi cancelada!")
                else:
                    QtWidgets.QMessageBox.warning(self,"Aviso",f"Não é possível desativar o produto '{nome_produto}' pois ele faz parte de pelo menos uma encomenda.")
        else:
            QtWidgets.QMessageBox.warning(self,"Aviso","É necessário selecionar a linha da tabela que contém o produto a desativar!")