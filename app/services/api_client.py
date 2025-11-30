import httpx
import os

# Configuraciones de la API externa
API_KEY = os.getenv("EXTERNAL_API_KEY")
BASE_URL = os.getenv("EXTERNAL_API_URL")

async def fetch_city_info(city: str):
 # Realiza una llamada asíncrona a una API externa para obtener información de la ciudad
    params = {"city": city}
    headers = {"X-Api-Key": API_KEY}

    # Usamos un cliente asíncrono para no bloquear el servidor mientras esperamos la respuesta
    async with httpx.AsyncClient() as client:
        try:
            #Se establece un timeout de 10 segundos para evitar esperas largas si la API falla
            response = await client.get(BASE_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json() # Retorna la respuesta JSON de la API externa
        except httpx.HTTPError as e:
            print(f"Error al llamar a la API externa: {e}")
            return {"error": "No se pudo obtener información de la ciudad"}