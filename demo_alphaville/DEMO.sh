#!/usr/bin/env bash
# ============================================================
#  DEMO ARGAMASSA ALPHAVILLE — Script de Apresentacao
# ============================================================
#  Execute cada ato separado conforme o roteiro.
#  Voce esta na pasta: /home/user/agno
# ============================================================

PYTHON=".venv/bin/python"

echo ""
echo "============================================================"
echo "  DEMO ARGAMASSA ALPHAVILLE — PRONTA PARA EXECUTAR"
echo "============================================================"
echo ""
echo "  COMANDOS DISPONIVEIS:"
echo ""
echo "  ATO 1 — Agente Simples (30 seg)"
echo "  $PYTHON demo_alphaville/ato1_agente_simples.py"
echo ""
echo "  ATO 2 — Pipeline de 3 Agentes (60-90 seg)"
echo "  $PYTHON demo_alphaville/ato2_workflow.py"
echo ""
echo "  ATO 3 — Time de Agentes Debatendo (30 seg)"
echo "  $PYTHON demo_alphaville/ato3_time_agentes.py"
echo ""
echo "  EXTRAS:"
echo "  $PYTHON demo_alphaville/extras.py cadencia"
echo "  $PYTHON demo_alphaville/extras.py copy"
echo "  $PYTHON demo_alphaville/extras.py objecao"
echo "  $PYTHON demo_alphaville/extras.py memoria"
echo ""
echo "  AGENTÓS (interface web — abrir os.agno.com depois)"
echo "  $PYTHON demo_alphaville/run_agentOS.py"
echo ""
echo "============================================================"
echo "  VARIACOES DE PROMPT PARA ATO 1 (copiar e colar):"
echo "============================================================"
echo ""
echo '  $PYTHON demo_alphaville/ato1_agente_simples.py "Empreiteira de obras publicas, porte medio, foco em alvenaria estrutural no ABC Paulista"'
echo ""
echo '  $PYTHON demo_alphaville/ato1_agente_simples.py "Incorporadora de alto padrao em Barueri, constroi residenciais com acabamento premium"'
echo ""
echo '  $PYTHON demo_alphaville/ato2_workflow.py "Construtora Nova Era, obras comerciais em Jundiai, quer trocar argamassa por produto com mais suporte tecnico"'
echo ""
