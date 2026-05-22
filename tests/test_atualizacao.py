# -*- coding: utf-8 -*-
"""
TESTES PARA AUTO-UPDATE
================================================================================
Testa as funções de verificação de atualização no GitHub.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import MagicMock, patch
from config import VERSAO_ATUAL, GITHUB_REPO, GITHUB_API_URL


class TestConfiguracoes:
    """Testes para configurações do auto-update"""
    
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
    
    def test_github_api_url_valida(self):
        """Teste: GITHUB_API_URL é uma URL válida"""
        assert GITHUB_API_URL.startswith("https://")
        assert "api.github.com" in GITHUB_API_URL


class TestVerificarAtualizacao:
    """Testes para função verificar_atualizacao"""
    
    @patch('atualizacao.urllib.request.urlopen')
    def test_verificar_atualizacao_sem_internet(self, mock_urlopen):
        """Teste: sem internet, não deve lançar exceção"""
        from atualizacao import verificar_atualizacao
        
        mock_urlopen.side_effect = Exception("Sem internet")
        
        mock_gui = MagicMock()
        
        try:
            verificar_atualizacao(mock_gui)
            assert True
        except Exception:
            assert False, "verificar_atualizacao lançou exceção mesmo sem internet"
    
    @patch('atualizacao.urllib.request.urlopen')
    def test_verificar_atualizacao_chama_callback(self, mock_urlopen):
        """Teste: callback é chamado quando está atualizado"""
        from atualizacao import verificar_atualizacao
        
        import json
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            'tag_name': f'v{VERSAO_ATUAL}',
            'html_url': 'https://github.com/test/repo',
            'body': 'Notas da versão'
        }).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        mock_gui = MagicMock()
        mock_callback = MagicMock()
        
        verificar_atualizacao(mock_gui, mock_callback)
        
        # Aguardar um pouco para a thread executar
        import time
        time.sleep(0.5)
        
        # O callback deve ser chamado (está atualizado)
        mock_gui.after.assert_called()