from PyQt5 import QtWidgets
from Interfaces.formCriarAlterarProduto import Ui_MainWindow
from base_dados import ligacao_BD, listagem_BD, consultaUmValor, operacao_DML

class formCriarAlterarProduto(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Variáveis de controlo
        self.id_produto = None
        self.designacao_original = None
        self.em_edicao = False
        
        # Conexões dos botões
        self.pushButton_CriarAlterar.clicked.connect(self.gravar)
        self.pushButton_Voltar.clicked.connect(self.voltar)
        self.checkBox.stateChanged.connect(self.atualizar_interface)
        
        # Carrega os dados iniciais
        self.carregar_categorias()
        self.carregar_fornecedores()
        self.limpar_formulario()

    def voltar(self):
        self.close()
    
    def carregar_categorias(self):
        """Carrega as categorias ativas da base de dados"""
        try:
            conn_BD = ligacao_BD()
            if not conn_BD:
                QtWidgets.QMessageBox.critical(self, "Erro", "Ligação à BD não estabelecida")
                return
            
            cmd_sql = "SELECT id, designacao FROM Categoria WHERE ativo = TRUE ORDER BY designacao;"
            resultados = listagem_BD(conn_BD, cmd_sql)
            
            if resultados != -1:
                self.comboBox_Categoria.clear()
                for categoria in resultados:
                    self.comboBox_Categoria.addItem(categoria[1], categoria[0])
            
            conn_BD.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Erro ao carregar categorias: {e}")
    
    def carregar_fornecedores(self):
        """Carrega os fornecedores ativos da base de dados"""
        try:
            conn_BD = ligacao_BD()
            if not conn_BD:
                QtWidgets.QMessageBox.critical(self, "Erro", "Ligação à BD não estabelecida")
                return
            
            cmd_sql = "SELECT id, nome FROM Fornecedor WHERE ativo = TRUE ORDER BY nome;"
            resultados = listagem_BD(conn_BD, cmd_sql)
            
            if resultados != -1:
                self.comboBox_Fornecedor.clear()
                for fornecedor in resultados:
                    self.comboBox_Fornecedor.addItem(fornecedor[1], fornecedor[0])
            
            conn_BD.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Erro ao carregar fornecedores: {e}")
    
    def limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.lineEdit_Id.clear()
        self.lineEdit_Id.setEnabled(True)
        self.lineEdit_Designacao.clear()
        self.lineEdit_Preco.clear()
        self.lineEdit_PrecoRevenda.clear()
        self.lineEdit_Stock.clear()
        self.checkBox.setChecked(True)
        self.pushButton_CriarAlterar.setText("Criar")
        self.em_edicao = False
        self.id_produto = None
        self.designacao_original = None
    
    def mode_edicao(self, id_produto):
        """Carrega um produto existente para edição"""
        try:
            conn_BD = ligacao_BD()
            if not conn_BD:
                QtWidgets.QMessageBox.critical(self, "Erro", "Ligação à BD não estabelecida")
                return
            
            cmd_sql = """SELECT id, idCategoria, idFornecedor, designacao, 
                               preco, precoRevenda, stock, ativo 
                        FROM Produto WHERE id = %s;"""
            cursor = conn_BD.cursor()
            cursor.execute(cmd_sql, (id_produto,))
            resultado = cursor.fetchone()
            cursor.close()
            conn_BD.close()
            
            if not resultado:
                QtWidgets.QMessageBox.warning(self, "Aviso", "Produto não encontrado")
                return
            
            # Preenche os campos
            self.id_produto = resultado[0]
            self.lineEdit_Id.setText(str(resultado[0]))
            self.lineEdit_Id.setEnabled(False)
            
            # Seleciona a categoria
            idx_cat = self.comboBox_Categoria.findData(resultado[1])
            if idx_cat >= 0:
                self.comboBox_Categoria.setCurrentIndex(idx_cat)
            
            # Seleciona o fornecedor
            idx_forn = self.comboBox_Fornecedor.findData(resultado[2])
            if idx_forn >= 0:
                self.comboBox_Fornecedor.setCurrentIndex(idx_forn)
            
            self.lineEdit_Designacao.setText(resultado[3])
            self.designacao_original = resultado[3]
            self.lineEdit_Preco.setText(str(resultado[4]))
            self.lineEdit_PrecoRevenda.setText(str(resultado[5]))
            self.lineEdit_Stock.setText(str(resultado[6]))
            self.checkBox.setChecked(bool(resultado[7]))
            
            self.pushButton_CriarAlterar.setText("Alterar")
            self.em_edicao = True
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Erro ao carregar produto: {e}")
    
    def validar_dados(self):
        """Valida os dados do formulário"""
        id_txt = self.lineEdit_Id.text().strip()
        designacao = self.lineEdit_Designacao.text().strip()
        preco_txt = self.lineEdit_Preco.text().strip()
        preco_revenda_txt = self.lineEdit_PrecoRevenda.text().strip()
        stock_txt = self.lineEdit_Stock.text().strip()
        
        if not designacao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "A designação do produto é obrigatória!")
            return None
        
        if not preco_txt:
            QtWidgets.QMessageBox.warning(self, "Aviso", "O preço de compra é obrigatório!")
            return None
        
        if not preco_revenda_txt:
            QtWidgets.QMessageBox.warning(self, "Aviso", "O preço de revenda é obrigatório!")
            return None
        
        if not stock_txt:
            QtWidgets.QMessageBox.warning(self, "Aviso", "O stock é obrigatório!")
            return None
        
        try:
            preco = float(preco_txt)
            preco_revenda = float(preco_revenda_txt)
            stock = int(stock_txt)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Preço e stock devem ser números válidos!")
            return None
        
        if preco < 0 or preco_revenda < 0:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Preços não podem ser negativos!")
            return None
        
        if stock < 0:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Stock não pode ser negativo!")
            return None
        
        if preco_revenda < preco:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Preço de revenda não pode ser menor que o preço de compra!")
            return None
        
        return {
            'designacao': designacao,
            'preco': preco,
            'preco_revenda': preco_revenda,
            'stock': stock
        }
    
    def atualizar_interface(self):
        """Atualiza a interface conforme necessário"""
        pass
    
    def gravar(self):
        try:
            # Validação dos dados
            dados = self.validar_dados()
            if not dados:
                return
            
            conn_BD = ligacao_BD()
            if not conn_BD:
                QtWidgets.QMessageBox.critical(self, "Erro", "Ligação à BD não estabelecida")
                return
            
            id_categoria = self.comboBox_Categoria.currentData()
            id_fornecedor = self.comboBox_Fornecedor.currentData()
            ativo = self.checkBox.isChecked()
            
            if self.em_edicao:
                # Modo edição - Alterar produto existente
                cmd_sql = """UPDATE Produto SET designacao = %s, preco = %s, 
                                               precoRevenda = %s, stock = %s, 
                                               ativo = %s, idCategoria = %s, 
                                               idFornecedor = %s 
                             WHERE id = %s;"""
                params = (dados['designacao'], dados['preco'], dados['preco_revenda'], 
                         dados['stock'], ativo, id_categoria, id_fornecedor, self.id_produto)
                
                numRegistos = operacao_DML(conn_BD, cmd_sql, params)
                
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Erro ao alterar o produto")
                    conn_BD.close()
                    return
                
                QtWidgets.QMessageBox.information(self, "Sucesso", "Produto alterado com sucesso!")
            else:
                # Modo criação - Novo produto
                id_produto = self.lineEdit_Id.text().strip()
                
                if not id_produto:
                    QtWidgets.QMessageBox.warning(self, "Aviso", "Id do produto é obrigatório!")
                    conn_BD.close()
                    return
                
                # Verifica se o ID já existe
                cmd_sql = "SELECT COUNT(*) FROM Produto WHERE id = %s;"
                numRegistos = consultaUmValor(conn_BD, cmd_sql, (id_produto,))
                
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Erro ao verificar ID do produto")
                    conn_BD.close()
                    return
                
                if numRegistos > 0:
                    QtWidgets.QMessageBox.warning(self, "Aviso", f"Já existe um produto com ID {id_produto}!")
                    conn_BD.close()
                    return
                
                # Insere novo produto
                cmd_sql = """INSERT INTO Produto (id, idCategoria, idFornecedor, 
                                                   designacao, preco, precoRevenda, 
                                                   stock, ativo) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
                params = (id_produto, id_categoria, id_fornecedor, dados['designacao'], 
                         dados['preco'], dados['preco_revenda'], dados['stock'], ativo)
                
                numRegistos = operacao_DML(conn_BD, cmd_sql, params)
                
                if numRegistos == -1:
                    QtWidgets.QMessageBox.critical(self, "Erro", "Erro ao criar o produto")
                    conn_BD.close()
                    return
                
                QtWidgets.QMessageBox.information(self, "Sucesso", "Produto criado com sucesso!")
                self.limpar_formulario()
            
            conn_BD.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Erro: {e}")