from PyQt5 import uic, QtWidgets
from infos import *
from conexao_qt import *

numero_cpf = 0

def update_infos():
    nome = menu_edicao.lineEdit_2.text()
    email = menu_edicao.lineEdit_3.text()
    endereco = menu_edicao.lineEdit_4.text()
    telefone = menu_edicao.lineEdit_5.text()

    con = connect(LOCALHOST, USER, PASSWORD, SCHEMA)
    cursor = con.cursor()
    cursor.execute("UPDATE clientes SET nome = '{}', email = '{}', endereco = '{}', telefone = '{}' WHERE cpf = '{}'".format(nome, email, endereco, telefone, numero_cpf))
    con.commit()

    menu_edicao.close()
    lista_de_usuarios.close()
    lista_de_usuario_tela()

def Menu_edit():
    global numero_cpf
    linha = lista_de_usuarios.tableWidget.currentRow()
    con = connect(LOCALHOST, USER, PASSWORD, SCHEMA)
    cursor = con.cursor()
    cursor.execute("SELECT cpf FROM clientes")
    dados_lidos = cursor.fetchall()
    valor_cpf = dados_lidos[linha][0]
    
    cursor.execute("SELECT * FROM clientes where cpf="+str(valor_cpf))
    cpf = cursor.fetchall()
    numero_cpf = valor_cpf


    menu_edicao.lineEdit.setText(str(cpf[0][0]))
    menu_edicao.lineEdit_2.setText(str(cpf[0][1]))
    menu_edicao.lineEdit_3.setText(str(cpf[0][2]))
    menu_edicao.lineEdit_4.setText(str(cpf[0][3]))
    menu_edicao.lineEdit_5.setText(str(cpf[0][4]))
    menu_edicao.show()

    print(cpf)

def delet_users():
    linha = lista_de_usuarios.tableWidget.currentRow()
    lista_de_usuarios.tableWidget.removeRow(linha)

    con = connect(LOCALHOST, USER, PASSWORD, SCHEMA)
    cursor = con.cursor()
    cursor.execute("DELETE FROM clientes where cpf is null")
    sql = f"select CPF from clientes"
    cursor.execute(sql)
    result = cursor.fetchall()
    valor_cpf_delete = result[linha][0]
    vsql = "DELETE FROM clientes where cpf ="+str(valor_cpf_delete)
    cursor.execute(vsql)
    con.commit()

def collect_informations():
    con = connect(LOCALHOST, USER, PASSWORD, SCHEMA)
    nome = control.lineEdit.text()
    cpf = control.lineEdit_2.text()
    email = control.lineEdit_3.text()
    telefone = control.lineEdit_4.text()
    endereço = control.lineEdit_5.text()

    insert(con, cpf, nome, email, endereço, telefone)
    close_connect(con)
    control.lineEdit.setText("")
    control.lineEdit_2.setText("")
    control.lineEdit_3.setText("")
    control.lineEdit_4.setText("")
    control.lineEdit_5.setText("")

def lista_de_usuario_tela():
    lista_de_usuarios.show()
    con = connect(LOCALHOST, USER, PASSWORD, SCHEMA)
    cursor = con.cursor()
    sql = f"select * from clientes"
    cursor.execute(sql)
    result = cursor.fetchall()

    lista_de_usuarios.tableWidget.setRowCount(len(result))
    lista_de_usuarios.tableWidget.setColumnCount(5)
    for i in range(0, len(result)):
        for j in range(0, 5):
            lista_de_usuarios.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))

    close_connect(con)

def consultar_por_cpf():
    consulta = lista_de_usuarios.lineEdit.text()
    con = connect(LOCALHOST, USER, PASSWORD, SCHEMA)
    cursor = con.cursor()
    sql = "select * from clientes WHERE cpf = "+str(consulta)
    cursor.execute(sql)
    result = cursor.fetchall()

    lista_de_usuarios.tableWidget_2.setRowCount(len(result))
    lista_de_usuarios.tableWidget_2.setColumnCount(5)
    for i in range(0, len(result)):
        for j in range(0, 5):
            lista_de_usuarios.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))

app = QtWidgets.QApplication([])
control = uic.loadUi("PYTHON\\qt design\\cadastro\\controle.ui")
control.pushButton.clicked.connect(collect_informations)
control.pushButton_2.clicked.connect(lista_de_usuario_tela)

lista_de_usuarios = uic.loadUi("PYTHON\\qt design\\cadastro\\lista_de_usuarios.ui")
lista_de_usuarios.pushButton.clicked.connect(delet_users)
lista_de_usuarios.pushButton_2.clicked.connect(consultar_por_cpf)
lista_de_usuarios.pushButton_3.clicked.connect(Menu_edit)

menu_edicao = uic.loadUi("D:\\Aplicativos\\python\\programas\\PYTHON\\qt design\\cadastro\\menu_edicao.ui")
menu_edicao.pushButton.clicked.connect(update_infos)

control.show()
app.exec()