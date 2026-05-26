import streamlit as st
import random

st.set_page_config(page_title="TiTA IA", page_icon="🎓", layout="wide")

# =========================================
# ESTADO INICIAL
# =========================================
if "page" not in st.session_state:
    st.session_state.page = "inicio"
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "tema" not in st.session_state:
    st.session_state.tema = "Tecnologías emergentes"
if "estado_animo" not in st.session_state:
    st.session_state.estado_animo = ""
if "puntos" not in st.session_state:
    st.session_state.puntos = 0
if "nivel" not in st.session_state:
    st.session_state.nivel = 1
if "energia" not in st.session_state:
    st.session_state.energia = 100
if "insignias" not in st.session_state:
    st.session_state.insignias = []
if "historial" not in st.session_state:
    st.session_state.historial = []
if "chat" not in st.session_state:
    st.session_state.chat = [
        {
            "role": "assistant",
            "content": "¡Hola! Soy TiTA IA ✨, tu chatbot educativo gamificado. Estoy aquí para acompañarte, resolver dudas, proponerte retos y ayudarte a aprender de forma más dinámica, autónoma y motivadora."
        }
    ]
if "reto_actual" not in st.session_state:
    st.session_state.reto_actual = ""
if "quiz_pregunta" not in st.session_state:
    st.session_state.quiz_pregunta = None
if "quiz_respondido" not in st.session_state:
    st.session_state.quiz_respondido = False
if "interacciones" not in st.session_state:
    st.session_state.interacciones = 0

# =========================================
# DATOS DEL BOT
# =========================================
retos_abiertos = [
    "Explica dos beneficios de integrar Inteligencia Artificial en educación.",
    "Describe cómo la gamificación puede mejorar la motivación académica.",
    "Propón una forma en que TiTA IA apoyaría el aprendizaje autónomo de un estudiante.",
    "Explica cómo TiTA IA puede aportar en contextos de educación híbrida.",
    "Escribe una recomendación breve para un estudiante con baja motivación.",
    "Menciona dos ventajas de usar analítica de aprendizaje en una plataforma educativa.",
    "Describe cómo un chatbot puede ayudar a mejorar la gestión del tiempo académico."
]

quizzes = [
    {
        "pregunta": "¿Cuál es una función principal de la Inteligencia Artificial en TiTA IA?",
        "opciones": [
            "Reemplazar por completo al docente",
            "Personalizar respuestas y acompañar al estudiante",
            "Eliminar el aprendizaje autónomo",
            "Evitar toda interacción humana"
        ],
        "correcta": "Personalizar respuestas y acompañar al estudiante",
        "retro": "Correcto. En TiTA IA, la IA se orienta a interpretar preguntas, generar respuestas contextualizadas y ofrecer acompañamiento personalizado."
    },
    {
        "pregunta": "¿Qué elemento corresponde a la gamificación?",
        "opciones": [
            "Insignias y niveles",
            "Silencio en la interfaz",
            "Eliminación de metas",
            "Desconexión del progreso"
        ],
        "correcta": "Insignias y niveles",
        "retro": "Muy bien. La gamificación se expresa mediante puntos, niveles, insignias y recompensas que fortalecen la participación."
    },
    {
        "pregunta": "¿Qué busca fortalecer TiTA IA principalmente?",
        "opciones": [
            "La memorización mecánica",
            "El aprendizaje autónomo",
            "La dependencia total del sistema",
            "La reducción del diálogo"
        ],
        "correcta": "El aprendizaje autónomo",
        "retro": "Exacto. El proyecto busca fortalecer el aprendizaje autónomo mediante acompañamiento, motivación y personalización."
    },
    {
        "pregunta": "¿Qué aporta la educación híbrida al proyecto?",
        "opciones": [
            "Combina escenarios presenciales y virtuales",
            "Elimina la interacción digital",
            "Sustituye toda planificación",
            "Evita el seguimiento"
        ],
        "correcta": "Combina escenarios presenciales y virtuales",
        "retro": "Correcto. La educación híbrida permite que TiTA IA acompañe al estudiante dentro y fuera del aula."
    }
]

