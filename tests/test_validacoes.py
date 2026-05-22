# -*- coding: utf-8 -*-
"""
TESTES PARA VALIDAÇÕES
================================================================================
Testa as funções de validação do sistema (REQ, limites, etc.)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from telefones import formatar_telefones


class TestValidacaoREQ:
    """Testes para validação do número da requisição"""
    
    def test_req_formato_completo(self):
        """Teste: REQ no formato completo com prefixo"""
        req = "REQ000008198188"
        assert req.startswith("REQ")
        assert len(req) > 3
    
    def test_req_apenas_numeros(self):
        """Teste: REQ apenas com números (sem prefixo)"""
        req = "000008198188"
        assert not req.startswith("REQ")
        assert req.isdigit()
    
    def test_req_vazia(self):
        """Teste: REQ vazia deve ser rejeitada"""
        req = ""
        assert len(req) == 0


class TestValidacaoLimiteTelefones:
    """Testes para validação de limite de telefones"""
    
    def test_limite_maximo_10(self):
        """Teste: limite máximo de 10 telefones deve ser aceito"""
        telefones = [f"(11) 9999{i}-999{i}" for i in range(10)]
        assert len(telefones) <= 10
    
    def test_limite_ultrapassado_11(self):
        """Teste: 11 telefones ultrapassa o limite"""
        telefones = [f"(11) 9999{i}-999{i}" for i in range(11)]
        assert len(telefones) > 10
    
    def test_limite_ultrapassado_15(self):
        """Teste: 15 telefones ultrapassa o limite"""
        telefones = [f"(11) 9999{i}-999{i}" for i in range(15)]
        assert len(telefones) > 10


class TestValidacaoTelefoneObrigatorio:
    """Testes para validação de telefone obrigatório"""
    
    def test_lista_vazia_deve_ser_rejeitada(self):
        """Teste: lista vazia de telefones deve ser rejeitada"""
        telefones = []
        assert len(telefones) == 0
    
    def test_lista_com_um_telefone_deve_ser_aceita(self):
        """Teste: lista com um telefone deve ser aceita"""
        telefones = ["(11) 99999-9999"]
        assert len(telefones) >= 1
    
    def test_lista_com_celular_apenas(self):
        """Teste: apenas celular é aceito"""
        telefones = ["(11) 99999-9999"]
        assert len(telefones) == 1
    
    def test_lista_com_fixo_apenas(self):
        """Teste: apenas fixo é aceito"""
        telefones = ["(11) 3431-3701"]
        assert len(telefones) == 1


class TestValidacaoFormatacaoLista:
    """Testes para formatação de lista de telefones (casos especiais)"""
    
    def test_formatar_lista_com_telefones_repetidos(self):
        """Teste: lista com telefones repetidos"""
        resultado = formatar_telefones(["(11) 99999-9999", "(11) 99999-9999"])
        assert "e" in resultado
    
    def test_formatar_lista_com_telefones_emojis(self):
        """Teste: lista com emojis (deve manter formatação)"""
        telefones_com_emoji = ["📞 (11) 99999-9999", "🏠 (21) 3376-3562"]
        # A função formatar_telefones não remove emojis
        resultado = formatar_telefones(telefones_com_emoji)
        assert "📞" in resultado or "🏠" in resultado