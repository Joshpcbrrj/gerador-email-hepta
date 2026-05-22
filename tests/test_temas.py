# -*- coding: utf-8 -*-
"""
TESTES PARA TEMAS
================================================================================
Testa as cores dos temas claro e escuro.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from temas import CORES


class TestCores:
    """Testes para as cores dos temas"""
    
    def test_temas_existem(self):
        """Teste: temas claro e escuro existem"""
        assert 'claro' in CORES
        assert 'escuro' in CORES
    
    def test_tema_claro_tem_campos_necessarios(self):
        """Teste: tema claro tem as chaves necessárias"""
        tema = CORES['claro']
        campos_necessarios = ['bg', 'fg', 'frame_bg', 'entry_bg', 'listbox_bg']
        for campo in campos_necessarios:
            assert campo in tema
    
    def test_tema_escuro_tem_campos_necessarios(self):
        """Teste: tema escuro tem as chaves necessárias"""
        tema = CORES['escuro']
        campos_necessarios = ['bg', 'fg', 'frame_bg', 'entry_bg', 'listbox_bg']
        for campo in campos_necessarios:
            assert campo in tema
    
    def test_cores_sao_hexadecimais(self):
        """Teste: cores estão em formato hexadecimal"""
        for tema_nome, tema in CORES.items():
            for cor_nome, cor_valor in tema.items():
                if isinstance(cor_valor, str) and cor_valor.startswith('#'):
                    # Verifica se é hex válido (# seguido de 6 caracteres)
                    assert len(cor_valor) == 7
                    assert all(c in '0123456789ABCDEFabcdef' for c in cor_valor[1:])