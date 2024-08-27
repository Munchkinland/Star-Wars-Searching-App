import sqlite3

def print_table_structure(table_name):
    conn = sqlite3.connect('star_wars_data.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    for column in columns:
        print(column)
    conn.close()

# Imprimir la estructura de cada tabla
print_table_structure('Personajes')
print_table_structure('Planetas')
print_table_structure('Naves')