descripciones_insignias = {
    "Explorador": {
        "descripcion": "Reconoce que comenzaste a explorar activamente la plataforma y a interactuar con TiTA IA.",
        "como": "Se obtiene al alcanzar 20 puntos.",
        "valor": "Premia la curiosidad inicial y la disposición para empezar."
    },
    "Aprendiz constante": {
        "descripcion": "Reconoce la constancia en la interacción y el compromiso con el proceso de aprendizaje.",
        "como": "Se obtiene al alcanzar 50 puntos.",
        "valor": "Fortalece el hábito de estudio y la continuidad."
    },
    "Mente curiosa": {
        "descripcion": "Destaca a quienes profundizan en conceptos, hacen varias consultas y exploran nuevos temas.",
        "como": "Se obtiene al alcanzar 80 puntos.",
        "valor": "Valora la iniciativa intelectual y la búsqueda activa de conocimiento."
    },
    "Jugador estratégico": {
        "descripcion": "Reconoce a quienes combinan consultas, retos, quizzes y seguimiento de progreso.",
        "como": "Se obtiene al alcanzar 110 puntos.",
        "valor": "Refuerza el uso inteligente de las herramientas del sistema."
    },
    "Maestro TiTA": {
        "descripcion": "Es la insignia de mayor nivel dentro del MVP y representa un uso integral y sostenido de la plataforma.",
        "como": "Se obtiene al alcanzar 140 puntos.",
        "valor": "Premia autonomía, participación y aprovechamiento continuo del entorno."
    }
}

# =========================================
# FUNCIONES
# =========================================
def actualizar_nivel():
    p = st.session_state.puntos
    if p >= 140:
        st.session_state.nivel = 5
    elif p >= 110:
        st.session_state.nivel = 4
    elif p >= 80:
        st.session_state.nivel = 3
    elif p >= 40:
        st.session_state.nivel = 2
    else:
        st.session_state.nivel = 1

def actualizar_insignias():
    p = st.session_state.puntos
    badges = st.session_state.insignias

    if p >= 20 and "Explorador" not in badges:
        badges.append("Explorador")
    if p >= 50 and "Aprendiz constante" not in badges:
        badges.append("Aprendiz constante")
    if p >= 80 and "Mente curiosa" not in badges:
        badges.append("Mente curiosa")
    if p >= 110 and "Jugador estratégico" not in badges:
        badges.append("Jugador estratégico")
    if p >= 140 and "Maestro TiTA" not in badges:
        badges.append("Maestro TiTA")

def recompensar(puntos=0, energia=-2):
    st.session_state.puntos += puntos
    st.session_state.energia = max(0, min(100, st.session_state.energia + energia))
    actualizar_nivel()
    actualizar_insignias()

def registrar_interaccion(tipo):
    st.session_state.interacciones += 1
    st.session_state.historial.append(tipo)

def recomendacion_del_dia():
    recomendaciones = [
        "Empieza con una pregunta breve y conviértela en un pequeño logro.",
        "No necesitas hacerlo todo hoy; necesitas empezar de forma clara y posible.",
        "Una consulta + un reto + una revisión del progreso = una sesión de estudio muy valiosa.",
        "La motivación crece cuando ves evidencia concreta de tu avance.",
        "Aprender mejor no siempre implica estudiar más, sino estudiar con intención y seguimiento."
    ]
    return random.choice(recomendaciones)

def opciones_motivacion():
    return {
        "Plan exprés de 10 minutos": "Empieza con una sola tarea pequeña durante 10 minutos. El objetivo no es terminar todo, sino romper la inercia inicial.",
        "Organizar prioridades": "Haz una lista con 3 tareas: una urgente, una importante y una corta. Empieza por la más fácil para ganar impulso.",
        "Meta mínima del día": "Define una meta muy concreta, por ejemplo: leer un apartado, responder una pregunta o completar un reto breve.",
        "Pausa activa + retorno": "Haz una pausa de 5 minutos, respira, toma agua y vuelve con una sola actividad específica.",
        "Acompañamiento guiado": "Haz una consulta a TiTA, responde un quiz o completa un reto. La idea es que no estudies en solitario absoluto."
    }

