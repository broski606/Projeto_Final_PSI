from PyQt5 import QtWidgets, QtCore
from Interfaces.formSaidasDeMaterial import Ui_MainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML

class formSaidasDeMaterial(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Principal = formPrincipal
        self.form_Login = formPrincipal.form_Login if formPrincipal is not None else None
        
        #Definir os forms
        from form_CriarAlterar_Encomenda_Loja import formCriarAlterarEncomendaLoja
        self.form_CriarAlterar_Encomenda_Loja = formCriarAlterarEncomendaLoja(self)

        #Definir os botões
        self.pushButton_Voltar.clicked.connect(self.Voltar)
        self.pushButton_Logout.clicked.connect(self.mostrar_form_login)
        self.pushButton_Limpar.clicked.connect(self.LimparFiltro)
        self.pushButton_Pesquisar.clicked.connect(self.listagemEncomenda)
        self.pushButton_Criar.clicked.connect(self.criarEncomenda)
        self.pushButton_Alterar.clicked.connect(self.alterarEncomenda)
        # adicionar botão cancelar caso exista
        try:
            self.pushButton_Cancelar.clicked.connect(self.cancelar_encomenda)
        except Exception:
            pass
        # botão entregar
        try:
            self.pushButton_Entregue.clicked.connect(self.marcar_entregue)
            self.pushButton_Entregue.setEnabled(False)
        except Exception:
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

    #Listagem e filtros
    def LimparFiltro(self):
        self.lineEdit.setText("")
        try:
            self.radioButton.setChecked(True)
        except Exception:
            pass
        # other radios will be ignored since todos selected
        self.listagemEncomenda()
    
    def listagemEncomenda(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text().strip()
                todos = getattr(self, 'radioButton', None) and self.radioButton.isChecked()
                entregues = getattr(self, 'radioButton_3', None) and self.radioButton_3.isChecked()
                por_entregar = getattr(self, 'radioButton_4', None) and self.radioButton_4.isChecked()
                canceladas = getattr(self, 'radioButton_2', None) and self.radioButton_2.isChecked()

                # montar condições
                if canceladas:
                    wheres = ["EncomendaLoja.ativo = 0"]
                else:
                    wheres = ["EncomendaLoja.ativo = 1"]

                if filtro:
                    wheres.append(f"(Utilizador.nome LIKE '%{filtro}%' OR Loja.nome LIKE '%{filtro}%')")
                if not todos:
                    if entregues and not por_entregar:
                        wheres.append("dataEntrega IS NOT NULL")
                    elif por_entregar and not entregues:
                        wheres.append("dataEntrega IS NULL")

                where_sql = " AND ".join(wheres)
                cmd_sql = f"SELECT nEncomendaLoja, Utilizador.nome, Loja.nome, dataEncomenda, dataEntrega FROM EncomendaLoja JOIN Utilizador ON EncomendaLoja.idUtilizador = Utilizador.id JOIN Loja ON EncomendaLoja.idLoja = Loja.id WHERE {where_sql} ORDER BY EncomendaLoja.dataEncomenda DESC;"
                #if len(filtro) == 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == False: #Cábula: radioButton1 - Entregues e radioButton2 - Por entregar
                #    cmd_sql = f"SELECT encomenda.nEncomendaLoja, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id ORDER BY encomenda.dataEncomenda DESC;"
                #
                #elif len(filtro) > 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == False:
                #    cmd_sql = f"SELECT encomenda.nEncomendaLoja, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' ORDER BY encomenda.dataEncomenda DESC;"
                #
                #elif len(filtro) > 0 and self.radioButton.isChecked() == True and self.radioButton_2.isChecked() == False:
                #    cmd_sql = f"SELECT encomenda.nEncomendaLoja, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' AND encomenda.dataEntrega IS NOT NULL ORDER BY encomenda.dataEncomenda DESC;"
                #
                #elif len(filtro) > 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == True:
                #    cmd_sql = f"SELECT encomenda.nEncomendaLoja, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND cliente.nome LIKE '%{filtro}%' AND encomenda.dataEntrega IS NULL ORDER BY encomenda.dataEncomenda DESC;"
                #
                #elif len(filtro) == 0 and self.radioButton.isChecked() == True and self.radioButton_2.isChecked() == False:
                #    cmd_sql = f"SELECT encomenda.nEncomendaLoja, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND encomenda.dataEntrega IS NOT NULL ORDER BY encomenda.dataEncomenda DESC;"
                #
                #elif len(filtro) == 0 and self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == True:
                #    cmd_sql = f"SELECT encomenda.nEncomendaLoja, CONCAT(cliente.id, '-', cliente.nome), dataEncomenda, dataEntrega FROM encomenda, cliente WHERE encomenda.idCliente = cliente.id AND encomenda.dataEntrega IS NULL ORDER BY encomenda.dataEncomenda DESC;"
                
                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                self.tableView.verticalHeader().setVisible(False)
                modelo.setHorizontalHeaderLabels(["Nº Encomenda", "Utilizador", "Loja", "Data Encomenda", "Data Entrega"])
                for linha in dados:
                    modelo.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                self.tableView.setModel(modelo)

                #Chamar a atualização dos detalhes da encomenda
                self.tableView.selectionModel().selectionChanged.connect(self.listagemDetalhesEncomenda)
                # atualizar estado do botão entregar
                self.tableView.selectionModel().selectionChanged.connect(self.atualizar_estado_entrega)
                # atualizar estado de imediato
                self.atualizar_estado_entrega()
                
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
                cursor.execute("SELECT dataEntrega, ativo FROM EncomendaLoja WHERE nEncomendaLoja = %s;", (n,))
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
        selecionados = self.tableView.selectionModel().selectedRows()
        if not selecionados:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione uma encomenda para marcar como entregue.")
            return
        linha = selecionados[0].row()
        modelo = self.tableView.model()
        n_encomenda = modelo.data(modelo.index(linha,0))
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD != -1:
                cursor = conn_BD.cursor()
                cursor.execute("SELECT dataEntrega, ativo FROM EncomendaLoja WHERE nEncomendaLoja = %s;", (n_encomenda,))
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
                cmd_sql = "UPDATE EncomendaLoja SET dataEntrega = %s WHERE nEncomendaLoja = %s;"
                num = operacao_DML(conn_BD, cmd_sql, (now, n_encomenda))
                if num > 0:
                    # diminuir stock dos produtos da encomenda, verificando disponibilidade
                    cursor = conn_BD.cursor()
                    cursor.execute("SELECT idProduto, quantidade FROM DetalheEncomendaLoja WHERE nEncomendaLoja = %s;", (n_encomenda,))
                    detalhes = cursor.fetchall()
                    cursor.close()
                    insuficiencia = []
                    for id_prod, qt in detalhes:
                        atual = consultaUmValor(conn_BD, "SELECT stock FROM Produto WHERE id = %s;", (id_prod,))
                        if atual is not None and atual < qt:
                            insuficiencia.append((id_prod, atual, qt))
                    if insuficiencia:
                        msg = "Stock insuficiente para os seguintes artigos:\n"
                        for idp, atual, neces in insuficiencia:
                            msg += f"produto {idp}: atual {atual}, pedido {neces}\n"
                        QtWidgets.QMessageBox.warning(self, "Aviso", msg)
                        return
                    for id_prod, qt in detalhes:
                        operacao_DML(conn_BD, "UPDATE Produto SET stock = stock - %s WHERE id = %s;", (qt, id_prod))
                    QtWidgets.QMessageBox.information(self,"Sucesso","Encomenda marcada como entregue!")
                    self.listagemEncomenda()
                else:
                    QtWidgets.QMessageBox.warning(self,"Aviso","Nenhum registo foi alterado!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro: {e}")
    def listagemDetalhesEncomenda(self, selecao):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                selecao = self.tableView.selectionModel().selectedRows()
                if selecao:
                    linha = selecao[0].row()
                    modelo = self.tableView.model()
                    nEncomendaLoja = modelo.data(modelo.index(linha, 0))
                    cmd_sql = f"SELECT Produto.id, Produto.Designacao, DetalheEncomendaLoja.Quantidade, DetalheEncomendaLoja.precoUnitario, DetalheEncomendaLoja.precoUnitario*DetalheEncomendaLoja.Quantidade AS Total FROM DetalheEncomendaLoja JOIN Produto ON Produto.id = DetalheEncomendaLoja.idProduto WHERE nEncomendaLoja = {nEncomendaLoja} ORDER BY DetalheEncomendaLoja.idProduto ASC;"
                    dados = listagem_BD(conn_BD, cmd_sql)
                    modelo2 = QStandardItemModel()
                    self.tableView_2.verticalHeader().setVisible(False)
                    modelo2.setHorizontalHeaderLabels(["Id. Artigo", "Designação", "Quantidade", "Preço Unit.", "Total"])
                    for linha in dados:
                        modelo2.appendRow([QStandardItem(str(celula) if celula is not None else "") for celula in linha])
                    self.tableView_2.setModel(modelo2)
                    self.tableView_2.resizeColumnsToContents()
                else:
                    return
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

    def criarEncomenda(self):
        self.hide()
        self.form_CriarAlterar_Encomenda_Loja.show()
        self.form_CriarAlterar_Encomenda_Loja.inicializar(None, "novo")

    def alterarEncomenda(self):
        selecao = self.tableView.selectionModel().selectedRows()
        if not selecao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione uma encomenda para alterar.")
            return
        self.hide()
        self.form_CriarAlterar_Encomenda_Loja.show()
        self.form_CriarAlterar_Encomenda_Loja.inicializar(selecao, "alterar")

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
                cmd_sql = "SELECT dataEntrega FROM EncomendaLoja WHERE nEncomendaLoja = %s;"
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
                    cmd_sql = "UPDATE EncomendaLoja SET ativo = 0 WHERE nEncomendaLoja = %s;"
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