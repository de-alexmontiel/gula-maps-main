import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Función para obtener detalles del lugar
def obtener_detalles_lugar(place_id, api_key):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number&key={api_key}'
    response = requests.get(url)
    json_data = response.json()
    return json_data['result']

# Función para obtener place_ids existentes en Google Sheets
def obtener_place_ids_existentes(sheet):
    records = sheet.get_all_records()
    existing_place_ids = [row['Place ID'] for row in records]
    return set(existing_place_ids)

# Función para obtener establecimientos y guardarlos en Google Sheets
def obtener_establecimientos(latlon, radius, api_key, sheet, tipo_lugar):
    url_base = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latlon}&radius={radius}&type={tipo_lugar}&key={api_key}'
    url = url_base
    paginacion = 0
    todo = []

    # Obtener place_ids existentes para evitar duplicados
    existing_place_ids = obtener_place_ids_existentes(sheet)

    # Headers para las columnas
    headers = ['Place ID', 'Nombre', 'Cercanía', 'Dirección', 'Latitud', 'Longitud', 'Rating', 'Abierto Ahora', 'Tipos', 'Nivel de Precios', 'Estado del Negocio', 'Teléfono', 'URL del Lugar']
    
    # Añadir encabezados solo si no están
    if len(sheet.get_all_records()) == 0:
        sheet.append_row(headers)

    while True:
        response = requests.get(url)
        json_data = response.json()
        results = json_data['results']

        # Avisar estado de búsqueda
        print(f'Procesando página {paginacion + 1} de resultados para "{tipo_lugar}"...')
        
        for result in results:
            place_id = result['place_id']

            # Validar si el place_id ya existe para evitar duplicados
            if place_id in existing_place_ids:
                print(f'Ya existe {place_id}. Saltando...')
                continue  # Saltar si ya existe

            details = obtener_detalles_lugar(place_id, api_key)
            name = result['name']
            vicinity = result.get('vicinity', 'No disponible')
            formatted_address = result.get('formatted_address', 'No disponible')
            location = result['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            rating = result.get('rating', 0)
            opening_hours = result.get('opening_hours', {}).get('open_now', 'No disponible')
            types = ", ".join(result.get('types', []))
            price_level = result.get('price_level', 'No disponible')
            business_status = result.get('business_status', 'No disponible')
            phone = details.get('formatted_phone_number', 'No disponible')
            
            # URL del lugar en Google Maps
            place_url = f'https://www.google.com/maps/search/?api=1&query={name.replace(" ", "+")}'
            
            # Añadir fila de resultados a la lista
            todo.append([place_id, name, vicinity, formatted_address, lat, lng, rating, opening_hours, types, price_level, business_status, phone, place_url])

        # Escribir los datos en Google Sheets en una sola llamada
        print(f'Escribiendo datos en Google Sheets desde página {paginacion + 1} para "{tipo_lugar}"...')
        if todo:
            sheet.append_rows(todo)  # Escribe todas las filas de una sola vez
        todo = []  # Limpiar la lista para los nuevos resultados
        print(f'Terminé de escribir los datos de la página {paginacion + 1} para "{tipo_lugar}".')

        # Manejar paginación si existe un token de página siguiente
        if 'next_page_token' in json_data:
            paginacion += 1
            print(f'Se detectó una página siguiente. Esperando 2 segundos antes de continuar a la página {paginacion + 1} para "{tipo_lugar}"...')
            time.sleep(2)  # Esperar para que el token sea válido
            next_page_token = json_data['next_page_token']
            url = f"{url_base}&pagetoken={next_page_token}"
        else:
            print(f'No hay más páginas para "{tipo_lugar}". Se procesaron {paginacion + 1} páginas en total.')
            break

# Autenticación con Google Sheets
def conectar_google_sheets(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

# Función principal para iniciar el script
def main():
    api_key = 'AIzaSyCBJFNQ18_xSW-SwNdywldYZC4Ck0W1FyA'  # Reemplaza con tu clave de API de Google
    latlon = '25.682809737499124, -100.31794403410137' #'18.40207318673618, -93.20988629430245'  # Coordenadas Ciudad, Ejemplo: Paraiso Tabasco
    radius = 10000  # Radio de búsqueda en metros
    sheet_name = 'Establecimientos'  # Nombre de tu hoja de Google Sheets

    # Lista de tipos de lugares a buscar
    tipos_lugares = ['restaurant', 'bar', 'cafe']

    # Conectar con Google Sheets
    print('Conectando con Google Sheets...')
    sheet = conectar_google_sheets(sheet_name)
    print('Conexión con Google Sheets establecida.')

    # Iterar sobre los tipos de lugares y obtener establecimientos para cada tipo
    for tipo in tipos_lugares:
        print(f'Iniciando obtención de establecimientos para "{tipo}"...')
        obtener_establecimientos(latlon, radius, api_key, sheet, tipo)
        print(f'Finalizada la obtención de establecimientos para "{tipo}".')

if __name__ == '__main__':
    main()
