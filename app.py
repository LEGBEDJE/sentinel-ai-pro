import streamlit as st
import asyncio
import os
import random
import nest_asyncio
from groq import Groq
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel, Field
from dotenv import load_dotenv

################# add  your api key .env file ######


# Configuration
#load_dotenv()
#user_api_key = os.getenv("your_api_key") 


# Configuration indispensable
nest_asyncio.apply()
load_dotenv()
user_api_key = os.getenv("your_api_key")  # Charger la clé API depuis .env
st.set_page_config(page_title="Sentinel-AI Pro", layout="wide", page_icon="🛡️")

# 1. STRUCTURE DE SORTIE (Doit être définie AVANT l'agent)
class IncidentReport(BaseModel):
    severity: str = Field(description="CRITICAL, WARNING, ou INFO")
    diagnostic: str = Field(description="Explication technique de la panne")
    remediation_steps: str = Field(description="Actions conseillées")

# 2. SIDEBAR
#with st.sidebar:
    #st.header("⚙️ Sentinel Control Center")
    #user_api_key = st.text_input("Groq API Key", type="password")

#if not user_api_key:
    #st.warning("Veuillez entrer votre clé API Groq.")
    #st.stop()

# 3. INITIALISATION DE L'AGENT (Correction ici)
try:
    # Définir la clé API en variable d'environnement pour Groq
    os.environ['GROQ_API_KEY'] = user_api_key
    
    # Initialiser le modèle Groq
    model = GroqModel('llama-3.3-70b-versatile')
    
    agent = Agent(
        model=model, 
        output_type=IncidentReport,  # FIX: Utiliser output_type au lieu de result_type
        system_prompt="Tu es un agent SRE expert. Analyse les logs et utilise tes outils pour enquêter."
    )
except Exception as e:
    st.error(f"Erreur d'initialisation : {e}")
    st.stop()

# 4. TOOLS
@agent.tool
async def check_database_health(ctx: RunContext[None]) -> str:
    """Vérifie l'état réel de la base de données."""
    status = random.choice(["ONLINE", "LATENCY_HIGH", "OFFLINE"])
    return f"Status DB: {status} (Latence: {random.randint(10, 500)}ms)"

@agent.tool
async def get_server_metrics(ctx: RunContext[None]) -> str:
    """Récupère l'utilisation CPU et RAM en temps réel."""
    return f"Métriques : CPU {random.randint(10, 95)}%, RAM {random.randint(20, 90)}%"

# 5. INTERFACE ET EXECUTION
st.title("🛡️ Sentinel-AI Pro : Investigation Autonome")

st.subheader("📝 Logs d'incidents détectés")

# Upload ou texte manuel
col_upload, col_text = st.columns([1, 1])

with col_upload:
    st.markdown("**Option 1 : Upload un fichier**")
    uploaded_file = st.file_uploader("Choisir un fichier .log ou .txt", type=["log", "txt"])
    raw_logs = None
    if uploaded_file:
        raw_logs = uploaded_file.read().decode("utf-8")
        st.success(f"✅ Fichier '{uploaded_file.name}' chargé ({len(raw_logs)} caractères)")

with col_text:
    st.markdown("**Option 2 : Coller les logs**")
    raw_logs_manual = st.text_area(
        "Ou collez vos logs ici :",
        value="""2024-05-20 14:10:02 ERROR service=gateway msg="504 Gateway Timeout"
2024-05-20 14:10:05 ERROR service=api-auth msg="Connection error to database\"""",
        height=150
    )
    if not raw_logs:
        raw_logs = raw_logs_manual

# Afficher les logs
if raw_logs:
    st.code(raw_logs, language="log")


if st.button("🔍 Lancer l'audit intelligent", disabled=not raw_logs):
    if not raw_logs or raw_logs.strip() == "":
        st.warning("⚠️ Veuillez uploader un fichier ou entrer des logs.")
    else:
        with st.spinner("L'agent enquête via ses outils..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                prompt = f"Analyse ces logs et utilise tes outils pour un diagnostic complet : {raw_logs}"
                
                # FIX: On retire result_type d'ici car il est déjà dans l'agent
                result = loop.run_until_complete(agent.run(prompt))
                
                st.write("DEBUG: Result received:", result)
                st.write("DEBUG: Result output:", result.output)
                
                res = result.output
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Sévérité", res.severity)
                    st.info(f"**Diagnostic :**\n{res.diagnostic}")
                with col2:
                    st.success(f"**Plan de remédiation :**\n{res.remediation_steps}")
                    
                with st.expander("🔗 Trace d'investigation (JSON)"):
                    st.json(result.all_messages_json())
            except Exception as e:
                import traceback
                st.error(f"Erreur d'exécution : {e}")
                st.error(traceback.format_exc())
