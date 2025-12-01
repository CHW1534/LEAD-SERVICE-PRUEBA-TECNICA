

Microservicio de Gestión de Leads  
Este proyecto es una API backend de alto rendimiento construida con Python y FastAPI, diseñada para recibir, validar, almacenar y buscar clientes potenciales (leads) utilizando algoritmos de similitud. con enriquecimiento de Datos (Geocoding): Integración con API Ninjas para convertir automáticamente el nombre de la ciudad en coordenadas geográficas (Latitud y Longitud) al momento de crear  leads.



##Estructura del Proyecto

LEAD-SERVICE/
├── app/
│   ├── services/
│   │   ├── api_client.py    # Conexión con APIs externas
│   │   └── vector_service.py # Lógica de vectores/similitud
│   ├── db.py                # Configuración de base de datos
│   ├── main.py              # Punto de entrada y Endpoints
│   ├── models.py            # Esquemas de Pydantic (Validación)
│   └── schemas.py           # Modelos ORM (Tablas BD)
├── .env.example             # Ejemplo de variables de entorno
├── requisitos.txt         # Dependencias


## Requisitos previos y instalacion
###Instalación de Python 3.10
Este proyecto requiere específicamente Python 3.10.X
Ve a [Python.org Downloads](https://www.python.org/downloads/release/python-3100/).
Descarga el "Windows installer (64-bit)".
Al ejecutarlo, marca la casilla que dice "Add Python 3.10 to PATH" antes de dar clic en "Install Now".
Verifica abriendo una terminal y escribiendo: `python --version`.

###Instalación de PostgreSQL
Necesitamos este motor de base de datos para simular un entorno de producción real.
Ve a [PostgreSQL Downloads](https://www.postgresql.org/download/) y baja el instalador para tu sistema operativo.
Instalar: Sigue los pasos del asistente.
Se te pedirá una contraseña para el superusuario (`postgres`). ¡Recuérdala! (suele usarse `root` o `admin` en desarrollo local).
El puerto por defecto es `5432`. Déjalo así.
Herramienta Visual (Opcional):
Se instalará pgAdmin 4 automáticamente, que sirve para ver tus tablas gráficamente.

Instalación del Proyecto (Paso a Paso)
Abrir la terminal powershell
Clonar el Repositorio con el siguente comando
git clone https://github.com/CHW1534/LEAD-SERVICE-PRUEBA-TECNICA.git

Ingresar el siguiente comando para ubicarse en la carpeta raiz del proyecto
cd LEAD-SERVICE-PRUEBA-TECNICA

Crear el Entorno Virtual (De esta manera aislamos dependencias para que no interfieran con otros proyectos.)
python -m venv .venv  (Para crear el entorno virtual )

Activar entorno virtual
.\.venv\Scripts\Activate

Instalar Dependencias
pip install -r requisitos.txt
Explicación de Dependencias
fastapi & uvicorn: Framework y Servidor Web de alto rendimiento.
sqlalchemy: ORM que traduce nuestro código Python a comandos SQL para Postgres.
psycopg2-binary: El "traductor" necesario para que SQLAlchemy hable con PostgreSQL.
pydantic: Validador de datos (asegura que los emails sean emails).
httpx: Cliente para consumir APIs externas de forma asíncrona.

“Lee automaticamente el archivo requisitos.txt línea por línea e instala exactamente las librerías necesarias para el proyecto en el entorno virtual activo”.

Configuración de Base de Datos (PostgreSQL)
Para que Python se conecte a PostgreSQL, necesitamos preparar la base de datos y el driver.
pip install psycopg2-binary(Omitir se ah instalado el driver durante la instalacion requisitos.txt)

Crear la Base de Datos
Abre tu terminal de SQL (SQL Shell o pgAdmin) y ejecuta el siguiente comando para crear el contenedor de datos
CREATE DATABASE leads_db;

Configurar Variables de Entorno (.env)
Crea el archivo .env en la raíz del proyecto.

Configura la URL de conexión usando tus credenciales de Postgres. 
Sintaxis: postgresql://USUARIO:CONTRASEÑA@LOCALHOST/NOMBRE_DB

# Ejemplo de archivo .env
# Reemplaza 'postgres' y 'tupassword' con TUS datos reales de instalación
# Configuración de Base de Datos
DATABASE_URL="postgresql://postgres:root@localhost/leads_db"
# API Ninjas (Geocoding)
# Regístrate en: https://api-ninjas.com/api/geocoding
EXTERNAL_API_URL="https://api.api-ninjas.com/v1/geocoding"
EXTERNAL_API_KEY="tu_api_key_de_ninjas_aqui"

Una vez configurado el .env y creada la base de datos en Postgres, arranca la aplicación:
uvicorn app.main:app --reload
verás: INFO: Uvicorn running on http://127.0.0.1:8000.
Al arrancar por primera vez, el sistema creará automáticamente las tablas en PostgreSQL.

Tienes dos formas de probar los endpoints de la API: mediante la interfaz visual interactiva o vía terminal.

Opción 1: Interfaz Visual (Swagger UI)
Abre tu navegador y ve a: http://127.0.0.1:8000/docs
Verás una lista con 4 endpoints.
GET/health
Health Check

POST/api/leads/
Create Lead

GET/api/leads/
Read Leads

POST/api/leads/search
Search Leads
Haz clic en el botón "Try it out" de cada uno, llena los datos y dale a "Execute"

EJEMPLO DATOS DE PRUEBAS MEDIANTE CURL EN POWERSHELL
Crear Lead (POST)
curl -X POST "http://127.0.0.1:8000/api/leads/" -H "accept: application/json" -H "Content-Type: application/json" -d '{"name": "Tacos El Rey", "email": "rey@tacos.com", "phone": "555-1111", "restaurant_type": "Mexicana", "city": "Ciudad de Mexico"}'

curl -X POST "http://127.0.0.1:8000/api/leads/" -H "accept: application/json" -H "Content-Type: application/json" -d '{"name": "Luigi Pizza", "email": "luigi@pizza.com", "phone": "555-2222", "restaurant_type": "Italiana", "city": "Ciudad de Mexico"}'
Crear un restaurante nuevo. Nota: Recuerda que esto consumirá tu API de Ninjas para buscar la latitud/longitud.
Listar Todos (GET)
curl -X GET "http://127.0.0.1:8000/api/leads/?skip=0&limit=10" -H "accept: application/json"
Buscar (Search con Similitud)
Vamos a buscar "tacos" en CDMX. Debería salir primero "Tacos El Rey".
curl -X POST "http://127.0.0.1:8000/api/leads/search" -H "accept: application/json" -H "Content-Type: application/json" -d '{"query": "tacos en ciudad de mexico"}'


