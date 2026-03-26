from PyQt5 import QtWidgets
import re

def verificar_tipo_dados(valor):
    try:
        int(valor)
        return "inteiro"
    except ValueError:
        return "não inteiro"


def validar_email(email):
    """
    Valida o formato de um email.
    Retorna: (True, "") se válido, (False, mensagem_erro) se inválido
    """
    if not email or len(email.strip()) == 0:
        return False, "Email não pode estar vazio"
    
    # Padrão simples para validação de email
    padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(padrao_email, email):
        return False, f"Email '{email}' não tem um formato válido"
    
    return True, ""


def validar_telefone(telefone):
    """
    Valida o formato de um telefone (deve ter 9 dígitos).
    Retorna: (True, "") se válido, (False, mensagem_erro) se inválido
    """
    if not telefone or len(telefone.strip()) == 0:
        return False, "Telefone não pode estar vazio"
    
    # Remove espaços
    telefone_limpo = telefone.replace(" ", "").replace("-", "").replace("+", "")
    
    # Verifica se tem 9 dígitos
    if not telefone_limpo.isdigit():
        return False, "Telefone deve conter apenas números"
    
    if len(telefone_limpo) != 9:
        return False, f"Telefone deve ter 9 dígitos (tem {len(telefone_limpo)})"
    
    return True, ""


def validar_nif(nif):
    """
    Valida o formato de um NIF (entre 6 e 20 caracteres).
    Retorna: (True, "") se válido, (False, mensagem_erro) se inválido
    """
    if not nif or len(nif.strip()) == 0:
        return False, "NIF não pode estar vazio"
    
    nif_limpo = nif.strip()
    
    if len(nif_limpo) < 6 or len(nif_limpo) > 20:
        return False, f"NIF deve ter entre 6 e 20 caracteres (tem {len(nif_limpo)})"
    
    # Verifica se contém apenas caracteres válidos (letras, números, hífen)
    if not re.match(r'^[a-zA-Z0-9\-]+$', nif_limpo):
        return False, "NIF contém caracteres inválidos"
    
    return True, ""


def validar_campos_obrigatorios(campos_dict):
    """
    Valida múltiplos campos obrigatórios.
    Recebe um dicionário com {'nome_campo': 'valor'} ou similar.
    Retorna: (True, "") se todos válidos, (False, mensagem_erro) se algum vazio
    """
    campos_vazios = []
    for nome_campo, valor in campos_dict.items():
        if valor is None or len(str(valor).strip()) == 0:
            campos_vazios.append(nome_campo)
    
    if campos_vazios:
        campos_str = ", ".join(campos_vazios)
        return False, f"Campos por preencher: {campos_str}"
    
    return True, ""


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