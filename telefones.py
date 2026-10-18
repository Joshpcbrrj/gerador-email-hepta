# -*- coding: utf-8 -*-
"""
FORMATAÇÃO DE TELEFONES
================================================================================
1. Formata números no padrão brasileiro: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
2. Junta vários telefones para o texto do e-mail

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import re


def formatar_celular(telefone_str: str) -> str:
    """
    Formata número de telefone CELULAR no padrão (XX) 9XXXX-XXXX

    Exemplos:
    - "21979142434" -> "(21) 97914-2434"
    - "2179142434"  -> "(21) 97914-2434"  (acrescenta o 9)
    """
    numeros = re.sub(r"\D", "", telefone_str)
    if len(numeros) >= 10:
        ddd = numeros[:2]
        numero = numeros[2:]
        if len(numero) == 8:
            numero = f"9{numero}"
        if len(numero) == 9:
            numero = f"{numero[:5]}-{numero[5:]}"
        return f"({ddd}) {numero}"
    return telefone_str


def formatar_fixo(telefone_str: str) -> str:
    """
    Formata número de telefone FIXO no padrão (XX) XXXX-XXXX

    Exemplos:
    - "2133763562" -> "(21) 3376-3562"
    - "1134313701" -> "(11) 3431-3701"
    """
    numeros = re.sub(r"\D", "", telefone_str)
    if len(numeros) >= 10:
        ddd = numeros[:2]
        numero = numeros[2:]
        if len(numero) == 9 and numero.startswith("9"):
            numero = numero[1:]
        if len(numero) == 8:
            numero = f"{numero[:4]}-{numero[4:]}"
        return f"({ddd}) {numero}"
    return telefone_str


def formatar_telefones(telefones: list[str]) -> str:
    """
    Junta a lista de telefones para o texto do e-mail.

    - 1 telefone:  "(11) 99999-9999"
    - 2 telefones: "(11) 99999-9999 e (21) 98888-8888"
    - 3 telefones: "(11) 99999-9999, (21) 98888-8888 e (31) 97777-7777"
    """
    if len(telefones) == 0:
        return ""
    if len(telefones) == 1:
        return telefones[0]
    return ", ".join(telefones[:-1]) + " e " + telefones[-1]
