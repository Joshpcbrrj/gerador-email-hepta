# -*- coding: utf-8 -*-
"""
UTILITÁRIOS
================================================================================
Localização de arquivos do programa (imagens, modelos de e-mail).
"""

import os
import sys

# Pasta do código-fonte (quando executado como .py)
PASTA_PROGRAMA = os.path.dirname(os.path.abspath(__file__))


def resource_path(relative_path: str) -> str:
    """
    Caminho absoluto de um arquivo do programa.

    - Como .py: relativo à pasta do código (funciona de qualquer diretório).
    - Como .exe (PyInstaller): relativo à pasta temporária onde o .exe se extrai.
    """
    base_path = getattr(sys, "_MEIPASS", PASTA_PROGRAMA)
    return os.path.join(base_path, relative_path)
