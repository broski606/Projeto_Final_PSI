from PyQt5 import QtWidgets
from Interfaces.formUtilizadores import Ui_MainWindow

class formUtilizadores(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, formPrincipal = None):
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

    def ListagemUtilizadores():
        pass