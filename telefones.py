# -*- coding: utf-8 -*-
"""
FUNCOES PARA FORMATACAO DE TELEFONES
================================================================================
Este modulo e responsavel por:
1. Coletar numeros de telefone do usuario
2. Formatar numeros no padrao brasileiro (XX) XXXXX-XXXX
3. Organizar multiplos telefones para exibicao no e-mail

Autor: Josue B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import re


# ============================================================================
# FORMATACAO DE TELEFONE INDIVIDUAL
# ============================================================================

def formatar_celular(telefone_str):
    """
    Formata número de telefone CELULAR no padrão (XX) 9XXXX-XXXX
    
    Exemplos:
    - "21979142434" -> "(21) 97914-2434"
    - "119991234567" -> "(11) 99912-3456"
    """
    numeros = re.sub(r'\D', '', telefone_str)
    if len(numeros) >= 10:
        ddd = numeros[:2]
        numero = numeros[2:]
        if len(numero) == 8:
            numero = f"9{numero}"
        if len(numero) == 9:
            numero = f"{numero[:5]}-{numero[5:]}"
        return f"({ddd}) {numero}"
    return telefone_str


def formatar_fixo(telefone_str):
    """
    Formata número de telefone FIXO no padrão (XX) XXXX-XXXX
    
    Exemplos:
    - "2133763562" -> "(21) 3376-3562"
    - "1134313701" -> "(11) 3431-3701"
    """
    numeros = re.sub(r'\D', '', telefone_str)
    if len(numeros) >= 10:
        ddd = numeros[:2]
        numero = numeros[2:]
        if len(numero) == 9 and numero.startswith('9'):
            numero = numero[1:]
        if len(numero) == 8:
            numero = f"{numero[:4]}-{numero[4:]}"
        return f"({ddd}) {numero}"
    return telefone_str


# ============================================================================
# FORMATACAO DE LISTA DE TELEFONES (NOVA FUNÇÃO)
# ============================================================================

def formatar_telefones(telefones):
    """
    Formata lista de telefones para aparecer no texto do e-mail.
    
    EXEMPLOS:
    - 1 telefone:  "(11) 99999-9999"
    - 2 telefones: "(11) 99999-9999 e (21) 98888-8888"
    - 3 telefones: "(11) 99999-9999, (21) 98888-8888 e (31) 97777-7777"
    """
    if len(telefones) == 0:
        return ""
    elif len(telefones) == 1:
        return telefones[0]
    else:
        return ", ".join(telefones[:-1]) + " e " + telefones[-1]


# ============================================================================
# COLETA DE TELEFONES DO USUARIO (para versão terminal)
# ============================================================================

def obter_telefones():
    """
    Interage com o usuario para coletar os numeros de telefone do cliente.
    (Usado na versão terminal - main.py)
    """
    while True:
        try:
            qtd = int(input("Quantos telefones o cliente possui? "))
            if qtd >= 1:
                break
            print("Digite pelo menos 1 telefone.")
        except ValueError:
            print("Digite um numero valido.")
    
    telefones = []
    
    for i in range(qtd):
        print(f"\n--- Telefone {i+1} ---")
        telefone_input = input("Digite o telefone (ex: 119991234567): ").strip()
        
        # Tenta formatar como celular primeiro, depois como fixo
        if len(re.sub(r'\D', '', telefone_input)) >= 11:
            telefone_formatado = formatar_celular(telefone_input)
        else:
            telefone_formatado = formatar_fixo(telefone_input)
        
        telefones.append(telefone_formatado)
        print(f"  -> Formatado como: {telefone_formatado}")
    
    return telefones