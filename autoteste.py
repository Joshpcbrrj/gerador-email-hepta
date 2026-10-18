# -*- coding: utf-8 -*-
"""
AUTOTESTE DO EXECUTÁVEL
================================================================================
`GeradorEmailHepta.exe --autoteste` gera os e-mails em memória, sem abrir a
janela, e confere se os modelos e as imagens foram empacotados no .exe.
Sai com código 0 se estiver tudo certo e 1 se algo faltar.

Usado no workflow de release antes de publicar o executável.
"""

from datetime import datetime

from geracao_email import montar_emails
from imagens import obter_logo_base64, obter_winvnc_base64
from tipo_email import TipoEmail


def executar() -> int:
    momento = datetime(2026, 1, 1, 9, 0)
    problemas = []

    winvnc, logo = obter_winvnc_base64(), obter_logo_base64()
    if not winvnc:
        problemas.append("imagem do WinVNC não encontrada")
    if not logo:
        problemas.append("logo não encontrado")

    try:
        aviso = montar_emails(TipoEmail.AVISO_1, "1", "Teste", ["(61) 3424-4800"], momento)
        fechamento = montar_emails(TipoEmail.FECHAMENTO, "1", "Teste", [], momento)
    except Exception as erro:  # modelo ausente ou com campo inválido
        problemas.append(f"falha ao montar os e-mails: {erro!r}")
    else:
        html_aviso = aviso[0].html
        if "Prezado Cliente" not in html_aviso or "01/01/2026 às 09:00 BRT" not in html_aviso:
            problemas.append("texto do e-mail de aviso incompleto")
        if winvnc and winvnc not in html_aviso:
            problemas.append("imagem do WinVNC não embutida no aviso")
        if len(fechamento) != 2 or "IMPRODUTIVO" not in fechamento[1].html:
            problemas.append("e-mail de fechamento ou nota incompletos")

    return 1 if problemas else 0
