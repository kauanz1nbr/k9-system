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

# Configuração Secreta da API Groq na Nuvem para Inteligência Real
# COLE SUA CHAVE GSK_ AQUI DENTRO DAS ASPAS SE QUISER TRAVAR DIRETO, OU DEIXE ANÔNIMO:
GROQ_API_KEY = "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"

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
        {"role": "assistant", "content": "Sensores ativos na nuvem. Pronto para gerenciar seus sistemas, Mestre."}
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
        "Caso contrário, apenas converse normalmente respondendo de forma inteligente."
    )
    
    # Faz requisição para a IA ultra-rápida na nuvem
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
        return r.json()['choices'][0]['message']['content']
    except Exception:
        # Fallback inteligente local por texto caso esteja sem chave
        t = texto_usuario.lower()
        if "geekie" in t: return "[ABRIR_GEEKIE]"
        if "tiktok" in t: return "[ABRIR_TIKTOK]"
        if "instagram" in t: return "[ABRIR_INSTAGRAM]"
        if "spotify" in t: return "[ABRIR_SPOTIFY]"
        if "steam" in t: return "[ABRIR_STEAM]"
        if "youtube" in t: return "[ABRIR_YOUTUBE]"
        return "Sistemas operacionais online, Mestre. Comando de texto recebido."

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
        elif "[ABRIR_SPOTIFY]" in resposta_ia:
            status = "Afirmativo, Mestre. Carregando reprodutor musical do Spotify."
            url_redirecionar = "https://spotify.com"
        elif "[ABRIR_YOUTUBE]" in resposta_ia:
            status = "Afirmativo, Mestre. Conectando aos servidores do YouTube."
            url_redirecionar = "https://youtube.com"
        elif "[ABRIR_STEAM]" in resposta_ia:
            if eh_dispositivo_movel:
                status = "Aviso: A plataforma Steam requer a arquitetura de hardware do computador de mesa, Mestre."
            else:
                status = "Afirmativo, Mestre. Comando Steam enviado. (Abra pelo app local se estiver usando a rede de casa)."
                url_redirecionar = "steam://open/main"

        # Garante que o status limpe os gatilhos de texto ao exibir
        status_exibir = status.replace("[ABRIR_GEEKIE]","").replace("[ABRIR_TIKTOK]","").replace("[ABRIR_INSTAGRAM]","").replace("[ABRIR_SPOTIFY]","").replace("[ABRIR_STEAM]","").replace("[ABRIR_YOUTUBE]","")
        
        if status_exibir.strip() == "":
            status_exibir = status
            
        with st.chat_message("assistant"):
            st.write(status_exibir)
        st.session_state.messages.append({"role": "assistant", "content": status_exibir})
        
        falar_no_dispositivo(status_exibir)
        
        if url_redirecionar:
            forcar_abertura_web(url_redirecionar)
        
    except Exception as e:
        st.error(f"Erro nos sensores: {e}")





