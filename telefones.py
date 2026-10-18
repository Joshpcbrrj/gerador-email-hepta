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

    Use validar_telefone antes: números com dígitos a mais ou a menos não
    são corrigidos aqui.
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


# ============================================================================
# VALIDAÇÃO E LEITURA DE VÁRIOS NÚMEROS
# ============================================================================

# Separadores comuns quando os números vêm juntos do chamado
_SEPARADORES = re.compile(r"[,;/|\n\t]+|\s+(?:e|ou)\s+", re.IGNORECASE)


def apenas_digitos(texto: str) -> str:
    return re.sub(r"\D", "", texto)


def normalizar_digitos(digitos: str) -> str:
    """
    Remove prefixos que não fazem parte de DDD + número:

    - "0" de operadora/interurbano: "021 3376-3562" -> "2133763562"
    - código do país:  "+55 21 97914-2434" -> "21979142434"
    """
    if len(digitos) in (11, 12) and digitos.startswith("0"):
        digitos = digitos[1:]
    if len(digitos) in (12, 13) and digitos.startswith("55"):
        digitos = digitos[2:]
    return digitos


def validar_telefone(digitos: str) -> str | None:
    """
    Recebe os dígitos já normalizados e retorna o problema encontrado,
    ou None se o número for válido (DDD + 8 ou 9 dígitos).
    """
    if len(digitos) not in (10, 11):
        return (
            f"O número tem {len(digitos)} dígitos. Informe DDD + número, "
            "com 10 ou 11 dígitos (ex: 21 97914-2434)."
        )
    if "0" in digitos[:2]:
        return f"DDD inválido: {digitos[:2]}."
    if len(digitos) == 11 and digitos[2] != "9":
        return "Número com 11 dígitos precisa começar com 9 depois do DDD (celular)."
    return None


def eh_celular(digitos: str) -> bool:
    """Celular: 9 dígitos após o DDD, ou 8 começando com 6 a 9 (formato antigo)."""
    return len(digitos) == 11 or (len(digitos) == 10 and digitos[2] in "6789")


def formatar_automatico(digitos: str) -> str:
    """Formata como celular ou fixo conforme o próprio número."""
    return formatar_celular(digitos) if eh_celular(digitos) else formatar_fixo(digitos)


def extrair_telefones(texto: str) -> list[str]:
    """
    Separa um texto com vários números em trechos, um por telefone.

    Aceita separadores como vírgula, barra, ponto e vírgula, quebra de linha,
    " e " / " ou ", e também números separados só por espaço:
    "21 97914-2434 / 21 3376-3562" -> ["21 97914-2434", "21 3376-3562"]
    """
    trechos = []
    for parte in _SEPARADORES.split(texto):
        if not apenas_digitos(parte):
            continue
        if len(normalizar_digitos(apenas_digitos(parte))) <= 11:
            trechos.append(parte.strip())
        else:
            trechos.extend(_separar_por_espaco(parte))
    return trechos


def _separar_por_espaco(texto: str) -> list[str]:
    """Agrupa pedaços separados por espaço até formar DDD + número."""
    pecas = texto.split()
    grupos, atual = [], []
    for i, peca in enumerate(pecas):
        atual.append(peca)
        digitos = apenas_digitos("".join(atual))
        proxima = apenas_digitos(pecas[i + 1]) if i + 1 < len(pecas) else ""
        completo = len(normalizar_digitos(digitos)) >= 10
        if completo and (not proxima or len(normalizar_digitos(digitos + proxima)) > 11):
            grupos.append(" ".join(atual))
            atual = []
    if atual:
        grupos.append(" ".join(atual))
    return grupos
