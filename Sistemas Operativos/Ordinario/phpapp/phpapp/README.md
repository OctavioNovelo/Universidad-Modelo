# PHP Hello World with Docker

Esta es una aplicación simple de PHP "Hola Mundo" configurada para correr en un contenedor Docker con Apache y Composer.

## Requisitos
- Docker instalado.

## Instrucciones

#####
## Deploy del app sencillo / para flojos ##
#####
Ejecute el siguiente comando
docker compose up -d

### 3. Acceder a la aplicación
Abre tu navegador en:
[http://localhost:8080](http://localhost:8080)


#####
## Para lanzar aplicación de forma manual
### 1. Construir la imagen
Ejecuta el siguiente comando en la raíz del proyecto:
```bash
docker build -t php-hello-world .
```

### 2. Ejecutar el contenedor
Inicia el contenedor mapeando el puerto 8080 de tu máquina al puerto 80 del contenedor:
```bash
docker run -d -p 8080:80 --name my-php-app php-hello-world
```

### 3. Acceder a la aplicación
Abre tu navegador en:
[http://localhost:8080](http://localhost:8080)

## Estructura del Proyecto
- `src/`: Contiene el código fuente de PHP.
- `composer.json`: Para gestionar dependencias de PHP.
- `Dockerfile`: Configuración de la imagen de Docker (PHP 8.3 + Apache + Composer).
