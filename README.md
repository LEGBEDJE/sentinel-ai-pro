# 🛡️ Sentinel-AI Pro

Sentinel-AI Pro est un **Agent SRE (Site Reliability Engineering)** autonome conçu pour transformer le monitoring brut en diagnostic actionnable. 

Contrairement à un simple chatbot, cet agent utilise le **Tool Calling** pour enquêter activement sur l'infrastructure avant de rendre un rapport.

## 🛠️ Points Forts Techniques
- **Investigation Autonome** : L'agent appelle des fonctions Python (outils) pour vérifier la santé de la DB et du CPU.
- **Raisonnement Agentique** : Utilisation du framework **Pydantic-AI** pour orchestrer le cycle Pensée-Action-Observation.
- **Validation Strict** : Sortie structurée via Pydantic pour garantir des données exploitables par des systèmes tiers.

## 🚀 Stack
- **Modèle** : Llama-3.3-70b via Groq.
- **Logiciel** : Streamlit (Frontend), Pydantic-AI (Orchestration).
- **Architecture** : Asynchrone (Asyncio) pour des performances optimales.

## 📖 Utilisation
1. Entrez votre clé API Groq.
2. Cliquez sur "Lancer l'audit".
3. Observez l'agent appeler les outils dans la section "Trace d'investigation".
