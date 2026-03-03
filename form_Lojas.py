from PyQt5 import QtWidgets
from Interfaces.formLojas import Ui_MainWindow
#from form_categorias import formCategorias
#from form_artigos import formArtigos
#from form_cliente import formCliente
#from form_encomendas import formEncomendas

class formLojas(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.form_Principal = formPrincipal

        #Definir os botões
        self.pushButton_Voltar.clicked.connect(self.Voltar)
        
    #Métodos
    def Voltar(self):
        self.close()
        self.form_Principal.show()
        self.form_Principal.ListagemStock()

    def ListagemLojas():
        pass