def responder(mensaje):
    m = mensaje.lower()

    if "hola" in m or "buenas" in m:
        return "¡Hola! Qué bueno tenerte aquí. Cuéntame, ¿quieres resolver una duda, hacer un reto o revisar estrategias para estudiar mejor?"
    elif "ia" in m or "inteligencia artificial" in m:
        return "La Inteligencia Artificial en TiTA IA permite interpretar preguntas, generar respuestas contextualizadas y ofrecer acompañamiento académico más flexible, inmediato y personalizado."
    elif "gamificación" in m or "gamificacion" in m:
        return "La gamificación incorpora puntos, niveles, insignias y recompensas para convertir el aprendizaje en una experiencia más atractiva, constante y motivadora."
    elif "aprendizaje adaptativo" in m:
        return "El aprendizaje adaptativo ajusta recomendaciones, dificultad y orientación según el desempeño, el ritmo y las necesidades del estudiante. En TiTA IA esto se refleja en rutas de apoyo personalizadas."
    elif "aprendizaje autónomo" in m or "autonomo" in m:
        return "TiTA IA fortalece el aprendizaje autónomo al ofrecer orientación en tiempo real, metas pequeñas, retroalimentación inmediata y seguimiento del progreso."
    elif "educación híbrida" in m or "hibrida" in m:
        return "En educación híbrida, TiTA IA puede acompañar al estudiante tanto dentro como fuera del aula, integrando apoyo conversacional, retos y seguimiento en escenarios presenciales y virtuales."
    elif "motivación" in m or "motivar" in m:
        return "Cuando la motivación baja, conviene dividir el estudio en tareas pequeñas, usar refuerzos positivos y visualizar el avance. Ahí TiTA IA puede actuar como acompañante estratégico."
    elif "tiempo" in m or "organización" in m or "organizar" in m:
        return "Una estrategia útil es trabajar con prioridades, sesiones cortas y metas concretas. La organización también es una habilidad que se entrena."
    elif "estrés" in m or "estres" in m or "cansado" in m:
        return "Respiremos un poco 😌. Si te sientes saturado, empecemos por algo breve: una duda puntual, un quiz o un reto corto. Avanzar poco también cuenta."
    elif "necesito organizarme" in m or "organizarme" in m:
        return "Claro. Podemos organizar tu estudio con opciones simples: un plan exprés de 10 minutos, una lista de 3 prioridades, una meta mínima del día o una pausa activa antes de retomar."
    elif "plan exprés" in m or "10 minutos" in m:
        return "Plan exprés: elige una sola tarea, trabaja 10 minutos sin interrupciones y termina escribiendo una idea clave. Eso ya es progreso real."
    elif "prioridades" in m:
        return "Te propongo priorizar así: 1 tarea urgente, 1 importante y 1 corta. Empieza por la corta para ganar impulso y luego avanza hacia la importante."
    elif "meta mínima" in m:
        return "Una meta mínima puede ser leer un apartado, responder una pregunta o completar un quiz. Cuando bajas la barrera de entrada, es más fácil empezar."
    elif "pausa activa" in m:
        return "Haz una pausa breve de 5 minutos, estírate, toma agua y vuelve con una sola actividad definida. El descanso también es parte de una buena estrategia."
    elif "reto" in m or "actividad" in m or "ejercicio" in m:
        st.session_state.page = "reto"
        st.session_state.reto_actual = random.choice(retos_abiertos)
        return "¡Vamos con toda! Te llevo a un reto breve para poner en práctica lo aprendido."
    elif "quiz" in m or "pregunta de opción múltiple" in m:
        st.session_state.page = "quiz"
        st.session_state.quiz_pregunta = random.choice(quizzes)
        st.session_state.quiz_respondido = False
        return "Perfecto. Te abriré un quiz rápido para seguir sumando puntos."
    else:
        return "Puedo ayudarte con IA en educación, gamificación, aprendizaje adaptativo, aprendizaje autónomo, motivación académica, organización del tiempo y educación híbrida. ¿Por dónde quieres empezar?"

# =========================================
# SIDEBAR
# =========================================
st.sidebar.title("📊 Panel TiTA")
st.sidebar.metric("Puntos", st.session_state.puntos)
st.sidebar.metric("Nivel", st.session_state.nivel)
st.sidebar.metric("Interacciones", st.session_state.interacciones)
st.sidebar.progress(st.session_state.energia / 100)
st.sidebar.caption(f"Energía académica: {st.session_state.energia}%")

st.sidebar.write("### 🏅 Insignias")
if st.session_state.insignias:
    for b in st.session_state.insignias:
        st.sidebar.success(b)
else:
    st.sidebar.info("Aún no tienes insignias.")

