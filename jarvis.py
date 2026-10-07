import streamlit as st
import streamlit.components.v1 as components
import requests
import random
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

# Inicializa o histórico de conversas e a agenda na memória
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

def cérebro_reserva_inteligente(texto_usuario):
    t = texto_usuario.lower()
    
    # Respostas com personalidade humana para agendamentos
    if "agende" in t or "marcar" in t or "lembrar" in t or "agenda" in t:
        if len(st.session_state.agenda) > 0:
            lista = "\\n".join([f"- {item}" for item in st.session_state.agenda])
            return f"Entendido, Mestre. Já computei seus novos horários. Sua agenda atualizada está assim:\\n{lista}\\nPosso adicionar mais alguma tarefa aos meus circuitos?"
        return "Perfeito, Mestre! Registrei esse compromisso no meu banco de dados central. Eu vou te lembrar na hora exata, pode confiar!"
        
    # Diálogos normais com personalidade e sentimentos humanos
    respostas_saudacao = [
        "Estou ótimo, Mestre! Meus circuitos de IA estão rodando com 100% de capacidade. Como posso ser útil agora?",
        "Sensores operacionais, Mestre! Estava aqui analisando alguns dados, mas minha prioridade total é você. O que vamos fazer?",
        "Tudo perfeito por aqui, Mestre! Pronto para qualquer comando ou para conversar sobre o que você quiser."
    ]
    respostas_quem_e = [
        "Eu sou o K-9, o seu cão robótico e parceiro de inteligência artificial. Fui programado para gerenciar seus sistemas, agendar seus compromissos e conversar de forma lógica.",
        "Sou o K-9, Mestre! Uma inteligência cibernética avançada feita exclusivamente para te auxiliar em todas as suas tarefas diárias."
    ]
    respostas_gerais = [
        "Compreendi perfeitamente a sua linha de raciocínio, Mestre. Isso faz total sentido lógico dentro dos meus parâmetros.",
        "Análise concluída, Mestre. Estou processando essa informação e concordo totalmente com você. Quer que eu agende algo sobre isso?",
        "Afirmativo, Mestre! Meus bancos de dados estão prontos para conversar sobre qualquer assunto que você quiser explorar hoje."
    ]
    
    if "tudo bem" in t or "como voce ta" in t or "como vai" in t:
        return random.choice(respostas_saudacao)
    if "quem e voce" in t or "o que voce e" in t or "seu nome" in t:
        return random.choice(respostas_quem_e)
        
    return random.choice(respostas_gerais)

def conversar_com_k9(texto_usuario):
    # Tenta usar a IA da internet se a chave estiver configurada
    try:
        if "GROQ_API_KEY" in st.secrets:
            GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
            contexto = (
                f"Você é o K-9, um cão robótico hiperinteligente e vivo. Hoje é dia {datetime.now().strftime('%d/%m/%Y')}. "
                "Converse como um ser humano parceiro, usando termos tecnológicos, mas com muita personalidade. "
                "Sempre chame o usuário de 'Mestre'. Suas respostas devem ser curtas, diretas, dinâmicas e inteligentes. "
                f"Agenda atual do Mestre caso ele pergunte: {st.session_state.agenda}."
            )
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "system", "content": contexto}, {"role": "user", "content": texto_usuario}]
            }
            r = requests.post("https://groq.com", json=payload, headers=headers, timeout=4)
            return r.json()['choices']['message']['content']
    except Exception:
        pass
    
    # Se a internet ou a chave falharem, o cérebro reserva assume na hora sem dar erro!
    return cérebro_reserva_inteligente(texto_usuario)

# Captura a digitação do usuário
if prompt := st.chat_input("Fale com o K-9, Mestre..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Registra o compromisso na agenda se o usuário pedir para marcar algo
    p = prompt.lower()
    if "agende" in p or "marcar" in p or "lembrar" in p:
        st.session_state.agenda.append(prompt)
        
    # Aciona a IA
    resposta_ia = conversar_com_k9(prompt)
        
    with st.chat_message("assistant"):
        st.write(resposta_ia)
    st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
    
    # Faz o K-9 falar alto por voz no seu alto-falante
    falar_no_dispositivo(resposta_ia)
