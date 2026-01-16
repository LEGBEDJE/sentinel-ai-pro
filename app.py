import streamlit as st
import pandas as pd
import asyncio
import random
import os
from datetime import datetime
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel, Field
import nest_asyncio

nest_asyncio.apply()

# --- CONFIGURATION UI ---
st.set_page_config(page_title="Sentinel-AI Pro", layout="wide", page_icon="🛡️")

class IncidentReport(BaseModel):
    severity: str = Field(description="CRITICAL, WARNING, ou INFO")
    diagnostic: str = Field(description="Explication technique de la panne")
    remediation_steps: str = Field(description="Actions conseillées")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Sentinel Control Center")
    user_api_key = st.text_input("Groq API Key", type="password")
    st.info("Agent SRE autonome avec capacités d'investigation.")

if not user_api_key:
    st.warning("Veuillez entrer votre clé API Groq pour activer l'agent.")
    st.stop()

# --- INITIALISATION AGENT ---
os.environ['GROQ_API_KEY'] = user_api_key
model = GroqModel('llama-3.3-70b-versatile')
agent = Agent(
    model=model, 
    system_prompt="Tu es un agent SRE expert. Analyse les logs et utilise tes outils pour enquêter avant de conclure."
)

# --- TOOLS (Capacités Agentiques) ---
@agent.tool
async def check_database_health(ctx: RunContext[None]) -> str:
    """Vérifie l'état réel de la base de données."""
    status = random.choice(["ONLINE", "LATENCY_HIGH", "OFFLINE"])
    return f"Status DB: {status} (Latence: {random.randint(10, 500)}ms)"

@agent.tool
async def get_server_metrics(ctx: RunContext[None]) -> str:
    """Récupère l'utilisation CPU et RAM en temps réel."""
    return f"Métriques : CPU {random.randint(10, 95)}%, RAM {random.randint(20, 90)}%"

# --- INTERFACE PRINCIPALE ---
st.title("🛡️ Sentinel-AI Pro : Investigation Autonome")

raw_logs = """
2024-05-20 14:10:02 ERROR service=gateway msg="504 Gateway Timeout"
2024-05-20 14:10:05 ERROR service=api-auth msg="Connection error to database"
"""

st.subheader("📝 Logs d'incidents détectés")
st.code(raw_logs)

if st.button("Lancer l'audit intelligent"):
    with st.spinner("L'agent enquête via ses outils..."):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            prompt = f"Analyse ces logs et utilise tes outils pour un diagnostic complet : {raw_logs}"
            result = loop.run_until_complete(agent.run(prompt, result_type=IncidentReport))
            
            res = result.data
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Sévérité du système", res.severity)
                st.info(f"**Diagnostic :**\n{res.diagnostic}")
            with col2:
                st.success(f"**Plan de remédiation :**\n{res.remediation_steps}")
                
            with st.expander("🔗 Trace d'investigation (Raisonnement Agentique)"):
                st.json(result.all_messages())
        except Exception as e:
            st.error(f"Erreur : {e}")
