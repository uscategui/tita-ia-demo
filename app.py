import streamlit as st
import random

st.set_page_config(page_title="TiTA IA", page_icon="🎓", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "inicio"
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "tema" not in st.session_state:
    st.session_state.tema = "Tecnologías emergentes"
if "puntos" not in st.session_state:
    st.session_state.puntos = 0
if "nivel" not in st.session_state:
    st.session_state.nivel = 1
if "insignias" not in st.session_state:
    st.session_state.insignias = []
if "chat" not in st.session_state:
    st.session_state.chat = [
        ("TiTA", "¡Hola! Soy TiTA IA, tu acompañante académico inteligente. Estoy aquí para ayudarte a aprender de forma más dinámica, personalizada y motivadora.")
    ]
if "estado" not in st.session_state:
    st.session_state.estado = ""
if "reto_actual" not in st.session_state:
    st.session_state.reto_actual = ""

retos = [
    "Explica dos beneficios de usar inteligencia artificial en educación.",
    "Menciona dos formas en que la gamificación puede mejorar la motivación estudiantil.",
    "Describe cómo el aprendizaje adaptativo puede ayudar a un estudiante con dificultades de organización.",
    "Propón una idea para usar TiTA IA en un entorno híbrido o virtual.",
    "Escribe una recomendación para mejorar los hábitos de estudio con apoyo de un chatbot."
]

def actualizar_gamificacion(extra=0):
    st.session_state.puntos += extra

    if st.session_state.puntos >= 20 and "Explorador" not in st.session_state.insignias:
        st.session_state.insignias.append("Explorador")
    if st.session_state.puntos >= 50 and "Aprendiz constante" not in st.session_state.insignias:
        st.session_state.insignias.append("Aprendiz constante")
    if st.session_state.puntos >= 80 and "Participación activa" not in st.session_state.insignias:
        st.session_state.insignias.append("Participación activa")
    if st.session_state.puntos >= 120 and "Maestro TiTA" not in st.session_state.insignias:
        st.session_state.insignias.append("Maestro TiTA")

    if st.session_state.puntos >= 120:
        st.session_state.nivel = 4
    elif st.session_state.puntos >= 80:
        st.session_state.nivel = 3
    elif st.session_state.puntos >= 40:
        st.session_state.nivel = 2
    else:
        st.session_state.nivel = 1

def responder(mensaje):
    m = mensaje.lower()

    if "motivado" in m or "bien" in m or "animado" in m:
        return "¡Qué bueno! Cuando hay motivación, podemos aprovecharla con retos cortos, retroalimentación inmediata y metas claras para fortalecer tu aprendizaje."
    elif "cansado" in m or "desmotivado" in m or "estresado" in m:
        return "Entiendo. Podemos empezar con tareas pequeñas, dividir el estudio en pasos cortos y usar recompensas para recuperar el ritmo sin sobrecarga."
    elif "gamificación" in m or "gamificacion" in m:
        return "La gamificación aplica puntos, niveles, insignias y recompensas para aumentar la participación, el compromiso y la continuidad del aprendizaje."
    elif "ia" in m or "inteligencia artificial" in m:
        return "La inteligencia artificial en educación permite responder dudas, personalizar contenidos, ofrecer retroalimentación inmediata y acompañar procesos de autoaprendizaje."
    elif "aprendizaje adaptativo" in m:
        return "El aprendizaje adaptativo ajusta contenidos, dificultad y recomendaciones según el desempeño y las necesidades del estudiante."
    elif "aprendizaje autónomo" in m or "autonomo" in m:
        return "El aprendizaje autónomo se fortalece cuando el estudiante recibe orientación oportuna, metas claras, seguimiento y recursos personalizados."
    elif "educación híbrida" in m or "hibrida" in m:
        return "En educación híbrida, TiTA IA puede acompañar al estudiante dentro y fuera del aula, resolviendo dudas, proponiendo retos y dando seguimiento al progreso."
    elif "motivación" in m or "motivar" in m:
        return "Para fortalecer la motivación académica, es útil combinar metas pequeñas, refuerzo positivo, actividades breves y seguimiento visible del avance."
    elif "tiempo" in m or "organización" in m:
        return "Una estrategia útil es dividir el trabajo en sesiones cortas, priorizar tareas y usar recordatorios con objetivos concretos por día."
    elif "reto" in m or "actividad" in m or "ejercicio" in m:
        st.session_state.page = "reto"
        st.session_state.reto_actual = random.choice(retos)
        return "¡Perfecto! Te llevaré a un reto breve para seguir avanzando."
    else:
        return "Puedo ayudarte con motivación académica, gestión del tiempo, aprendizaje autónomo, IA en educación, gamificación, educación híbrida y aprendizaje adaptativo."

st.sidebar.title("📊 Panel TiTA")
st.sidebar.metric("Puntos", st.session_state.puntos)
st.sidebar.metric("Nivel", st.session_state.nivel)

st.sidebar.write("### 🏅 Insignias")
if st.session_state.insignias:
    for ins in st.session_state.insignias:
        st.sidebar.success(ins)
else:
    st.sidebar.info("Aún no tienes insignias.")

st.sidebar.write("### 🎯 Estado actual")
if st.session_state.estado:
    st.sidebar.write(st.session_state.estado)
else:
    st.sidebar.write("Sin diagnóstico inicial")

if st.session_state.page == "inicio":
    st.title("🎓 TiTA IA")
    st.subheader("Chatbot educativo gamificado para acompañamiento académico y aprendizaje adaptativo")
    st.text_input("Escribe tu nombre", key="nombre")
    st.selectbox(
        "Selecciona un tema principal",
        [
            "Tecnologías emergentes",
            "Aprendizaje autónomo",
            "Motivación académica",
            "Educación híbrida",
            "Gamificación",
            "IA en educación",
            "Aprendizaje adaptativo"
        ],
        key="tema"
    )

    st.write("### ¿Cómo te sientes hoy frente al estudio?")
    col1, col2, col3 = st.columns(3)
    if col1.button("Motivado"):
        st.session_state.estado = "Motivado"
        st.session_state.chat.append(("Tú", "Hoy me siento motivado"))
        st.session_state.chat.append(("TiTA", responder("motivado")))
        actualizar_gamificacion(10)
    if col2.button("Cansado"):
        st.session_state.estado = "Cansado"
        st.session_state.chat.append(("Tú", "Hoy me siento cansado"))
        st.session_state.chat.append(("TiTA", responder("cansado")))
        actualizar_gamificacion(10)
    if col3.button("Desmotivado"):
        st.session_state.estado = "Desmotivado"
        st.session_state.chat.append(("Tú", "Hoy me siento desmotivado"))
        st.session_state.chat.append(("TiTA", responder("desmotivado")))
        actualizar_gamificacion(10)

    if st.button("Entrar a TiTA"):
        st.session_state.page = "chat"
        st.rerun()

elif st.session_state.page == "chat":
    st.title(f"Hola, {st.session_state.nombre or 'estudiante'} 👋")
    st.write(f"**Tema principal:** {st.session_state.tema}")
    st.write("### Conversación con TiTA")

    for autor, mensaje in st.session_state.chat:
        if autor == "TiTA":
            st.markdown(f"**🤖 {autor}:** {mensaje}")
        else:
            st.markdown(f"**🧑 {autor}:** {mensaje}")

    st.write("### Preguntas rápidas")
    c1, c2, c3 = st.columns(3)
    if c1.button("¿Qué es la gamificación?"):
        q = "¿Qué es la gamificación?"
        st.session_state.chat.append(("Tú", q))
        st.session_state.chat.append(("TiTA", responder(q)))
        actualizar_gamificacion(10)
        st.rerun()

    if c2.button("¿Cómo ayuda la IA?"):
        q = "¿Cómo ayuda la IA en educación?"
        st.session_state.chat.append(("Tú", q))
        st.session_state.chat.append(("TiTA", responder(q)))
        actualizar_gamificacion(10)
        st.rerun()

    if c3.button("Dame un reto"):
        q = "Dame un reto"
        st.session_state.chat.append(("Tú", q))
        st.session_state.chat.append(("TiTA", responder(q)))
        actualizar_gamificacion(10)
        st.rerun()

    c4, c5, c6 = st.columns(3)
    if c4.button("Tengo poca motivación"):
        q = "Necesito ayuda con motivación"
        st.session_state.chat.append(("Tú", q))
        st.session_state.chat.append(("TiTA", responder("motivación")))
        actualizar_gamificacion(10)
        st.rerun()

    if c5.button("No organizo mi tiempo"):
        q = "No organizo bien mi tiempo"
        st.session_state.chat.append(("Tú", q))
        st.session_state.chat.append(("TiTA", responder("tiempo")))
        actualizar_gamificacion(10)
        st.rerun()

    if c6.button("¿Qué es aprendizaje adaptativo?"):
        q = "¿Qué es aprendizaje adaptativo?"
        st.session_state.chat.append(("Tú", q))
        st.session_state.chat.append(("TiTA", responder(q)))
        actualizar_gamificacion(10)
        st.rerun()

    c7, c8, c9 = st.columns(3)
    if c7.button("Aprendizaje autónomo"):
        q = "¿Cómo fortalecer el aprendizaje autónomo?"
        st.session_state.chat.append(("Tú", q))
        st.session_state.chat.append(("TiTA", responder("aprendizaje autónomo")))
        actualizar_gamificacion(10)
        st.rerun()

    if c8.button("Educación híbrida"):
        q = "¿Cómo funciona TiTA en educación híbrida?"
        st.session_state.chat.append(("Tú", q))
        st.session_state.chat.append(("TiTA", responder("educación híbrida")))
        actualizar_gamificacion(10)
        st.rerun()

    if c9.button("Ver progreso"):
        st.session_state.page = "progreso"
        st.rerun()

    mensaje_usuario = st.text_input("Escribe tu pregunta aquí")
    if st.button("Enviar"):
        if mensaje_usuario.strip():
            st.session_state.chat.append(("Tú", mensaje_usuario))
            st.session_state.chat.append(("TiTA", responder(mensaje_usuario)))
            actualizar_gamificacion(15)
            st.rerun()

elif st.session_state.page == "reto":
    st.title("⚡ Reto interactivo")
    if not st.session_state.reto_actual:
        st.session_state.reto_actual = random.choice(retos)

    st.write(st.session_state.reto_actual)
    respuesta = st.text_area("Escribe tu respuesta")

    if st.button("Enviar respuesta"):
        if respuesta.strip():
            actualizar_gamificacion(25)
            st.success("¡Muy bien! Has completado el reto y ganado 25 puntos.")
            st.write("Retroalimentación automática:")
            st.info("Tu respuesta muestra comprensión del tema. TiTA recomienda continuar con una nueva consulta o revisar tu panel de progreso para identificar fortalezas y oportunidades de mejora.")
        else:
            st.warning("Debes escribir una respuesta antes de enviar.")

    col1, col2 = st.columns(2)
    if col1.button("Nuevo reto"):
        st.session_state.reto_actual = random.choice(retos)
        st.rerun()

    if col2.button("Ir a progreso"):
        st.session_state.page = "progreso"
        st.rerun()

elif st.session_state.page == "progreso":
    st.title("🏆 Tu progreso de aprendizaje")
    st.write(f"**Nombre:** {st.session_state.nombre or 'Estudiante'}")
    st.write(f"**Tema principal:** {st.session_state.tema}")
    st.write(f"**Estado inicial:** {st.session_state.estado if st.session_state.estado else 'No registrado'}")
    st.write(f"**Puntos acumulados:** {st.session_state.puntos}")
    st.write(f"**Nivel actual:** {st.session_state.nivel}")

    progreso = min(st.session_state.puntos / 120, 1.0)
    st.progress(progreso)

    st.write("### Insignias obtenidas")
    if st.session_state.insignias:
        cols = st.columns(len(st.session_state.insignias))
        for i, ins in enumerate(st.session_state.insignias):
            cols[i].success(f"🏅 {ins}")
    else:
        st.info("Aún no has desbloqueado insignias.")

    st.write("### Recomendación personalizada")
    if st.session_state.estado == "Desmotivado":
        st.warning("Te recomendamos iniciar con actividades breves, metas pequeñas y refuerzos positivos para recuperar la motivación.")
    elif st.session_state.estado == "Cansado":
        st.info("Te recomendamos organizar sesiones cortas de estudio, priorizar tareas y alternar entre consulta y práctica.")
    else:
        st.success("Tu nivel de disposición es favorable. Puedes avanzar a retos más complejos y profundizar en el aprendizaje adaptativo.")

    st.write("### Próximo paso sugerido")
    if st.session_state.puntos < 40:
        st.info("Explora más preguntas rápidas para fortalecer la comprensión del tema.")
    elif st.session_state.puntos < 80:
        st.info("Ya tienes una buena base. Intenta completar nuevos retos y revisar el tema de educación híbrida.")
    else:
        st.info("Tu avance es sólido. Ahora puedes analizar cómo escalar TiTA IA hacia analítica de aprendizaje e integración con LMS.")

    col1, col2 = st.columns(2)
    if col1.button("Volver al chat"):
        st.session_state.page = "chat"
        st.rerun()

    if col2.button("Reiniciar demo"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()