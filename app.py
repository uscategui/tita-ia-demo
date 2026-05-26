import streamlit as st
import random
import os
from openai import OpenAI

st.set_page_config(page_title="TiTA IA", page_icon="🎓", layout="wide")

# =========================================
# ESTILOS VISUALES
# =========================================
st.markdown("""
<style>
.bloque-color {
    padding: 16px 18px;
    border-radius: 12px;
    margin-bottom: 14px;
    border-left: 6px solid #6c63ff;
    background-color: #f4f2ff;
    color: #2b2b2b;
}
.bloque-verde {
    padding: 16px 18px;
    border-radius: 12px;
    margin-bottom: 14px;
    border-left: 6px solid #2e8b57;
    background-color: #eefaf3;
    color: #2b2b2b;
}
.bloque-azul {
    padding: 16px 18px;
    border-radius: 12px;
    margin-bottom: 14px;
    border-left: 6px solid #2f80ed;
    background-color: #eef5ff;
    color: #2b2b2b;
}
.bloque-naranja {
    padding: 16px 18px;
    border-radius: 12px;
    margin-bottom: 14px;
    border-left: 6px solid #f2994a;
    background-color: #fff4ea;
    color: #2b2b2b;
}
.bloque-rosa {
    padding: 16px 18px;
    border-radius: 12px;
    margin-bottom: 14px;
    border-left: 6px solid #d16ba5;
    background-color: #fff0f7;
    color: #2b2b2b;
}
.titulo-bonito {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 6px;
}
.texto-suave {
    font-size: 0.97rem;
    line-height: 1.55;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# OPENAI CLIENTE
# =========================================
api_key = None
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
elif os.getenv("OPENAI_API_KEY"):
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) if api_key else None

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
if "interacciones" not in st.session_state:
    st.session_state.interacciones = 0

# Quiz secuencial
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_feedback" not in st.session_state:
    st.session_state.quiz_feedback = ""
if "quiz_contestado" not in st.session_state:
    st.session_state.quiz_contestado = False

# =========================================
# DATOS
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
        "retro": "En TiTA IA, la IA se usa para interpretar preguntas, generar respuestas contextualizadas y ofrecer acompañamiento académico más flexible, inmediato y cercano. No busca reemplazar al docente, sino complementar el proceso educativo."
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
        "retro": "La gamificación incorpora dinámicas propias del juego, como puntos, insignias, niveles, retos y recompensas. Estas mecánicas ayudan a aumentar la motivación, hacer visible el avance y fortalecer la continuidad del aprendizaje."
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
        "retro": "Uno de los propósitos centrales de TiTA IA es fortalecer el aprendizaje autónomo. Para ello combina orientación en tiempo real, retroalimentación, retos, organización del estudio y seguimiento del progreso."
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
        "retro": "La educación híbrida permite que TiTA IA acompañe al estudiante tanto en contextos presenciales como virtuales. Esto amplía el acceso al apoyo académico y hace más continua la experiencia de aprendizaje."
    },
    {
        "pregunta": "¿Qué busca el uso responsable de la IA en TiTA IA?",
        "opciones": [
            "Que el estudiante copie sin pensar",
            "Que la IA sustituya el análisis propio",
            "Que la herramienta apoye sin anular el proceso cognitivo",
            "Que no exista revisión docente"
        ],
        "correcta": "Que la herramienta apoye sin anular el proceso cognitivo",
        "retro": "El uso responsable de la IA implica que la herramienta apoye, oriente y facilite procesos, pero sin reemplazar la reflexión, el pensamiento crítico, el contraste de fuentes ni la supervisión pedagógica."
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
        "descripcion": "Reconoce a quienes combinan consultas, retos, quiz y seguimiento de progreso.",
        "como": "Se obtiene al alcanzar 110 puntos.",
        "valor": "Refuerza el uso inteligente de las herramientas del sistema."
    },
    "Maestro TiTA": {
        "descripcion": "Es la insignia de mayor nivel dentro del MVP y representa un uso integral y sostenido de la plataforma.",
        "como": "Se obtiene al alcanzar 140 puntos.",
        "valor": "Premia autonomía, participación y aprovechamiento continuo del entorno."
    }
}

metodos_productividad = {
    "Pomodoro": {
        "descripcion": "Trabajas durante 25 minutos con máxima concentración y luego descansas 5 minutos.",
        "cuando_usarlo": "Ideal si te distraes fácil o necesitas comenzar con una estructura clara.",
        "ejemplo": "25 minutos leyendo o escribiendo + 5 minutos de pausa."
    },
    "Método Flowtime": {
        "descripcion": "Trabajas de forma continua hasta notar fatiga o distracción, y luego defines la pausa según el tiempo real de concentración.",
        "cuando_usarlo": "Ideal si entras en concentración profunda y no quieres cortar el ritmo arbitrariamente.",
        "ejemplo": "Si estudiaste 45 minutos con buena concentración, descansas 10."
    },
    "Método 50/10 o 52/17": {
        "descripcion": "Estudias entre 50 y 52 minutos con concentración total y luego descansas entre 10 y 17 minutos.",
        "cuando_usarlo": "Muy útil para lecturas largas, tareas densas y sesiones académicas exigentes.",
        "ejemplo": "50 minutos de lectura crítica + 10 minutos de pausa."
    },
    "Técnica 90/20": {
        "descripcion": "Se basa en ciclos ultradianos: 90 minutos de trabajo intenso seguidos por 20 minutos de descanso real.",
        "cuando_usarlo": "Útil para personas con buena capacidad de atención sostenida.",
        "ejemplo": "90 minutos desarrollando un trabajo + 20 minutos de desconexión total."
    },
    "Técnica 'Solo un poquito' (Kaizen)": {
        "descripcion": "Empiezas por una meta muy pequeña para reducir la resistencia psicológica al inicio.",
        "cuando_usarlo": "Perfecta si estás procrastinando o te cuesta arrancar.",
        "ejemplo": "Leer una sola página o estudiar 5 minutos."
    },
    "Bloques personalizados": {
        "descripcion": "Ajustas la duración de las sesiones según tu energía y cansancio, en vez de usar una sola fórmula fija.",
        "cuando_usarlo": "Ideal si ya conoces tus ritmos de atención.",
        "ejemplo": "Empiezas con 90 minutos y luego haces bloques de 50 o 25."
    }
}

manual_motivacion = {
    "Reducción del esfuerzo inicial": [
        ("Regla de los 5 minutos", "Comprométete a estudiar solo cinco minutos. La barrera más difícil es empezar; una vez rompes la inercia, el cerebro tiende a continuar."),
        ("Micro-objetivos", "Divide una tarea grande en pasos ridículamente pequeños. En lugar de 'estudiar historia', proponte 'leer solo la primera página del capítulo uno'."),
        ("Gamificación", "Transforma el estudio en una misión. Usa aplicaciones como Habitica para ganar puntos, subir de nivel y obtener recompensas virtuales al cumplir tareas.")
    ],
    "Estímulos visuales y del entorno": [
        ("Sistemas de recompensa inmediata", "Establece un premio físico y claro justo al terminar la sesión. Puede ser un dulce, diez minutos de tu videojuego favorito o ver un video."),
        ("Técnica del progreso visual", "Usa un frasco con canicas o una lista física para tachar con colores. Ver físicamente cómo avanzas libera dopamina y te impulsa a seguir."),
        ("Estudio en doble (Body Doubling)", "Estudia junto a otra persona, ya sea en silencio, mediante videollamada o con videos tipo 'Study With Me'. La presencia ajena reduce la tentación de distraerse.")
    ],
    "Enfoque mental y físico": [
        ("Anclaje de mentalidad", "Diseña un ritual de inicio idéntico cada vez. Limpiar el escritorio, encender una lámpara específica o poner una lista de reproducción fija le avisa a tu cerebro que es hora de concentrarse."),
        ("Aceptación de la distracción", "Ten una libreta de 'descarga mental' al lado. Si recuerdas algo pendiente mientras estudias, anótalo ahí para sacarlo de tu cabeza y revísalo solo al final.")
    ]
}

bibliografia_saber_mas = [
    "Chou, Y. (2025). 10,000 Hours of Play: The Science of Gamification and Engagement. Octalysis Media.",
    "Clark, G. (2025). The AI Primary Classroom: How to Use Artificial Intelligence to Enhance Learning in Primary Education. Routledge.",
    "García, J. A., & Martínez, M. (2025). Chatbots en la enseñanza: Asistentes virtuales y aprendizaje ubicuo. Editorial Octaedro.",
    "Harvard Business Review. (2025). The Year in Tech, 2026: The Insights You Need from Harvard Business Review. Harvard Business Review Press.",
    "López, R. (2024). Chatbots educativos: Inteligencia artificial transformando el aprendizaje. Ediciones Gesvin.",
    "Mollick, E. (2026). Co-Intelligence: Living and Working with AI. Virtual Enterprise Press.",
    "Narayanan, A., & Kapoor, S. (2024). AI Snake Oil: What Artificial Intelligence Can Do, What It Can't, and How to Tell the Difference. Princeton University Press.",
    "Rodríguez, A. (2025). Inteligencia artificial aplicada a la educación: Manual para docentes, estudiantes y directivos. Alpha Editorial.",
    "Sánchez, M., & Torres, L. (2025). Manual de gamificación y AI en educación: Estrategias lúdicas digitales. Editorial Universitaria.",
    "Springer Nature. (2026). Gamified Education: Innovating Learning Through Play and Technology. Springer International Publishing.",
    "Suleyman, M., & Bhaskar, M. (2024). The Coming Wave: Technology, Power, and the Twenty-first Century's Greatest Dilemma. Crown Publishing Group."
]

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

def responder_con_openai(mensaje, tema, estado_animo):
    if client is None:
        return "No encontré una API key configurada. Agrega OPENAI_API_KEY en los secretos de Streamlit o en .streamlit/secrets.toml."

    try:
        prompt_sistema = f"""
Eres TiTA IA, un chatbot educativo gamificado.
Responde en español, de forma clara, útil y pedagógica.
Contexto del estudiante:
- Tema principal: {tema}
- Estado inicial: {estado_animo}

Instrucciones:
- Responde como tutor de apoyo.
- Sé concreto pero explicativo.
- Si aplica, sugiere una estrategia de estudio.
- No inventes fuentes.
- Si la pregunta se relaciona con motivación, organización del tiempo, IA, gamificación o aprendizaje autónomo, conecta tu respuesta con el propósito educativo de TiTA IA.
"""
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": mensaje}
            ]
        )
        return response.output_text

    except Exception as e:
        return f"Ocurrió un error al consultar OpenAI: {e}"

def responder(mensaje):
    m = mensaje.lower()

    if "hola" in m or "buenas" in m:
        return "¡Hola! Qué bueno tenerte aquí. Cuéntame, ¿quieres resolver una duda, hacer un reto o revisar estrategias para estudiar mejor?"
    elif "cómo ayuda la ia" in m or "como ayuda la ia" in m or "ia en educación" in m:
        return """La IA en educación puede aportar en varios niveles:
1) **Personalización**, porque adapta recomendaciones y respuestas según la necesidad del estudiante;
2) **Retroalimentación inmediata**, útil para resolver dudas en tiempo real;
3) **Acompañamiento continuo**, especialmente en entornos híbridos o virtuales;
4) **Organización del aprendizaje**, al sugerir rutas, prioridades y estrategias;
5) **Analítica**, al identificar patrones de interacción que luego pueden orientar mejoras pedagógicas.

