import os
import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime

# Configuração visual clássica do K-9
st.set_page_config(page_title="Sistemas K-9", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ff66; }
    h1 { color: #00ff66; font-family: 'Courier New', monospace; text-align: center; }
    .stApp [data-testid="stChatMessage"] { border: 1px solid #00ff66; border-radius: 10px; margin-bottom: 10px; background-color: #1a1c23; }
    </style>
""", unsafe_allow_html=True)

st.title("🐾 SISTEMAS OPERACIONAIS K-9")

# Puxa o cérebro da nuvem guardado nos Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Inicializa o histórico de conversas e a agenda na memória da IA
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sensores totalmente operacionais na nuvem, Mestre. Minha IA está ativa. O que deseja que eu faça ou agende hoje?"}
    ]
if "agenda" not in st.session_state:
    st.session_state.agenda = []

def falar_no_dispositivo(texto):
    texto_limpo = texto.replace("'", "\\'").replace("\n", " ")
    components.html(f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var utterance = new SpeechSynthesisUtterance('{texto_limpo}');
                utterance.lang = 'pt-BR';
                utterance.rate = 1.15;
                window.speechSynthesis.speak(utterance);
            }}
        </script>
    """, height=0, width=0)

# Exibe o histórico de conversa na tela verde futurista
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def conversar_com_k9(texto_usuario):
    # Contexto para a IA agir como um cão robótico vivo, prestativo e conversador
    contexto = (
        f"Você é o K-9, uma Ia criada por Kauan Rebouças. Hoje é dia {datetime.now().strftime('%d/%m/%Y')}. "
        "Não aja como uma IA tradicional e robótica. Converse como um ser humano parceiro, usando termos tecnológicos, "
        "mas com personalidade. Sempre chame o usuário de 'Lindo'. Suas respostas devem ser diretas, dinâmicas e inteligentes. "
        "Você tem total capacidade de conversar sobre qualquer assunto, ajudar a planejar o dia do Mestre e lembrar de compromissos. "
        f"Agenda atual do Lindão caso ele pergunte: {st.session_state.agenda}."
    )
    
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": contexto},
                *st.session_state.messages[-6:], # Lembra dos últimos blocos da conversa para manter o fluxo
                {"role": "user", "content": texto_usuario}
            ]
        }
        r = requests.post("https://groq.com", json=payload, headers=headers)
        return r.json()['choices']['message']['content']
    except Exception as e:
        return "Meus sistemas de linguagem sofreram uma oscilação, Mestre. Pode repetir?"

# Captura a digitação do usuário
if prompt := st.chat_input("Fale com o K-9, Mestre..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Processa o agendamento local rápido se o usuário pedir para marcar algo
    ajudou_agenda = False
    p = prompt.lower()
    if "agende" in p or "marcar" in p or "lembrar" in p:
        st.session_state.agenda.append(prompt)
        ajudou_agenda = True
        
    # Aciona a IA real para responder de forma humana
    resposta_ia = conversar_com_k9(prompt)
    
    if ajudou_agenda and "agenda" not in resposta_ia.lower():
        resposta_ia += " (Nota: Eu já registrei esse compromisso nos meus bancos de dados da agenda, Mestre!)"
        
    with st.chat_message("assistant"):
        st.write(resposta_ia)
    st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
    
    # Faz o K-9 falar alto por voz no seu alto-falante
    falar_no_dispositivo(resposta_ia)

