import json

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

REGLAS = [
    {
        "recomendacion": "Investigador IA/ML",
        "condicion": {
            "rendimiento_es": {
                "Cálculo": "Alto",
                "Estadistica": "Alto",
                "Estructura de datos": "Alto",
            },
            "intereses_incluyen_alguno": ['Entender "cómo funcionan" las cosas'],
        },
        "justificacion": "Tu rendimiento excepcional en las áreas teóricas fundamentales (Cálculo, Estadística, Algoritmos) es el pilar de la investigación en IA.",
    },
    {
        "recomendacion": "Cientifico de datos",
        "condicion": {
            "rendimiento_es": {"Estadistica": "Alto", "Bases de datos": "Alto"},
            "intereses_incluyen_todos": ["Estrategia y negocios"],
        },
        "justificacion": "Combinas una fuerte habilidad analítica (Estadística) y de manejo de datos (BBDD) con un interés clave en cómo los datos impactan en el negocio.",
    },
    {
        "recomendacion": "Ingeniero Backend",
        "condicion": {
            "rendimiento_es": {"Estructura de datos": "Alto", "Bases de datos": "Alto"},
            "rendimiento_no_es": {"Redes": "Bajo", "Sistemas Operativos": "Bajo"},
            "intereses_incluyen_todos": ['Entender "cómo funcionan" las cosas'],
        },
        "justificacion": "Tu dominio de la lógica de negocio (Algoritmos) y los datos (BBDD), junto con tu interés en sistemas, es el perfil ideal para construir lógica de servidor.",
    },
    {
        "recomendacion": "Ingeniero Frontend",
        "condicion": {
            "intereses_incluyen_todos": [
                "Construcción practica",
                "Diseño y aspecto visual",
            ],
            "rendimiento_no_es": {"Estructura de datos": "Bajo"},
        },
        "justificacion": "Tu interés se centra en la parte tangible y visual del software. Valoras la construcción práctica y la estética por encima de la teoría algorítmica pura.",
    },
    {
        "recomendacion": "Ingeniero DevOps/SRE",
        "condicion": {
            "rendimiento_es": {"Redes": "Alto", "Sistemas Operativos": "Alto"},
            "intereses_incluyen_todos": [
                "Automatizar tareas",
                'Entender "cómo funcionan" las cosas',
            ],
        },
        "justificacion": "Eres un experto en infraestructura (Redes, SO) y te apasiona la automatización. Este es el perfil exacto de un ingeniero DevOps/SRE.",
    },
    {
        "recomendacion": "Ingeniero en Ciberseguridad",
        "condicion": {
            "rendimiento_es": {"Redes": "Alto", "Sistemas Operativos": "Alto"},
            "intereses_incluyen_todos": [
                "Seguridad",
                'Entender "cómo funcionan" las cosas',
            ],
        },
        "justificacion": "Tu interés explícito en seguridad, combinado con un conocimiento profundo de cómo funcionan los sistemas (Redes, SO), es la base de la ciberseguridad.",
    },
    {
        "recomendacion": "Ingeniero en Hardware/IoT",
        "condicion": {
            "rendimiento_es": {"Sistemas Operativos": "Alto"},
            "intereses_incluyen_todos": [
                'Sistemas de "bajo nivel"',
                'Entender "cómo funcionan" las cosas',
            ],
        },
        "justificacion": "Te atrae el 'metal'. Tu interés en el bajo nivel y los sistemas operativos se alinea con el desarrollo de hardware, firmware y sistemas embebidos.",
    },
    {
        "recomendacion": "Product Manager",
        "condicion": {
            "intereses_incluyen_todos": ["Estrategia y negocios"],
            "intereses_incluyen_alguno": [
                "Diseño y aspecto visual",
                "Construcción practica",
            ],
            "rendimiento_no_es": {
                "Estructura de datos": "Bajo",
                "Bases de datos": "Bajo",
            },
        },
        "justificacion": "Tu foco principal es el negocio y la estrategia. Tienes suficiente conocimiento técnico para comunicarte con los desarrolladores y un interés en el producto.",
    },
]


def _verificar_condicion(condicion, perfil):
    # 1. Verificar "rendimiento_es"
    # El perfil debe tener EXACTAMENTE este nivel en estas asignaturas.
    if "rendimiento_es" in condicion:
        for asignatura, nivel_requerido in condicion["rendimiento_es"].items():
            nivel_usuario = perfil.get("rendimiento", {}).get(asignatura)
            if nivel_usuario != nivel_requerido:
                return False  # Falla: no tiene el nivel requerido

    # 2. Verificar "rendimiento_no_es"
    # El perfil NO debe tener este nivel en estas asignaturas.
    if "rendimiento_no_es" in condicion:
        for asignatura, nivel_prohibido in condicion["rendimiento_no_es"].items():
            nivel_usuario = perfil.get("rendimiento", {}).get(asignatura)
            if nivel_usuario == nivel_prohibido:
                return False  # Falla: tiene un nivel prohibido (ej. "Bajo")

    # Convertimos los intereses del usuario a un Set para búsquedas eficientes
    intereses_usuario = set(perfil.get("intereses", []))

    # 3. Verificar "intereses_incluyen_todos"
    # El perfil debe tener TODOS los intereses de esta lista.
    if "intereses_incluyen_todos" in condicion:
        intereses_requeridos = set(condicion["intereses_incluyen_todos"])
        # Aquí usamos la lógica issubset que propusiste
        if not intereses_requeridos.issubset(intereses_usuario):
            return False  # Falla: no tiene todos los intereses requeridos

    # 4. Verificar "intereses_incluyen_alguno"
    # El perfil debe tener AL MENOS UNO de los intereses de esta lista.
    if "intereses_incluyen_alguno" in condicion:
        intereses_opcionales = set(condicion["intereses_incluyen_alguno"])
        # Si la intersección está vacía, no tiene ninguno de los opcionales
        if not intereses_usuario.intersection(intereses_opcionales):
            return False  # Falla: no tiene ninguno de los intereses opcionales

    # Si pasó todas las verificaciones, la condición se cumple
    return True


def evaluar_perfil(perfil):
    """
    Función principal del motor de inferencia.
    Recibe un perfil de usuario estructurado.
    Retorna una LISTA de todas las recomendaciones que coinciden.
    """

    # IMPORTANTE: No retornamos el primer match, sino TODOS los matches.
    # Un estudiante puede ser un buen candidato para más de un perfil.
    recomendaciones_encontradas = []

    for regla in REGLAS:
        # Verificamos si el perfil cumple la condición de la regla
        if _verificar_condicion(regla["condicion"], perfil):
            # Si cumple, añadimos la recomendación a nuestra lista
            recomendaciones_encontradas.append(
                {
                    "area": regla["recomendacion"],
                    "justificacion": regla["justificacion"],
                }
            )

    # Si no se encontró ninguna regla, retornamos un resultado por defecto
    if not recomendaciones_encontradas:
        return [
            {
                "area": "Perfil Generalista",
                "justificacion": "Tu perfil es balanceado y no coincide de forma estricta con una especialidad. Explora cursos optativos para descubrir tus intereses.",
            }
        ]

    return recomendaciones_encontradas
