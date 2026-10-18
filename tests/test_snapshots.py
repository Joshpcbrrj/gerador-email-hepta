# -*- coding: utf-8 -*-
"""
TESTES DE SNAPSHOT DOS E-MAILS
================================================================================
Garante que o HTML gerado continua IDÊNTICO ao que a equipe já usa.

Os arquivos em tests/snapshots/ são o resultado esperado de cada caso
(as imagens em base64 aparecem como {{WINVNC_BASE64}} e {{LOGO_BASE64}}
para os arquivos ficarem pequenos).

Se você alterar um texto do e-mail DE PROPÓSITO (em templates/), atualize os
snapshots com:  python tests/test_snapshots.py --atualizar
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime

import pytest

from geracao_email import montar_emails
from imagens import obter_logo_base64, obter_winvnc_base64
from tipo_email import TipoEmail

PASTA_SNAPSHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snapshots")

CASOS = {
    "aviso1_um_tel": (
        TipoEmail.AVISO_1,
        "000008198188",
        "Josué B. Almeida",
        ["(21) 97914-2434"],
        datetime(2026, 10, 17, 9, 5),
    ),
    "aviso2_dois_tel": (
        TipoEmail.AVISO_2,
        "REQ000008198188",
        "Maria da Silva",
        ["(21) 97914-2434", "(21) 3376-3562"],
        datetime(2026, 1, 2, 14, 30),
    ),
    "aviso3_tres_tel": (
        TipoEmail.AVISO_3,
        "req555",
        "João D'Ávila",
        ["(11) 99999-9999", "(21) 3376-3562", "(31) 97777-7777"],
        datetime(2026, 12, 31, 23, 59),
    ),
    "aviso2_dez_tel": (
        TipoEmail.AVISO_2,
        "7",
        "Carlos",
        [f"(11) 9999{i}-000{i}" for i in range(10)],
        datetime(2026, 7, 7, 7, 7),
    ),
    "fechamento": (
        TipoEmail.FECHAMENTO,
        "000008198188",
        "Josué B. Almeida",
        [],
        datetime(2026, 10, 17, 16, 45),
    ),
    "fechamento_req": (
        TipoEmail.FECHAMENTO,
        "REQ123",
        "Ana",
        ["(21) 97914-2434"],
        datetime(2026, 3, 8, 7, 0),
    ),
}


def _normalizar(html):
    """Troca as imagens em base64 por marcadores."""
    return html.replace(obter_winvnc_base64(), "{{WINVNC_BASE64}}").replace(
        obter_logo_base64(), "{{LOGO_BASE64}}"
    )


def _gerar(caso):
    """Retorna {nome_snapshot: html_normalizado} para o caso."""
    resultado = {}
    for email in montar_emails(*CASOS[caso]):
        sufixo = "nota" if email.nome_arquivo.startswith("nota") else "email"
        resultado[f"{caso}__{sufixo}.html"] = _normalizar(email.html)
    return resultado


@pytest.mark.parametrize("caso", sorted(CASOS))
def test_email_identico_ao_snapshot(caso):
    for nome_snapshot, html in _gerar(caso).items():
        with open(os.path.join(PASTA_SNAPSHOTS, nome_snapshot), encoding="utf-8") as f:
            esperado = f.read()
        assert html == esperado, f"{nome_snapshot} mudou em relação ao snapshot"


def test_imagens_estao_embutidas():
    """Os e-mails levam as imagens reais (não o aviso de imagem não encontrada)."""
    aviso = montar_emails(*CASOS["aviso1_um_tel"])[0].html
    assert obter_winvnc_base64() and obter_winvnc_base64() in aviso
    assert obter_logo_base64() and obter_logo_base64() in aviso
    assert "IMAGEM NÃO ENCONTRADA" not in aviso


def test_nomes_dos_arquivos():
    assert [e.nome_arquivo for e in montar_emails(*CASOS["aviso3_tres_tel"])] == [
        "email_555_3.html"
    ]
    assert [e.nome_arquivo for e in montar_emails(*CASOS["fechamento_req"])] == [
        "email_123_4.html",
        "nota_improdutivo_123.html",
    ]


if __name__ == "__main__" and "--atualizar" in sys.argv:
    for caso in CASOS:
        for nome_snapshot, html in _gerar(caso).items():
            caminho = os.path.join(PASTA_SNAPSHOTS, nome_snapshot)
            with open(caminho, "w", encoding="utf-8", newline="\n") as f:
                f.write(html)
            print("atualizado:", caminho)
