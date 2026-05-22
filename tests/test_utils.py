# -*- coding: utf-8 -*-
"""
TESTES PARA UTILS
================================================================================
Testa as funções utilitárias.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest


class TestResourcePath:
    """Testes para resource_path"""
    
    def test_resource_path_retorna_caminho_como_py(self):
        """Teste: resource_path retorna caminho normal quando executado como .py"""
        from utils import resource_path
        
        caminho = resource_path("teste.txt")
        # Deve conter o nome do arquivo
        assert "teste.txt" in caminho
        assert isinstance(caminho, str)
    
    def test_resource_path_funciona_com_arquivo_existente(self):
        """Teste: resource_path funciona com arquivo que existe"""
        from utils import resource_path
        
        # Testa com um arquivo que deve existir
        caminho = resource_path("logo.png")
        assert "logo.png" in caminho
        assert isinstance(caminho, str)
    
    def test_resource_path_com_nome_diferente(self):
        """Teste: resource_path com diferentes nomes de arquivo"""
        from utils import resource_path
        
        arquivos = ["winvnc.png", "logo.png", "config.py", "main.py"]
        for arquivo in arquivos:
            caminho = resource_path(arquivo)
            assert arquivo in caminho
            assert isinstance(caminho, str)