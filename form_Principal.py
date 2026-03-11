from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Interfaces.formPrincipal import Ui_MainWindow
from form_Utilizadores import formUtilizadores
from form_Lojas import formLojas
from form_Fornecedores import formFornecedores
from form_Entradas_de_Material import formEntradasDeMaterial
from form_Saidas_de_Material import formSaidasDeMaterial
from form_CriarAlterar_Produto import formCriarAlterarProduto
from form_Categorias import formCategorias
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML

class formPrincipal(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formLogin):
        super().__init__()
        self.setupUi(self)
        #Variáveis
        self.email = None
        self.admin = None

        #Definir os forms
        self.form_Login = formLogin
        self.form_Utilizadores = formUtilizadores(self)
        self.form_Lojas = formLojas(self)
        self.form_Fornecedores = formFornecedores(self)
        self.form_Entradas_de_Material = formEntradasDeMaterial(self)
        self.form_Saidas_de_Material = formSaidasDeMaterial(self)
        self.form_Categorias = formCategorias(self)
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
        self.pushButton_Categorias.clicked.connect(self.mostrar_form_Categorias)
        self.pushButton_Entradas_de_Material.clicked.connect(self.mostrar_form_Entradas_de_Material)
        self.pushButton_Saidas_de_Material.clicked.connect(self.mostrar_form_Saidas_de_Material)
        
    #Métodos
    def inicializar(self):
        conn_BD = ligacao_BD()
        if conn_BD and conn_BD != -1:
            #Preencher a comboBox das categorisa
            cmd_sql = "SELECT designacao FROM Categoria WHERE ativo = 1 ORDER BY designacao ASC;"
            dados = listagem_BD(conn_BD, cmd_sql)
            self.comboBox_Categoria.clear()  # Limpa a comboBox antes de a preencher
            self.comboBox_Categoria.addItem("Todas")
            if dados:
                categorias = [str(linha[0]) for linha in dados]
                self.comboBox_Categoria.addItems(categorias)

            #PReencher a comboBox do fornecedotes
            cmd_sql = "SELECT nome FROM Fornecedor WHERE ativo = 1 ORDER BY nome ASC;"
            dados = listagem_BD(conn_BD, cmd_sql)
            self.comboBox_Fornecedor.clear()  # Limpa antes de preencher
            self.comboBox_Fornecedor.addItem("Todos")
            if dados:
                fornecedores = [str(linha[0]) for linha in dados]
                self.comboBox_Fornecedor.addItems(fornecedores)
        self.ListagemStock()
    #Verificar se é admin ou não
    def es_administrador(self):
        try:
            conn_BD = ligacao_BD()
            cmd_sql = "SELECT admin FROM Utilizador WHERE email = %s AND Utilizador.ativo = 1;"
            admin = consultaUmValor(conn_BD, cmd_sql, (self.email,))
            if admin == 1:
                print("O utilizador é administrador.")
                self.admin = True
            else:
                self.admin = False
                print("O utilizador não é administrador.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")
            self.admin = False
            return False

    #Mostrar forms
    def mostrar_form_login(self):
        self.hide()
        self.form_Login.show()
        self.form_Login.lineEdit_Palavra_Passe.setText("")

    def mostrar_form_Utilizadores(self):
        self.hide()
        # comunicar ao formulário de utilizadores se o user corrente é administrador
        self.form_Utilizadores.configurar_permissao(self.admin)
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

    def mostrar_form_Categorias(self):
        self.hide()
        self.form_Categorias.show()
        self.form_Categorias.ListagemCategorias()

    def mostrar_form_Saidas_de_Material(self):
        self.hide()
        self.form_Saidas_de_Material.show()
        self.form_Saidas_de_Material.listagemEncomenda()

    #Pesquisa e Filtros
    def LimparFiltro(self):
        self.lineEdit.setText("")

        # Limpar filtros adicionais
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(True)

        # Usar primeiro item do combobox (deve ser "Todas" / "Todos")
        if self.comboBox_Categoria.count() > 0:
            self.comboBox_Categoria.setCurrentIndex(0)
        if self.comboBox_Fornecedor.count() > 0:
            self.comboBox_Fornecedor.setCurrentIndex(0)

        self.ListagemStock()

    def ListagemStock(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD != -1:
                filtro = self.lineEdit.text().strip()
                categoria = self.comboBox_Categoria.currentText().strip()
                fornecedor = self.comboBox_Fornecedor.currentText().strip()
                em_stock = self.radioButton_3.isChecked()
                fora_stock = self.radioButton_2.isChecked()

                # Construir WHERE com base nos filtros
                where = "Produto.ativo = 1"
                if filtro:
                    where += f" AND Produto.designacao LIKE '%{filtro}%'"
                if categoria and categoria != "Todas":
                    where += f" AND Categoria.designacao = '{categoria}'"
                if fornecedor and fornecedor != "Todos":
                    where += f" AND Fornecedor.nome = '{fornecedor}'"
                if em_stock:
                    where += " AND Produto.stock > 0"
                elif fora_stock:
                    where += " AND Produto.stock = 0"

                cmd_sql = f"SELECT Produto.id, Categoria.designacao, Fornecedor.nome, Produto.designacao, Produto.preco, Produto.precoRevenda, Produto.stock FROM Produto, Fornecedor, Categoria WHERE Produto.idCategoria = Categoria.id AND Produto.idFornecedor = Fornecedor.id AND {where} ORDER BY Produto.designacao ASC;"
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