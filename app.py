from flask import Flask, render_template, request, jsonify, url_for
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('star_wars_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('name', '').strip().lower()
    print(f"Search Query: {query}")  # Depuración

    conn = get_db_connection()
    cursor = conn.cursor()

    # Crear una lista para almacenar resultados
    items = []

    # Buscar en la tabla de Personajes
    cursor.execute("""
        SELECT 'Personajes' AS type, name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld, films, species, vehicles, starships, created, edited, url, image_path 
        FROM Personajes 
        WHERE LOWER(name) LIKE ?
    """, ('%' + query + '%',))
    items.extend(cursor.fetchall())

    # Buscar en la tabla de Planetas
    cursor.execute("""
        SELECT 'Planetas' AS type, name, rotation_period, orbital_period, diameter, climate, gravity, terrain, surface_water, population, residents, films, created, edited, url, image_path 
        FROM Planetas 
        WHERE LOWER(name) LIKE ?
    """, ('%' + query + '%',))
    items.extend(cursor.fetchall())

    # Buscar en la tabla de Naves
    cursor.execute("""
        SELECT 'Naves' AS type, name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity, consumables, hyperdrive_rating, MGLT, starship_class, pilots, films, created, edited, url, image_path 
        FROM Naves 
        WHERE LOWER(name) LIKE ?
    """, ('%' + query + '%',))
    items.extend(cursor.fetchall())

    conn.close()

    # Convertir los resultados a una lista de diccionarios
    result_list = []
    for row in items:
        # Define la carpeta de imágenes basada en el tipo
        image_folder = {
            'Personajes': 'personajes',
            'Planetas': 'planetas',
            'Naves': 'naves'
        }.get(row['type'], '')

        # Construir la ruta de la imagen desde la base de datos
        image_path = row['image_path'] if row['image_path'] else ''
        full_image_path = url_for('static', filename=image_path.replace(os.path.sep, '/'))

        result_dict = {
            'type': row['type'],
            'name': row['name'],
            'height': row['height'] if row['height'] is not None else '',
            'mass': row['mass'] if row['mass'] is not None else '',
            'hair_color': row['hair_color'] if row['hair_color'] is not None else '',
            'skin_color': row['skin_color'] if row['skin_color'] is not None else '',
            'eye_color': row['eye_color'] if row['eye_color'] is not None else '',
            'birth_year': row['birth_year'] if row['birth_year'] is not None else '',
            'gender': row['gender'] if row['gender'] is not None else '',
            'homeworld': row['homeworld'] if row['homeworld'] is not None else '',
            'films': row['films'] if row['films'] is not None else '',
            'species': row['species'] if row['species'] is not None else '',
            'vehicles': row['vehicles'] if row['vehicles'] is not None else '',
            'starships': row['starships'] if row['starships'] is not None else '',
            'created': row['created'] if row['created'] is not None else '',
            'edited': row['edited'] if row['edited'] is not None else '',
            'url': row['url'] if row['url'] is not None else '',
            'image_path': full_image_path
        }
        print(f"Result Dict: {result_dict}")  # Depuración
        result_list.append(result_dict)
    
    return jsonify(result_list)

if __name__ == "__main__":
    app.run(debug=True)

    app.run(debug=True)


