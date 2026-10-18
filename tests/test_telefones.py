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


from telefones import (  # noqa: E402
    apenas_digitos,
    eh_celular,
    extrair_telefones,
    normalizar_digitos,
    validar_telefone,
)


class TestValidarTelefone:
    @pytest.mark.parametrize("numero", ["21979142434", "2133763562", "2179142434"])
    def test_validos(self, numero):
        assert validar_telefone(numero) is None

    @pytest.mark.parametrize(
        "numero",
        [
            "119991234567",  # 12 dígitos: antes perdia um dígito sem avisar
            "979142434",  # sem DDD
            "12345",
            "20979142434",  # DDD com zero (não existe)
            "21379142434",  # 11 dígitos sem o 9
        ],
    )
    def test_invalidos(self, numero):
        assert validar_telefone(normalizar_digitos(numero)) is not None

    def test_mensagem_informa_quantidade_de_digitos(self):
        assert "12 dígitos" in validar_telefone("119991234567")


class TestNormalizarDigitos:
    def test_codigo_do_pais(self):
        assert normalizar_digitos(apenas_digitos("+55 21 97914-2434")) == "21979142434"

    def test_zero_de_operadora(self):
        assert normalizar_digitos(apenas_digitos("021 3376-3562")) == "2133763562"

    def test_numero_normal_nao_muda(self):
        assert normalizar_digitos("21979142434") == "21979142434"


class TestEhCelular:
    def test_onze_digitos(self):
        assert eh_celular("21979142434")

    def test_fixo(self):
        assert not eh_celular("2133763562")

    def test_celular_antigo_oito_digitos(self):
        assert eh_celular("2179142434")


class TestExtrairTelefones:
    def test_um_numero(self):
        assert extrair_telefones("(21) 97914-2434") == ["(21) 97914-2434"]

    @pytest.mark.parametrize(
        "texto",
        [
            "21 97914-2434 / 21 3376-3562",
            "21 97914-2434, 21 3376-3562",
            "21 97914-2434; 21 3376-3562",
            "21 97914-2434 e 21 3376-3562",
            "21 97914-2434 ou 21 3376-3562",
            "21 97914-2434\n21 3376-3562",
            "21979142434 2133763562",
            "21 97914 2434 21 3376 3562",
            "+55 21 97914-2434 21 3376-3562",
        ],
    )
    def test_dois_numeros(self, texto):
        digitos = [normalizar_digitos(apenas_digitos(t)) for t in extrair_telefones(texto)]
        assert digitos == ["21979142434", "2133763562"]

    def test_texto_sem_numeros(self):
        assert extrair_telefones("sem telefone") == []
