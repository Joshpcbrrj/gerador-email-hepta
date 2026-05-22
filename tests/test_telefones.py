# -*- coding: utf-8 -*-
"""
TESTES PARA FORMATAÇÃO DE TELEFONES
================================================================================
Testa as funções de formatação de números de telefone.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from telefones import formatar_celular, formatar_fixo, formatar_telefones


class TestFormatarCelular:
    """Testes para formatação de telefone celular"""
    
    def test_celular_11_digitos(self):
        """Teste: celular com 11 dígitos (DDD + 9 + 8 dígitos)"""
        resultado = formatar_celular("21979142434")
        assert resultado == "(21) 97914-2434"
    
    def test_celular_com_espacos(self):
        """Teste: celular com espaços"""
        resultado = formatar_celular("21 97914 2434")
        assert resultado == "(21) 97914-2434"
    
    def test_celular_10_digitos(self):
        """Teste: celular com 10 dígitos (adiciona 9 automaticamente)"""
        resultado = formatar_celular("2134313701")
        assert resultado == "(21) 93431-3701"
    
    def test_celular_invalido(self):
        """Teste: celular inválido (menos de 10 dígitos)"""
        resultado = formatar_celular("12345")
        assert resultado == "12345"


class TestFormatarFixo:
    """Testes para formatação de telefone fixo"""
    
    def test_fixo_10_digitos(self):
        """Teste: fixo com 10 dígitos (DDD + 8 dígitos)"""
        resultado = formatar_fixo("2133763562")
        assert resultado == "(21) 3376-3562"
    
    def test_fixo_11_digitos_com_9(self):
        """Teste: fixo digitado com 9 na frente (remove o 9)"""
        resultado = formatar_fixo("21933763562")
        assert resultado == "(21) 3376-3562"
    
    def test_fixo_invalido(self):
        """Teste: fixo inválido (menos de 10 dígitos)"""
        resultado = formatar_fixo("12345")
        assert resultado == "12345"


class TestFormatarListaTelefones:
    """Testes para formatação de lista de telefones"""
    
    def test_um_telefone(self):
        """Teste: lista com um telefone"""
        resultado = formatar_telefones(["(11) 99999-9999"])
        assert resultado == "(11) 99999-9999"
    
    def test_dois_telefones(self):
        """Teste: lista com dois telefones"""
        resultado = formatar_telefones(["(11) 99999-9999", "(21) 98888-8888"])
        assert resultado == "(11) 99999-9999 e (21) 98888-8888"
    
    def test_lista_vazia(self):
        """Teste: lista vazia"""
        resultado = formatar_telefones([])
        assert resultado == ""