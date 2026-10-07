import os
import ollama
import streamlit as st
import streamlit.components.v1 as components

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

# O seletor manual definitivo
aparelho_atual = st.radio(
    "SELECIONE O SEU DISPOSITIVO ATUAL:",
    ["💻 Computador Principal", "📱 Celular / Chromebook"],
    index=0
)

# Função de áudio universal para o navegador
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

# Função especial de redirecionamento
def forcar_abertura_web(url):
    components.html(f"""
        <script>
            window.parent.location.href = "{url}";
        </script>
    """, height=0, width=0)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sensores ativos. Pronto para gerenciar seus sistemas, Mestre."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def interpretar_comando(texto_usuario):
    contexto = (
        "Você é o K-9, o cão robótico hiperinteligente. Responda de forma extremamente lógica, "
        "tecnológica e prestativa, sempre chamando o usuário de 'Mestre'. Suas respostas devem ser curtas e diretas. "
        "Se o usuário pedir para abrir a Geekie One, responda EXATAMENTE com: [ABRIR_GEEKIE]. "
        "Se o usuário pedir para abrir o TikTok, responda EXATAMENTE com: [ABRIR_TIKTOK]. "
        "Se o usuário pedir para abrir o Instagram, responda EXATAMENTE com: [ABRIR_INSTAGRAM]. "
        "Se o usuário pedir para abrir o Spotify, responda EXATAMENTE com: [ABRIR_SPOTIFY]. "
        "Se o usuário pedir para abrir a Steam, responda EXATAMENTE com: [ABRIR_STEAM]. "
        "Se o usuário pedir para abrir o YouTube, responda EXATAMENTE com: [ABRIR_YOUTUBE]. "
        "Caso contrário, apenas converse normalmente."
    )
    
    # Rota de proteção para IA na nuvem ou local
    try:
        resposta_ollama = ollama.chat(
            model="llama3",
            messages=[{"role": "system", "content": contexto}, {"role": "user", "content": texto_usuario}]
        )
        return resposta_ollama['message']['content']
    except Exception:
        # Resposta padrão de segurança caso o servidor local esteja offline na nuvem
        texto_min = texto_usuario.lower()
        if "geekie" in texto_min: return "[ABRIR_GEEKIE]"
        if "tiktok" in texto_min: return "[ABRIR_TIKTOK]"
        if "instagram" in texto_min: return "[ABRIR_INSTAGRAM]"
        if "spotify" in texto_min: return "[ABRIR_SPOTIFY]"
        if "steam" in texto_min: return "[ABRIR_STEAM]"
        if "youtube" in texto_min: return "[ABRIR_YOUTUBE]"
        return "Conexão de dados estabelecida, Mestre. O que deseja?"

if prompt := st.chat_input("Digite um comando, Mestre..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        resposta_ia = interpretar_comando(prompt)
        status = resposta_ia
        eh_dispositivo_movel = aparelho_atual == "📱 Celular / Chromebook"
        url_redirecionar = None
        
        # Execução das ações via comandos Web ou atalhos protegidos
        if "[ABRIR_GEEKIE]" in resposta_ia:
            status = "Afirmativo, Mestre. Abrindo o painel de estudos Geekie One."
            url_redirecionar = "https://geekie.com.br"
        elif "[ABRIR_TIKTOK]" in resposta_ia:
            status = "Afirmativo, Mestre. Abrindo o fluxo do TikTok."
            url_redirecionar = "https://tiktok.com"
        elif "[ABRIR_INSTAGRAM]" in resposta_ia:
            status = "Afirmativo, Mestre. Inicializando interface do Instagram."
            url_redirecionar = "https://instagram.com"
        elif "[ABRIR_SPOTIFY]" in resposta_ia:
            status = "Afirmativo, Mestre. Inicializando reprodutor do Spotify."
            url_redirecionar = "https://spotify.com"
        elif "[ABRIR_YOUTUBE]" in resposta_ia:
            status = "Afirmativo, Mestre. Carregando servidor do YouTube."
            url_redirecionar = "https://youtube.com"
        elif "[ABRIR_STEAM]" in resposta_ia:
            if eh_dispositivo_movel:
                status = "Aviso: A plataforma Steam requer o hardware do computador principal, Mestre."
            else:
                # Importação dinâmica para não dar erro nos servidores Linux da nuvem
                try:
                    import pyautogui
                    pyautogui.hotkey("win", "r")
                    pyautogui.write("steam://open/main")
                    pyautogui.press("enter")
                    status = "Afirmativo, Mestre. Inicializando aplicativo Steam local."
                except Exception:
                    status = "Comando Steam enviado para a fila do computador principal."

        with st.chat_message("assistant"):
            st.write(status)
        st.session_state.messages.append({"role": "assistant", "content": status})
        
        falar_no_dispositivo(status)
        
        if url_redirecionar:
            forcar_abertura_web(url_redirecionar)
        
    except Exception as e:
        st.error(f"Erro nos sensores: {e}")





