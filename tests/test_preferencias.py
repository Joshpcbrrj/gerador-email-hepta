# -*- coding: utf-8 -*-
"""
TESTES PARA PREFERÊNCIAS
================================================================================
Tema e nome do funcionário lembrados entre execuções.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

import preferencias


@pytest.fixture(autouse=True)
def arquivo_temporario(tmp_path, monkeypatch):
    arquivo = tmp_path / "GeradorEmailHepta" / "preferencias.json"
    monkeypatch.setattr(preferencias, "ARQUIVO_PREFERENCIAS", str(arquivo))
    return arquivo


def test_sem_arquivo_usa_padrao():
    assert preferencias.ler("funcionario", "Padrão") == "Padrão"


def test_salva_e_le():
    preferencias.salvar("funcionario", "Maria da Silva")
    assert preferencias.ler("funcionario") == "Maria da Silva"


def test_salvar_uma_chave_mantem_as_outras():
    preferencias.salvar("tema", "escuro")
    preferencias.salvar("funcionario", "Ana")
    assert preferencias.ler("tema") == "escuro"
    assert preferencias.ler("funcionario") == "Ana"


def test_arquivo_corrompido_usa_padrao(arquivo_temporario):
    arquivo_temporario.parent.mkdir(parents=True)
    arquivo_temporario.write_text("{ isso não é json", encoding="utf-8")
    assert preferencias.ler("tema", "claro") == "claro"
