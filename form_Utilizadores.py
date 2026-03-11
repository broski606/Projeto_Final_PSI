from PyQt5 import QtWidgets
from Interfaces.formUtilizadores import Ui_MainWindow
from base_dados import ligacao_BD, listagem_BD, operacao_DML
from form_CriarAlterarUtilizador import formCriarAlterarUtilizador
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class formUtilizadores(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal = None):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Principal = formPrincipal
        #Solução para aquele erro estranho das libaries
        self.form_Login = formPrincipal.form_Login if formPrincipal is not None else None

        # estado de administrador do utilizador logado
        self.admin = False

        #Definir os botões
        #Pesquisa e Filtros
        self.pushButton_Limpar.clicked.connect(self.LimparFiltro)
        self.pushButton_Pesquisar.clicked.connect(self.ListagemUtilizadores)
        # Ações CRUD
        self.pushButton_Alterar.clicked.connect(self.alterar)
        self.pushButton_Criar.clicked.connect(self.novo)
        self.pushButton_Desativar.clicked.connect(self.DesativarUtilizador)
        #Barra de Utilidades
        self.pushButton_Voltar.clicked.connect(self.Voltar)
        self.pushButton_Logout.clicked.connect(self.mostrar_form_login)

        # criar formulário auxiliar
        self.form_Criar_Alterar_Utilizador = formCriarAlterarUtilizador(self)

        # garantir visibilidade dos botões de ação pelo estado atual
        self.atualizar_botoes_por_permissao()
        
    #Métodos:
    #Mostrar Formulários
    def Voltar(self):
        self.close()
        self.form_Principal.show()
        self.form_Principal.inicializar()

    def configurar_permissao(self, is_admin: bool):
        """Atualiza o formulário com base na indicação se o utilizador logado é administrador."""
        self.admin = is_admin
        self.atualizar_botoes_por_permissao()

    def atualizar_botoes_por_permissao(self):
        # apenas administradores podem criar, alterar ou desativar
        visible = self.admin
        self.pushButton_Criar.setVisible(visible)
        self.pushButton_Alterar.setVisible(visible)
        self.pushButton_Desativar.setVisible(visible)
    
    def mostrar_form_login(self):
        self.hide()
        self.form_Login.show()
        self.form_Login.lineEdit_Palavra_Passe.setText("")

    #Pesquisa e Filtros
    def LimparFiltro(self):
        self.lineEdit.setText("") 
        self.radioButton_2.setChecked(False) # Não Admin
        self.radioButton_3.setChecked(False) # Admin
        self.ListagemUtilizadores()

    def ListagemUtilizadores(self):
        # sempre atualizar a visibilidade dos botões caso o estado admin tenha mudado
        self.atualizar_botoes_por_permissao()


        try:
            conn_BD = ligacao_BD()
            if conn_BD and conn_BD!=-1:
                filtro = self.lineEdit.text().strip()
                admin_checked = self.radioButton_3.isChecked()
                nao_admin_checked = self.radioButton_2.isChecked()

                # Montar query usando apenas if statements (sem lógica dinâmica complexa)
                if filtro and admin_checked:
                    cmd_sql = f"SELECT id, nome, email, admin FROM Utilizador WHERE (nome LIKE '%{filtro}%' OR email LIKE '%{filtro}%') AND admin = 1 ORDER BY nome ASC;"
                elif filtro and nao_admin_checked:
                    cmd_sql = f"SELECT id, nome, email, admin FROM Utilizador WHERE (nome LIKE '%{filtro}%' OR email LIKE '%{filtro}%') AND admin = 0 ORDER BY nome ASC;"
                elif admin_checked:
                    cmd_sql = "SELECT id, nome, email, admin FROM Utilizador WHERE admin = 1 ORDER BY nome ASC;"
                elif nao_admin_checked:
                    cmd_sql = "SELECT id, nome, email, admin FROM Utilizador WHERE admin = 0 ORDER BY nome ASC;"
                elif filtro:
                    cmd_sql = f"SELECT id, nome, email, admin FROM Utilizador WHERE nome LIKE '%{filtro}%' OR email LIKE '%{filtro}%' ORDER BY nome ASC;"
                else:
                    cmd_sql = "SELECT id, nome, email, admin FROM Utilizador ORDER BY nome ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                modelo = QStandardItemModel()
                modelo.setHorizontalHeaderLabels(["id", "nome", "email", "admin"])
                for linha in dados:
                    valores = [str(celula) if celula is not None else "" for celula in linha]
                    if len(valores) == 4:
                        valores[3] = "Sim" if linha[3] == 1 or linha[3] == True else "Não"
                    modelo.appendRow([QStandardItem(v) for v in valores])
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
        self.form_Criar_Alterar_Utilizador.show()
        self.form_Criar_Alterar_Utilizador.inicializar(selecao, "alterar")

    def novo(self):
        self.hide()
        self.form_Criar_Alterar_Utilizador.show()
        self.form_Criar_Alterar_Utilizador.inicializar(None, "novo")

    def DesativarUtilizador(self):
        selecionados = self.tableView.selectionModel().selectedRows()
        if selecionados:
            linha = selecionados[0].row()
            modelo = self.tableView.model()
            id_user = modelo.data(modelo.index(linha, 0))
            nome_user = modelo.data(modelo.index(linha, 1))

            conn_BD = ligacao_BD()
            if conn_BD and conn_BD != -1:
                resposta = QtWidgets.QMessageBox.question(
                    self,
                    "Questão",
                    f"Tem certeza de que deseja desativar o utilizador com identificador {id_user} e nome '{nome_user}'?"
                )
                if resposta == QtWidgets.QMessageBox.Yes:
                    cmd_sql = "UPDATE Utilizador SET ativo = 0 WHERE id = %s;"
                    num_registos = operacao_DML(conn_BD, cmd_sql, (id_user,))
                    if num_registos > 0:
                        QtWidgets.QMessageBox.information(self, "Sucesso", "O utilizador foi desativado com sucesso!")
                        self.ListagemUtilizadores()
                    else:
                        QtWidgets.QMessageBox.warning(self, "Aviso", "Nenhum registo foi alterado !")
                else:
                    QtWidgets.QMessageBox.warning(self, "Aviso", "A desativação do utilizador foi cancelada!")
        else:
            QtWidgets.QMessageBox.warning(self,"Aviso","É necessário selecionar a linha da tabela que contém o utilizador a desativar!")
