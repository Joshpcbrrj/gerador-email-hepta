# -*- coding: utf-8 -*-
"""
TESTES PARA IMAGENS
================================================================================
Testa as funções de manipulação de imagens.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import patch, MagicMock


class TestImagemToBase64:
    """Testes para conversão de imagem para base64"""
    
    def test_imagem_to_base64_arquivo_nao_existe(self):
        """Teste: arquivo não existe retorna None"""
        from imagens import imagem_to_base64
        
        resultado = imagem_to_base64("arquivo_que_nao_existe.png")
        assert resultado is None
    
    def test_imagem_to_base64_com_logo_png(self):
        """Teste: logo.png existe e é convertido"""
        from imagens import imagem_to_base64
        
        if os.path.exists("logo.png"):
            resultado = imagem_to_base64("logo.png")
            assert resultado is not None
            assert isinstance(resultado, str)
            assert len(resultado) > 0
        else:
            pytest.skip("logo.png não encontrado para teste")
    
    def test_imagem_to_base64_com_winvnc_png(self):
        """Teste: winvnc.png existe e é convertido"""
        from imagens import imagem_to_base64
        
        if os.path.exists("winvnc.png"):
            resultado = imagem_to_base64("winvnc.png")
            assert resultado is not None
            assert isinstance(resultado, str)
        else:
            pytest.skip("winvnc.png não encontrado para teste")
    
    @patch('imagens.os.path.exists')
    @patch('imagens.open')
    def test_imagem_to_base64_simulado(self, mock_open, mock_exists):
        """Teste: simula conversão bem-sucedida"""
        from imagens import imagem_to_base64
        
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = b"teste"
        mock_open.return_value = mock_file
        
        resultado = imagem_to_base64("teste.png")
        assert resultado is not None
        assert isinstance(resultado, str)


class TestVerificarImagens:
    """Testes para verificar_imagens"""
    
    def test_verificar_imagens_nao_lanca_excecao(self):
        """Teste: verificar_imagens não lança exceção"""
        from imagens import verificar_imagens
        
        try:
            verificar_imagens()
            assert True
        except Exception:
            assert False, "verificar_imagens lançou exceção"


class TestResourcePath:
    """Testes para resource_path"""
    
    def test_resource_path_retorna_caminho(self):
        """Teste: resource_path retorna um caminho válido"""
        from utils import resource_path
        
        caminho = resource_path("logo.png")
        assert caminho is not None
        assert "logo.png" in caminho
        assert isinstance(caminho, str)