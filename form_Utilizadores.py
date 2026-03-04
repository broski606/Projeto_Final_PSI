from PyQt5 import QtWidgets
from Interfaces.formUtilizadores import Ui_MainWindow
from base_dados import ligacao_BD, listagem_BD, operacao_DML
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class formUtilizadores(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal = None):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Principal = formPrincipal
        # Avoid circular import: use the login form instance from formPrincipal if provided
        self.form_Login = formPrincipal.form_Login if formPrincipal is not None else None

        #Definir os botões
        #Pesquisa e Filtros
        self.pushButton_Limpar.clicked.connect(self.LimparFiltro)
        self.pushButton_Pesquisar.clicked.connect(self.ListagemUtilizadores)
        #Barra de Utilidades
        self.pushButton_Voltar.clicked.connect(self.Voltar)
        self.pushButton_Logout.clicked.connect(self.mostrar_form_login)
        
    #Métodos:
    #Mostrar Formulários
    def Voltar(self):
        self.close()
        self.form_Principal.show()
        self.form_Principal.ListagemStock()
    
    def mostrar_form_login(self):
        self.hide()
        self.form_Login.show()
        self.form_Login.lineEdit_Palavra_Passe.setText("")

    #Pesquisa e Filtros
    def LimparFiltro(self):
        self.lineEdit.setText("") 
        #self.lineEdit.clear()
        self.ListagemUtilizadores()

    def ListagemUtilizadores(self):
        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text()
                if len(filtro) > 0:
                    cmd_sql = f"SELECT id, nome, email FROM Utilizador WHERE nome LIKE '%{filtro}%' OR email LIKE '%{filtro}%' ORDER BY nome ASC;"
                else:
                    cmd_sql = "SELECT id, nome, email FROM Utilizador ORDER BY nome ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["id", "nome", "email"])
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