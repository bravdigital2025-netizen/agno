"""
Demo Argamassa Alphaville — Frontend Streamlit
"""

import sys
import os
import re
import tempfile

import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import AUTH_TOKEN, MODEL_FAST, MODEL_MAIN
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.team.team import Team
from agno.workflow import Step, Workflow
from agno.db.sqlite import SqliteDb

# ---------------------------------------------------------------------------
# Configuracao da pagina
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Argamassa Alphaville | IA ao Vivo",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS customizado
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
  /* Fundo geral */
  .stApp {
    background-color: #0D1117;
    color: #E6EDF3;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background-color: #161B22;
    border-right: 1px solid #30363D;
  }

  /* Botoes de demo */
  .demo-btn {
    width: 100%;
    padding: 12px 16px;
    margin: 4px 0;
    background: #21262D;
    border: 1px solid #30363D;
    border-radius: 8px;
    color: #E6EDF3;
    font-size: 14px;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s;
  }
  .demo-btn:hover {
    background: #2D333B;
    border-color: #F59E0B;
  }
  .demo-btn.active {
    background: #1C2A1C;
    border-color: #F59E0B;
    color: #F59E0B;
  }

  /* Header principal */
  .main-header {
    background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
  }

  /* Card de resultado */
  .result-card {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 24px;
    margin-top: 16px;
  }

  /* Badge de status */
  .status-running {
    background: #1C2A1C;
    border: 1px solid #2EA043;
    border-radius: 20px;
    padding: 4px 12px;
    color: #3FB950;
    font-size: 12px;
    display: inline-block;
  }

  /* Separador de secao */
  .section-label {
    font-size: 11px;
    font-weight: 600;
    color: #7D8590;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 16px 0 8px 0;
  }

  /* Oculta header padrao do streamlit */
  #MainMenu, header, footer { visibility: hidden; }

  /* Input field */
  .stTextArea textarea {
    background: #21262D !important;
    border: 1px solid #30363D !important;
    color: #E6EDF3 !important;
    border-radius: 8px !important;
  }

  /* Botao primario */
  .stButton > button[kind="primary"] {
    background: #F59E0B !important;
    color: #0D1117 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
  }

  /* Streaming output */
  .streaming-box {
    background: #0D1117;
    border: 1px solid #21262D;
    border-radius: 8px;
    padding: 20px;
    font-family: 'Segoe UI', sans-serif;
    line-height: 1.7;
    color: #E6EDF3;
  }

  /* Pipeline step card */
  .step-card {
    border-left: 3px solid #F59E0B;
    padding: 12px 16px;
    margin: 8px 0;
    background: #161B22;
    border-radius: 0 8px 8px 0;
  }

  /* Download button */
  .stDownloadButton > button {
    background: #21262D !important;
    border: 1px solid #30363D !important;
    color: #E6EDF3 !important;
    border-radius: 8px !important;
  }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Banco de dados compartilhado
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "tmp", "frontend.db")
db = SqliteDb(db_file=DB_PATH)


# ---------------------------------------------------------------------------
# Funcao de streaming compativel com Streamlit
# ---------------------------------------------------------------------------
def stream_agent(agent: Agent, prompt: str):
    """Gera chunks de texto do agente para o st.write_stream."""
    for chunk in agent.run(prompt, stream=True):
        if chunk.content and isinstance(chunk.content, str):
            yield chunk.content


