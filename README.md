# CommonKADS example

Tematica: Sistema experto para orientación vocacional de estudiantes de informática.

## Instrucciones de uso

### Docker (Recomendado)

El proyecto cuenta con un Dockerfile/docker-compose por lo que para levanatarlo solo es necesario, esta es la forma más recomenda de usar el proyecto ya que evita problema con las versiones de python

```bash
docker compose up
```

Luego visite localhost en el puerto 8000 (Se puede cambiar en el docker-compose.yaml), [localhost:8000](localhost:8000)

### Manual

En caso de querer levantar la pagina de forma manual, esta es la forma sugerida usando uv

```bash
# Usamos uv para tener mayor rapides en la instalación de las librerias
$ uv venv venv
# Luego instalamos todos los requerimientos
$ uv add -r requerimientos.txt

# Para ejecutar existen varias opcione, por ejemplo la interfaz de flask
$ flask --app=app run

```

## Testing

El `engine.py` tiene 3 pruebas se puede ejecutar directamente para probar el funcionamiento del motor
