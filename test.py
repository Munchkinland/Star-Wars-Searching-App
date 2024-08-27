import sqlite3

def print_db_contents():
    conn = sqlite3.connect('star_wars_data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Verificar contenido de la tabla Personajes
    cursor.execute("SELECT * FROM Personajes LIMIT 10")
    rows = cursor.fetchall()
    print("Personajes:")
    for row in rows:
        print(dict(row))

    # Verificar contenido de la tabla Planetas
    cursor.execute("SELECT * FROM Planetas LIMIT 10")
    rows = cursor.fetchall()
    print("Planetas:")
    for row in rows:
        print(dict(row))

    # Verificar contenido de la tabla Naves
    cursor.execute("SELECT * FROM Naves LIMIT 10")
    rows = cursor.fetchall()
    print("Naves:")
    for row in rows:
        print(dict(row))

    conn.close()

print_db_contents()
