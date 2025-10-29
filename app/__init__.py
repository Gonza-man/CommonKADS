from flask import Flask, request, render_template

app = Flask(_name_)

INTERESES_DISPONIBLES = [
    "Construcción practica",
    "Diseño y aspecto visual",
    "Automatizar tareas",
    'Entender "cómo funcionan" las cosas',
    "Estrategia y negocios",
    'Sistemas de "bajo nivel"',
    "Seguridad",
]

ASIGNATURAS = [
    "Cálculo",
    "Estadistica",
    "Estructura de datos",
    "Redes",
    "Sistemas Operativos",
    "Bases de datos",
]


@app.route("/")
def home():
    return render_template(
        "index.html", intereses=INTERESES_DISPONIBLES, asignaturas=ASIGNATURAS
    )
