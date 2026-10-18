# -*- coding: utf-8 -*-
"""
TESTES DO BOTÃO "COPIAR E-MAIL"
================================================================================
O HTML copiado tem só o e-mail (sem instruções e sem créditos), com os
estilos embutidos e as imagens, no formato de área de transferência do Windows.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime

import pytest

from area_transferencia import html_para_colar, montar_cf_html, texto_simples
from geracao_email import montar_emails
from imagens import obter_logo_base64, obter_winvnc_base64
from tipo_email import TipoEmail

MOMENTO = datetime(2026, 10, 17, 9, 5)


def _email(tipo):
    return montar_emails(tipo, "123", "Maria", ["(21) 97914-2434"], MOMENTO)[0].html


@pytest.mark.parametrize("tipo", [TipoEmail.AVISO_1, TipoEmail.FECHAMENTO])
def test_copia_so_o_email(tipo):
    fragmento = html_para_colar(_email(tipo))
    assert "COMO COPIAR ESTE E-MAIL" not in fragmento
    assert "Programa feito por" not in fragmento
    assert "Prezado Cliente," in fragmento
    assert "Atenciosamente," in fragmento
    assert "(61) 3424-4800" in fragmento


@pytest.mark.parametrize("tipo", [TipoEmail.AVISO_1, TipoEmail.FECHAMENTO])
def test_estilos_embutidos_sem_classes(tipo):
    fragmento = html_para_colar(_email(tipo))
    assert "class=" not in fragmento
    assert "<style" not in fragmento
    assert 'style="font-size: 14pt; font-weight: bold' in fragmento  # título


def test_imagens_copiadas_com_estilo():
    fragmento = html_para_colar(_email(TipoEmail.AVISO_1))
    assert obter_winvnc_base64() in fragmento
    assert obter_logo_base64() in fragmento
    assert '<img style="max-width: 100px; height: auto"' in fragmento  # logo
    assert '<img style="max-width: 100%' in fragmento  # WinVNC


def test_fechamento_nao_tem_imagem_winvnc():
    assert obter_winvnc_base64() not in html_para_colar(_email(TipoEmail.FECHAMENTO))


def test_texto_simples():
    texto = texto_simples(html_para_colar(_email(TipoEmail.AVISO_1)))
    assert texto.startswith("REQ123 - 1º aviso de tentativa de contato com o cliente")
    assert "<" not in texto


def test_cabecalho_cf_html_aponta_para_o_trecho():
    fragmento = "<p>Olá — ação</p>"  # acentos: posições são em bytes UTF-8
    dados = montar_cf_html(fragmento)
    posicoes = {k.decode(): int(v) for k, v in re.findall(rb"(\w+):(\d{10})", dados)}
    assert dados[posicoes["StartFragment"] : posicoes["EndFragment"]].decode() == fragmento
    assert dados[posicoes["StartHTML"] :].startswith(b"<html>")
    assert posicoes["EndHTML"] == len(dados)


@pytest.mark.skipif(sys.platform != "win32", reason="área de transferência do Windows")
def test_copiar_e_ler_de_volta():
    import ctypes

    from area_transferencia import _api, copiar_html

    try:
        copiar_html("<p>teste gerador</p>", "teste gerador")
    except OSError as erro:
        pytest.skip(f"área de transferência indisponível: {erro}")

    user32, kernel32 = _api()
    user32.GetClipboardData.argtypes = [ctypes.c_uint]
    user32.GetClipboardData.restype = ctypes.c_void_p
    assert user32.OpenClipboard(None)
    try:
        alca = user32.GetClipboardData(13)  # CF_UNICODETEXT
        texto = ctypes.wstring_at(kernel32.GlobalLock(alca))
        kernel32.GlobalUnlock(alca)
        tem_html = user32.IsClipboardFormatAvailable(user32.RegisterClipboardFormatW("HTML Format"))
    finally:
        user32.CloseClipboard()
    assert texto == "teste gerador"
    assert tem_html
