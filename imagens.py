# -*- coding: utf-8 -*-
"""
IMAGENS DOS E-MAILS
================================================================================
Converte as imagens de assets/ para base64, para embuti-las no HTML:

    <img src="data:image/png;base64,iVBORw0KGgo...">

Assim a imagem viaja dentro do próprio e-mail ao copiar e colar,
sem depender de anexo ou de link externo.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import base64
import logging
import os
from functools import cache

from utils import resource_path

CAMINHO_WINVNC = os.path.join("assets", "winvnc.png")
CAMINHO_LOGO = os.path.join("assets", "logo.png")

log = logging.getLogger(__name__)


def imagem_to_base64(caminho_imagem: str) -> str | None:
    """
    Retorna o conteúdo da imagem em base64, ou None se não for encontrada.

    Procura no caminho informado e, se não existir, na pasta do programa
    (que, no .exe, é a pasta onde o PyInstaller extrai os arquivos).
    """
    for caminho in (caminho_imagem, resource_path(caminho_imagem)):
        try:
            if os.path.exists(caminho):
                with open(caminho, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode("utf-8")
        except OSError as erro:
            log.error("Erro ao carregar imagem %s: %s", caminho, erro)
            return None

    log.error("Imagem não encontrada: %s", caminho_imagem)
    return None


@cache
def obter_winvnc_base64() -> str | None:
    """Imagem da janela do WinVNC (lida uma vez e reaproveitada)."""
    return imagem_to_base64(CAMINHO_WINVNC)


@cache
def obter_logo_base64() -> str | None:
    """Logo da Hepta (lida uma vez e reaproveitada)."""
    return imagem_to_base64(CAMINHO_LOGO)
