import sqlite3
import os

# Conectar a la base de datos
conn = sqlite3.connect('star_wars_data.db')
cursor = conn.cursor()

# Directorio de las imágenes
base_image_dir = 'static'

# Lista de tablas y carpetas correspondientes
tables = {
    'Personajes': 'personajes',
    'Planetas': 'planetas',
    'Naves': 'naves'
}

# Función para obtener la ruta completa de la imagen
def get_image_path(name, image_folder):
    image_name = name.replace(' ', '-') + '.jpg'
    image_path = os.path.join(image_folder, image_name)
    return image_path

# Actualizar la ruta de la imagen en la base de datos
for table, folder in tables.items():
    print(f"Updating {table}...")
    cursor.execute(f"SELECT name FROM {table}")
    rows = cursor.fetchall()
    for row in rows:
        name = row[0]
        image_path = get_image_path(name, folder)
        # Verificar si la imagen existe
        if os.path.isfile(os.path.join(base_image_dir, image_path)):
            cursor.execute(f"UPDATE {table} SET image_path = ? WHERE name = ?", (image_path, name))
            print(f"Updated {name} with path {image_path}")
        else:
            print(f"Image not found for {name}")

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()
