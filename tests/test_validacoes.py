# -*- coding: utf-8 -*-
"""
TESTES PARA VALIDAÇÕES DO FORMULÁRIO
================================================================================
Testa as regras reais de geracao_email (REQ, telefones, nome) e os tipos.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from config import MAX_TELEFONES
from geracao_email import normalizar_req, validar_formulario
from tipo_email import TipoEmail

UM_TELEFONE = ["(11) 99999-9999"]


class TestNormalizarReq:
    def test_apenas_numeros_ganha_prefixo(self):
        assert normalizar_req("000008198188") == ("REQ000008198188", "000008198188")

    def test_com_prefixo(self):
        assert normalizar_req("REQ000008198188") == ("REQ000008198188", "000008198188")

    def test_prefixo_minusculo_vira_maiusculo(self):
        assert normalizar_req("req555") == ("REQ555", "555")

    def test_espacos_sao_ignorados(self):
        assert normalizar_req("  123  ") == ("REQ123", "123")


class TestValidarFormulario:
    def test_formulario_valido(self):
        assert validar_formulario("123", TipoEmail.AVISO_1, UM_TELEFONE, "Ana") is None

    def test_req_vazia(self):
        erro = validar_formulario("   ", TipoEmail.AVISO_1, UM_TELEFONE, "Ana")
        assert erro and "REQ" in erro.status

    def test_aviso_sem_telefone(self):
        erro = validar_formulario("123", TipoEmail.AVISO_2, [], "Ana")
        assert erro and "telefone" in erro.status

    def test_fechamento_nao_exige_telefone(self):
        assert validar_formulario("123", TipoEmail.FECHAMENTO, [], "Ana") is None

    def test_limite_de_telefones_aceito(self):
        telefones = UM_TELEFONE * MAX_TELEFONES
        assert validar_formulario("123", TipoEmail.AVISO_3, telefones, "Ana") is None

    def test_limite_de_telefones_ultrapassado(self):
        telefones = UM_TELEFONE * (MAX_TELEFONES + 1)
        erro = validar_formulario("123", TipoEmail.AVISO_3, telefones, "Ana")
        assert erro and "Remova 1 telefone" in erro.detalhe

    def test_nome_vazio_nao_assina_com_nome_de_outra_pessoa(self):
        erro = validar_formulario("123", TipoEmail.AVISO_1, UM_TELEFONE, "  ")
        assert erro and "funcionário" in erro.status


class TestTipoEmail:
    def test_valores_compativeis_com_nomes_de_arquivo(self):
        assert [t.value for t in TipoEmail] == ["1", "2", "3", "4"]

    def test_textos_dos_avisos(self):
        assert TipoEmail.AVISO_2.ordinal == "2º"
        assert TipoEmail.AVISO_3.extenso == "terceira"

    def test_somente_fechamento_dispensa_telefone(self):
        assert [t.exige_telefone for t in TipoEmail] == [True, True, True, False]

    def test_valor_invalido(self):
        with pytest.raises(ValueError):
            TipoEmail("5")
