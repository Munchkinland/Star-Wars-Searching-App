import sqlite3
import os

def get_db_connection():
    conn = sqlite3.connect('star_wars_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def normalize_filename(filename):
    """ Normaliza el nombre del archivo para eliminar espacios y convertir a minúsculas. """
    return filename.lower().replace(' ', '_')

def rename_images_for_type(image_type, folder_path):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Consultar los nombres de la base de datos según el tipo
    cursor.execute(f"SELECT name FROM {image_type}")
    names = cursor.fetchall()
    
    # Normalizar los nombres
    normalized_names = {normalize_filename(name['name'] + '.jpg'): name['name'] for name in names}

    # Renombrar los archivos de imagen en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg'):
            normalized_filename = normalize_filename(filename)
            if normalized_filename in normalized_names:
                old_path = os.path.join(folder_path, filename)
                new_filename = normalized_names[normalized_filename] + '.jpg'
                new_path = os.path.join(folder_path, new_filename)
                
                if old_path != new_path:
                    os.rename(old_path, new_path)
                    print(f'Renombrado: {old_path} -> {new_path}')

    conn.close()

if __name__ == "__main__":
    # Carpetas de imágenes
    folders = {
        'Personajes': 'static/personajes',
        'Planetas': 'static/planetas',
        'Naves': 'static/naves'
    }

    for image_type, folder_path in folders.items():
        rename_images_for_type(image_type, folder_path)