st.sidebar.write("### 🎯 Recomendación del día")
st.sidebar.info(recomendacion_del_dia())

# =========================================
# INICIO
# =========================================
if st.session_state.page == "inicio":
    st.title("🎓 TiTA IA")
    st.subheader("Un chatbot educativo gamificado para acompañamiento académico y aprendizaje adaptativo")
    st.write("Bienvenido/a a una experiencia de apoyo académico más dinámica, cercana y personalizada.")

    st.text_input("Escribe tu nombre", key="nombre")
    st.selectbox(
        "Selecciona un tema principal",
        [
            "Tecnologías emergentes",
            "IA en educación",
            "Gamificación",
            "Aprendizaje adaptativo",
            "Aprendizaje autónomo",
            "Educación híbrida",
            "Motivación académica"
        ],
        key="tema"
    )

    st.write("### ¿Cómo te sientes hoy frente al estudio?")
    c1, c2, c3 = st.columns(3)

    if c1.button("💪 Motivado/a"):
        st.session_state.estado_animo = "Motivado/a"
        st.session_state.chat.append({"role": "user", "content": "Hoy me siento motivado/a"})
        st.session_state.chat.append({"role": "assistant", "content": "¡Qué bien! Aprovechemos esa energía con consultas, retos y seguimiento visible del progreso."})
        recompensar(10, -1)
        registrar_interaccion("diagnóstico")
        st.rerun()

    if c2.button("😵 Cansado/a"):
        st.session_state.estado_animo = "Cansado/a"
        st.session_state.chat.append({"role": "user", "content": "Hoy me siento cansado/a"})
        st.session_state.chat.append({"role": "assistant", "content": "Gracias por decirlo. Podemos trabajar con pasos cortos, metas pequeñas y actividades de baja carga cognitiva."})
        recompensar(10, -1)
        registrar_interaccion("diagnóstico")
        st.rerun()

    if c3.button("😕 Desmotivado/a"):
        st.session_state.estado_animo = "Desmotivado/a"
        st.session_state.chat.append({"role": "user", "content": "Hoy me siento desmotivado/a"})
        st.session_state.chat.append({"role": "assistant", "content": "Tranqui, empecemos suave. A veces una sola acción pequeña puede reactivar el proceso. Estoy aquí para acompañarte."})
        recompensar(10, -1)
        registrar_interaccion("diagnóstico")
        st.rerun()

    if st.button("Entrar a TiTA 🚀"):
        st.session_state.page = "chat"
        st.rerun()

