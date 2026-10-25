# 🎓 Proyecto 2: Tutor Virtual Inteligente

Aplicación web interactiva desarrollada con **Streamlit** y la API de **OpenAI** (modelo `gpt-4o-mini`), diseñada para actuar como un tutor pedagógico personalizado que guía el aprendizaje paso a paso y refuerza los conocimientos mediante preguntas de comprobación activa.

---

## 🚀 Características Principales

- **Interfaz de Chat Moderna:** Basada en los componentes nativos de chat de Streamlit (`st.chat_message` y `st.chat_input`) con streaming en tiempo real para una interacción fluida.
- **Barra Lateral de Configuración:**
  - **API Key Segura:** Campo con máscara de contraseña (`type="password"`) compatible con variables de entorno (`.env`).
  - **Áreas de Conocimiento:** Especialización en *Programación*, *Matemáticas*, *IA* o *General*.
  - **Nivel de Explicación Dinámico:** Control deslizante para alternar entre niveles *Principiante*, *Intermedio* y *Avanzado*.
  - **Control de Sesión:** Botón para reiniciar y limpiar el historial de la conversación.
- **Enfoque Pedagógico Socrático:** El `system_prompt` instruye al modelo a descomponer los problemas paso a paso, evitar dar respuestas directas sin razonamiento y formular preguntas de validación al finalizar cada explicación.
- **Manejo Robusto de Excepciones:** Detección y mensajes amigables ante fallos de autenticación (`AuthenticationError`), cuota de API (`RateLimitError`), pérdida de conexión o fallos generales.

---

## 🛠 Requisitos Previos

- **Python 3.8 o superior** instalado en el sistema.
- Una **API Key de OpenAI** con acceso a modelos GPT (puedes obtenerla en [OpenAI Platform](https://platform.openai.com/)).

---

## 📦 Instalación y Configuración Paso a Paso

### 1. Navegar al directorio del proyecto
Abre tu terminal y ubícate en la carpeta `tutor_virtual`:

```bash
cd tutor_virtual
```

### 2. Crear y activar un entorno virtual

**En Windows (PowerShell / CMD):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**En macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias
Instala los paquetes necesarios definidos en `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. (Opcional) Configurar variable de entorno
Puedes crear un archivo `.env` dentro de la carpeta `tutor_virtual/` para no tener que ingresar tu API Key manualmente en cada sesión:

```env
OPENAI_API_KEY=tu-api-key-aqui
```

*(También puedes ingresarla directamente desde la barra lateral de la aplicación).*

---

## ▶️ Ejecución de la Aplicación

Con el entorno virtual activado, inicia el servidor de desarrollo de Streamlit:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador web predeterminado en `http://localhost:8501`.

---

## 📚 Estructura de Archivos

```
tutor_virtual/
├── app.py              # Código fuente principal de la aplicación Streamlit
├── requirements.txt    # Lista de dependencias del proyecto
└── README.md           # Documentación y guía de uso del Proyecto 2
```

---

## 💡 Tecnologías Utilizadas

- **[Python](https://www.python.org/)**
- **[Streamlit](https://streamlit.io/)** (Framework frontend interactivo)
- **[OpenAI API](https://platform.openai.com/)** (Modelo `gpt-4o-mini`)
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** (Gestión de variables de entorno)
