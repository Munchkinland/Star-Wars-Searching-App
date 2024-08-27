import requests
import pandas as pd
from time import sleep

# Función para obtener todos los datos de una URL base de SWAPI
def obtener_datos(url):
    datos_completos = []
    while url:
        try:
            respuesta = requests.get(url)
            respuesta.raise_for_status()  # Lanza un error si la respuesta no es 200 OK
            datos = respuesta.json()
            datos_completos.extend(datos['results'])
            url = datos.get('next')  # Usa get() para manejar posibles claves ausentes
            print(f"Obtenidos {len(datos_completos)} registros de {url}")
            sleep(1)  # Pausa para evitar exceso de solicitudes en un corto periodo
        except requests.RequestException as e:
            print(f"Error al obtener datos de {url}: {e}")
            break
    return datos_completos

# URLs base de SWAPI
url_personajes = "https://swapi.dev/api/people/"
url_planetas = "https://swapi.dev/api/planets/"
url_naves = "https://swapi.dev/api/starships/"

# Obtener todos los personajes
print("Obteniendo personajes...")
personajes = obtener_datos(url_personajes)

# Obtener todos los planetas
print("Obteniendo planetas...")
planetas = obtener_datos(url_planetas)

# Obtener todas las naves
print("Obteniendo naves...")
naves = obtener_datos(url_naves)

# Verificar el número total de registros
print(f"Total de personajes: {len(personajes)}")
print(f"Total de planetas: {len(planetas)}")
print(f"Total de naves: {len(naves)}")

# Crear DataFrames de Pandas
df_personajes = pd.DataFrame(personajes)
df_planetas = pd.DataFrame(planetas)
df_naves = pd.DataFrame(naves)

# Guardar en un archivo Excel
with pd.ExcelWriter('star_wars_data.xlsx') as writer:
    df_personajes.to_excel(writer, sheet_name='Personajes', index=False)
    df_planetas.to_excel(writer, sheet_name='Planetas', index=False)
    df_naves.to_excel(writer, sheet_name='Naves', index=False)

print("Datos guardados en star_wars_data.xlsx")
