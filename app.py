import streamlit as st

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
        ("TiTA", "¡Hola! Soy TiTA IA, tu asistente educativo gamificado. Estoy aquí para acompañarte.")
    ]

def actualizar_gamificacion(extra=0):
    st.session_state.puntos += extra
    if st.session_state.puntos >= 30 and "Explorador" not in st.session_state.insignias:
        st.session_state.insignias.append("Explorador")
    if st.session_state.puntos >= 60 and "Aprendiz constante" not in st.session_state.insignias:
        st.session_state.insignias.append("Aprendiz constante")
    if st.session_state.puntos >= 100 and "Maestro TiTA" not in st.session_state.insignias:
        st.session_state.insignias.append("Maestro TiTA")

    if st.session_state.puntos >= 100:
        st.session_state.nivel = 3
    elif st.session_state.puntos >= 50:
        st.session_state.nivel = 2
    else:
        st.session_state.nivel = 1

def responder(mensaje):
    m = mensaje.lower()
    if "gamificación" in m or "gamificacion" in m:
        return "La gamificación incorpora puntos, niveles, retos e insignias para fortalecer la motivación y el compromiso del estudiante."
    elif "ia" in m or "inteligencia artificial" in m:
        return "La inteligencia artificial en educación permite personalizar el acompañamiento, responder dudas y adaptar contenidos según las necesidades del estudiante."
    elif "aprendizaje adaptativo" in m:
        return "El aprendizaje adaptativo ajusta el nivel de dificultad, las recomendaciones y las actividades según el progreso del estudiante."
    elif "actividad" in m or "reto" in m:
        st.session_state.page = "reto"
        return "Te llevaré a un reto rápido para poner en práctica lo aprendido."
    else:
        return "Puedo ayudarte con temas como IA, gamificación, aprendizaje adaptativo, motivación académica y hábitos de estudio."

st.sidebar.title("📊 Panel TiTA")
st.sidebar.metric("Puntos", st.session_state.puntos)
st.sidebar.metric("Nivel", st.session_state.nivel)
st.sidebar.write("### Insignias")
if st.session_state.insignias:
    for i in st.session_state.insignias:
        st.sidebar.success(f"🏅 {i}")
else:
    st.sidebar.info("Aún no tienes insignias.")

if st.session_state.page == "inicio":
    st.title("🎓 TiTA IA")
    st.subheader("Chatbot educativo gamificado para acompañamiento académico y aprendizaje adaptativo")
    st.text_input("Escribe tu nombre", key="nombre")
    st.selectbox("Selecciona un tema", ["Tecnologías emergentes", "IA en educación", "Gamificación", "Aprendizaje adaptativo"], key="tema")
    if st.button("Entrar"):
        st.session_state.page = "chat"
        st.rerun()

elif st.session_state.page == "chat":
    st.title(f"Hola, {st.session_state.nombre or 'estudiante'} 👋")
    st.write(f"**Tema actual:** {st.session_state.tema}")

    for autor, mensaje in st.session_state.chat:
        if autor == "TiTA":
            st.markdown(f"**🤖 {autor}:** {mensaje}")
        else:
            st.markdown(f"**🧑 {autor}:** {mensaje}")

    col1, col2, col3 = st.columns(3)
    if col1.button("¿Qué es la gamificación?"):
        pregunta = "¿Qué es la gamificación?"
        st.session_state.chat.append(("Tú", pregunta))
        st.session_state.chat.append(("TiTA", responder(pregunta)))
        actualizar_gamificacion(10)
        st.rerun()

    if col2.button("Explícame IA en educación"):
        pregunta = "Explícame IA en educación"
        st.session_state.chat.append(("Tú", pregunta))
        st.session_state.chat.append(("TiTA", responder(pregunta)))
        actualizar_gamificacion(10)
        st.rerun()

    if col3.button("Dame una actividad"):
        pregunta = "Dame una actividad"
        st.session_state.chat.append(("Tú", pregunta))
        st.session_state.chat.append(("TiTA", responder(pregunta)))
        actualizar_gamificacion(10)
        st.rerun()

    mensaje_usuario = st.text_input("Escribe tu pregunta")
    if st.button("Enviar pregunta"):
        if mensaje_usuario.strip():
            st.session_state.chat.append(("Tú", mensaje_usuario))
            st.session_state.chat.append(("TiTA", responder(mensaje_usuario)))
            actualizar_gamificacion(10)
            st.rerun()

    if st.button("Ver progreso"):
        st.session_state.page = "progreso"
        st.rerun()

elif st.session_state.page == "reto":
    st.title("⚡ Reto rápido")
    st.write("Menciona dos ventajas de integrar IA y gamificación en educación.")
    respuesta = st.text_area("Tu respuesta")

    if st.button("Enviar reto"):
        if respuesta.strip():
            actualizar_gamificacion(30)
            st.success("¡Excelente! Identificaste elementos clave del proyecto. Has ganado 30 puntos.")
            st.write("Retroalimentación: la IA favorece la personalización del aprendizaje y la gamificación fortalece la motivación y continuidad del estudiante.")
        else:
            st.warning("Escribe una respuesta para continuar.")

    if st.button("Ir a progreso"):
        st.session_state.page = "progreso"
        st.rerun()

elif st.session_state.page == "progreso":
    st.title("🏆 Tu progreso")
    st.write(f"**Puntos acumulados:** {st.session_state.puntos}")
    st.write(f"**Nivel actual:** {st.session_state.nivel}")
    progreso = min(st.session_state.puntos / 100, 1.0)
    st.progress(progreso)

    st.write("### Insignias")
    if st.session_state.insignias:
        cols = st.columns(len(st.session_state.insignias))
        for idx, ins in enumerate(st.session_state.insignias):
            cols[idx].success(f"🏅 {ins}")
    else:
        st.info("Sigue interactuando para desbloquear insignias.")

    st.write("### Recomendación personalizada")
    if st.session_state.puntos < 30:
        st.info("Te recomendamos empezar con conceptos básicos sobre IA y gamificación.")
    elif st.session_state.puntos < 60:
        st.info("Vas bien. El siguiente paso es profundizar en aprendizaje adaptativo.")
    else:
        st.info("Tienes un buen avance. Ya puedes explorar analítica del aprendizaje y escalabilidad institucional.")

    col1, col2 = st.columns(2)
    if col1.button("Volver al chat"):
        st.session_state.page = "chat"
        st.rerun()
    if col2.button("Reiniciar demo"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()