from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Interfaces.formPrincipal import Ui_MainWindow
from form_Utilizadores import formUtilizadores
from form_Lojas import formLojas
from form_Fornecedores import formFornecedores
from form_Entradas_de_Material import formEntradasDeMaterial
from form_Saidas_de_Material import formSaidasDeMaterial
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML

class formPrincipal(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Utilizadores = formUtilizadores(self)
        self.form_Lojas = formLojas()
        self.form_Fornecedores = formFornecedores()
        self.form_Entradas_de_Material = formEntradasDeMaterial()
        self.form_Saidas_de_Material = formSaidasDeMaterial()

        #Definir os botões
        #Pesquisa e Filtros
        self.pushButton_Limpar.clicked.connect(self.LimparFiltro)
        self.pushButton_Pesquisar.clicked.connect(self.ListagemStock)

        #Barra de Utilidades
        self.pushButton_Utilizadores.clicked.connect(self.mostrar_form_Utilizadores)
        self.pushButton_Lojas.clicked.connect(self.mostrar_form_Lojas)
        self.pushButton_Fornercedores.clicked.connect(self.mostrar_form_Fornecedores)
        self.pushButton_Entradas_de_Material.clicked.connect(self.mostrar_form_Entradas_de_Material)
        self.pushButton_Saidas_de_Material.clicked.connect(self.mostrar_form_Saidas_de_Material)
        
    #Métodos
    #Mostrar forms
    def mostrar_form_Utilizadores(self):
        self.hide()
        self.form_Utilizadores.show()
        #self.formUtilizadores.ListagemUtilizadores()

    def mostrar_form_Lojas(self):
        self.hide()
        self.form_Lojas.show()
        #self.formUtilizadores.ListagemUtilizadores()

    def mostrar_form_Fornecedores(self):
        self.hide()
        self.form_Fornecedores.show()
        #self.formUtilizadores.ListagemUtilizadores()
    
    def mostrar_form_Entradas_de_Material(self):
        self.hide()
        self.form_Entradas_de_Material.show()
        #self.formUtilizadores.ListagemUtilizadores()

    def mostrar_form_Saidas_de_Material(self):
        self.hide()
        self.form_Saidas_de_Material.show()
        #self.formUtilizadores.ListagemUtilizadores()

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
                    cmd_sql = f"SELECT id, idCategoria, designacao, preco, stock FROM Produto WHERE designacao LIKE '%{filtro}%' ORDER BY designacao ASC;"
                else:
                    cmd_sql = "SELECT id, idCategoria, designacao, preco, stock FROM Produto ORDER BY designacao ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["id", "idCategoria", "designação", "preco", "stock"])
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