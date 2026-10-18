# -*- coding: utf-8 -*-
"""
TESTES DO FLUXO COMPLETO DO BOTÃO "GERAR E-MAIL"
================================================================================
Simula a interface e confere o que acontece de ponta a ponta: arquivos
gravados na pasta temporária, navegador aberto, nome lembrado e mensagens.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

import geracao_email
from tipo_email import TipoEmail

MOMENTO = datetime(2026, 10, 17, 14, 30)


def _gui(tipo="1", req="000008198188", nome="Maria da Silva", momento=MOMENTO):
    gui = MagicMock()
    gui.tipo_email.get.return_value = tipo
    gui.entry_req.get.return_value = req
    gui.entry_nome.get.return_value = nome
    gui.obter_data_hora_contato.return_value = momento
    return gui


@pytest.fixture
def ambiente(tmp_path):
    """Pasta temporária isolada, navegador e janelas de erro simulados."""
    with (
        patch.object(geracao_email, "obter_pasta_temp", lambda: str(tmp_path)),
        patch.object(geracao_email.webbrowser, "open") as navegador,
        patch.object(geracao_email, "messagebox") as janelas,
    ):
        yield tmp_path, navegador, janelas


def _gerar(gui, telefones):
    geracao_email.gerar_email(gui, lambda _gui: list(telefones))


def test_aviso_grava_arquivo_e_abre_no_navegador(ambiente):
    pasta, navegador, janelas = ambiente
    gui = _gui(tipo=TipoEmail.AVISO_2.value)

    _gerar(gui, ["(21) 97914-2434"])

    arquivo = pasta / "email_000008198188_2.html"
    assert arquivo.exists()
    html = arquivo.read_text(encoding="utf-8")
    assert "REQ000008198188 - 2º aviso de tentativa de contato com o cliente" in html
    assert "17/10/2026 às 14:30 BRT" in html
    navegador.assert_called_once_with(f"file://{arquivo}")
    gui.lembrar_funcionario.assert_called_once_with("Maria da Silva")
    janelas.showerror.assert_not_called()


def test_fechamento_abre_email_e_nota(ambiente):
    pasta, navegador, _ = ambiente

    _gerar(_gui(tipo=TipoEmail.FECHAMENTO.value, req="REQ123"), [])

    abertos = [chamada.args[0] for chamada in navegador.call_args_list]
    assert abertos == [
        f"file://{pasta / 'email_123_4.html'}",
        f"file://{pasta / 'nota_improdutivo_123.html'}",
    ]


@pytest.mark.parametrize(
    ("gui", "telefones", "trecho_do_erro"),
    [
        (_gui(req=""), ["(21) 97914-2434"], "requisição"),
        (_gui(), [], "telefone"),
        (_gui(nome="  "), ["(21) 97914-2434"], "funcionário"),
    ],
)
def test_formulario_incompleto_nao_gera_nada(ambiente, gui, telefones, trecho_do_erro):
    pasta, navegador, janelas = ambiente

    _gerar(gui, telefones)

    assert list(pasta.iterdir()) == []
    navegador.assert_not_called()
    gui.lembrar_funcionario.assert_not_called()
    assert trecho_do_erro in janelas.showerror.call_args.args[1]


def test_data_manual_invalida_nao_gera_nada(ambiente):
    pasta, navegador, janelas = ambiente
    gui = _gui()
    gui.obter_data_hora_contato.side_effect = ValueError("Data/hora inválida: 31/02/2026 10:00")

    _gerar(gui, ["(21) 97914-2434"])

    assert list(pasta.iterdir()) == []
    navegador.assert_not_called()
    assert "31/02/2026" in janelas.showerror.call_args.args[1]


def test_copiar_email_vai_para_area_de_transferencia_sem_navegador(ambiente):
    pasta, navegador, _ = ambiente
    gui = _gui()

    with patch.object(geracao_email, "copiar_html") as copiar:
        geracao_email.copiar_email(gui, lambda _gui: ["(21) 97914-2434"])

    fragmento, texto = copiar.call_args.args
    assert "Prezado Cliente," in fragmento and "COMO COPIAR" not in fragmento
    assert texto.startswith("REQ000008198188 - 1º aviso")
    navegador.assert_not_called()
    assert list(pasta.iterdir()) == []
    gui.lembrar_funcionario.assert_called_once_with("Maria da Silva")


def test_copiar_fechamento_abre_so_a_nota(ambiente):
    pasta, navegador, _ = ambiente

    with patch.object(geracao_email, "copiar_html") as copiar:
        geracao_email.copiar_email(
            _gui(tipo=TipoEmail.FECHAMENTO.value, req="REQ123"), lambda _gui: []
        )

    assert "Chamado Fechado" in copiar.call_args.args[0]
    navegador.assert_called_once_with(f"file://{pasta / 'nota_improdutivo_123.html'}")


def test_falha_ao_copiar_avisa_e_sugere_o_navegador(ambiente):
    _, _, janelas = ambiente
    gui = _gui()

    with patch.object(geracao_email, "copiar_html", side_effect=OSError("em uso")):
        geracao_email.copiar_email(gui, lambda _gui: ["(21) 97914-2434"])

    assert "Gerar e-mail" in janelas.showerror.call_args.args[1]
    gui.lembrar_funcionario.assert_not_called()
