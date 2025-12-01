Microservicio de Gestión de Leads 

Este proyecto es una API backend de alto rendimiento construida con Python y FastAPI, diseñada para recibir, validar, almacenar y buscar clientes potenciales (leads) utilizando algoritmos de similitud.



#Estructura del Proyecto

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
├── requirements.txt         # Dependencias

