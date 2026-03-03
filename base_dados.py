import mysql.connector
from mysql.connector import Error

def ligacao_BD():
    try:
        ligacaoBD = mysql.connector.connect(
        host="localhost",
        database="Columbofilia_Armazem",
        user="root",
        password=""
        ) #estabelecer ligação à BD
        if ligacaoBD.is_connected(): #testar se a ligação à BD está estabelecida
            print("Ligação à BD Columbofilia_Armazem estabelecida com sucesso!")
            return ligacaoBD
        else:
            print("Erro na ligação à BD Columbofilia_Armazem!")
            return -1
    except Error as e: #Se ocorrer algum erro, exibe a mensagem de erro
        print(f"Erro: {e}")
        return -1

def listagem_BD(conn,comando_sql):
    try: 
        cursor = conn.cursor()
        cursor.execute(comando_sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    except Error as e:
        print(f"Erro: {e}")
        return -1
    
def consultaUmValor(conn,comando_sql, parametros=None):
    try: 
        cursor = conn.cursor()
        cursor.execute(comando_sql, parametros or ())
        dado = cursor.fetchone()
        cursor.close()
        return dado[0] if dado else -1
    except Error as e:
        print(f"Erro: {e}")
        return -1
    
def operacao_DML(conn,comando_sql, parametros=None):
    try: 
        cursor = conn.cursor()
        cursor.execute(comando_sql, parametros or ())
        conn.commit()
        registos_afetados = cursor.rowcount
        cursor.close()
        return registos_afetados
    except Error as e:
        print(f"Erro: {e}")
        return -1