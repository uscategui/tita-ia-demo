import streamlit as st
import random

st.set_page_config(page_title="TiTA IA", page_icon="🎓", layout="wide")

# -----------------------------
# Estado inicial
# -----------------------------
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
            "content": "¡Hola! Soy TiTA IA ✨, tu chatbot educativo gamificado. Estoy aquí para acompañarte, resolver dudas, proponerte retos y ayudarte a aprender de forma más dinámica."
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

# -----------------------------
# Datos del bot
# -----------------------------
retos_abiertos = [
    "Explica dos beneficios de integrar Inteligencia Artificial en educación.",
    "Describe cómo la gamificación puede mejorar la motivación académica.",
    "Propón una forma en que TiTA IA apoyaría el aprendizaje autónomo de un estudiante.",
    "Explica cómo TiTA IA puede aportar en contextos de educación híbrida.",
    "Escribe una recomendación breve para un estudiante con baja motivación."
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
        "retro": "Correcto. En el proyecto, la IA se entiende como una tecnología para interpretar preguntas, generar respuestas contextualizadas y acompañar procesos de aprendizaje de forma personalizada."
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
        "retro": "Muy bien. La gamificación en TiTA IA se basa en puntos, insignias, niveles y recompensas para fortalecer la participación y la continuidad."
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
        "retro": "Exacto. El proyecto plantea a TiTA IA como una herramienta para fortalecer el aprendizaje autónomo mediante acompañamiento, motivación y personalización."
    }
]

# -----------------------------
# Funciones de apoyo
# -----------------------------
def actualizar_nivel():
    p = st.session_state.puntos
    if p >= 140:
        st.session_state.nivel = 5
    elif p >= 100:
        st.session_state.nivel = 4
    elif p >= 70:
        st.session_state.nivel = 3
    elif p >= 35:
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
        "Hoy puedes empezar por una consulta corta y luego pasar a un reto. Paso a paso también es progreso.",
        "Si te sientes saturado, prueba sesiones breves de estudio con metas muy concretas.",
        "La clave no es estudiar más horas, sino estudiar con intención, seguimiento y retroalimentación.",
        "Un buen hábito académico nace cuando conviertes pequeñas acciones en rutina.",
        "Haz una pregunta, completa un reto y revisa tu progreso: ese ciclo fortalece el aprendizaje autónomo."
    ]
    return random.choice(recomendaciones)

def responder(mensaje):
    m = mensaje.lower()

    if "hola" in m or "buenas" in m:
        return "¡Hola! Qué bueno tenerte aquí. Cuéntame, ¿quieres resolver una duda, hacer un reto o revisar estrategias para estudiar mejor?"
    elif "ia" in m or "inteligencia artificial" in m:
        return "La Inteligencia Artificial en TiTA IA permite interpretar preguntas, generar respuestas contextualizadas y ofrecer acompañamiento académico más flexible, inmediato y personalizado."
    elif "gamificación" in m or "gamificacion" in m:
        return "La gamificación incorpora puntos, niveles, insignias y recompensas para convertir el aprendizaje en una experiencia más atractiva, constante y motivadora."
    elif "aprendizaje adaptativo" in m:
        return "El aprendizaje adaptativo ajusta recomendaciones, dificultad y orientación según el desempeño, el ritmo y las necesidades del estudiante. En TiTA IA, esto se refleja en sugerencias personalizadas y rutas de apoyo."
    elif "aprendizaje autónomo" in m or "autonomo" in m:
        return "TiTA IA fortalece el aprendizaje autónomo al ofrecer orientación en tiempo real, metas pequeñas, retroalimentación inmediata y seguimiento del progreso."
    elif "educación híbrida" in m or "hibrida" in m:
        return "En educación híbrida, TiTA IA puede acompañar al estudiante tanto dentro como fuera del aula, integrando apoyo conversacional, retos y seguimiento en escenarios presenciales y virtuales."
    elif "motivación" in m or "motivar" in m:
        return "Cuando la motivación baja, conviene dividir el estudio en tareas pequeñas, usar refuerzos positivos y visualizar el avance. Ahí es donde TiTA IA puede convertirse en un acompañante estratégico."
    elif "tiempo" in m or "organización" in m or "organizar" in m:
        return "Una buena estrategia es priorizar tareas, trabajar en bloques cortos y cerrar cada sesión con una meta concreta. La organización también se entrena."
    elif "estrés" in m or "estres" in m or "cansado" in m:
        return "Respiremos un poco 😌. Si te sientes saturado, empecemos por algo breve: una duda puntual o un reto corto. El objetivo es avanzar sin sobrecarga."
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

# -----------------------------
# Sidebar
# -----------------------------
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

# -----------------------------
# Página inicio
# -----------------------------
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

# -----------------------------
# Página chat
# -----------------------------
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

    mensaje_usuario = st.chat_input("Escribe tu pregunta aquí...")
    if mensaje_usuario:
        st.session_state.chat.append({"role": "user", "content": mensaje_usuario})
        st.session_state.chat.append({"role": "assistant", "content": responder(mensaje_usuario)})
        recompensar(15, -3)
        registrar_interaccion("consulta_libre")
        st.rerun()

    col_a, col_b = st.columns(2)
    if col_a.button("Ver progreso"):
        st.session_state.page = "progreso"
        st.rerun()
    if col_b.button("Ver analítica"):
        st.session_state.page = "analitica"
        st.rerun()

# -----------------------------
# Página reto
# -----------------------------
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
            st.info("Retroalimentación TiTA: tu respuesta refleja comprensión del tema. El siguiente paso recomendado es complementar esta reflexión con una nueva consulta o un quiz de opción múltiple.")
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

# -----------------------------
# Página quiz
# -----------------------------
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

# -----------------------------
# Página progreso
# -----------------------------
elif st.session_state.page == "progreso":
    st.title("🏆 Tu progreso")
    st.write(f"**Nombre:** {st.session_state.nombre or 'Estudiante'}")
    st.write(f"**Tema principal:** {st.session_state.tema}")
    st.write(f"**Estado inicial:** {st.session_state.estado_animo or 'No registrado'}")
    st.write(f"**Puntos acumulados:** {st.session_state.puntos}")
    st.write(f"**Nivel actual:** {st.session_state.nivel}")

    progreso = min(st.session_state.puntos / 140, 1.0)
    st.progress(progreso)

    st.write("### Insignias logradas")
    if st.session_state.insignias:
        cols = st.columns(len(st.session_state.insignias))
        for i, ins in enumerate(st.session_state.insignias):
            cols[i].success(f"🏅 {ins}")
    else:
        st.info("Todavía no has desbloqueado insignias.")

    st.write("### Recomendación personalizada")
    if st.session_state.estado_animo == "Desmotivado/a":
        st.warning("Te conviene empezar por metas pequeñas, retos breves y consultas de baja complejidad para recuperar la motivación.")
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
    if c2.button("Ver analítica"):
        st.session_state.page = "analitica"
        st.rerun()
    if c3.button("Reiniciar demo"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# -----------------------------
# Página analítica
# -----------------------------
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