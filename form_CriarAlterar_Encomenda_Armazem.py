from PyQt5 import QtWidgets
from Interfaces.formCriarAlterarEncomendaArmazem import Ui_MainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from datetime import date

class formCriarAlterarEncomendaArmazem(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, formPrincipal):
        super().__init__()
        self.setupUi(self)
        # Definição vars
        self.modo_funcionamento = None
        self.form_Principal = formPrincipal
        self.form_Login = formPrincipal.form_Login if formPrincipal is not None else None

        # Carrinho como lista de dicionários: {'idProduto': , 'designacao': , 'quantidade': , 'precoUnitario': }
        self.carrinho = []

        # Definição dos botões
        self.pushButton_Pesquisar.clicked.connect(self.limpar_filtros)
        self.pushButton_Filtrar.clicked.connect(self.pesquisar_produtos)

        # Ajustar textos dos botões
        self.pushButton_Pesquisar.setText("Limpar")
        self.pushButton_Filtrar.setText("Pesquisar")
        self.pushButton_Adicionar.clicked.connect(self.adicionar_ao_carrinho)
        self.pushButton_Remover.clicked.connect(self.remover_do_carrinho)
        self.pushButton_Voltar.clicked.connect(self.voltar)
        self.pushButton_Concluir.clicked.connect(self.gravar)

    def inicializar(self, selecao=None, modo_funcionamento="novo"):
        self.modo_funcionamento = modo_funcionamento
        if modo_funcionamento == "novo":
            self.carrinho = []
            self.atualizar_carrinho()

            conn_BD = ligacao_BD()
            if conn_BD and conn_BD != -1:
                # Preencher comboBox_CategoriaFiltro
                cmd_sql = "SELECT designacao FROM Categoria WHERE ativo = 1 ORDER BY designacao ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                self.comboBox_CategoriaFiltro.clear()
                self.comboBox_CategoriaFiltro.addItem("Todas")
                if dados:
                    categorias = [str(linha[0]) for linha in dados]
                    self.comboBox_CategoriaFiltro.addItems(categorias)

            self.listar_produtos()
        elif modo_funcionamento == "alterar":
            if selecao:
                linha = selecao[0].row()
                modelo = self.form_Principal.tableView.model()
                self.nEncomenda_alterar = modelo.data(modelo.index(linha, 0))

                conn_BD = ligacao_BD()
                if conn_BD and conn_BD != -1:
                    # Preencher comboBox_CategoriaFiltro
                    cmd_sql = "SELECT designacao FROM Categoria WHERE ativo = 1 ORDER BY designacao ASC;"
                    dados = listagem_BD(conn_BD, cmd_sql)
                    self.comboBox_CategoriaFiltro.clear()
                    self.comboBox_CategoriaFiltro.addItem("Todas")
                    if dados:
                        categorias = [str(linha[0]) for linha in dados]
                        self.comboBox_CategoriaFiltro.addItems(categorias)

                    # Carregar detalhes no carrinho
                    cmd_sql = "SELECT idProduto, Produto.designacao, quantidade, precoUnitario FROM DetalheEncomendaArmazem JOIN Produto ON Produto.id = DetalheEncomendaArmazem.idProduto WHERE nEncomendaArmazem = %s;"
                    dados = listagem_BD(conn_BD, cmd_sql, (self.nEncomenda_alterar,))
                    self.carrinho = [{'idProduto': linha[0], 'designacao': linha[1], 'quantidade': linha[2], 'precoUnitario': linha[3]} for linha in dados]
                    self.atualizar_carrinho()
                    self.listar_produtos()

    def listar_produtos(self, filtro_nome="", categoria="Todas"):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD != -1:
                where = "Produto.ativo = 1"
                if filtro_nome:
                    where += f" AND Produto.designacao LIKE '%{filtro_nome}%'"
                if categoria != "Todas":
                    where += f" AND Categoria.designacao = '{categoria}'"

                cmd_sql = f"SELECT Produto.id, Produto.designacao, Categoria.designacao, Fornecedor.nome, Produto.preco FROM Produto, Categoria, Fornecedor WHERE Produto.idCategoria = Categoria.id AND Produto.idFornecedor = Fornecedor.id AND {where} ORDER BY Produto.designacao ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)

                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["ID", "Designação", "Categoria", "Fornecedor", "Preço"])
                for linha in dados:
                    modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                self.tableView_Produtos.setModel(modelo)
                self.tableView_Produtos.resizeColumnsToContents()
                self.tableView_Produtos.verticalHeader().setVisible(False)
                self.tableView_Produtos.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                self.tableView_Produtos.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                self.tableView_Produtos.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")

    def pesquisar_produtos(self):
        filtro = self.lineEdit_Pesquisar.text().strip()
        categoria = self.comboBox_CategoriaFiltro.currentText()
        self.listar_produtos(filtro, categoria)

    def limpar_filtros(self):
        self.lineEdit_Pesquisar.clear()
        if self.comboBox_CategoriaFiltro.count() > 0:
            self.comboBox_CategoriaFiltro.setCurrentIndex(0)
        self.listar_produtos()

    def adicionar_ao_carrinho(self):
        selecao = self.tableView_Produtos.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione um produto para adicionar.")
            return

        quantidade_texto = self.lineEdit_Quantidade.text().strip()
        if not quantidade_texto.isdigit() or int(quantidade_texto) <= 0:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Insira uma quantidade válida.")
            return

        quantidade = int(quantidade_texto)
        linha = selecao[0].row()
        modelo = self.tableView_Produtos.model()
        id_produto = int(modelo.data(modelo.index(linha, 0)))
        designacao = modelo.data(modelo.index(linha, 1))
        preco = float(modelo.data(modelo.index(linha, 4)))

        # Verificar se já está no carrinho
        for item in self.carrinho:
            if item['idProduto'] == id_produto:
                item['quantidade'] += quantidade
                break
        else:
            self.carrinho.append({
                'idProduto': id_produto,
                'designacao': designacao,
                'quantidade': quantidade,
                'precoUnitario': preco
            })

        self.atualizar_carrinho()
        self.lineEdit_Quantidade.clear()

    def atualizar_carrinho(self):
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(["ID Produto", "Designação", "Quantidade", "Preço Unit.", "Total"])
        for item in self.carrinho:
            total = item['quantidade'] * item['precoUnitario']
            modelo.appendRow([
                QStandardItem(str(item['idProduto'])),
                QStandardItem(item['designacao']),
                QStandardItem(str(item['quantidade'])),
                QStandardItem(str(item['precoUnitario'])),
                QStandardItem(str(total))
            ])
        self.tableView_Carrinho.setModel(modelo)
        self.tableView_Carrinho.resizeColumnsToContents()
        self.tableView_Carrinho.verticalHeader().setVisible(False)
        self.tableView_Carrinho.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableView_Carrinho.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.tableView_Carrinho.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)

    def remover_do_carrinho(self):
        selecao = self.tableView_Carrinho.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione um item para remover.")
            return

        linha = selecao[0].row()
        del self.carrinho[linha]
        self.atualizar_carrinho()

    def voltar(self):
        self.close()
        self.form_Principal.show()
        self.form_Principal.listagemEncomenda()

    def gravar(self):
        if self.modo_funcionamento == "novo":
            if not self.carrinho:
                QtWidgets.QMessageBox.warning(self, "Aviso", "O carrinho está vazio.")
                return

            try:
                conn_BD = ligacao_BD()
                if conn_BD and conn_BD != -1:
                    # Obter idUtilizador
                    cmd_sql = "SELECT id FROM Utilizador WHERE email = %s AND ativo = 1;"
                    id_utilizador = consultaUmValor(conn_BD, cmd_sql, (self.form_Principal.form_Principal.email,))

                    if not id_utilizador:
                        QtWidgets.QMessageBox.warning(self, "Aviso", "Não foi possível identificar o utilizador logado; faça logout e volte a entrar.")
                        return

                    # Inserir EncomendaArmazem
                    data_encomenda = date.today()
                    cmd_sql = "INSERT INTO EncomendaArmazem (idUtilizador, dataEncomenda, ativo) VALUES (%s, %s, 1);"
                    operacao_DML(conn_BD, cmd_sql, (id_utilizador, data_encomenda))

                    # Obter nEncomendaArmazem
                    cmd_sql = "SELECT LAST_INSERT_ID();"
                    n_encomenda = consultaUmValor(conn_BD, cmd_sql)

                    # Inserir DetalheEncomendaArmazem
                    for item in self.carrinho:
                        cmd_sql = "INSERT INTO DetalheEncomendaArmazem (nEncomendaArmazem, idProduto, quantidade, precoUnitario) VALUES (%s, %s, %s, %s);"
                        operacao_DML(conn_BD, cmd_sql, (n_encomenda, item['idProduto'], item['quantidade'], item['precoUnitario']))

                    QtWidgets.QMessageBox.information(self, "Sucesso", "Encomenda criada com sucesso!")
                    self.carrinho.clear()
                    self.atualizar_carrinho()
                    self.voltar()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")
        elif self.modo_funcionamento == "alterar":
            if not self.carrinho:
                QtWidgets.QMessageBox.warning(self, "Aviso", "O carrinho está vazio.")
                return

            try:
                conn_BD = ligacao_BD()
                if conn_BD and conn_BD != -1:
                    # Deletar detalhes antigos
                    cmd_sql = "DELETE FROM DetalheEncomendaArmazem WHERE nEncomendaArmazem = %s;"
                    operacao_DML(conn_BD, cmd_sql, (self.nEncomenda_alterar,))

                    # Inserir novos detalhes
                    for item in self.carrinho:
                        cmd_sql = "INSERT INTO DetalheEncomendaArmazem (nEncomendaArmazem, idProduto, quantidade, precoUnitario) VALUES (%s, %s, %s, %s);"
                        operacao_DML(conn_BD, cmd_sql, (self.nEncomenda_alterar, item['idProduto'], item['quantidade'], item['precoUnitario']))

                    QtWidgets.QMessageBox.information(self, "Sucesso", "Encomenda alterada com sucesso!")
                    self.carrinho.clear()
                    self.atualizar_carrinho()
                    self.voltar()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")