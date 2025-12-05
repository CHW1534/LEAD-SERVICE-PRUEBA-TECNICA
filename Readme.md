
# Microservicio de Gestión de Leads

Este proyecto es una API backend construida con Python y FastAPI, diseñada para recibir, validar, almacenar y buscar clientes potenciales (leads) utilizando algoritmos de similitud, con enriquecimiento de datos (Geocoding).
Incluye integración con **API Ninjas** para convertir automáticamente el nombre de la ciudad en coordenadas geográficas (Latitud y Longitud) al momento de crear leads.

---

## Estructura del Proyecto

```
LEAD-SERVICE/
├── app/
│   ├── services/
│   │   ├── api_client.py     # Conexión con APIs externas
│   │   └── vector_service.py # Lógica de vectores/similitud
│   ├── db.py                  # Configuración de base de datos
│   ├── main.py                # Punto de entrada y Endpoints
│   ├── models.py              # Esquemas de Pydantic (Validación)
│   └── schemas.py             # Modelos ORM (Tablas BD)
├── .env.example               # Ejemplo de variables de entorno
├── requisitos.txt             # Dependencias
```

---

## Requisitos previos e instalación

### Instalación de Python 3.10

Este proyecto requiere específicamente **Python 3.10.X**.

1. Ve a: [https://www.python.org/downloads/release/python-3100/](https://www.python.org/downloads/release/python-3100/)
2. Descarga: **Windows installer (64-bit)**
3. Al instalar, marca la casilla: **Add Python 3.10 to PATH**
4. Verifica en terminal:

```bash
python --version
```

---

### Instalación de PostgreSQL

Necesitamos este motor de base de datos para simular un entorno de producción real.

1. Ve a: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
2. Descarga el instalador para tu sistema operativo
3. Sigue el asistente de instalación
4. Define contraseña para el usuario `postgres` (recuerda esta contraseña)
5. Deja el puerto por defecto: **5432**
6. Opcional: se instalará **pgAdmin 4** (interfaz gráfica)

---

## Instalación del Proyecto (Paso a Paso)

1. Abre tu terminal (PowerShell)

2. Clona el repositorio:

```bash
git clone https://github.com/CHW1534/LEAD-SERVICE-PRUEBA-TECNICA.git
```

3. Entra a la carpeta raíz del proyecto:

```bash
cd LEAD-SERVICE-PRUEBA-TECNICA
```

4. Crear el entorno virtual (aislar dependencias):

```bash
python -m venv .venv
```

5. Activar entorno virtual:

```bash
.\.venv\Scripts\Activate
```

6. Instalar dependencias:

```bash
pip install -r requisitos.txt
```

### Explicación de Dependencias

* **fastapi & uvicorn**: Framework y servidor web de alto rendimiento.
* **sqlalchemy**: ORM que traduce código Python a SQL para PostgreSQL.
* **psycopg2-binary**: Driver para conectar Python con PostgreSQL.
* **pydantic / pydantic[email]**: Validador de datos (asegura emails válidos).
* **httpx**: Cliente para consumir APIs externas de forma asíncrona.
* **python-dotenv**: Permite cargar las variables desde el archivo `.env`.
* **email-validator**: Validación estricta de correos electrónicos.

> El comando `pip install -r requisitos.txt` lee automáticamente el archivo línea por línea e instala exactamente las librerías necesarias en el entorno virtual activo.

---

## Configuración de Base de Datos (PostgreSQL)

Antes de ejecutar el proyecto, debes crear la base de datos en tu equipo local (**localhost**) usando PostgreSQL.

### Crear la base de datos en localhost

Tienes dos formas principales de hacerlo:

### Opción 1: Usando SQL Shell (psql)

1. Abre **SQL Shell (psql)** desde el menú de inicio de Windows.
2. Cuando te lo pida, presiona **Enter** para aceptar los valores por defecto:

   * Server: `localhost`
   * Database: `postgres`
   * Port: `5432`
   * Username: `postgres`
3. Ingresa la contraseña que configuraste al instalar PostgreSQL.
4. Una vez dentro, ejecuta el siguiente comando:

```sql
CREATE DATABASE leads_db;
```

5. Si la creación fue exitosa verás un mensaje similar a:

```
CREATE DATABASE
```

La base de datos ya estará creada en tu **localhost:5432**.

---

### Opción 2: Usando pgAdmin 4 (modo gráfico)

1. Abre **pgAdmin 4**.
2. Conéctate al servidor `PostgreSQL` (localhost).
3. En el menú lateral, haz clic derecho sobre **Databases** → **Create** → **Database...**
4. En el campo **Database**, escribe:

```
leads_db
```

5. Da clic en **Save**.

La base de datos quedará creada en tu máquina local.

---


## Configurar Variables de Entorno (.env)

Crea un archivo llamado `.env` en la raíz del proyecto y pega el contenido:

```
DATABASE_URL="postgresql://postgres:root@localhost/leads_db"

EXTERNAL_API_URL="https://api.api-ninjas.com/v1/geocoding"
EXTERNAL_API_KEY="tu_api_key_de_ninjas_aqui"
```

> Reemplaza `postgres` y `root` por tus credenciales reales.

---

## Ejecución del Servidor

Una vez creado el `.env` y la base de datos:

```bash
uvicorn app.main:app --reload
```

Verás:

```
INFO: Uvicorn running on http://127.0.0.1:8000
```

Al iniciar por primera vez, el sistema crea las tablas automáticamente.

---

## Probar la API

### Opción 1: Swagger (Interfaz Visual)

Abre en el navegador:

```
http://127.0.0.1:8000/docs
```

Endpoints disponibles:

* **GET** `/health` → Health Check
* **POST** `/api/leads/` → Crear Lead
* **GET** `/api/leads/` → Listar Leads
* **POST** `/api/leads/search` → Buscar por similitud

Haz clic en **Try it out**, ingresa datos y luego **Execute**.

---

## Ejemplos con CURL (PowerShell)

### Crear Lead

```bash
curl -X POST "http://127.0.0.1:8000/api/leads/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\": \"Tacos El Rey\", \"email\": \"rey@tacos.com\", \"phone\": \"555-1111\", \"restaurant_type\": \"Mexicana\", \"city\": \"Ciudad de Mexico\"}"
```

```bash
curl -X POST "http://127.0.0.1:8000/api/leads/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\": \"Luigi Pizza\", \"email\": \"luigi@pizza.com\", \"phone\": \"555-2222\", \"restaurant_type\": \"Italiana\", \"city\": \"Ciudad de Mexico\"}"
```

> Nota: cada creación consume la API de Ninjas para obtener latitud y longitud.

---

### Listar Todos

```bash
curl -X GET "http://127.0.0.1:8000/api/leads/?skip=0&limit=10" -H "accept: application/json"
```

---

### Buscar por similitud

Buscar "tacos en ciudad de mexico":

```bash
curl -X POST "http://127.0.0.1:8000/api/leads/search" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"query\": \"tacos en ciudad de mexico\"}"
```

Debería aparecer primero: **Tacos El Rey**.


---

## Probar la API

### Opción 1: Swagger (Interfaz Visual)

Abre en el navegador:

```
http://127.0.0.1:8000/docs
```

Endpoints disponibles:

* **GET** `/health` → Health Check
* **POST** `/api/leads/` → Crear Lead
* **GET** `/api/leads/` → Listar Leads
* **POST** `/api/leads/search` → Buscar por similitud

Haz clic en **Try it out**, ingresa datos y luego **Execute**.

---

## Ejemplos con CURL (PowerShell)

### Crear Lead

```bash
curl -X POST "http://127.0.0.1:8000/api/leads/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\": \"Tacos El Rey\", \"email\": \"rey@tacos.com\", \"phone\": \"555-1111\", \"restaurant_type\": \"Mexicana\", \"city\": \"Ciudad de Mexico\"}"
```

```bash
curl -X POST "http://127.0.0.1:8000/api/leads/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\": \"Luigi Pizza\", \"email\": \"luigi@pizza.com\", \"phone\": \"555-2222\", \"restaurant_type\": \"Italiana\", \"city\": \"Ciudad de Mexico\"}"
```

> Nota: cada creación consume la API de Ninjas para obtener latitud y longitud.

---

### Listar Todos

```bash
curl -X GET "http://127.0.0.1:8000/api/leads/?skip=0&limit=10" -H "accept: application/json"
```

---

### Buscar por similitud

Buscar "tacos en ciudad de mexico":

```bash
curl -X POST "http://127.0.0.1:8000/api/leads/search" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"query\": \"tacos en ciudad de mexico\"}"
```

Debería aparecer primero: **Tacos El Rey**.
