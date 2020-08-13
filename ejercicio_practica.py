'''
SQL [Python]
Ejercicios de clase
---------------------------
Autor: Ishef Glatzel
Version: 1.0

Descripcion:
Transformacion de archivo legacy .csv
a base de datos .sql
'''
__author__ = "Ishef Glatzel"
__email__ = "ishefglatzel@gmail.com"
__version__ = "1.0"

import os
import re

import csv
import sqlite3

direccion = (os.path.dirname(os.path.abspath(__file__)))
database_path = (direccion + '\databases')


def create_schema():
    """
    Crea una database `libreria.db` y una tabla `libro` con el formato:
        [id] INTEGER PRIMARY KEY AUTOINCREMENT,
        [title] TEXT NOT NULL,
        [pags] INTEGER,
        [author] TEXT

    NOTA: En caso de ya existir dicha tabla, la elimina
    """
    conn = sqlite3.connect('{}\libreria.db'.format(database_path))
    c = conn.cursor()

    c.execute("""
                DROP TABLE IF EXISTS libro;
            """)

    c.execute("""
            CREATE TABLE libro(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [title] TEXT NOT NULL,
                [pags] INTEGER,
                [author] TEXT
            );
            """)

    conn.commit()
    conn.close()


def fill():
    """
    Rellena la tabla `libro` del archivo `libreria.db` con los datos del 
    archivo `libreria.csv`
    """
    def fetch_data():
        """
        Recorre el csv mencionado y recolecta los datos\n
        Return: Devuelve una lista con tuplas con el formato:
            ('titulo', 'cantidad_paginas', 'autor')
        """
        with open('{}\libreria.csv'.format(database_path)) as csvfile:
            data = list(csv.DictReader(csvfile))
            return [( libro['titulo'], libro['cantidad_paginas'], libro['autor'] ) for libro in data]
            
    def insert_group(group):
        """
        Inserta el conjunto de datos retornado por `fetch_data()` en el archivo.db mencionado
        """
        conn = sqlite3.connect('{}\libreria.db'.format(database_path))
        c = conn.cursor()

        c.executemany("""
            INSERT INTO libro (title, pags, author)
            VALUES (?,?,?);""", group)
        conn.commit()
        conn.close()

    dataset = fetch_data()
    insert_group(dataset)
        

def fetch(id=0):
    """
    Retorna en pantalla el resultado de hacer una query a la tabla `libro` del archivo `libreria.db`\n
    @param id: `int` ID que sera buscado:\n
        ID = 0: Retorna la tabla entera
        ID mayor que 0: Retorna la fila correspondiente a esa ID o un aviso si no existe
        ID menor que 0 or type(ID) != int: Retorna una advertencia de que no se admiten IDs negativas o strings
    """
    conn = sqlite3.connect('{}\libreria.db'.format(database_path))
    c = conn.cursor()

    if id == 0:
        c.execute('SELECT * FROM libro')
        print('----------------------------------------------------------------------------------------------------')
        while True:
            row = c.fetchone()
            if row is None:
                break
            print('ID: {row[0]} \t| NOMBRE: {row[1]}  |  PAGINAS: {row[2]}  |  AUTOR: {row[3]}'.format(row=row))
        print('----------------------------------------------------------------------------------------------------')


    elif id > 0:
        try:
            print('----------------------------------------------------------------------------------------------------')
            c.execute("""SELECT * FROM libro WHERE id = {}""".format(id))
            row = c.fetchone()
            if row == None:
                print('La ID buscada esta fuera de rango')
                print('----------------------------------------------------------------------------------------------------')
                return
            print('ID: {row[0]} \t| NOMBRE: {row[1]}  |  PAGINAS: {row[2]}  |  AUTOR: {row[3]}'.format(row=row))
        except sqlite3.Error as err:
            print(err)

        print('----------------------------------------------------------------------------------------------------')

    else:
        print('----------------------------------------------------------------------------------------------------')
        print('No se aceptan IDs Negativas (-) ni strings') 
        print('----------------------------------------------------------------------------------------------------')


def search_author(book_title):
    """
    Retorna en pantalla el autor de hacer una query a la tabla `libro` del archivo `libreria.db`\n
    @param book_title: `str` nombre del libro del que sera buscado su autor:\n
    """
    conn = sqlite3.connect('{}\libreria.db'.format(database_path))
    c = conn.cursor()
    c.execute("""SELECT author FROM libro WHERE title = '{}'""".format(book_title)) 
    print('----------------------------------------------------------------------------------------------------')
    while True:
        row = c.fetchone()
        if row is None:
            print('No se ha podido localizar un libro con esa ID')
            break
        print('AUTOR: {row[0]}'.format(row=row))
    print('----------------------------------------------------------------------------------------------------')


def update_book(name, id):
    """
    Modifica el nombre de un libro de la tabla `libro` del arhcivo `libreria.db`\n
    @param name: `str` Nombre que reemplazara al libro en cuestion\n
    @param id: `int` ID utilizada para rastrear el libro a actualizar
    """
    conn = sqlite3.connect('{}\libreria.db'.format(database_path))
    c = conn.cursor()
    c.execute("""UPDATE libro SET title = '{}' WHERE id = '{}'""".format(name, id)) 
    conn.commit()
    print('----------------------------------------------------------------------------------------------------')
    fetch(id)
    print('----------------------------------------------------------------------------------------------------')
    conn.close()


def delete_book(id):
    """
    Elimina una fila de la tabla `libro` del arhcivo `libreria.db`\n
    @param id: `int` ID utilizada para rastrear el libro a eliminar
    """
    conn = sqlite3.connect('{}\libreria.db'.format(database_path))
    c = conn.cursor()
    c.execute("""DELETE FROM libro WHERE id = '{}'""".format(id)) 
    conn.commit()
    print('----------------------------------------------------------------------------------------------------')
    while True:
        row = c.fetchone()
        if row is None:
            break
        print('AUTOR: {row[0]}'.format(row=row))
    print('----------------------------------------------------------------------------------------------------')
    conn.close()


if __name__ == "__main__":
    # Crear DB
    create_schema()

    # Completar la DB con el CSV
    fill()
    print('----------------------------------------------------------------------------------------------------')
    while True:
        print('1. Buscar fila por ID | Imprimir tabla entera')
        print('2. Buscar autor por libro')
        print('3. Actualizar nombre-libro por ID')
        print('4. Borrar libro por ID')
        print('5. Salir')
        print('----------------------------------------------------------------------------------------------------')
        entrada = input('\n')

        if entrada == '1':
            id = int(input('Introduzca la ID de la fila a mostrar\n(0: Tabla entera)\n'))
            fetch(id)

        elif entrada == '2':
            book = input('Introduzca el libro del autor a encontrar:\n')
            search_author(book)
            
        elif entrada == '3':
            id = int(input('Introduzca la ID del libro a actualizar:\n'))
            name = input('Introduza el nuevo nombre del libro:\n')
            update_book(name, id)

        elif entrada == '4':
            id = int(input('Introduzca la ID del libro a eliminar:\n'))
            delete_book(id)

        elif entrada == '5':
            quit()
    


    # Leer filas
    # fetch()  # Ver todo el contenido de la DB
    # fetch(3)  # Ver la fila 3
    # fetch(20)  # Ver la fila 20

    # # Buscar autor
    # search_author('Relato de un naufrago')