# =========================================
# CHAT
# =========================================
elif st.session_state.page == "chat":
    st.title(f"Hola, {st.session_state.nombre or 'estudiante'} 👋")
    st.write(f"**Tema principal:** {st.session_state.tema}")
    st.write(f"**Estado inicial:** {st.session_state.estado_animo or 'Sin registrar'}")

    st.write("### Conversación")
    for msg in st.session_state.chat:
        with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
            st.write(msg["content"])

    st.write("### Acciones rápidas")
    c1, c2, c3 = st.columns(3)
    if c1.button("¿Qué es la gamificación?"):
        q = "¿Qué es la gamificación?"
        st.session_state.chat.append({"role": "user", "content": q})
        st.session_state.chat.append({"role": "assistant", "content": responder(q)})
        recompensar(10, -2)
        registrar_interaccion("pregunta_rápida")
        st.rerun()

    if c2.button("¿Cómo ayuda la IA?"):
        q = "¿Cómo ayuda la IA en educación?"
        st.session_state.chat.append({"role": "user", "content": q})
        st.session_state.chat.append({"role": "assistant", "content": responder(q)})
        recompensar(10, -2)
        registrar_interaccion("pregunta_rápida")
        st.rerun()

    if c3.button("Quiero un reto"):
        q = "Quiero un reto"
        st.session_state.chat.append({"role": "user", "content": q})
        st.session_state.chat.append({"role": "assistant", "content": responder(q)})
        recompensar(12, -3)
        registrar_interaccion("reto")
        st.rerun()

    c4, c5, c6 = st.columns(3)
    if c4.button("Tengo poca motivación"):
        q = "Necesito apoyo con motivación"
        st.session_state.chat.append({"role": "user", "content": q})
        st.session_state.chat.append({"role": "assistant", "content": responder("motivación")})
        recompensar(10, -2)
        registrar_interaccion("motivación")
        st.rerun()

    if c5.button("No organizo mi tiempo"):
        q = "Necesito ayuda con organización del tiempo"
        st.session_state.chat.append({"role": "user", "content": q})
        st.session_state.chat.append({"role": "assistant", "content": responder("organización")})
        recompensar(10, -2)
        registrar_interaccion("organización")
        st.rerun()

    if c6.button("Hazme un quiz"):
        q = "Hazme un quiz"
        st.session_state.chat.append({"role": "user", "content": q})
        st.session_state.chat.append({"role": "assistant", "content": responder("quiz")})
        recompensar(12, -3)
        registrar_interaccion("quiz")
        st.rerun()

    st.write("### Apoyo cuando falta motivación")
    m1, m2, m3 = st.columns(3)

    if m1.button("Necesito organizarme"):
        st.session_state.chat.append({"role": "user", "content": "Necesito organizarme mejor"})
        st.session_state.chat.append({
            "role": "assistant",
            "content": "Claro 💡. Aquí tienes opciones concretas para retomar el estudio: Plan exprés de 10 minutos, Organizar prioridades, Meta mínima del día, Pausa activa + retorno o Acompañamiento guiado. Dime cuál quieres probar."
        })
        recompensar(10, -1)
        registrar_interaccion("apoyo_organizacion")
        st.rerun()

    if m2.button("Dame opciones para hoy"):
        st.session_state.chat.append({"role": "user", "content": "Dame opciones para hoy porque me siento desmotivado/a"})
        st.session_state.chat.append({
            "role": "assistant",
            "content": "Hoy no necesitas hacerlo todo; necesitas empezar. Te propongo tres caminos: 1) una tarea de 10 minutos, 2) un reto breve conmigo, 3) organizar tres prioridades. ¿Cuál quieres probar?"
        })
        recompensar(10, -1)
        registrar_interaccion("apoyo_motivacional")
        st.rerun()

    if m3.button("Quiero un plan breve"):
        st.session_state.chat.append({"role": "user", "content": "Quiero un plan breve para estudiar"})
        st.session_state.chat.append({
            "role": "assistant",
            "content": "Perfecto. Plan breve sugerido: 1) haz una consulta, 2) toma nota de una idea clave, 3) resuelve un quiz o reto corto, 4) revisa tu progreso. Es pequeño, pero muy poderoso."
        })
        recompensar(10, -1)
        registrar_interaccion("plan_breve")
        st.rerun()

    st.write("### Estrategias de organización")
    o1, o2, o3, o4, o5 = st.columns(5)

    if o1.button("Plan exprés"):
        st.session_state.chat.append({"role": "user", "content": "Quiero aplicar un plan exprés"})
        st.session_state.chat.append({"role": "assistant", "content": responder("plan exprés")})
        recompensar(8, -1)
        registrar_interaccion("plan_expres")
        st.rerun()

    if o2.button("Prioridades"):
        st.session_state.chat.append({"role": "user", "content": "Ayúdame con prioridades"})
        st.session_state.chat.append({"role": "assistant", "content": responder("prioridades")})
        recompensar(8, -1)
        registrar_interaccion("prioridades")
        st.rerun()

    if o3.button("Meta mínima"):
        st.session_state.chat.append({"role": "user", "content": "Necesito una meta mínima"})
        st.session_state.chat.append({"role": "assistant", "content": responder("meta mínima")})
        recompensar(8, -1)
        registrar_interaccion("meta_minima")
        st.rerun()

    if o4.button("Pausa activa"):
        st.session_state.chat.append({"role": "user", "content": "Necesito una pausa activa"})
        st.session_state.chat.append({"role": "assistant", "content": responder("pausa activa")})
        recompensar(8, -1)
        registrar_interaccion("pausa_activa")
        st.rerun()

    if o5.button("Acompañamiento guiado"):
        st.session_state.chat.append({"role": "user", "content": "Quiero acompañamiento guiado"})
        st.session_state.chat.append({
            "role": "assistant",
            "content": "Vamos paso a paso 😊. Te propongo este recorrido: 1) haz una pregunta, 2) responde un quiz, 3) completa un reto, 4) revisa tu progreso. Yo te acompaño en cada parte."
        })
        recompensar(8, -1)
        registrar_interaccion("acompanamiento_guiado")
        st.rerun()

    mensaje_usuario = st.chat_input("Escribe tu pregunta aquí...")
    if mensaje_usuario:
        st.session_state.chat.append({"role": "user", "content": mensaje_usuario})
        st.session_state.chat.append({"role": "assistant", "content": responder(mensaje_usuario)})
        recompensar(15, -3)
        registrar_interaccion("consulta_libre")
        st.rerun()

    col_a, col_b, col_c = st.columns(3)
    if col_a.button("Ver progreso"):
        st.session_state.page = "progreso"
        st.rerun()
    if col_b.button("Ver analítica"):
        st.session_state.page = "analitica"
        st.rerun()
    if col_c.button("Ver insignias"):
        st.session_state.page = "insignias"
        st.rerun()

