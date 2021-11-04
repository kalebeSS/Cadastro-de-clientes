import mysql.connector
from mysql.connector import Error
from mysql.connector import Error

def connect(host, usuario, senha, banco):
    return mysql.connector.connect(host = host, user = usuario, password = senha, database = banco)

def close_connect(con):
    return con.close()

def insert(con, cpf, nome, email, endereço, telefone):
    cursor = con.cursor()
    sql = "INSERT INTO clientes(cpf, nome, email, endereco, telefone) values (%s, %s, %s, %s, %s)"
    valores = (cpf, nome, email, endereço, telefone)
    cursor.execute(sql, valores)
    cursor.close()
    con.commit()

def select(con, table):
    cursor = con.cursor()
    sql = f"select * from {table}"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)
    con.close()

def Query(con , cpf, table):
    try:
        cursor = con.cursor()
        Query_sql = f'select * from {table} WHERE cpf = {cpf}'
        cursor.execute(Query_sql)
        linhas = cursor.fetchall()
        for linha in linhas:
            print(linha)   
    except Error as er:
        print(er)
    finally:
        if (con.is_connected()):
            cursor.close()
            con.close()

def delete(con, cpf, database):
    try:
        cursor = con.cursor()
        sql = f"DELETE FROM {database} WHERE cpf = {cpf}"
        cursor.execute(sql)
        con.commit()

    except Error as er:
        print(er)
    finally:
        print("CPF Deletado")
