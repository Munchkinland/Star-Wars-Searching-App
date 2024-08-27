import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re
import sqlite3

# Función para descargar la imagen
def download_image(url, folder, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if not os.path.exists(folder):
            os.makedirs(folder)
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return filepath
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

# Función para buscar imágenes en Bing
def search_images(query, num_images=1):
    search_url = f"https://www.bing.com/images/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching search results for {query}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all('a', {'class': 'iusc'})
    
    img_urls = []
    for img_tag in image_tags:
        m = re.search(r'"murl":"(http[^"]+)"', str(img_tag))
        if m:
            img_url = m.group(1)
            img_urls.append(img_url)
            if len(img_urls) >= num_images:
                break

    return img_urls

# Función para procesar cada hoja y guardar en la base de datos
def process_sheet(sheet_name, conn, num_images=1):
    df = pd.read_excel('star_wars_data.xlsx', sheet_name=sheet_name)
    df['image_path'] = None

    folder_name = sheet_name.lower()

    for index, row in df.iterrows():
        name = row['name']
        print(f"Processing {name}...")
        img_urls = search_images(name, num_images)
        if img_urls:
            filename = f"{name}.jpg".replace(' ', '_')
            filepath = download_image(img_urls[0], folder_name, filename)
            df.at[index, 'image_path'] = filepath

    df.to_sql(sheet_name, conn, if_exists='replace', index=False)
    print(f"Finished processing {sheet_name}.")

if __name__ == "__main__":
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('star_wars_data.db')

    sheets = ['Personajes', 'Planetas', 'Naves']  # Nombres de las hojas

    for sheet in sheets:
        process_sheet(sheet, conn, num_images=1)

    conn.close()