# =========================================
# RETO
# =========================================
elif st.session_state.page == "reto":
    st.title("⚡ Reto interactivo")
    if not st.session_state.reto_actual:
        st.session_state.reto_actual = random.choice(retos_abiertos)

    st.write("### Desafío del momento")
    st.info(st.session_state.reto_actual)

    respuesta = st.text_area("Escribe tu respuesta")

    if st.button("Enviar respuesta del reto"):
        if respuesta.strip():
            recompensar(25, -5)
            registrar_interaccion("respuesta_reto")
            st.success("¡Excelente! Completaste el reto y ganaste 25 puntos.")
            st.info("Retroalimentación TiTA: tu respuesta muestra comprensión del tema. El siguiente paso recomendado es complementar esta reflexión con un quiz o una nueva consulta.")
        else:
            st.warning("Necesitas escribir una respuesta antes de enviarla.")

    c1, c2, c3 = st.columns(3)
    if c1.button("Nuevo reto"):
        st.session_state.reto_actual = random.choice(retos_abiertos)
        st.rerun()
    if c2.button("Ir al chat"):
        st.session_state.page = "chat"
        st.rerun()
    if c3.button("Ir al progreso"):
        st.session_state.page = "progreso"
        st.rerun()

# =========================================
# QUIZ
# =========================================
elif st.session_state.page == "quiz":
    st.title("🧠 Quiz rápido")
    if st.session_state.quiz_pregunta is None:
        st.session_state.quiz_pregunta = random.choice(quizzes)

    pregunta = st.session_state.quiz_pregunta
    st.write(pregunta["pregunta"])

    opcion = st.radio("Selecciona una respuesta", pregunta["opciones"], key="respuesta_quiz")

    if st.button("Enviar quiz"):
        if opcion == pregunta["correcta"]:
            recompensar(20, -4)
            st.success("¡Respuesta correcta! +20 puntos para ti.")
        else:
            recompensar(5, -2)
            st.error("No era esa, pero igual seguiste participando. +5 puntos por intentarlo.")
        registrar_interaccion("respuesta_quiz")
        st.info(pregunta["retro"])
        st.session_state.quiz_respondido = True

    c1, c2, c3 = st.columns(3)
    if c1.button("Otro quiz"):
        st.session_state.quiz_pregunta = random.choice(quizzes)
        st.session_state.quiz_respondido = False
        st.rerun()
    if c2.button("Ir al chat desde quiz"):
        st.session_state.page = "chat"
        st.rerun()
    if c3.button("Ver progreso desde quiz"):
        st.session_state.page = "progreso"
        st.rerun()

