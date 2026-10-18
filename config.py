# -*- coding: utf-8 -*-
"""
MÓDULO DE CONFIGURAÇÃO
================================================================================
Constantes e configurações globais do programa.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

# ============================================================================
# VERSÃO DO PROGRAMA
# ============================================================================
# ATENÇÃO: Atualize este número a cada nova release no GitHub!
VERSAO_ATUAL = "2.6"

# Intervalo da verificação automática de atualizações (programa aberto)
INTERVALO_VERIFICAR_ATUALIZACAO_MS = 4 * 60 * 60 * 1000  # 4 horas

# ============================================================================
# CONFIGURAÇÕES DO GITHUB PARA AUTO-UPDATE
# ============================================================================
# Nome do repositório no formato "usuario/repositorio"
GITHUB_REPO = "Joshpcbrrj/gerador-email-hepta"

# URL da API do GitHub para buscar a última release
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"