Su valor no está en reemplazar al docente, sino en ampliar el acceso, ofrecer apoyo oportuno y hacer más flexible la experiencia formativa."""
    elif "gamificación" in m or "gamificacion" in m:
        return """La gamificación es la incorporación de mecánicas del juego en contextos no lúdicos, como el aprendizaje.
En educación, esto puede incluir **puntos, insignias, niveles, retos, metas visibles, recompensas y sensación de progreso**.

Su fuerza pedagógica está en varios frentes:
1) aumenta la motivación y el compromiso;
2) hace visible el avance del estudiante;
3) favorece la continuidad y los hábitos;
4) transforma tareas que parecen pesadas en experiencias más dinámicas;
5) refuerza la participación mediante reconocimiento simbólico.

Además, este mismo entorno usa gamificación con **insignias** para reconocer tu progreso. Si quieres profundizar, puedes revisar la sección **Ver insignias** y también el recurso de **Saber más** al final."""
    elif "aprendizaje adaptativo" in m:
        return "El aprendizaje adaptativo ajusta recomendaciones, dificultad y orientación según el desempeño, el ritmo y las necesidades del estudiante. En TiTA IA esto se refleja en rutas de apoyo personalizadas."
    elif "aprendizaje autónomo" in m or "autonomo" in m:
        return "TiTA IA fortalece el aprendizaje autónomo al ofrecer orientación en tiempo real, metas pequeñas, retroalimentación inmediata y seguimiento del progreso."
    elif "educación híbrida" in m or "hibrida" in m:
        return "En educación híbrida, TiTA IA puede acompañar al estudiante tanto dentro como fuera del aula, integrando apoyo conversacional, retos y seguimiento en escenarios presenciales y virtuales."
    elif "motivación" in m or "motivar" in m:
        return "Cuando la motivación baja, conviene reducir la barrera de inicio, usar recompensas visibles y apoyarte en técnicas concretas. Abajo puedes entrar al recurso especial **Manual de técnicas de motivación** para explorar opciones útiles."
    elif "tiempo" in m or "organización" in m or "organizar" in m:
        return "Claro. Puedo ayudarte con técnicas para organizar tu tiempo, como Pomodoro, Flowtime, 50/10, 90/20, Kaizen o bloques personalizados. Abajo puedes abrir el recurso **Métodos de productividad para organizar tu tiempo**."
    elif "quiero leer" in m or "leer" in m:
        return "¡Qué buena idea! Abajo, en los recursos especiales, tienes el menú desplegable **Saber más**, donde reunimos libros y textos para entender mejor herramientas, procesos, IA, chatbots y gamificación."
    elif "reto" in m or "actividad" in m or "ejercicio" in m:
        st.session_state.page = "reto"
        st.session_state.reto_actual = random.choice(retos_abiertos)
        return "¡Vamos con toda! Te llevo a un reto breve para poner en práctica lo aprendido."
    elif "quiz" in m:
        st.session_state.page = "quiz"
        return "Perfecto. Te llevaré a un quiz rápido de 5 preguntas para seguir sumando puntos."
    elif "ética" in m or "uso responsable" in m or "manual" in m:
        st.session_state.page = "manual_ia"
        return "Claro. Te llevo al minimanual de uso responsable y ético de la IA para el aprendizaje."
    else:
        return responder_con_openai(
            mensaje,
            st.session_state.tema,
            st.session_state.estado_animo or "Sin registrar"
        )

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

    st.write("### 1. Tema principal")
    st.write(f"**{st.session_state.tema}**")

    st.write("### 2. Estado inicial")
    st.write(f"**{st.session_state.estado_animo or 'Sin registrar'}**")

    st.write("### 3. Acciones rápidas")
    c1, c2, c3 = st.columns(3)
    if c1.button("¿Qué es la gamificación?"):
        q = "¿Qué es la gamificación?"
        st.session_state.chat.append({"role": "user", "content": q})
        st.session_state.chat.append({"role": "assistant", "content": responder(q)})
        recompensar(10, -2)
        registrar_interaccion("pregunta_rápida")
        st.rerun()

    if c2.button("¿Cómo ayuda la IA en educación?"):
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

    if c6.button("Hazme un quiz rápido"):
        q = "Hazme un quiz"
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_contestado = False
        st.session_state.quiz_feedback = ""
        st.session_state.chat.append({"role": "user", "content": q})
        st.session_state.chat.append({"role": "assistant", "content": responder("quiz")})
        recompensar(12, -3)
        registrar_interaccion("quiz")
        st.rerun()

    c7, c8, c9 = st.columns(3)
    if c7.button("Quiero leer"):
        q = "Quiero leer"
        st.session_state.chat.append({"role": "user", "content": q})
        st.session_state.chat.append({"role": "assistant", "content": responder(q)})
        recompensar(8, -1)
        registrar_interaccion("lectura")
        st.rerun()

    st.write("### 4. Chat bot")
    for msg in st.session_state.chat:
        with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
            st.write(msg["content"])

    mensaje_usuario = st.chat_input("Escribe tu pregunta aquí...")
    if mensaje_usuario:
        st.session_state.chat.append({"role": "user", "content": mensaje_usuario})
        st.session_state.chat.append({"role": "assistant", "content": responder(mensaje_usuario)})
        recompensar(15, -3)
        registrar_interaccion("consulta_libre")
        st.rerun()

    st.write("### 5. Seguimiento")
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

    st.write("### 6. Recursos especiales")

    col_r1, col_r2, col_r3 = st.columns(3)

    with col_r1:
        st.info("🌿 Uso responsable")
        if st.button("Minimanual de uso responsable de IA"):
            st.session_state.page = "manual_ia"
            st.rerun()

    with col_r2:
        if st.button("Métodos de productividad para organizar tu tiempo"):
            st.session_state.page = "manual_tiempo"
            st.rerun()

    with col_r3:
        if st.button("Manual de técnicas de motivación"):
            st.session_state.page = "manual_motivacion"
            st.rerun()

    with st.expander("📚 Saber más"):
        st.write("Estos libros y textos te ayudan a entender mejor herramientas, procesos, chatbots, gamificación e inteligencia artificial aplicada al aprendizaje.")
        for ref in bibliografia_saber_mas:
            st.write(f"- {ref}")

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
            st.info("Retroalimentación TiTA: tu respuesta muestra comprensión del tema. El siguiente paso recomendado es complementar esta reflexión con el quiz o una nueva consulta.")
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

    total_preguntas = len(quizzes)

    if st.session_state.quiz_index < total_preguntas:
        pregunta_actual = quizzes[st.session_state.quiz_index]
        st.write(f"**Pregunta {st.session_state.quiz_index + 1} de {total_preguntas}**")
        st.progress((st.session_state.quiz_index + 1) / total_preguntas)
        st.write(pregunta_actual["pregunta"])

        opcion = st.radio(
            "Selecciona una respuesta",
            pregunta_actual["opciones"],
            key=f"quiz_radio_{st.session_state.quiz_index}"
        )

        if not st.session_state.quiz_contestado:
            if st.button("Responder pregunta"):
                respuesta_correcta = pregunta_actual["correcta"]

                if opcion == respuesta_correcta:
                    st.session_state.quiz_score += 1
                    recompensar(10, -2)
                    st.session_state.quiz_feedback = (
                        f"✅ **Respuesta correcta:** {respuesta_correcta}\n\n"
                        f"{pregunta_actual['retro']}\n\n"
                        "Esta respuesta es correcta porque se alinea con el propósito del prototipo: "
                        "ofrecer acompañamiento académico, retroalimentación contextualizada y apoyo al aprendizaje autónomo."
                    )
                    st.success("¡Correcta! +10 puntos.")
                else:
                    recompensar(3, -1)
                    st.session_state.quiz_feedback = (
                        f"❌ **Tu respuesta:** {opcion}\n\n"
                        f"✅ **La respuesta correcta era:** {respuesta_correcta}\n\n"
                        f"{pregunta_actual['retro']}\n\n"
                        "La opción que elegiste no era la más adecuada porque no refleja con precisión "
                        "el enfoque del proyecto ni las funciones centrales de TiTA IA. "
                        "La idea es que el quiz no solo evalúe, sino que también te ayude a comprender mejor el concepto."
                    )
                    st.error("Respuesta incorrecta. +3 puntos por participar.")

                registrar_interaccion("respuesta_quiz")
                st.session_state.quiz_contestado = True
                st.rerun()

        else:
            st.info(st.session_state.quiz_feedback)
            if st.button("Siguiente pregunta"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_contestado = False
                st.session_state.quiz_feedback = ""
                st.rerun()
    else:
        st.success(f"Terminaste el quiz. Resultado final: {st.session_state.quiz_score}/{total_preguntas}")

        if st.session_state.quiz_score == total_preguntas:
            st.balloons()
            st.info("Excelente desempeño. Dominas muy bien los conceptos centrales del prototipo.")
        elif st.session_state.quiz_score >= 3:
            st.info("Buen resultado. Tienes una comprensión sólida, aunque todavía puedes reforzar algunos conceptos.")
        else:
            st.warning("Terminaste el quiz, pero conviene repasar temas como IA en educación, gamificación y uso responsable antes de seguir avanzando.")

        st.write("### ¿Qué sigue?")
        st.write("Puedes volver al chat para resolver dudas, revisar las insignias o consultar los recursos especiales para fortalecer tu comprensión de los temas.")

        c1, c2 = st.columns(2)
        if c1.button("Volver al chat desde quiz"):
            st.session_state.page = "chat"
            st.rerun()
        if c2.button("Ver progreso desde quiz"):
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
        st.warning("Te conviene empezar por metas pequeñas, recompensas visibles y estrategias que reduzcan la fricción de iniciar.")
    elif st.session_state.estado_animo == "Cansado/a":
        st.info("Lo ideal es trabajar en sesiones cortas o intermedias, alternar teoría y práctica, e incorporar pausas reales.")
    else:
        st.success("Tu disposición es favorable. Puedes avanzar a desafíos más complejos y profundizar en temas como analítica o educación híbrida.")

    st.write("### Próximo paso sugerido")
    if st.session_state.puntos < 40:
        st.info("Haz dos consultas más y luego completa un reto.")
    elif st.session_state.puntos < 90:
        st.info("Tu progreso va bien. Ahora conviene combinar quiz, consulta abierta y revisión de insignias.")
    else:
        st.info("Ya tienes una participación sólida. El siguiente paso es explorar escalabilidad, analítica del aprendizaje e integración con LMS.")

    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Volver al chat"):
        st.session_state.page = "chat"
        st.rerun()
    if c2.button("Ver insignias"):
        st.session_state.page = "insignias"
        st.rerun()
    if c3.button("Ver minimanual IA"):
        st.session_state.page = "manual_ia"
        st.rerun()
    if c4.button("Reiniciar demo"):
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
                st.markdown(f"""
                <div class="bloque-naranja">
                    <div class="titulo-bonito">¿Qué significa?</div>
                    <div class="texto-suave">{descripciones_insignias[ins]['descripcion']}</div>
                </div>
                <div class="bloque-verde">
                    <div class="titulo-bonito">¿Cómo se obtiene?</div>
                    <div class="texto-suave">{descripciones_insignias[ins]['como']}</div>
                </div>
                <div class="bloque-azul">
                    <div class="titulo-bonito">¿Qué reconoce?</div>
                    <div class="texto-suave">{descripciones_insignias[ins]['valor']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Aún no has desbloqueado insignias. Sigue interactuando con TiTA para obtenerlas.")

    st.write("### Insignias disponibles")
    for nombre, info in descripciones_insignias.items():
        with st.expander(f"✨ {nombre}"):
            st.markdown(f"""
            <div class="bloque-color">
                <div class="titulo-bonito">Descripción</div>
                <div class="texto-suave">{info['descripcion']}</div>
            </div>
            <div class="bloque-verde">
                <div class="titulo-bonito">Cómo se obtiene</div>
                <div class="texto-suave">{info['como']}</div>
            </div>
            <div class="bloque-azul">
                <div class="titulo-bonito">Valor pedagógico</div>
                <div class="texto-suave">{info['valor']}</div>
            </div>
            """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    if c1.button("Volver al chat desde insignias"):
        st.session_state.page = "chat"
        st.rerun()
    if c2.button("Ir al progreso desde insignias"):
        st.session_state.page = "progreso"
        st.rerun()

# =========================================
# MANUAL TIEMPO
# =========================================
elif st.session_state.page == "manual_tiempo":
    st.title("⏱️ Métodos de productividad para organizar tu tiempo")
    st.write("Estos métodos te ayudan a estudiar con más estructura, menos saturación y mejor gestión de energía.")

    for nombre, info in metodos_productividad.items():
        with st.expander(f"⏱️ {nombre}"):
            st.markdown(f"""
            <div class="bloque-azul">
                <div class="titulo-bonito">¿En qué consiste?</div>
                <div class="texto-suave">{info['descripcion']}</div>
            </div>
            <div class="bloque-verde">
                <div class="titulo-bonito">¿Cuándo usarlo?</div>
                <div class="texto-suave">{info['cuando_usarlo']}</div>
            </div>
            <div class="bloque-naranja">
                <div class="titulo-bonito">Ejemplo práctico</div>
                <div class="texto-suave">{info['ejemplo']}</div>
            </div>
            """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    if c1.button("Volver al chat desde tiempo"):
        st.session_state.page = "chat"
        st.rerun()
    if c2.button("Ir al progreso desde tiempo"):
        st.session_state.page = "progreso"
        st.rerun()

# =========================================
# MANUAL MOTIVACION
# =========================================
elif st.session_state.page == "manual_motivacion":
    st.title("🚀 Manual de técnicas de motivación")
    st.write("Estas técnicas ayudan a empezar cuando cuesta arrancar, sostener la atención y hacer visible el progreso.")

    for categoria, tecnicas in manual_motivacion.items():
        st.markdown(f"""
        <div class="bloque-color">
            <div class="titulo-bonito">{categoria}</div>
            <div class="texto-suave">Explora estas estrategias para activar tu motivación y sostener el estudio.</div>
        </div>
        """, unsafe_allow_html=True)

        for nombre, descripcion in tecnicas:
            st.markdown(f"""
            <div class="bloque-rosa">
                <div class="titulo-bonito">{nombre}</div>
                <div class="texto-suave">{descripcion}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bloque-verde">
        <div class="titulo-bonito">Tip TiTA</div>
        <div class="texto-suave">Si te interesa la gamificación, recuerda que este mismo entorno usa insignias como parte del refuerzo positivo. Puedes revisar más en la sección "Ver insignias".</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    if c1.button("Volver al chat desde motivación"):
        st.session_state.page = "chat"
        st.rerun()
    if c2.button("Ir al progreso desde motivación"):
        st.session_state.page = "progreso"
        st.rerun()

# =========================================
# MANUAL IA
# =========================================
elif st.session_state.page == "manual_ia":
    st.title("📘 Minimanual de uso responsable y ético de la IA")
    st.write("Este minimanual promueve un uso crítico, humano y ambientalmente consciente de TiTA IA.")

    st.markdown("""
    <div class="bloque-verde">
        <div class="titulo-bonito">1. La IA apoya, pero no reemplaza tu pensamiento</div>
        <div class="texto-suave">Usa TiTA IA para orientarte, aclarar dudas, practicar y organizarte; no para copiar respuestas sin comprenderlas.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bloque-azul">
        <div class="titulo-bonito">2. Contrasta la información</div>
        <div class="texto-suave">Toda respuesta del chatbot debe compararse con tus apuntes, lecturas, fuentes académicas y orientación docente.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bloque-color">
        <div class="titulo-bonito">3. Mantén tu agencia como estudiante</div>
        <div class="texto-suave">La decisión final sobre qué estudiar, cómo interpretarlo y cómo argumentarlo sigue siendo tuya. La IA debe fortalecer tu autonomía, no anularla.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bloque-rosa">
        <div class="titulo-bonito">4. Evita la dependencia excesiva</div>
        <div class="texto-suave">No conviertas a TiTA IA en sustituto permanente del análisis, la escritura propia o la reflexión. Úsala como apoyo, no como piloto automático.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bloque-verde">
        <div class="titulo-bonito">5. Sé transparente con su uso</div>
        <div class="texto-suave">Si usaste IA para organizar ideas, resumir o practicar, reconócelo cuando sea necesario dentro del contexto académico.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bloque-azul">
        <div class="titulo-bonito">6. Cuidado con datos personales</div>
        <div class="texto-suave">Evita compartir información sensible, datos privados, contraseñas o contenidos que no deban circular en plataformas digitales.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bloque-naranja">
        <div class="titulo-bonito">7. Piensa también en el impacto ambiental</div>
        <div class="texto-suave">La IA funciona sobre infraestructura de centros de datos que consume energía y también agua, especialmente para refrigeración. Por eso conviene usarla con intención, hacer consultas útiles y evitar interacciones innecesarias.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bloque-color">
        <div class="titulo-bonito">8. Regla TiTA de uso inteligente</div>
        <div class="texto-suave">Pregunta con intención, aprende con criterio, contrasta con otras fuentes y conserva siempre tu protagonismo cognitivo.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    if c1.button("Volver al chat desde manual"):
        st.session_state.page = "chat"
        st.rerun()
    if c2.button("Ir al progreso desde manual"):
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