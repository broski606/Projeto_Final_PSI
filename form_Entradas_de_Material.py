from PyQt5 import QtWidgets, QtCore
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
        self.pushButton_Cancelar.clicked.connect(self.cancelar_encomenda)
        # botão marcar como entregue
        try:
            self.pushButton_Entregue.clicked.connect(self.marcar_entregue)
            self.pushButton_Entregue.setEnabled(False)
        except AttributeError:
            pass
        
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
        self.radioButton.setChecked(True)
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
                    # incluir id para alinhar corretamente as colunas
                    cmd_sql = f"SELECT Produto.id, Produto.Designacao, DetalheEncomendaArmazem.Quantidade, DetalheEncomendaArmazem.precoUnitario, DetalheEncomendaArmazem.precoUnitario * DetalheEncomendaArmazem.Quantidade AS Total FROM DetalheEncomendaArmazem JOIN Produto ON Produto.id = DetalheEncomendaArmazem.idProduto WHERE nEncomendaArmazem = {nEncomendaArmazem} ORDER BY DetalheEncomendaArmazem.idProduto ASC;"
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
                filtro = self.lineEdit.text().strip()
                todos = self.radioButton.isChecked()
                entregues = self.radioButton_3.isChecked()
                por_entregar = self.radioButton_4.isChecked()
                canceladas = self.radioButton_2.isChecked()

                # montar condições
                # mostrar canceladas ou activas conforme checkbox
                if canceladas:
                    wheres = ["EncomendaArmazem.ativo = 0"]
                else:
                    wheres = ["EncomendaArmazem.ativo = 1"]

                if filtro:
                    wheres.append(f"Utilizador.nome LIKE '%{filtro}%'" )
                # entrega só quando não estiver em 'todos'
                if not todos:
                    if entregues and not por_entregar:
                        wheres.append("dataEntrega IS NOT NULL")
                    elif por_entregar and not entregues:
                        wheres.append("dataEntrega IS NULL")

                where_sql = " AND ".join(wheres)
                cmd_sql = f"SELECT nEncomendaArmazem, Utilizador.nome, dataEncomenda, dataEntrega FROM EncomendaArmazem JOIN Utilizador ON EncomendaArmazem.idUtilizador = Utilizador.id WHERE {where_sql} ORDER BY EncomendaArmazem.dataEncomenda DESC;"

                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                self.tableView.verticalHeader().setVisible(False)
                modelo.setHorizontalHeaderLabels(["Nº Encomenda", "Utilizador", "Data Encomenda", "Data Entrega"])
                for linha in dados:
                    modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                self.tableView.setModel(modelo)

                #Chamar a atualização dos detalhes da encomenda
                self.tableView.selectionModel().selectionChanged.connect(self.listagemDetalhesEncomenda)
                # sempre activar/desactivar botão entregue consoante seleção
                self.tableView.selectionModel().selectionChanged.connect(self.atualizar_estado_entrega)
                # atualizar estado imediatamente
                self.atualizar_estado_entrega()

                # ajustar visual da tabela
                self.tableView.resizeColumnsToContents()
                # Selecionar apenas linhas inteiras
                self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                self.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                self.tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

    def atualizar_estado_entrega(self):
        selecionados = self.tableView.selectionModel().selectedRows()
        habilita = False
        if selecionados:
            linha = selecionados[0].row()
            modelo = self.tableView.model()
            n = modelo.data(modelo.index(linha,0))
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD != -1:
                cursor = conn_BD.cursor()
                cursor.execute("SELECT dataEntrega, ativo FROM EncomendaArmazem WHERE nEncomendaArmazem = %s;", (n,))
                row = cursor.fetchone()
                cursor.close()
                if row:
                    dataEntrega, ativo = row
                    habilita = (dataEntrega is None and ativo == 1)
        try:
            self.pushButton_Entregue.setEnabled(habilita)
        except AttributeError:
            pass

    def marcar_entregue(self):
        selecao = self.tableView.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione uma encomenda para marcar como entregue.")
            return
        linha = selecao[0].row()
        modelo = self.tableView.model()
        n_encomenda = modelo.data(modelo.index(linha,0))
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD != -1:
                cursor = conn_BD.cursor()
                cursor.execute("SELECT dataEntrega, ativo FROM EncomendaArmazem WHERE nEncomendaArmazem = %s;", (n_encomenda,))
                row = cursor.fetchone()
                cursor.close()
                if row:
                    dataEntrega, ativo = row
                    if ativo == 0:
                        QtWidgets.QMessageBox.warning(self,"Aviso","Não é possível marcar uma encomenda cancelada como entregue.")
                        return
                    if dataEntrega is not None:
                        QtWidgets.QMessageBox.information(self,"Info","A encomenda já se encontra entregue.")
                        return
                now = QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')
                cmd_sql = "UPDATE EncomendaArmazem SET dataEntrega = %s WHERE nEncomendaArmazem = %s;"
                num = operacao_DML(conn_BD, cmd_sql, (now, n_encomenda))
                if num > 0:
                    # incrementar stock dos produtos da encomenda
                    cursor = conn_BD.cursor()
                    cursor.execute("SELECT idProduto, quantidade FROM DetalheEncomendaArmazem WHERE nEncomendaArmazem = %s;", (n_encomenda,))
                    detalhes = cursor.fetchall()
                    cursor.close()
                    for id_prod, qt in detalhes:
                        operacao_DML(conn_BD, "UPDATE Produto SET stock = stock + %s WHERE id = %s;", (qt, id_prod))
                    QtWidgets.QMessageBox.information(self,"Sucesso","Encomenda marcada como entregue!")
                    self.listagemEncomenda()
                else:
                    QtWidgets.QMessageBox.warning(self,"Aviso","Nenhum registo foi alterado!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro: {e}")

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

    def cancelar_encomenda(self):
        selecao = self.tableView.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione uma encomenda para cancelar.")
            return

        linha = selecao[0].row()
        modelo = self.tableView.model()
        n_encomenda = modelo.data(modelo.index(linha, 0))

        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD != -1:
                # Verificar se a encomenda já foi entregue
                cmd_sql = "SELECT dataEntrega FROM EncomendaArmazem WHERE nEncomendaArmazem = %s;"
                data_entrega = consultaUmValor(conn_BD, cmd_sql, (n_encomenda,))
                if data_entrega is not None:
                    QtWidgets.QMessageBox.warning(self, "Aviso", "Não é possível cancelar uma encomenda já entregue.")
                    return

                resposta = QtWidgets.QMessageBox.question(
                    self,
                    "Questão",
                    f"Tem certeza de que deseja cancelar a encomenda {n_encomenda}?"
                )
                if resposta == QtWidgets.QMessageBox.Yes:
                    cmd_sql = "UPDATE EncomendaArmazem SET ativo = 0 WHERE nEncomendaArmazem = %s;"
                    num_registos = operacao_DML(conn_BD, cmd_sql, (n_encomenda,))
                    if num_registos > 0:
                        QtWidgets.QMessageBox.information(self, "Sucesso", "A encomenda foi cancelada com sucesso!")
                        self.listagemEncomenda()
                    else:
                        QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum registo foi alterado!")
                else:
                    QtWidgets.QMessageBox.warning(self, "Aviso", "O cancelamento da encomenda foi cancelado!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")