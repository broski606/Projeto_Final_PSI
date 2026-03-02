from PyQt5 import QtWidgets

def verificar_tipo_dados(valor):
    try:
        int(valor)
        return "inteiro"
    except ValueError:
        return "não inteiro"

def novoRegisto(self):
    # Passar dados (identificador e designação) do formulário para variáveis
    identificador = self.lineEdit_id.text()
    designacao = self.lineEdit_designacao.text()
    # Validar dados: campos de preenchimento obrigatório
    if len(designacao)==0 or len(identificador)==0:
        QtWidgets.QMessageBox.warning(self, "Aviso", "É obrigatório inserir o identificador e a designação\npara o tipo de produto!")
        return
    # Validar dados: tipos de dados de acordo com o definido na BD (número inteiro, data,...)
    tipoDados_id = verificar_tipo_dados(identificador)
    if tipoDados_id != "inteiro":
        QtWidgets.QMessageBox.warning(self, "Aviso", "O identificador do tipo de produto tem que ser um\nvalor inteiro!")
        return
    # Validar dados: repetição de dados em campos cujo valor tem de ser único (campos chave,...)
    # Ligar à BD e efetuar a inserção do registo
    # Após inserção atualizar a listagem na QTableView
    # Fechar o formulário de edição e mostrar o formulário principal