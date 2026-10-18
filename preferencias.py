# -*- coding: utf-8 -*-
"""
MÓDULO DE PREFERÊNCIAS
================================================================================
Guarda escolhas do usuário entre execuções (tema, nome do funcionário) em
%APPDATA%\\GeradorEmailHepta\\preferencias.json.

Falhas de leitura/escrita nunca interrompem o programa: na pior hipótese,
o valor padrão é usado.
"""

import json
import logging
import os
from typing import Any

from config import PASTA_DADOS

ARQUIVO_PREFERENCIAS = os.path.join(PASTA_DADOS, "preferencias.json")

log = logging.getLogger(__name__)


def _carregar_tudo() -> dict:
    try:
        with open(ARQUIVO_PREFERENCIAS, encoding="utf-8") as f:
            dados = json.load(f)
        return dados if isinstance(dados, dict) else {}
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as erro:
        log.warning("Preferências ilegíveis, usando padrões: %s", erro)
        return {}


def ler(chave: str, padrao: Any = None) -> Any:
    """Retorna a preferência salva ou o valor padrão."""
    return _carregar_tudo().get(chave, padrao)


def salvar(chave: str, valor: Any) -> None:
    """Salva uma preferência, mantendo as demais."""
    dados = _carregar_tudo()
    if dados.get(chave) == valor:
        return
    dados[chave] = valor
    try:
        os.makedirs(os.path.dirname(ARQUIVO_PREFERENCIAS), exist_ok=True)
        with open(ARQUIVO_PREFERENCIAS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except OSError as erro:
        log.warning("Não foi possível salvar a preferência %r: %s", chave, erro)
