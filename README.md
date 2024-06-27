# Restaurant Reservations API

## Descripción
API para la gestión de reservas en restaurantes, permitiendo a los usuarios realizar, modificar y cancelar reservas. Incluye autenticación con JWT y manejo de datos de mesas y horarios.

## Instalación

### Requisitos Previos
- Python 3.6 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación
1. Clona el repositorio:
    ```bash
    git clone https://github.com/aun_no_esta_en_git/restaurant_reservations.git
    cd restaurant_reservations
    ```

2. Crea y activa el entorno virtual:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En macOS/Linux
    .venv\Scripts\activate  # En Windows
    ```

3. Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

4. Inicializa y migra la base de datos:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. Ejecuta el servidor Flask:
    ```bash
    flask run
    ```

## Uso
Usa herramientas como Postman o curl para interactuar con la API. A continuación se muestran ejemplos de algunas rutas disponibles:

- `POST /register`: Registrar un nuevo usuario.
- `POST /login`: Iniciar sesión.
- `POST /reservations`: Crear una nueva reserva.
- `GET /reservations/<int:id>`: Obtener una reserva por ID.
- `PUT /reservations/<int:id>`: Actualizar una reserva.
- `DELETE /reservations/<int:id>`: Eliminar una reserva.

## Objetivos del Proyecto

### Configuración Inicial del Proyecto
- [x] Crear el entorno virtual (`python -m venv .venv`)
- [x] Activar el entorno virtual (`source .venv/bin/activate` en macOS/Linux o `.venv\Scripts\activate` en Windows)
- [x] Instalar las dependencias necesarias (`pip install Flask Flask-Smorest Flask-JWT-Extended Flask-SQLAlchemy Flask-Migrate`)
- [x] Crear el archivo `requirements.txt` (`pip freeze > requirements.txt`)
- [x] Configurar la estructura del proyecto

### Configuración de Flask y Extensiones
- [x] Crear el archivo `app/__init__.py` y configurar Flask, SQLAlchemy, Flask-Migrate y Flask-JWT-Extended
- [x] Crear el archivo de configuración `config.py`

### Definición de Modelos
- [x] Crear el archivo `app/models.py`
- [x] Definir los modelos `User`, `Table` y `Reservation`

### Configuración de Migraciones
- [x] Inicializar las migraciones (`flask db init`)
- [x] Crear la primera migración (`flask db migrate -m "Initial migration."`)
- [x] Aplicar la migración (`flask db upgrade`)

### Definición de Esquemas
- [x] Crear el directorio `app/schemas/`
- [x] Definir los esquemas para `User`, `Table` y `Reservation` en `app/schemas/user.py`, `app/schemas/table.py`, y `app/schemas/reservation.py`

### Implementación de Recursos
- [x] Crear el directorio `app/resources/`
- [x] Implementar los recursos para autenticación en `app/resources/auth.py`
- [x] Implementar los recursos para usuarios en `app/resources/users.py`
- [x] Implementar los recursos para reservas en `app/resources/reservations.py`
- [x] Implementar los recursos para mesas en `app/resources/tables.py`

### Configuración de Autenticación
- [x] Implementar el registro de usuarios
- [x] Implementar el inicio de sesión de usuarios
- [x] Proteger las rutas con JWT

### Validación y Serialización
- [x] Utilizar Marshmallow para la validación y serialización de datos en los recursos

### Creación de Rutas y Blueprints
- [x] Registrar los blueprints en `app/__init__.py`

### Ejecución y Pruebas
- [x] Crear el archivo `run.py` para ejecutar la aplicación
- [x] Ejecutar el servidor Flask (`flask run`)
- [x] Probar las rutas de la API con Postman o curl

### Documentación y Mejora Continua
- [ ] Documentar las rutas y funcionalidades de la API
- [ ] Agregar manejo de errores y mensajes de error personalizados
- [ ] Escribir pruebas unitarias y de integración
- [ ] Optimizar el rendimiento de la API
- [ ] Implementar CI/CD (Integración Continua/Despliegue Continuo)

### Bonus: Despliegue
- [ ] Configurar Docker para la aplicación
- [ ] Crear un archivo `Dockerfile` para construir la imagen de la aplicación
- [ ] Crear un archivo `docker-compose.yml` para el despliegue
- [ ] Desplegar la aplicación en un servicio de hosting (Heroku, AWS, etc.)

## Contribuciones
Las contribuciones son bienvenidas. Por favor, sigue el flujo de trabajo de GitHub para hacer un fork del proyecto, crear una rama y enviar un pull request.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo `LICENSE`.