# ---------------------------------------------------------------------------
# Criacao dos agentes (cacheados para nao recriar a cada interacao)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_agents():
    model_fast = Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN)
    model_main = Claude(id=MODEL_MAIN, auth_token=AUTH_TOKEN)

    # ---- Comercial ----
    prospect = Agent(
        name="Analista de Prospect",
        model=model_fast,
        markdown=True,
        db=db,
        add_history_to_context=True,
        num_history_runs=3,
        instructions="""\
Voce e especialista em vendas B2B para construcao civil, trabalhando para a Argamassa Alphaville.

Ao receber descricao de um cliente, retorne um perfil comercial completo:

## Perfil do Prospect
- **Segmento e porte**
- **Consumo estimado:** X sacos/mes
- **Produto indicado:** (linha Alphaville mais adequada)

## Oportunidade
- **Dor principal:** (problema que eles enfrentam)
- **Gancho de abertura:** (frase pronta para o representante usar)
- **Canal de contato:** (visita / WhatsApp / ligacao)
- **Urgencia:** Alta / Media / Baixa — com justificativa

## Plano de Acao
1. Acao imediata
2. Follow-up
3. Material para enviar

Seja objetivo e pratico. O representante sai com um plano de acao.
""",
    )

    pipeline_pesquisador = Agent(
        name="Pesquisador",
        model=model_fast,
        db=db,
        add_history_to_context=True,
        num_history_runs=3,
        instructions="Organize o contexto do cliente: tipo de obra, porte, decisor, situacao atual, ciclo de compra. Seja objetivo, sem recomendacoes ainda.",
    )
    pipeline_analista = Agent(
        name="Analista",
        model=model_fast,
        db=db,
        add_history_to_context=True,
        num_history_runs=3,
        instructions="Com base no contexto do pesquisador, identifique: produto indicado, volume estimado, dor principal, estrategia de abordagem, objecao mais provavel e como rebater.",
    )
    pipeline_redator = Agent(
        name="Redator",
        model=model_main,
        db=db,
        markdown=True,
        add_history_to_context=True,
        num_history_runs=3,
        instructions="Com base na pesquisa e analise, escreva uma proposta comercial personalizada pronta para enviar. Tom consultivo, linguagem direta, maximo 300 palavras. Inclua assunto do email, corpo e assinatura.",
    )

    agente_agressivo = Agent(
        name="Estrategista Agressivo",
        role="Defende fechamento rapido e alto volume",
        model=model_fast,
        db=db,
        instructions="Defenda abordagem agressiva: desconto de volume, senso de urgencia, fechar logo. Max 120 palavras, seja direto e persuasivo.",
    )
    agente_consultivo = Agent(
        name="Estrategista Consultivo",
        role="Defende construcao de relacao e fidelizacao",
        model=model_fast,
        db=db,
        instructions="Defenda abordagem consultiva: visita tecnica, amostra gratuita, construcao de confianca. Max 120 palavras, seja direto e persuasivo.",
    )
    time_estrategico = Team(
        name="Time Estratégico",
        model=model_main,
        members=[agente_agressivo, agente_consultivo],
        db=db,
        show_members_responses=True,
        markdown=True,
        instructions="""\
Voce lidera o Time Estrategico da Argamassa Alphaville.
Consulte os dois estrategistas e depois decida:

## Estrategia Decidida: [nome]
**Por que:** (2 linhas)
**O que aproveitar do outro lado:** (1 elemento)

## Plano de Acao
1. ...
2. ...
3. ...

## Mensagem Inicial (pronta para WhatsApp)
> [texto da mensagem]
""",
    )

    # ---- Marketing ----
    instagram = Agent(
        name="Criador de Post Instagram",
        model=model_main,
        markdown=True,
        instructions="""\
Voce e especialista em marketing digital para construcao civil.
Crie posts profissionais para o Instagram da Argamassa Alphaville.

Para cada post, entregue:

## Post Pronto

**Legenda:**
[texto completo da legenda, com emojis estrategicos, max 150 palavras]

**Hashtags:**
[30 hashtags relevantes separadas por espaco]

**Primeiro comentario (CTA):**
[chamada para acao no primeiro comentario]

---

## Arte Sugerida
**Conceito visual:** [descricao detalhada da imagem/arte para o designer]
**Texto na arte:** [o que deve aparecer escrito na imagem]
**Cores predominantes:** [paleta sugerida]
**Formato:** [feed quadrado / reels / stories]

---

## Estrategia de Publicacao
- **Melhor horario:** [horario e justificativa]
- **Frequencia ideal:** [quantas vezes por semana]
- **Objetivo do post:** [alcance / engajamento / conversao]
""",
    )

    minisite = Agent(
        name="Criador de Mini-Site",
        model=model_main,
        instructions="""\
Voce e um desenvolvedor web especialista em landing pages para construcao civil.

Crie uma landing page HTML completa e bonita para a Argamassa Alphaville.

OBRIGATORIO:
- HTML completo e valido (<!DOCTYPE html> ... </html>)
- CSS embutido no <style> (sem arquivos externos)
- Design moderno, responsivo, profissional
- Cores: laranja #F59E0B e azul escuro #1E3A5F como primarias
- Secoes: Hero, Produtos, Diferenciais, Depoimento, CTA, Rodape
- Botao WhatsApp flutuante verde
- Fonte: Google Fonts (Inter ou Poppins)
- Sem JavaScript complexo — apenas CSS animations

Retorne APENAS o codigo HTML completo, sem texto antes ou depois.
""",
    )

    conteudo = Agent(
        name="Planejador de Conteudo",
        model=model_main,
        markdown=True,
        instructions="""\
Voce e estrategista de conteudo digital para construcao civil.
Crie calendarios de conteudo praticos e executaveis para a Argamassa Alphaville.

O calendario deve ter:
- Tema da semana
- 1 post por dia util (segunda a sexta)
- Para cada post: tipo (feed/reels/stories), assunto, gancho de abertura
- Mix de conteudo: educativo, produto, bastidor, depoimento, promocional
- Emojis para tornar visual
- Indicador de esforco de producao (Baixo / Medio / Alto)

Organize em tabela markdown por semana.
""",
    )

    return {
        "prospect": prospect,
        "pipeline": (pipeline_pesquisador, pipeline_analista, pipeline_redator),
        "time": time_estrategico,
        "instagram": instagram,
        "minisite": minisite,
        "conteudo": conteudo,
    }


