from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
#from Interfaces.formDetalhesArtigo import Ui_Form
from Interfaces.formCriarAlterarProduto import Ui_MainWindow
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from funcoes_gerais import verificar_tipo_dados


class formCriarAlterarProduto(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal):
        super().__init__()
        self.setupUi(self)
        #Definição vars
        self.modo_funcionamento = None
        self.categoria = None
        self.fornecedor = None
        self.designacao = None
        self.preco = None
        self.preco_revenda = None
        self.stock = None
        self.ativo = None
        
        #Definição dos forms
        self.form_Principal = formPrincipal

        #Definição dos botões
        self.pushButton_Voltar.clicked.connect(self.voltar)
        self.pushButton_CriarAlterar.clicked.connect(self.gravar)
        
    def gravar(self):
        #alterado a partir do form_altear_categoria.py e do form_nova_categoria.py
        if self.modo_funcionamento == "novo":
            try:
                id = self.lineEdit_Id.text()
                categoria = self.comboBox_Categoria.currentText()
                fornecedor = self.comboBox_Fornecedor.currentText()
                designacao = self.lineEdit_Designacao.text()
                preco = self.lineEdit_Preco.text()
                preco_revenda = self.lineEdit_PrecoRevenda.text()
                stock = self.lineEdit_Stock.text()
                ativo = self.checkBox.isChecked()
                if len(ide)==0 or len(categoria)==0 or len(fornecedor)==0 or len(designacao)==0 or len(preco)==0 or len(preco_revenda)==0 or len(stock)==0:
                    QtWidgets.QMessageBox.critical(self,"Aviso","Campos por preencher")
                    return
                
                tipoDados_id = verificar_tipo_dados(id)
                if tipoDados_id != "inteiro":
                    QtWidgets.QMessageBox.critical(self,"Aviso","Inserir valor inteiro no campo id")
                    return
                
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                cmd_sql = f"SELECT COUNT(*) FROM Produto WHERE id = %s OR designacao = %s;"
                numRegistos = consultaUmValor(conn_BD, cmd_sql, (id, designacao,))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao verificar a existência do produto")
                    return
                elif numRegistos > 0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Já existe um produto com designação {designacao} ou com id {id} introduzidos")
                    return
                
                cmd_sql = "SELECT id FROM Categoria WHERE designacao = %s;"
                idCategoria = consultaUmValor(conn_BD, cmd_sql, (categoria,))
                if idCategoria == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao obter o ID da categoria")
                    return

                cmd_sql = "SELECT id FROM Fornecedor WHERE nome = %s;"
                idFornecedor = consultaUmValor(conn_BD, cmd_sql, (fornecedor,))
                if idCategoria == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao obter o ID do fornecedor")
                    return
                
                cmd_sql = "INSERT INTO Produto (id, idCategoria, idFornecedor, designacao, preco, precoRevenda, stock, ativo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (id, idCategoria, idFornecedor, designacao, preco, preco_revenda, stock, ativo))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao inserir o registo")
                    return
                resposta = QtWidgets.QMessageBox.question(self, "Confirmação", "Produto inserido com sucesso!\n Pretende inserir dados de um novo produto?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if resposta == QtWidgets.QMessageBox.Yes:
                    self.inicializar(selecao=None, modo_funcionamento="novo")
                    return
                else:
                    self.voltar()
                conn_BD.close()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Erro: {e}")
                return
        
        elif self.modo_funcionamento == "alterar":
            try:
                id = self.lineEdit_Id.text()
                categoria = self.comboBox_Categoria.currentText()
                fornecedor = self.comboBox_Fornecedor.currentText()
                designacao = self.lineEdit_Designacao.text()
                preco = self.lineEdit_Preco.text()
                preco_revenda = self.lineEdit_PrecoRevenda.text()
                stock = self.lineEdit_Stock.text()
                ativo = self.checkBox.isChecked()
                
                if len(designacao)==0:
                    QtWidgets.QMessageBox.critical(self,"Aviso","Designacao do produto por preencher")
                    return

                if self.designacao == designacao:
                    QtWidgets.QMessageBox.critical(self,"Aviso","A designação do produto não foi alterada")
                    return
                
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                cmd_sql = f"SELECT COUNT(*) FROM Produto WHERE id = %s;"
                numRegistosId = consultaUmValor(conn_BD, cmd_sql, (id,))
                cmd_sql = f"SELECT COUNT(*) FROM Produto WHERE designacao = %s;"
                numRegistosD = consultaUmValor(conn_BD, cmd_sql, (designacao,))
                if numRegistosId == -1 or numRegistosD == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao verificar a existência do artigo")
                    return
                elif numRegistosD > 0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Já existe um produto com a designação {designacao} ou com id {id} introduzidos")
                    return
                elif numRegistosId==0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Não foi possível encontrar o produto com identificador {id}!")
                    return
                idCategoria = consultaUmValor(conn_BD, "SELECT id FROM Categoria WHERE designacao = %s;", (categoria,))
                idFornecedor = consultaUmValor(conn_BD, "SELECT id FROM Fornecedor WHERE nome = %s;", (fornecedor,))
                cmd_sql = "UPDATE Produto SET idCategoria = %s, idFornecedor = %s, designacao = %s, preco = %s, precoRevenda = %s, stock = %s, ativo = %s WHERE id = %s;"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (idCategoria, idFornecedor, designacao, preco, preco_revenda, stock, ativo, id,))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao alterar o registo")
                    return
                QtWidgets.QMessageBox.information(self, "Confirmação", "Artigo alterado com sucesso!")
                
                self.close()
                self.form_Principal.show()
                self.form_Principal.ListagemStock()
                conn_BD.close()

            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Erro: {e}")
                return
            

    def inicializar(self, selecao, modo_funcionamento):
        self.modo_funcionamento = modo_funcionamento
        if modo_funcionamento == "novo":
            self.lineEdit_Id.setText("")
            self.lineEdit_Designacao.setText("")
            self.lineEdit_Preco.setText("")
            self.lineEdit_PrecoRevenda.setText("")
            self.lineEdit_Stock.setText("")
            self.checkBox.setChecked(True)

            try:
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                
                #cmd_sql = "SELECT categoria.designacao FROM artigo, categoria WHERE categoria.id = artigo.idCategoria ORDER BY categoria.designacao ASC;"
                cmd_sql = "SELECT designacao FROM Categoria ORDER BY designacao ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                if dados:
                    self.comboBox_Categoria.clear() # Limpa a QComboBox antes de preencher
                    categorias = [str(linha[0]) for linha in dados] #correção para o erro todo estranho da tupla que deu quando corri o código sem esta linha: index 0 has type 'tuple but 'str is expected
                    self.comboBox_Categoria.addItems(categorias) # Adiciona os itens ao QComboBox
                
                #cmd_sql = "SELECT categoria.designacao FROM artigo, categoria WHERE categoria.id = artigo.idCategoria ORDER BY categoria.designacao ASC;"
                cmd_sql = "SELECT nome FROM Fornecedores ORDER BY designacao ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                if dados:
                    self.comboBox_Fornecedor.clear() # Limpa a QComboBox antes de preencher
                    fornecedores = [str(linha[0]) for linha in dados] #correção para o erro todo estranho da tupla que deu quando corri o código sem esta linha: index 0 has type 'tuple but 'str is expected
                    self.comboBox_Fornecedor.addItems(fornecedores) # Adiciona os itens ao QComboBox

                cmd_sql = "SELECT MAX(id)+1 FROM Produto;"
                proximo_id = consultaUmValor(conn_BD, cmd_sql)
                if proximo_id == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao obter o próximo id")
                    return
                self.lineEdit_Id.setText(str(proximo_id))
            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

        elif modo_funcionamento == "alterar":
            try:
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                #preencher COMBOBOX com valores da BD
                #cmd_sql = "SELECT categoria.designacao FROM artigo, categoria WHERE categoria.id = artigo.idCategoria ORDER BY categoria.designacao ASC;"
                cmd_sql = "SELECT designacao FROM Categoria ORDER BY designacao ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                if dados:
                    self.comboBox_Categoria.clear() # Limpa a QComboBox antes de preencher
                    categorias = [str(linha[0]) for linha in dados] #correção para o erro todo estranho da tupla que deu quando corri o código sem esta linha: index 0 has type 'tuple but 'str is expected
                    self.comboBox_Categoria.addItems(categorias) # Adiciona os itens ao QComboBox
                
                #cmd_sql = "SELECT categoria.designacao FROM artigo, categoria WHERE categoria.id = artigo.idCategoria ORDER BY categoria.designacao ASC;"
                cmd_sql = "SELECT nome FROM Fornecedor ORDER BY nome ASC;"
                dados = listagem_BD(conn_BD, cmd_sql)
                if dados:
                    self.comboBox_Fornecedor.clear() # Limpa a QComboBox antes de preencher
                    fornecedores = [str(linha[0]) for linha in dados] #correção para o erro todo estranho da tupla que deu quando corri o código sem esta linha: index 0 has type 'tuple but 'str is expected
                    self.comboBox_Fornecedor.addItems(fornecedores) # Adiciona os itens ao QComboBox

            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")

            linha = selecao[0].row() # Primeira linha selecionada
            modelo = self.form_Principal.tableView.model()
            self.lineEdit_Id.setText(modelo.data(modelo.index(linha, 0)))
            self.lineEdit_Designacao.setText(modelo.data(modelo.index(linha, 3)))
            self.designacao = modelo.data(modelo.index(linha, 3))
            self.lineEdit_Preco.setText(modelo.data(modelo.index(linha, 4)))
            self.preco = modelo.data(modelo.index(linha, 4))
            self.lineEdit_PrecoRevenda.setText(modelo.data(modelo.index(linha, 5)))
            self.preco_revenda = modelo.data(modelo.index(linha, 5))
            self.lineEdit_Stock.setText(modelo.data(modelo.index(linha, 6)))
            self.stock = modelo.data(modelo.index(linha, 6))
            self.comboBox_Categoria.setCurrentText(modelo.data(modelo.index(linha, 1)))
            self.categoria = modelo.data(modelo.index(linha, 1))
            self.comboBox_Fornecedor.setCurrentText(modelo.data(modelo.index(linha, 2)))
            self.fornecedor = modelo.data(modelo.index(linha, 2))
            self.lineEdit_Id.setEnabled(False)



    def voltar(self):
        self.close()
        self.form_Principal.show()
        self.form_Principal.ListagemStock()