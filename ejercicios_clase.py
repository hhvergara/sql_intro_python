#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de clase
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import sqlite3

# https://extendsclass.com/sqlite-browser.html


def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect('secundaria.db')

    # Crear el cursor para poder ejecutar las querys
    c = conn.cursor()

    # Ejecutar una query
    c.execute("""
                DROP TABLE IF EXISTS estudiante;
            """)

    # Ejecutar una query
    c.execute("""
            CREATE TABLE estudiante(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT NOT NULL,
                [age] INTEGER NOT NULL,
                [grade] INTEGER,
                [tutor] TEXT
            );
            """)

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()


def fill_db(group):
    print('Completemos esta tablita!')
    # Llenar la tabla de la secundaria con al munos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá ocmpletarlo
    # name --> El nombre del alumnos (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # profesor --> nombre de su tutor

    # Se debe utilizar la sentencia INSERT.
    # Observar que hay campos como "grade" y "profesor" que no son obligatorios
    # en el schema creado, puede obivar en algunos casos completar esos campos

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()

    # values = [name, age, grade, tutor]

    c.executemany("""
        INSERT INTO estudiante (name, age, grade, tutor)
        VALUES (?, ?, ?, ?);""", group)

    conn.commit()

    conn.close()

def fetch():
    print('Comprovemos su contenido, ¿qué hay en la tabla?')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # todas las filas con todas sus columnas
    # Utilizar fetchone para imprimir de una fila a la vez

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM estudiante 
        """)
    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row)

    conn.close()


def search_by_grade(grade):
    print('Operación búsqueda!')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # aquellos estudiantes que se encuentra en en año "grade"

    # De la lista de esos estudiantes el SELECT solo debe traer
    # las siguientes columnas por fila encontrada:
    # id / name / age

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    c.execute("SELECT id, name, age FROM estudiante WHERE grade=5;")
    data = c.fetchall()  # Primer forma, imprime todos los casos en que cumple condicion
    print(data)

    c.execute("SELECT * FROM estudiante;")
    while True:
        row = c.fetchone()
        row_grade = row[3]  # En este caso solo imprime el primero que cumple la condicion
        if row_grade is grade:
            print(row[:3])
            break

    c.execute("SELECT * FROM estudiante;")
    while True:
        row = c.fetchone() # En este caso imprime todos los casos que cumplen la condicion
        if row is None:
            break
        row_grade = row[3]
        if row_grade is grade:
            print(row[:3])

    #  Esta es otra forma de imprimir todos los casos en que cumple la condicion
    for row in c.execute('SELECT id, name, age FROM estudiante WHERE grade=3'):
        print(row)

    conn.close()


def insert(grade):
    print('Nuevos ingresos!')
    # Utilizar la sentencia INSERT para ingresar nuevos estudiantes
    # a la secundaria

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()

    c.execute("""INSERT INTO estudiante (name, age)
        VALUES (?, ?);""", new_student)
    conn.commit()
    conn. close()

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    c.execute("SELECT * FROM estudiante WHERE name='You';")
    data = c.fetchall()
    print(data)
    c.close()


def modify(id, name):
    print('Modificando la tabla')
    # Utilizar la sentencia UPDATE para modificar aquella fila (estudiante)
    # cuyo id sea el "id" pasado como parámetro,
    # modificar su nombre por "name" pasado como parámetro

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    rowcount = c.execute("UPDATE estudiante SET name = ? WHERE id = ?",
     (name, id)).rowcount
    print(rowcount)
    conn.commit()
    conn.close()

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    c.execute("SELECT * FROM estudiante WHERE id=2")
    data = c.fetchall()
    print(data)
    conn.close


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)

    group =[('Ruben', 16, 5, 'Carlos'),
            ('Marcos', 14, 3, 'Gloria'),
            ('Anabella', 16, 5, ''),
            ('Alejandra', 13, 2, 'Nora'),
            ]
    fill_db(group)
    fetch()

    grade = 5
    search_by_grade(grade)

    new_student = ['You', 16]
    insert(new_student)

    name = '¿Inove?'
    id = 2
    modify(id, name)
