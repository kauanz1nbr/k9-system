import os
import streamlit as st
import streamlit.components.v1 as components
import requests

# Configuração da página web do K-9
st.set_page_config(page_title="Sistemas K-9", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ff66; }
    h1 { color: #00ff66; font-family: 'Courier New', monospace; text-align: center; }
    .stChatMessage { border: 1px solid #00ff66; border-radius: 10px; margin-bottom: 10px; }
    .stRadio>label { color: #00ff66 !important; font-family: 'Courier New', monospace; }
    div[data-testid="stRadio"] { border: 1px solid #00ff66; padding: 10px; border-radius: 10px; background-color: #1a1c23; }
    </style>
""", unsafe_allow_html=True)

st.title("🐾 SISTEMAS K-9 OPERACIONAIS")

# Puxa a chave oculta da IA do baú seguro do Streamlit
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ABRE A PONTE LENDO DIRETO DO BAÚ DE SEGREDOS DA NUVEM
URL_PONTE_PC = st.secrets["URL_NGROK"] + "/comando"

# Seletor de dispositivo
aparelho_atual = st.radio(
    "SELECIONE O SEU DISPOSITIVO ATUAL:",
    ["💻 Computador Principal", "📱 Celular / Chromebook"],
    index=0
)

def falar_no_dispositivo(texto):
    texto_limpo = texto.replace("'", "\\'").replace("\n", " ")
    components.html(f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var utterance = new SpeechSynthesisUtterance('{texto_limpo}');
                utterance.lang = 'pt-BR';
                utterance.rate = 1.1;
                window.speechSynthesis.speak(utterance);
            }}
        </script>
    """, height=0, width=0)

def forcar_abertura_web(url):
    components.html(f"""
        <script>
            window.parent.location.href = "{url}";
        </script>
    """, height=0, width=0)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sensores ativos na nuvem. Ponte virtual K-9 inicializada. Pronto para suas ordens, Mestre."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def interpretar_comando_nuvem(texto_usuario):
    contexto = (
        "Você é o K-9, o cão robótico hiperinteligente. Responda de forma extremamente lógica, "
        "tecnológica e prestativa, sempre chamando o usuário de 'Mestre'. Suas respostas devem ser curtas e diretas. "
        "Se o usuário pedir para abrir a Geekie One, responda EXATAMENTE com: [ABRIR_GEEKIE]. "
        "Se o usuário pedir para abrir o TikTok, responda EXATAMENTE com: [ABRIR_TIKTOK]. "
        "Se o usuário pedir para abrir o Instagram, responda EXATAMENTE com: [ABRIR_INSTAGRAM]. "
        "Se o usuário pedir para abrir o Spotify, responda EXATAMENTE com: [ABRIR_SPOTIFY]. "
        "Se o usuário pedir para abrir a Steam, responda EXATAMENTE com: [ABRIR_STEAM]. "
        "Se o usuário pedir para abrir o YouTube, responda EXATAMENTE com: [ABRIR_YOUTUBE]. "
        "Se o usuário pedir para desligar o computador ou fechar o PC, responda EXATAMENTE com: [DESLIGAR_PC]. "
        "Caso contrário, apenas converse normalmente respondendo de forma inteligente."
    )
    
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": contexto},
                {"role": "user", "content": texto_usuario}
            ]
        }
        r = requests.post("https://groq.com", json=payload, headers=headers)
        return r.json()['choices']['message']['content']
    except Exception:
        t = texto_usuario.lower()
        if "geekie" in t: return "[ABRIR_GEEKIE]"
        if "tiktok" in t: return "[ABRIR_TIKTOK]"
        if "instagram" in t: return "[ABRIR_INSTAGRAM]"
        if "spotify" in t: return "[ABRIR_SPOTIFY]"
        if "steam" in t: return "[ABRIR_STEAM]"
        if "youtube" in t: return "[ABRIR_YOUTUBE]"
        if "desligar" in t or "fechar o pc" in t: return "[DESLIGAR_PC]"
        return "Sistemas operacionais online, Mestre. Aguardando conexão do túnel de rede."

if prompt := st.chat_input("Digite um comando, Mestre..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        resposta_ia = interpretar_comando_nuvem(prompt)
        status = resposta_ia
        eh_dispositivo_movel = aparelho_atual == "📱 Celular / Chromebook"
        url_redirecionar = None
        
        if "[ABRIR_GEEKIE]" in resposta_ia:
            status = "Afirmativo, Mestre. Conectando à plataforma Geekie One."
            url_redirecionar = "https://geekie.com.br"
            
        elif "[ABRIR_TIKTOK]" in resposta_ia:
            status = "Afirmativo, Mestre. Abrindo o fluxo de mídia do TikTok."
            url_redirecionar = "https://tiktok.com"
            
        elif "[ABRIR_INSTAGRAM]" in resposta_ia:
            status = "Afirmativo, Mestre. Inicializando interface do Instagram."
            url_redirecionar = "https://instagram.com"
            
        elif "[ABRIR_YOUTUBE]" in resposta_ia:
            status = "Afirmativo, Mestre. Conectando aos servidores do YouTube."
            url_redirecionar = "https://youtube.com"
            
        elif "[ABRIR_SPOTIFY]" in resposta_ia:
            if eh_dispositivo_movel:
                status = "Afirmativo, Mestre. Redirecionando dispositivo para o Spotify Web."
                url_redirecionar = "https://spotify.com"
            else:
                status = "Afirmativo, Mestre. Enviando sinal de ativação do Spotify para o receptor local."
                requests.post(URL_PONTE_PC, json={"acao": "SPOTIFY"}, verify=False)
                
        elif "[ABRIR_STEAM]" in resposta_ia:
            status = "Afirmativo, Mestre. Inicializando aplicativo Steam no computador principal via ponte."
            requests.post(URL_PONTE_PC, json={"acao": "STEAM"}, verify=False)
                
        elif "[DESLIGAR_PC]" in resposta_ia:
            status = "🚨 PROTOCOLO CRÍTICO: Iniciando encerramento do computador principal em 30 segundos, Mestre."
            requests.post(URL_PONTE_PC, json={"acao": "DESLIGAR_PC"}, verify=False)

        status_exibir = status.replace("[ABRIR_GEEKIE]","").replace("[ABRIR_TIKTOK]","").replace("[ABRIR_INSTAGRAM]","").replace("[ABRIR_SPOTIFY]","").replace("[ABRIR_STEAM]","").replace("[ABRIR_YOUTUBE]","").replace("[DESLIGAR_PC]","")
        if status_exibir.strip() == "":
            status_exibir = status
            
        with st.chat_message("assistant"):
            st.write(status_exibir)
        st.session_state.messages.append({"role": "assistant", "content": status_exibir})
        
        falar_no_dispositivo(status_exibir)
        
        if url_redirecionar:
            forcar_abertura_web(url_redirecionar)
        
    except Exception as e:
        st.error(f"Erro nos sensores de rede: {e}")

