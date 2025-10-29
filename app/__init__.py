from flask import Flask, request, render_template
from .engine import INTERESES_DISPONIBLES, ASIGNATURAS, evaluar_perfil

app = Flask(name)


@app.route("/")
def home():
    return render_template(
        "index.html", intereses=INTERESES_DISPONIBLES, asignaturas=ASIGNATURAS
    )


methods = ["POST"]


@app.route("/orientar", methods=methods)
def api_orientar():
    demo_data = ["DevOps", "Frontend"]

    return render_template("_recomendaciones.html", recomendaciones=demo_data)
