# -*- coding: utf-8 -*-
"""
MÓDULO DE GERAÇÃO DE HTML
================================================================================
Monta os e-mails (aviso, fechamento) e a nota de improdutivo a partir dos
modelos em templates/.

Para alterar um texto do e-mail, edite o arquivo .html correspondente em
templates/ — não é preciso mexer no código. Os campos variáveis aparecem
no modelo como $nome_do_campo.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import html
from functools import cache
from string import Template

from imagens import obter_logo_base64, obter_winvnc_base64
from tipo_email import TipoEmail
from utils import resource_path


@cache
def _carregar_template(nome: str) -> Template:
    with open(resource_path(f"templates/{nome}.html"), encoding="utf-8") as f:
        return Template(f.read())


def _texto(valor: str) -> str:
    """Escapa texto digitado pelo usuário (ex: '<' e '&' não quebram o HTML)."""
    return html.escape(valor, quote=False)


def _imagem_winvnc() -> str:
    winvnc = obter_winvnc_base64()
    if winvnc:
        return f'<img src="data:image/png;base64,{winvnc}" alt="WinVNC"/>'
    return "<p>⚠️ IMAGEM NÃO ENCONTRADA</p>"


def _imagem_logo() -> str:
    logo = obter_logo_base64()
    if logo:
        return f'<img src="data:image/png;base64,{logo}" alt="Hepta Tecnologia"/>'
    return "<b>Hepta Tecnologia</b>"


def gerar_email_aviso_html(
    titulo: str, num_req: str, nome: str, telefones: str, data_hora: str, tentativa: str
) -> str:
    """
    E-mail de AVISO (1ª, 2ª ou 3ª tentativa).

    - telefones: telefone(s) já formatado(s) para o texto
    - data_hora: ex. "17/10/2026 às 14:30 BRT"
    - tentativa: "1", "2" ou "3"
    """
    tipo = TipoEmail(tentativa) if tentativa in ("1", "2", "3") else TipoEmail.AVISO_1
    return _carregar_template("aviso").substitute(
        titulo=_texto(titulo),
        num_req=_texto(num_req),
        nome=_texto(nome),
        telefones=_texto(telefones),
        data_hora=_texto(data_hora),
        tentativa_texto=tipo.extenso,
        imagem_winvnc=_imagem_winvnc(),
        imagem_logo=_imagem_logo(),
    )


def gerar_email_fechamento_html(titulo: str, num_req: str, nome: str, data_hora: str) -> str:
    """E-mail de FECHAMENTO (após 3 tentativas sem sucesso)."""
    return _carregar_template("fechamento").substitute(
        titulo=_texto(titulo),
        num_req=_texto(num_req),
        nome=_texto(nome),
        data_hora=_texto(data_hora),
        imagem_logo=_imagem_logo(),
    )


def gerar_nota_improdutivo_html(num_req_completo: str = "") -> str:
    """Nota de chamado improdutivo (texto fixo), aberta junto com o fechamento."""
    return _carregar_template("nota_improdutivo").substitute()
