from PyQt5 import QtWidgets
from Interfaces.formUtilizadores import Ui_MainWindow
#from form_categorias import formCategorias
#from form_artigos import formArtigos
#from form_cliente import formCliente
#from form_encomendas import formEncomendas

class formUtilizadores(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #Definir os forms

        #Definir os botões
        
    #Métodos

    def ListagemUtilizadores():
        pass