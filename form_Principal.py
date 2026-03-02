from PyQt5 import QtWidgets
from Interfaces.formPrincipal import Ui_MainWindow
from form_Utilizadores import formUtilizadores
from form_Lojas import formLojas
#from form_categorias import formCategorias
#from form_artigos import formArtigos
#from form_cliente import formCliente
#from form_encomendas import formEncomendas

class formPrincipal(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #Definir os forms
        self.formUtilizadores = formUtilizadores(self)

        #Definir os botões
        
    #Métodos

    def mostrar_form_Utilizadores(self):
        self.hide()
        self.formUtilizadores.show()
        #self.formUtilizadores.ListagemUtilizadores()


    def ListagemStock(self):
        pass