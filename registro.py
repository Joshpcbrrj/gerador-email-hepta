# -*- coding: utf-8 -*-
"""
MÓDULO DE REGISTRO DE ERROS (LOG)
================================================================================
O executável não tem console, então erros impressos com print() se perdem.
Este módulo grava avisos e erros em %APPDATA%\\GeradorEmailHepta\\gerador.log
(até ~1 MB, com rotação), para ajudar quando alguém relatar um problema.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

from config import PASTA_DADOS, VERSAO_ATUAL

ARQUIVO_LOG = os.path.join(PASTA_DADOS, "gerador.log")


def configurar_log() -> None:
    """Configura o log em arquivo (avisos e erros). Falhas aqui são ignoradas."""
    raiz = logging.getLogger()
    if any(isinstance(h, RotatingFileHandler) for h in raiz.handlers):
        return
    try:
        os.makedirs(PASTA_DADOS, exist_ok=True)
        handler = RotatingFileHandler(
            ARQUIVO_LOG, maxBytes=500_000, backupCount=1, encoding="utf-8"
        )
    except OSError:
        return
    handler.setFormatter(
        logging.Formatter(f"%(asctime)s [v{VERSAO_ATUAL}] %(levelname)s %(name)s: %(message)s")
    )
    raiz.addHandler(handler)
    raiz.setLevel(logging.WARNING)
