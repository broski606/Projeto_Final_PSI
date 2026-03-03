from PyQt5 import QtWidgets
from Interfaces.formFornecedores import Ui_MainWindow
#from form_categorias import formCategorias
#from form_artigos import formArtigos
#from form_cliente import formCliente
#from form_encomendas import formEncomendas

class formFornecedores(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, form_Principal):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Principal = form_Principal

        #Definir os botões
        self.pushButton_Voltar.clicked.connect(self.Voltar)
        
    #Métodos
    def Voltar(self):
        self.close()
        self.form_Principal.show()
        self.form_Principal.ListagemStock()

    def ListagemFornecedores():
        pass