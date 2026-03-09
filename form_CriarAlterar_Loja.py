from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
#from Interfaces.formDetalhesArtigo import Ui_Form
from Interfaces.formCriarAlterarLoja import Ui_MainWindow
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
from funcoes_gerais import verificar_tipo_dados


class formCriarAlterarLoja(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formLojas):
        super().__init__()
        self.setupUi(self)
        #Definição vars
        self.id = None
        self.nome = None
        self.nif = None
        self.morada = None
        self.telefone = None
        self.email = None
        self.ativo = None
        
        #Definição dos forms
        self.form_Lojas = formLojas

        #Definição dos botões
        self.pushButton_Voltar.clicked.connect(self.voltar)
        self.pushButton_CriarAlterar.clicked.connect(self.gravar)
        
    def gravar(self):
        #alterado a partir do form_altear_categoria.py e do form_nova_categoria.py
        if self.modo_funcionamento == "novo":
            try:
                id = self.lineEdit_Id.text()
                nome = self.lineEdit_Nome.text()
                nif = self.lineEdit_NIF.text()
                morada = self.lineEdit_Morada.text()
                email = self.lineEdit_Email.text()
                telefone = self.lineEdit_Telefone.text()
                ativo = self.checkBox.isChecked()

                if len(id)==0 or len(nome)==0 or len(nif)==0 or len(morada)==0 or len(email)==0 or len(telefone)==0:
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
                
                cmd_sql = f"SELECT COUNT(*) FROM Loja WHERE id = %s OR nif = %s;"
                numRegistos = consultaUmValor(conn_BD, cmd_sql, (id, nif,))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao verificar a existência do produto")
                    return
                elif numRegistos > 0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Já existe uma loja com nif {nif} ou com id {id} introduzidos")
                    return
                
                cmd_sql = "INSERT INTO Loja (id, nome, nif, morada, email, telefone, ativo) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (id, nome, nif, morada, email, telefone, ativo))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao inserir o registo")
                    return
                resposta = QtWidgets.QMessageBox.question(self, "Confirmação", "Loja inserida com sucesso!\n Pretende inserir dados de uma nova loja?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
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
                #desativar 
                nome = self.lineEdit_Nome.text()
                nif = self.lineEdit_NIF.text()
                morada = self.lineEdit_Morada.text()
                email = self.lineEdit_Email.text()
                telefone = self.lineEdit_Telefone.text()
                ativo = self.checkBox.isChecked()
                
                if len(nome)==0:
                    QtWidgets.QMessageBox.critical(self,"Aviso","Nome da loja por preencher")
                    return
                
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                # Verificar se a loja existe (por id)
                cmd_sql = "SELECT COUNT(*) FROM Loja WHERE id = %s;"
                numRegistosId = consultaUmValor(conn_BD, cmd_sql, (id,))

                # Verificar se já existe outra loja com o mesmo NIF
                # (exclui a própria loja que está a ser alterada)
                cmd_sql = "SELECT COUNT(*) FROM Loja WHERE nif = %s AND id <> %s;"
                numRegistosNif = consultaUmValor(conn_BD, cmd_sql, (nif, id))

                if numRegistosId == -1 or numRegistosNif == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao verificar a existência da loja")
                    return
                elif numRegistosId == 0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Não foi possível encontrar a loja com identificador {id}!")
                    return
                elif numRegistosNif > 0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Já existe outra loja com o nif {nif} introduzido")
                    return
                elif numRegistosId==0:
                    QtWidgets.QMessageBox.critical(self,"Aviso", f"Não foi possível encontrar a loja com identificador {id}!")
                    return
                cmd_sql = "UPDATE Loja SET nome = %s, nif = %s, morada = %s, email = %s, telefone = %s, ativo = %s WHERE id = %s;"
                numRegistos = operacao_DML(conn_BD, cmd_sql, (nome, nif, morada, email, telefone, ativo, id,))
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao alterar o registo")
                    return
                QtWidgets.QMessageBox.information(self, "Confirmação", "Loja alterada com sucesso!")
                
                self.close()
                self.form_Lojas.show()
                self.form_Lojas.ListagemLojas()
                conn_BD.close()

            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Erro: {e}")
                return
            

    def inicializar(self, selecao, modo_funcionamento):
        self.modo_funcionamento = modo_funcionamento
        if modo_funcionamento == "novo":
            self.lineEdit_Id.setText("")
            self.lineEdit_Nome.setText("")
            self.lineEdit_NIF.setText("")
            self.lineEdit_Morada.setText("")
            self.lineEdit_Email.setText("")
            self.lineEdit_Telefone.setText("")
            self.checkBox.setChecked(True)

            try:
                conn_BD = ligacao_BD()
                if not conn_BD:
                    QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                    return
                
                cmd_sql = "SELECT MAX(id)+1 FROM Loja;"
                proximo_id = consultaUmValor(conn_BD, cmd_sql)
                if proximo_id == -1:
                    QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao obter o próximo id")
                    return
                self.lineEdit_Id.setText(str(proximo_id))
            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro",f"Ocorreu um erro:{e}")
            finally:
                if conn_BD:
                    conn_BD.close()

        elif modo_funcionamento == "alterar":
            linha = selecao[0].row() # Primeira linha selecionada
            modelo = self.form_Lojas.tableView.model()
            self.lineEdit_Id.setText(modelo.data(modelo.index(linha, 0)))
            self.lineEdit_Nome.setText(modelo.data(modelo.index(linha, 1)))
            self.lineEdit_NIF.setText(modelo.data(modelo.index(linha, 2)))
            self.lineEdit_Morada.setText(modelo.data(modelo.index(linha, 3)))
            self.lineEdit_Email.setText(modelo.data(modelo.index(linha, 4)))
            self.lineEdit_Telefone.setText(modelo.data(modelo.index(linha, 5)))
            self.checkBox.setChecked(True)
            self.lineEdit_Id.setEnabled(False)

    def voltar(self):
        self.close()
        self.form_Lojas.show()
        self.form_Lojas.ListagemLojas()