# -*- coding: utf-8 -*-
"""
MÓDULO DE CONFIGURAÇÃO
================================================================================
Constantes e configurações globais do programa.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import os

# ============================================================================
# VERSÃO DO PROGRAMA
# ============================================================================
# ATENÇÃO: atualize a cada nova release (veja docs/DESENVOLVIMENTO.md).
# O workflow de release falha se a tag não bater com este valor.
VERSAO_ATUAL = "2.7"

# Intervalo da verificação automática de atualizações (programa aberto)
INTERVALO_VERIFICAR_ATUALIZACAO_MS = 4 * 60 * 60 * 1000  # 4 horas

# ============================================================================
# CONFIGURAÇÕES DO GITHUB PARA AUTO-UPDATE
# ============================================================================
# Nome do repositório no formato "usuario/repositorio"
GITHUB_REPO = "Joshpcbrrj/gerador-email-hepta"

# URL da API do GitHub para buscar a última release
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# ============================================================================
# REGRAS DO FORMULÁRIO
# ============================================================================
MAX_TELEFONES = 10

# Nome sugerido no primeiro uso; depois o programa lembra o último nome usado
FUNCIONARIO_PADRAO = "Josué B. Almeida"

# ============================================================================
# PASTA DE DADOS DO USUÁRIO (preferências e log)
# ============================================================================
PASTA_DADOS = os.path.join(
    os.environ.get("APPDATA") or os.path.expanduser("~"), "GeradorEmailHepta"
)
