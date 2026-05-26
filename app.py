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
if "mostrar_metodos_tiempo" not in st.session_state:
    st.session_state.mostrar_metodos_tiempo = False

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
        "retro": "Exactamente. El uso responsable de la IA implica apoyo, no reemplazo del pensamiento crítico, la autonomía ni la supervisión pedagógica."
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

metodos_productividad = {
    "Método Flowtime": {
        "descripcion": "Trabajas de forma continua hasta notar fatiga o distracción, y luego defines la pausa según el tiempo real que estuviste concentrado/a.",
        "cuando_usarlo": "Es ideal si entras en concentración profunda y no quieres cortar el ritmo con un cronómetro rígido.",
        "ejemplo": "Si estudiaste 45 minutos con buena concentración, puedes tomar 10 minutos de descanso."
    },
    "Método 50/10 o 52/17": {
        "descripcion": "Consiste en estudiar entre 50 y 52 minutos con concentración total y luego descansar entre 10 y 17 minutos.",
        "cuando_usarlo": "Sirve mucho para tareas largas, lecturas densas, epígrafes extensos o sesiones universitarias exigentes.",
        "ejemplo": "50 minutos de lectura crítica + 10 minutos de pausa para moverte, hidratarte o despejarte."
    },
    "Técnica 90/20": {
        "descripcion": "Se basa en ciclos ultradianos: 90 minutos de trabajo intenso seguidos por 20 minutos de descanso real.",
        "cuando_usarlo": "Es útil para personas con buena capacidad de atención sostenida o cuando necesitas hiperfoco.",
        "ejemplo": "90 minutos desarrollando un trabajo o estudiando para examen + 20 minutos de desconexión total."
    },
    "Técnica 'Solo un poquito' (Kaizen)": {
        "descripcion": "Consiste en empezar por una meta muy pequeña para reducir la resistencia psicológica al inicio.",
        "cuando_usarlo": "Es perfecta si estás procrastinando o te cuesta mucho arrancar.",
        "ejemplo": "Leer una sola página, escribir una idea o estudiar 5 minutos; luego decides si paras o sigues."
    },
    "Bloques personalizados": {
        "descripcion": "Ajustas la duración de las sesiones según tu energía y nivel de cansancio, en vez de usar una sola fórmula fija.",
        "cuando_usarlo": "Es ideal si ya conoces tus ritmos y quieres combinar bloques largos y cortos estratégicamente.",
        "ejemplo": "Empiezas con 90 minutos en tu momento de más energía y luego haces bloques de 50 o 25 minutos."
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
        badges.append("Jugador 