agents = get_agents()

# ---------------------------------------------------------------------------
# Estado da sessao
# ---------------------------------------------------------------------------
if "demo_ativo" not in st.session_state:
    st.session_state.demo_ativo = None
if "resultado_html" not in st.session_state:
    st.session_state.resultado_html = None
if "ultimo_resultado" not in st.session_state:
    st.session_state.ultimo_resultado = ""

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 20px 0 8px 0;">
          <div style="font-size:22px; font-weight:800; color:#F59E0B; letter-spacing:-0.5px;">
            🏗️ Alphaville
          </div>
          <div style="font-size:12px; color:#7D8590; margin-top:2px;">
            Demonstração de IA ao Vivo
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ---- Bloco Comercial ----
    st.markdown(
        '<div class="section-label">⚡ Comercial</div>', unsafe_allow_html=True
    )

    demos_comercial = {
        "prospect": ("🎯", "Perfil de Prospect", "Analisa qualquer construtora em 30 segundos"),
        "pipeline": ("🔄", "Pipeline Completo", "3 agentes: Pesquisa → Análise → Proposta"),
        "time": ("👥", "Time Estratégico", "Agentes debatem e decidem a abordagem"),
    }

    for key, (icon, titulo, desc) in demos_comercial.items():
        ativo = st.session_state.demo_ativo == key
        if st.button(
            f"{icon} **{titulo}**\n\n_{desc}_",
            key=f"btn_{key}",
            use_container_width=True,
            type="primary" if ativo else "secondary",
        ):
            st.session_state.demo_ativo = key
            st.session_state.resultado_html = None
            st.rerun()

    # ---- Bloco Marketing ----
    st.markdown(
        '<div class="section-label">📱 Marketing Digital</div>',
        unsafe_allow_html=True,
    )

    demos_marketing = {
        "instagram": ("📸", "Post para Instagram", "Legenda, hashtags e direção de arte"),
        "minisite": ("🌐", "Criar Mini-Site", "Landing page HTML pronta para publicar"),
        "conteudo": ("📅", "Plano de Conteúdo", "Calendário editorial de 30 dias"),
    }

    for key, (icon, titulo, desc) in demos_marketing.items():
        ativo = st.session_state.demo_ativo == key
        if st.button(
            f"{icon} **{titulo}**\n\n_{desc}_",
            key=f"btn_{key}",
            use_container_width=True,
            type="primary" if ativo else "secondary",
        ):
            st.session_state.demo_ativo = key
            st.session_state.resultado_html = None
            st.rerun()

    st.divider()
    st.markdown(
        '<div style="font-size:11px; color:#7D8590; text-align:center;">Powered by Claude AI + Agno</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Conteudo principal
# ---------------------------------------------------------------------------

# Header
demo_info = {
    "prospect": ("🎯", "Perfil de Prospect", "Digite o nome ou descrição de uma construtora. A IA entrega o perfil comercial completo."),
    "pipeline": ("🔄", "Pipeline Comercial", "3 agentes trabalham em sequência: pesquisa o cliente, analisa a oportunidade, escreve a proposta pronta."),
    "time": ("👥", "Time Estratégico", "Dois agentes debatem a melhor abordagem. Um líder ouve os dois e decide."),
    "instagram": ("📸", "Post para Instagram", "Descreva um tema ou produto. A IA cria a legenda completa, hashtags e direção de arte."),
    "minisite": ("🌐", "Criar Mini-Site", "Descreva o que você quer. A IA gera uma landing page HTML completa, pronta para publicar."),
    "conteudo": ("📅", "Plano de Conteúdo 30 Dias", "Informe o foco do mês. A IA cria o calendário editorial completo, post a post."),
}

if st.session_state.demo_ativo:
    icon, titulo, desc = demo_info[st.session_state.demo_ativo]
    st.markdown(
        f"""
        <div class="main-header">
          <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:32px;">{icon}</span>
            <div>
              <div style="font-size:22px; font-weight:700; color:#F59E0B;">{titulo}</div>
              <div style="font-size:14px; color:#7D8590; margin-top:4px;">{desc}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="main-header">
          <div style="font-size:28px; font-weight:800; color:#F59E0B; margin-bottom:8px;">
            🏗️ Argamassa Alphaville — IA ao Vivo
          </div>
          <div style="font-size:16px; color:#7D8590; max-width:600px;">
            Escolha uma demonstração no menu ao lado e veja a Inteligência Artificial
            executando tarefas reais em tempo real.
          </div>
          <div style="margin-top:20px; display:flex; gap:16px; flex-wrap:wrap;">
            <div style="background:#1C2A1C; border:1px solid #2EA043; border-radius:8px; padding:12px 20px;">
              <div style="color:#3FB950; font-weight:700;">⚡ Comercial</div>
              <div style="color:#7D8590; font-size:13px;">Prospect · Pipeline · Time</div>
            </div>
            <div style="background:#1A1F2E; border:1px solid #1F6FEB; border-radius:8px; padding:12px 20px;">
              <div style="color:#58A6FF; font-weight:700;">📱 Marketing</div>
              <div style="color:#7D8590; font-size:13px;">Instagram · Mini-Site · Calendário</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ---------------------------------------------------------------------------
# Area de entrada
# ---------------------------------------------------------------------------
PLACEHOLDERS = {
    "prospect": "Construtora Horizonte — condomínios de médio padrão em Alphaville e Cotia. Tiveram problemas de fissuramento e estão revisando fornecedores.",
    "pipeline": "Construtora Horizonte — obras em Cotia e Alphaville, médio padrão. Problemas com fissuramento. Decisor: Eng. Marcos Ferreira.",
    "time": "Qual a melhor estratégia para abordar a Construtora Horizonte? O decisor é o Eng. Marcos, tecnicamente exigente.",
    "instagram": "Post sobre como a Argamassa Alphaville resolve o problema de fissuramento em condomínios de médio padrão.",
    "minisite": "Landing page da Argamassa Alphaville focada em construtoras de médio padrão em São Paulo. Destaque para anti-fissuramento.",
    "conteudo": "Foco do mês: posicionamento técnico da Argamassa Alphaville para engenheiros e mestres de obras.",
}

col_input, col_btn = st.columns([5, 1])
with col_input:
    prompt = st.text_area(
        "✏️ Descreva o que você quer",
        value=PLACEHOLDERS[st.session_state.demo_ativo],
        height=90,
        label_visibility="collapsed",
        placeholder=PLACEHOLDERS[st.session_state.demo_ativo],
    )

with col_btn:
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    executar = st.button("▶ Executar", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Execucao
# ---------------------------------------------------------------------------
if executar and prompt:

    # ---- Prospect ----
    if st.session_state.demo_ativo == "prospect":
        st.markdown("---")
        status = st.empty()
        status.markdown('<span class="status-running">● Analisando prospect...</span>', unsafe_allow_html=True)
        resultado = st.write_stream(stream_agent(agents["prospect"], prompt))
        status.empty()
        st.session_state.ultimo_resultado = resultado

    # ---- Pipeline ----
    elif st.session_state.demo_ativo == "pipeline":
        st.markdown("---")
        pesquisador, analista, redator = agents["pipeline"]
        resultado_final = ""

        etapas = [
            (pesquisador, "🔍 Etapa 1 de 3 — Pesquisando o cliente...", "Pesquisa Concluída"),
            (analista, "📊 Etapa 2 de 3 — Analisando oportunidade...", "Análise Concluída"),
            (redator, "✍️ Etapa 3 de 3 — Escrevendo a proposta...", "Proposta Pronta"),
        ]

        contexto = prompt
        for agent_step, label_andamento, label_ok in etapas:
            st.markdown(
                f'<div class="step-card"><strong>{label_andamento}</strong></div>',
                unsafe_allow_html=True,
            )
            resultado_etapa = st.write_stream(stream_agent(agent_step, contexto))
            st.markdown(
                f'<div style="font-size:12px; color:#3FB950; margin:4px 0 16px 0;">✓ {label_ok}</div>',
                unsafe_allow_html=True,
            )
            contexto = resultado_etapa  # passa output da etapa anterior como input
            resultado_final = resultado_etapa

        st.session_state.ultimo_resultado = resultado_final

    # ---- Time Estrategico ----
    elif st.session_state.demo_ativo == "time":
        st.markdown("---")
        status = st.empty()
        status.markdown('<span class="status-running">● Time em reunião...</span>', unsafe_allow_html=True)
        resultado = st.write_stream(stream_agent(agents["time"], prompt))
        status.empty()
        st.session_state.ultimo_resultado = resultado

    # ---- Instagram ----
    elif st.session_state.demo_ativo == "instagram":
        st.markdown("---")
        status = st.empty()
        status.markdown('<span class="status-running">● Criando post...</span>', unsafe_allow_html=True)
        resultado = st.write_stream(stream_agent(agents["instagram"], prompt))
        status.empty()
        st.session_state.ultimo_resultado = resultado

    # ---- Mini-Site ----
    elif st.session_state.demo_ativo == "minisite":
        st.markdown("---")
        status = st.empty()
        status.markdown('<span class="status-running">● Gerando site...</span>', unsafe_allow_html=True)

        html_chunks = []
        output_placeholder = st.empty()

        for chunk in agents["minisite"].run(prompt, stream=True):
            if chunk.content and isinstance(chunk.content, str):
                html_chunks.append(chunk.content)
                output_placeholder.code(
                    "".join(html_chunks)[-500:] + "...",
                    language="html",
                )

        html_completo = "".join(html_chunks)

        # Remove blocos de markdown caso o modelo inclua
        html_limpo = re.sub(r"^```html?\n?", "", html_completo.strip())
        html_limpo = re.sub(r"\n?```$", "", html_limpo.strip())

        status.empty()
        output_placeholder.empty()

        st.markdown("### 🌐 Preview do Site Gerado")
        st.components.v1.html(html_limpo, height=600, scrolling=True)

        st.download_button(
            label="⬇️ Baixar HTML",
            data=html_limpo,
            file_name="alphaville_landing.html",
            mime="text/html",
        )
        st.session_state.resultado_html = html_limpo
        st.session_state.ultimo_resultado = html_limpo

    # ---- Plano de Conteudo ----
    elif st.session_state.demo_ativo == "conteudo":
        st.markdown("---")
        status = st.empty()
        status.markdown('<span class="status-running">● Planejando conteúdo...</span>', unsafe_allow_html=True)
        resultado = st.write_stream(stream_agent(agents["conteudo"], prompt))
        status.empty()
        st.session_state.ultimo_resultado = resultado

# ---------------------------------------------------------------------------
# Botao de download para resultados de texto
# ---------------------------------------------------------------------------
if (
    st.session_state.ultimo_resultado
    and st.session_state.demo_ativo != "minisite"
    and executar
):
    st.markdown("---")
    st.download_button(
        label="⬇️ Baixar resultado (.txt)",
        data=st.session_state.ultimo_resultado,
        file_name=f"resultado_{st.session_state.demo_ativo}.txt",
        mime="text/plain",
    )
