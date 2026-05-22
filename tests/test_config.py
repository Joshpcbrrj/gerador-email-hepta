# -*- coding: utf-8 -*-
"""
TESTES PARA CONFIGURAÇÃO
================================================================================
Testa as constantes de configuração.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from config import VERSAO_ATUAL, GITHUB_REPO, GITHUB_API_URL


class TestConfig:
    """Testes para constantes de configuração"""
    
    def test_versao_atual_definida(self):
        """Teste: VERSAO_ATUAL está definida"""
        assert VERSAO_ATUAL is not None
        assert len(VERSAO_ATUAL) > 0
    
    def test_versao_atual_formato_valido(self):
        """Teste: VERSAO_ATUAL tem formato válido (ex: 2.2, 2.3)"""
        partes = VERSAO_ATUAL.split('.')
        assert len(partes) >= 2
        assert partes[0].isdigit()
        assert partes[1].isdigit()
    
    def test_github_repo_definido(self):
        """Teste: GITHUB_REPO está definido"""
        assert GITHUB_REPO is not None
        assert "/" in GITHUB_REPO
        assert "Joshpcbrrj" in GITHUB_REPO
    
    def test_github_api_url_valida(self):
        """Teste: GITHUB_API_URL é uma URL válida"""
        assert GITHUB_API_URL.startswith("https://")
        assert "api.github.com" in GITHUB_API_URL
        assert GITHUB_REPO in GITHUB_API_URL