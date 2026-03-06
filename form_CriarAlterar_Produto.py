from PyQt5 import QtWidgets
#from PyQt5.QtGui import QStandardItemModel, QStandardItem
#from Interfaces.formAlterarCategoria import Ui_Form
from Interfaces.formCriarAlterarProduto import Ui_MainWindow
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML
#from funcoes_gerais import verificar_tipo_dados

class formCriarAlterarProduto(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal):

        super().__init__()
        self.setupUi(self)
        '''self.designacao = None
        self.form_categorias = form_categorias

        self.pushButton_gravar.clicked.connect(self.gravar)
        self.pushButton_voltar.clicked.connect(self.voltar)'''

    def voltar(self):
        self.close()
        self.form_categorias.show()

    def inicializar(self, selecao):
        linha = selecao[0].row() # Primeira linha selecionada
        modelo =self.form_categorias.tableView.model()
        self.lineEdit_id.setText(modelo.data(modelo.index(linha, 0)))
        self.lineEdit_designacao.setText(modelo.data(modelo.index(linha, 1)))
        self.designacao = modelo.data(modelo.index(linha, 1))
        self.lineEdit_id.setEnabled(False)

    def gravar(self):
        try:
            id = self.lineEdit_id.text()
            designacao = self.lineEdit_designacao.text()
            if len(designacao)==0:
                QtWidgets.QMessageBox.critical(self,"Aviso","Designacao da categoria por preencher")
                return

            if self.designacao == designacao:
                QtWidgets.QMessageBox.critical(self,"Aviso","A designação da categoria não foi alterada")
                return
            conn_BD = ligacao_BD()
            if not conn_BD:
                QtWidgets.QMessageBox.critical(self,"Erro","A ligação à BD não está estabelecida")
                return
            cmd_sql = f"SELECT COUNT(*) FROM categoria WHERE id = %s;"
            numRegistosId = consultaUmValor(conn_BD, cmd_sql, (id,))
            cmd_sql = f"SELECT COUNT(*) FROM categoria WHERE designacao = %s;"
            numRegistosD = consultaUmValor(conn_BD, cmd_sql, (designacao,))
            if numRegistosId == -1 or numRegistosD == -1:
                QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao verificar a existência da categoria")
                return
            elif numRegistosD > 0:
                QtWidgets.QMessageBox.critical(self,"Aviso", f"Já existe uma categoria com designação {designacao} ou com id {id} introduzidos")
                return
            elif numRegistosId==0:
                QtWidgets.QMessageBox.critical(self,"Aviso", f"Não foi possível encontrar a categoria com identificador {id}!")
                return
            cmd_sql = "UPDATE categoria SET designacao = %s WHERE id = %s;"
            numRegistos = operacao_DML(conn_BD, cmd_sql, (designacao, id,))
            if numRegistos == -1:
                QtWidgets.QMessageBox.critical(self,"Erro","Ocorreu um erro ao alterar o registo")
                return
            QtWidgets.QMessageBox.information(self, "Confirmação", "Categoria alterada com sucesso!\n Pretende alterar dados de uma nova categoria?")
            self.close()
            self.form_categorias.show()
            self.form_categorias.listagemCategorias()
            conn_BD.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Erro",f"Erro: {e}")
            return