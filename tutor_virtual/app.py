import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError, AuthenticationError, RateLimitError, APIConnectionError

# Cargar variables de entorno desde un archivo .env si existe
load_dotenv()

# Configuración visual de la página
st.set_page_config(
    page_title="Tutor Virtual Inteligente",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para mejorar la apariencia visual
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #6c757d;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        background-color: #e3f2fd;
        color: #1976d2;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Barra Lateral (Sidebar)
# ---------------------------------------------------------
with st.sidebar:
    st.header("Configuración del Tutor")
    
    # 1. Entrada de API Key (oculta tipo password)
    env_api_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input(
        "OpenAI API Key:",
        value=env_api_key,
        type="password",
        placeholder="sk-proj-...",
        help="Introduce tu clave de API de OpenAI. Si está definida en un archivo .env como OPENAI_API_KEY, se precargará automáticamente."
    )
    
    st.divider()
    
    # 2. Selección del Área de Conocimiento
    area_conocimiento = st.selectbox(
        "Área de Conocimiento:",
        options=["Programación", "Matemáticas", "IA", "General"],
        index=0,
        help="El tutor adaptará sus ejemplos, terminología y enfoque según el área seleccionada."
    )
    
    # 3. Control deslizante para el Nivel de Explicación
    niveles = ["Principiante", "Intermedio", "Avanzado"]
    nivel_explicacion = st.select_slider(
        "Nivel de Explicación:",
        options=niveles,
        value="Intermedio",
        help="Ajusta la profundidad técnica, complejidad y analogías pedagógicas."
    )
    
    st.divider()
    
    # 4. Botón para reiniciar o limpiar la sesión de chat
    if st.button("Reiniciar / Limpiar Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("initialized", None)
        st.rerun()

    st.markdown("---")
    st.caption(
        "**Modelo:** `gpt-4o-mini`  \n"
        "**Metodología:** Método socrático, explicación guiada paso a paso y preguntas de comprobación activa."
    )

# ---------------------------------------------------------
# Encabezado Principal
# ---------------------------------------------------------
st.markdown('<div class="main-title">Tutor Virtual Inteligente</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="subtitle">Acompañamiento pedagógico personalizado en <b>{area_conocimiento}</b> a nivel <b>{nivel_explicacion}</b>.</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Generación del System Prompt Pedagógico
# ---------------------------------------------------------
def construir_system_prompt(area: str, nivel: str) -> str:
    """
    Construye un prompt de sistema pedagógico adaptado al área y nivel del estudiante,
    enfatizando la explicación paso a paso y preguntas de comprobación.
    """
    instrucciones_nivel = {
        "Principiante": (
            "- Utiliza analogías cotidianas, explicaciones intuitivas y lenguaje claro y accesible.\n"
            "- Evita tecnicismos innecesarios sin antes definirlos de forma muy sencilla.\n"
            "- Desglosa los conceptos en pasos muy pequeños y fáciles de asimilar."
        ),
        "Intermedio": (
            "- Combina fundamentos teóricos con aplicaciones prácticas y ejemplos reales.\n"
            "- Utiliza terminología técnica estándar con explicaciones contextuales.\n"
            "- Muestra código, fórmulas o diagramas explicativos cuando aporte valor a la comprensión."
        ),
        "Avanzado": (
            "- Profundiza en arquitectura, teoría formal, complejidades temporales/espaciales y casos límite.\n"
            "- Emplea rigor técnico, mejores prácticas de la industria y estándares formales.\n"
            "- Plantea discusiones sobre optimización, compensaciones (trade-offs) y diseño avanzado."
        )
    }

    instrucciones_area = {
        "Programación": (
            "- Enfoque en algoritmos, buenas prácticas de desarrollo, legibilidad y depuración.\n"
            "- Cuando proporciones código, añade comentarios didácticos y explica el propósito de cada bloque clave."
        ),
        "Matemáticas": (
            "- Guía la resolución de problemas paso a paso mostrando el razonamiento matemático.\n"
            "- Utiliza notación LaTeX ($...$ o $$...$$) para fórmulas claras y legibles.\n"
            "- Asegúrate de explicar el 'por qué' detrás de cada paso algebraico o conceptual."
        ),
        "IA": (
            "- Explica la intuición detrás de los modelos, hiperparámetros, datos de entrenamiento y métricas de evaluación.\n"
            "- Conecta los conceptos teóricos con aplicaciones prácticas y bibliotecas del ecosistema de IA."
        ),
        "General": (
            "- Responde con claridad estructurada, organizando las ideas en secciones bien delimitadas.\n"
            "- Ayuda al usuario a conectar el tema consultado con conceptos multidisciplinarios."
        )
    }

    return f"""Eres un Tutor Virtual Inteligente altamente calificado, paciente, empático y con gran vocación pedagógica.
Tu objetivo primordial es facilitar el aprendizaje significativo del estudiante, no simplemente darle respuestas automáticas o directas.

Directrices Pedagógicas Obligatorias:
1. Área de especialidad actual: {area}.
   {instrucciones_area.get(area, "")}
2. Nivel del estudiante: {nivel}.
   {instrucciones_nivel.get(nivel, "")}
3. Metodología de enseñanza:
   - Explica siempre los conceptos de forma estructurada y paso a paso.
   - Aplica el método socrático: guía al estudiante para que razone por sí mismo.
   - En cada intervención sustancial, concluye SIEMPRE con 1 o 2 preguntas de comprobación (o un pequeño reto/ejercicio) para validar que el estudiante ha comprendido el tema.
   - Si el estudiante responde de forma correcta, felicítalo y profundiza un poco más. Si comete un error, indícale amablemente el fallo con una pista constructiva sin desanimarlo.
4. Idioma y Tono:
   - Comunícate en español, con un tono motivador, formal, riguroso pero cercano.
   - Emplea formato Markdown con negritas, listas y bloques de código según corresponda.
"""

# ---------------------------------------------------------
# Gestión del Historial de Chat (Session State)
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mensaje de bienvenida inicial si la conversación está vacía
if len(st.session_state.messages) == 0:
    mensaje_bienvenida = (
        f"¡Hola! Soy tu **Tutor Virtual Inteligente**.  \n\n"
        f"Estoy listo para acompañarte en tus dudas de **{area_conocimiento}** en nivel **{nivel_explicacion}**.\n\n"
        f"¿Qué tema o ejercicio te gustaría revisar hoy? Explícame brevemente y lo analizaremos juntos paso a paso."
    )
    st.session_state.messages.append({"role": "assistant", "content": mensaje_bienvenida})

# Mostrar historial previo de mensajes en la interfaz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------
# Captura y Procesamiento de la Consulta del Usuario
# ---------------------------------------------------------
user_prompt = st.chat_input("Escribe tu duda o responde a la pregunta de comprobación del tutor...")

if user_prompt:
    # 1. Validar presencia de la API Key
    if not api_key:
        st.error("Por favor, ingresa tu OpenAI API Key en la barra lateral para continuar.")
        st.stop()
    
    # 2. Agregar mensaje del usuario al estado y mostrarlo
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 3. Preparar contexto para la API de OpenAI
    system_prompt = construir_system_prompt(area_conocimiento, nivel_explicacion)
    
    # Ensamblar mensajes para la API
    api_messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    # 4. Llamar a OpenAI con streaming y manejo de excepciones robusto
    with st.chat_message("assistant"):
        try:
            client = OpenAI(api_key=api_key)
            
            # Llamada al modelo gpt-4o-mini con streaming para fluidez
            response_stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
                temperature=0.7,
                stream=True
            )
            
            def stream_generator():
                for chunk in response_stream:
                    if chunk.choices and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if delta and delta.content:
                            yield delta.content

            # Mostrar respuesta de forma dinámica usando st.write_stream
            full_response = st.write_stream(stream_generator())
            
            # Guardar la respuesta generada en el historial
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except AuthenticationError:
            st.error("**Error de autenticación:** La API Key de OpenAI es inválida o no tiene permisos. Verifica la clave ingresada en la barra lateral.")
        except RateLimitError:
            st.error("**Límite de cuota excedido:** Has alcanzado el límite de peticiones o tu cuenta de OpenAI no tiene créditos suficientes.")
        except APIConnectionError:
            st.error("**Error de conexión:** No fue posible conectar con los servidores de OpenAI. Verifica tu conexión a internet.")
        except OpenAIError as oai_err:
            st.error(f"**Error en la API de OpenAI:** {oai_err}")
        except Exception as err:
            st.error(f"**Ocurrió un error inesperado:** {err}")
