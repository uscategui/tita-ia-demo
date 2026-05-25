import os
import json
import time
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="TiTA IA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- ESTILOS ----------
st.markdown("""
<style>
:root {
    --bg: #f6f4ef;
    --card: #fffdf9;
    --soft: #f0ebe2;
    --line: #ddd4c8;
    --text: #24211c;
    --muted: #6f6a61;
    --primary: #0f766e;
    --primary-2: #115e59;
    --accent: #eab308;
    --success: #2e7d32;
    --danger: #a61b4a;
}

html, body, [class*="css"]  {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

.stApp {
    background:
      radial-gradient(circle at top right, rgba(15,118,110,.08), transparent 24%),
      radial-gradient(circle at bottom left, rgba(234,179,8,.08), transparent 22%),
      var(--bg);
    color: var(--text);
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 1rem;
    max-width: 1400px;
}

h1, h2, h3 {
    color: var(--text);
    letter-spacing: -0.02em;
}

.hero {
    background: linear-gradient(135deg, #fffdf9 0%, #f3eee6 100%);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 10px 30px rgba(0,0,0,.04);
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: .35rem;
}

.hero-sub {
    color: var(--muted);
    font-size: 1rem;
}

.chip-row {
    display: flex;
    gap: .5rem;
    flex-wrap: wrap;
    margin-top: .9rem;
}

.chip {
    display: inline-block;
    padding: .42rem .75rem;
    border-radius: 999px;
    background: #efe8db;
    border: 1px solid var(--line);
    color: var(--text);
    font-size: .88rem;
    font-weight: 600;
}

.metric-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 1rem;
}

.metric-label {
    color: var(--muted);
    font-size: .85rem;
}
.metric-value {
    font-size: 1.45rem;
    font-weight: 800;
}

.feedback-box {
    background: #fffaf0;
    border: 1px dashed #e3c978;
    border-radius: 16px;
    padding: .9rem 1rem;
    color: #634c10;
    margin-top: .75rem;
}

.tita-bubble {
    background: #fffdf9;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: .9rem 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,.03);
}

.user-bubble {
    background: #dff3ef;
    border: 1px solid #b7ddd7;
    border-radius: 18px;
    padding: .9rem 1rem;
}

.small-note {
    color: var(--muted);
    font-size: .84rem;
}

.sidebar-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: .85rem;
    margin-bottom: .8rem;
}

.mission-box {
    background: linear-gradient(135deg, #fff7db 0%, #fff3c1 100%);
    border: 1px solid #edd67a;
    border-radius: 18px;
    padding: .95rem;
}

hr {
    border: none;
    border-top: 1px solid var(--line);
    margin: .8rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ---------- ESTADO ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! Soy **TiTA IA** 🎓✨ Tu compañera de estudio gamificada. Puedo ayudarte a comprender temas, planear tareas, repasar conceptos y mantener el ritmo con un tono claro, técnico y fresco. ¿Qué estás estudiando hoy?"
        }
    ]

if "points" not in st.session_state:
    st.session_state.points = 20
if "level" not in st.session_state:
    st.session_state.level = 1
if "streak" not in st.session_state:
    st.session_state.streak = 1
if "missions_done" not in st.session_state:
    st.session_state.missions_done = []
if "student_name" not in st.session_state:
    st.session_state.student_name = "Estudiante"
if "learning_mode" not in st.session_state:
    st.session_state.learning_mode = "Equilibrado"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Intermedio"

# ---------- LÓGICA ----------
mission_catalog = {
    "Hacer una pregunta": {"points": 10, "badge": "Curiosidad activada"},
    "Pedir un quiz": {"points": 15, "badge": "Modo reto"},
    "Solicitar plan de estudio": {"points": 20, "badge": "Estratega"},
    "Resolver una duda compleja": {"points": 25, "badge": "Pensamiento crítico"},
}

quick_prompts = [
    "Explícame este tema fácil pero con rigor",
    "Hazme un mini quiz de 5 preguntas",
    "Ayúdame a estudiar en 20 minutos",
    "Resume este concepto en puntos clave",
    "Dame un ejemplo aplicado",
    "Conviértelo en una actividad gamificada",
]

def compute_level(points: int) -> int:
    if points >= 180:
        return 5
    if points >= 120:
        return 4
    if points >= 75:
        return 3
    if points >= 35:
        return 2
    return 1


def award_points(reason: str):
    if reason in mission_catalog and reason not in st.session_state.missions_done:
        st.session_state.points += mission_catalog[reason]["points"]
        st.session_state.missions_done.append(reason)
        st.session_state.level = compute_level(st.session_state.points)
        return f"🏅 Ganaste {mission_catalog[reason]['points']} puntos por: {reason}. Insignia: {mission_catalog[reason]['badge']}."
    return None


def detect_intent(user_text: str) -> str:
    text = user_text.lower()
    if any(k in text for k in ["quiz", "preguntas", "evalúame", "evaluame", "reto"]):
        return "quiz"
    if any(k in text for k in ["plan", "cronograma", "organiza", "estudio", "horario"]):
        return "plan"
    if any(k in text for k in ["resume", "resumen", "síntesis", "sintesis", "puntos clave"]):
        return "summary"
    if any(k in text for k in ["ejemplo", "aplicado", "caso"]):
        return "example"
    return "explain"


def build_quiz(topic: str) -> str:
    return f"""
### 🎯 Mini quiz sobre {topic}
1. ¿Cuál es la idea central de {topic}?
2. ¿Qué problema resuelve o qué necesidad atiende?
3. ¿Qué concepto técnico está más relacionado con {topic}?
4. ¿Cómo se aplicaría {topic} en un contexto real?
5. ¿Qué error común se debe evitar al trabajar este tema?

**Modo pro:** responde una por una y yo te doy retroalimentación inmediata, breve y útil.
"""


def build_study_plan(topic: str) -> str:
    return f"""
### 🗂️ Plan express para estudiar {topic}
**Bloque 1 — Activación (5 min):** escribe qué entiendes por {topic} y qué te confunde.
**Bloque 2 — Comprensión (10 min):** identifica definición, características, ventajas y límites.
**Bloque 3 — Aplicación (10 min):** crea un ejemplo real o académico.
**Bloque 4 — Cierre (5 min):** resume {topic} en 3 ideas clave y 1 pregunta pendiente.

**Tip TiTA:** si estudias en sesiones cortas pero consistentes, retienes mejor y reduces la saturación cognitiva.
"""


def build_summary(topic: str) -> str:
    return f"""
### ✍️ Resumen ágil de {topic}
- Es un tema que conviene entender desde su **definición**, **función** y **aplicación**.
- Para dominarlo, no basta memorizar: hay que relacionarlo con un caso, problema o escenario real.
- Una buena respuesta académica sobre {topic} debería incluir concepto, contexto, ejemplo y reflexión crítica.
- Si quieres, después lo convertimos en mapa conceptual, ficha de estudio o quiz.
"""


def build_example(topic: str) -> str:
    return f"""
### 💡 Ejemplo aplicado de {topic}
Imagina un curso universitario donde el estudiantado necesita comprender {topic}. En vez de limitarse a teoría, el docente propone una actividad práctica, un caso real y una instancia de retroalimentación. Así, {topic} deja de ser una idea abstracta y se convierte en una herramienta para analizar, decidir y producir conocimiento.

**Lectura técnica, pero fresca:** entender un concepto no es solo “saber qué dice”, sino poder usarlo con criterio.
"""


def fallback_response(user_text: str) -> str:
    return f"""
### 🧠 Vamos con toda
Leí tu mensaje: **{user_text}**

Puedo ayudarte de varias formas:
- explicártelo paso a paso,
- convertirlo en resumen,
- diseñarte un quiz,
- organizarte un mini plan de estudio,
- o volverlo más académico para una entrega.

**Versión TiTA:** dime si lo quieres en modo *claro*, *técnico*, *creativo* o *rápido*.
"""


def local_response(user_text: str) -> str:
    bonus_msgs = []
    bonus = award_points("Hacer una pregunta")
    if bonus:
        bonus_msgs.append(bonus)

    intent = detect_intent(user_text)
    topic = user_text.strip().capitalize()

    if intent == "quiz":
        extra = award_points("Pedir un quiz")
        if extra:
            bonus_msgs.append(extra)
        body = build_quiz(topic)
    elif intent == "plan":
        extra = award_points("Solicitar plan de estudio")
        if extra:
            bonus_msgs.append(extra)
        body = build_study_plan(topic)
    elif intent == "summary":
        body = build_summary(topic)
    elif intent == "example":
        body = build_example(topic)
    else:
        body = fallback_response(user_text)

    energy = {
        "Principiante": "Voy a explicártelo con base conceptual, vocabulario claro y ejemplos concretos.",
        "Intermedio": "Voy a mantener un balance entre precisión conceptual y lenguaje cercano.",
        "Avanzado": "Voy a responder con mayor densidad conceptual, relaciones críticas y aplicación académica."
    }

    mode_line = {
        "Visual y amigable": "🎨 Te lo presentaré de forma clara, ordenada y fácil de escanear.",
        "Equilibrado": "⚖️ Mantendré un tono pedagógico, técnico y cercano.",
        "Reto académico": "🚀 Subimos el nivel: más análisis, más síntesis y más exigencia intelectual."
    }

    suffix = ""
    if bonus_msgs:
        suffix = "\n\n---\n" + "\n".join([f"- {m}" for m in bonus_msgs])

    return f"{mode_line.get(st.session_state.learning_mode)}\n\n{energy.get(st.session_state.difficulty)}\n\n{body}{suffix}"


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
    st.markdown("### 🎮 Perfil TiTA")
    st.text_input("Tu nombre", key="student_name")
    st.selectbox("Modo de interacción", ["Visual y amigable", "Equilibrado", "Reto académico"], key="learning_mode")
    st.selectbox("Nivel de profundidad", ["Principiante", "Intermedio", "Avanzado"], key="difficulty")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
    st.markdown("### 🧩 Misiones")
    for m, info in mission_catalog.items():
        done = "✅" if m in st.session_state.missions_done else "⬜"
        st.write(f"{done} {m} (+{info['points']} pts)")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='mission-box'>", unsafe_allow_html=True)
    st.markdown("### 🌟 Tip del día")
    st.write("Combina preguntas cortas, repaso activo y mini retos para mejorar retención y motivación.")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 Reiniciar conversación", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "¡Reiniciamos! Soy TiTA IA 🎓✨ Lista para acompañarte otra vez. Cuéntame qué tema quieres trabajar."
            }
        ]
        st.session_state.points = 20
        st.session_state.level = 1
        st.session_state.streak = 1
        st.session_state.missions_done = []
        st.rerun()

# ---------- CABECERA ----------
st.markdown(f"""
<div class='hero'>
    <div class='hero-title'>TiTA IA · chatbot educativo gamificado</div>
    <div class='hero-sub'>Acompañamiento académico interactivo, aprendizaje adaptativo y una experiencia más humana, fresca y útil.</div>
    <div class='chip-row'>
        <span class='chip'>🤖 IA conversacional</span>
        <span class='chip'>🎯 Gamificación</span>
        <span class='chip'>📚 Aprendizaje adaptativo</span>
        <span class='chip'>💬 Feedback inmediato</span>
    </div>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Estudiante</div><div class='metric-value'>{st.session_state.student_name}</div></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Puntos</div><div class='metric-value'>{st.session_state.points}</div></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Nivel</div><div class='metric-value'>Lv. {compute_level(st.session_state.points)}</div></div>", unsafe_allow_html=True)
with m4:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Misiones completas</div><div class='metric-value'>{len(st.session_state.missions_done)}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- ATAJOS ----------
st.markdown("#### ⚡ Atajos para empezar")
qcols = st.columns(3)
for i, prompt in enumerate(quick_prompts):
    with qcols[i % 3]:
        if st.button(prompt, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            reply = local_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ---------- CHAT ----------
st.markdown("#### 💬 Conversación")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(f"<div class='tita-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

user_input = st.chat_input("Escribe tu pregunta, tema o tarea…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f"<div class='user-bubble'>{user_input}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("TiTA está pensando tu mejor ruta de aprendizaje…"):
            time.sleep(0.6)
            answer = local_response(user_input)
            st.markdown(f"<div class='tita-bubble'>{answer}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.level = compute_level(st.session_state.points)

# ---------- PIE / AYUDA ----------
left, right = st.columns([1.2, 1])
with left:
    st.markdown("### 🛠️ Cómo mejorar el bot")
    st.markdown("""
- Conectar un modelo real vía API para respuestas más potentes.
- Integrar base de datos para usuarios, progreso y analítica.
- Añadir quizzes autocorregibles y tableros docentes.
- Conectar con Moodle o LMS institucional.
- Incorporar ranking, insignias y rutas de aprendizaje.
""")
with right:
    st.markdown("### 📌 Nota técnica")
    st.markdown("<div class='feedback-box'>Esta versión funciona como MVP interactivo en Streamlit con lógica local. Para convertirla en un asistente de IA completo, se puede enlazar con OpenAI, Claude o Gemini mediante variables de entorno y una capa de seguridad para datos educativos.</div>", unsafe_allow_html=True)