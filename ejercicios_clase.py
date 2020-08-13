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

import os
import sqlite3

direccion = (os.path.dirname(os.path.abspath(__file__)))
database_path = (direccion + '\databases')

# https://extendsclass.com/sqlite-browser.html


def insert_grupo(group):
    conn = sqlite3.connect('{}\secundaria.db'.format(database_path))
    c = conn.cursor()

    c.executemany("""
        INSERT INTO estudiante (name, age, grade)
        VALUES (?,?,?);""", group)
    conn.commit()
    conn.close()


def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect('{}\secundaria.db'.format(database_path))
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
                [grade] INTEGER NULL,
                [profesor] TEXT NULL
            );
            """)

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()


def fill_db():
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
    group = [('Rex', 20, 3),
             ('Ray', 13, 2),
             ('Phil', 20, 1),
             ('Max', 15, 4),
             ('Ren', 17, 3)]
    insert_grupo(group)


def fetch():
    print('Comprovemos su contenido, ¿qué hay en la tabla?')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # todas las filas con todas sus columnas
    # Utilizar fetchone para imprimir de una fila a la vez
    conn = sqlite3.connect('{}\secundaria.db'.format(database_path))
    c = conn.cursor()
    c.execute('SELECT * FROM estudiante')
    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row)

    conn.close()


def search_by_grade(grade):
    print('Operación búsqueda!')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # aquellos estudiantes que se encuentra en el año "grade"

    # De la lista de esos estudiantes el SELECT solo debe traer
    # las siguientes columnas por fila encontrada:
    # id / name / age
    conn = sqlite3.connect('{}\secundaria.db'.format(database_path))
    c = conn.cursor()
    c.execute('SELECT e.id, e.name, e.age FROM estudiante AS e WHERE e.grade = "{}"'.format(grade))
    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row)


def insert(grade):
    print('Nuevos ingresos!')
    # Utilizar la sentencia INSERT para ingresar nuevos estudiantes
    # a la secundaria
    conn = sqlite3.connect('{}\secundaria.db'.format(database_path))
    c = conn.cursor()
    c.execute("""
            INSERT INTO estudiante (name, age)
            VALUES (?,?);""", grade)
    conn.commit()
    conn.close()


def modify(name, id):
    input()
    print('Modificando la tabla')
    modification = (name, id)
    print(modification)
    # Utilizar la sentencia UPDATE para modificar aquella fila (estudiante)
    # cuyo id sea el "id" pasado como parámetro,
    # modificar su nombre por "name" pasado como parámetro
    conn = sqlite3.connect('{}\secundaria.db'.format(database_path))
    c = conn.cursor()

    c.execute("""
            UPDATE estudiante
            SET name = ? WHERE id = ?;""", modification)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
    fill_db()
    fetch()

    grade = 3
    search_by_grade(grade)

    new_student = ['You', 16]
    insert(new_student)

    name = '¿Inove?'
    id = 2
    modify(name, id)