# =========================================
# PROGRESO
# =========================================
elif st.session_state.page == "progreso":
    st.title("🏆 Tu progreso")
    st.write(f"**Nombre:** {st.session_state.nombre or 'Estudiante'}")
    st.write(f"**Tema principal:** {st.session_state.tema}")
    st.write(f"**Estado inicial:** {st.session_state.estado_animo or 'No registrado'}")
    st.write(f"**Puntos acumulados:** {st.session_state.puntos}")
    st.write(f"**Nivel actual:** {st.session_state.nivel}")

    progreso = min(st.session_state.puntos / 140, 1.0)
    st.progress(progreso)

    st.write("### Recomendación personalizada")
    if st.session_state.estado_animo == "Desmotivado/a":
        st.warning("Te conviene empezar por metas pequeñas, retos breves y consultas de baja complejidad para recuperar la motivación.")
        st.write("#### Opciones sugeridas para retomar el estudio")
        st.success("1. Hacer una consulta breve a TiTA")
        st.success("2. Organizar 3 prioridades")
        st.success("3. Completar un reto corto")
        st.success("4. Definir una meta mínima del día")
    elif st.session_state.estado_animo == "Cansado/a":
        st.info("Lo ideal es trabajar en sesiones cortas, alternar teoría y práctica, y evitar la sobrecarga.")
    else:
        st.success("Tu disposición es favorable. Puedes avanzar a desafíos más complejos y profundizar en temas como analítica o educación híbrida.")

    st.write("### Próximo paso sugerido")
    if st.session_state.puntos < 40:
        st.info("Haz dos consultas más y luego completa un reto.")
    elif st.session_state.puntos < 90:
        st.info("Tu progreso va bien. Ahora conviene combinar un quiz con una consulta abierta.")
    else:
        st.info("Ya tienes una participación sólida. El siguiente paso es explorar escalabilidad, analítica del aprendizaje e integración con LMS.")

    c1, c2, c3 = st.columns(3)
    if c1.button("Volver al chat"):
        st.session_state.page = "chat"
        st.rerun()
    if c2.button("Ver insignias"):
        st.session_state.page = "insignias"
        st.rerun()
    if c3.button("Reiniciar demo"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# =========================================
# INSIGNIAS
# =========================================
elif st.session_state.page == "insignias":
    st.title("🏅 Sistema de insignias")
    st.write("Las insignias en TiTA IA no solo recompensan; también explican qué hábito o comportamiento de aprendizaje está fortaleciendo el estudiante.")

    if st.session_state.insignias:
        for ins in st.session_state.insignias:
            with st.expander(f"🏅 {ins}"):
                st.write(f"**¿Qué significa?** {descripciones_insignias[ins]['descripcion']}")
                st.write(f"**¿Cómo se obtiene?** {descripciones_insignias[ins]['como']}")
                st.write(f"**¿Qué reconoce?** {descripciones_insignias[ins]['valor']}")
    else:
        st.info("Aún no has desbloqueado insignias. Sigue interactuando con TiTA para obtenerlas.")

    st.write("### Insignias disponibles")
    for nombre, info in descripciones_insignias.items():
        with st.expander(f"{nombre}"):
            st.write(f"**Descripción:** {info['descripcion']}")
            st.write(f"**Cómo se obtiene:** {info['como']}")
            st.write(f"**Valor pedagógico:** {info['valor']}")

    c1, c2 = st.columns(2)
    if c1.button("Volver al chat desde insignias"):
        st.session_state.page = "chat"
        st.rerun()
    if c2.button("Ir al progreso desde insignias"):
        st.session_state.page = "progreso"
        st.rerun()

# =========================================
# ANALÍTICA
# =========================================
elif st.session_state.page == "analitica":
    st.title("📈 Analítica básica del aprendizaje")
    st.write("Esta vista simula el seguimiento inicial del comportamiento del estudiante dentro del prototipo.")

    st.metric("Total de interacciones", st.session_state.interacciones)
    st.metric("Puntos obtenidos", st.session_state.puntos)
    st.metric("Nivel alcanzado", st.session_state.nivel)

    st.write("### Historial de interacción")
    if st.session_state.historial:
        conteo = {}
        for item in st.session_state.historial:
            conteo[item] = conteo.get(item, 0) + 1

        for k, v in conteo.items():
            st.write(f"- {k}: {v}")
    else:
        st.info("Aún no hay suficientes interacciones para mostrar datos.")

    st.write("### Interpretación")
    if st.session_state.interacciones < 3:
        st.info("El estudiante presenta una exploración inicial. Se recomienda motivar más consultas y actividades breves.")
    elif st.session_state.interacciones < 7:
        st.info("El estudiante muestra participación moderada. Conviene fortalecer el seguimiento con retos y retroalimentación continua.")
    else:
        st.success("El estudiante evidencia una participación activa. El sistema podría escalar hacia un módulo más robusto de analítica del aprendizaje.")

    st.write("### Proyección")
    st.write("En una versión futura, este módulo podría conectarse con LMS, tableros docentes y reglas adaptativas más complejas.")

    c1, c2 = st.columns(2)
    if c1.button("Volver al chat desde analítica"):
        st.session_state.page = "chat"
        st.rerun()
    if c2.button("Ir al progreso desde analítica"):
        st.session_state.page = "progreso"
        st.rerun()