# -*- coding: utf-8 -*-
"""
================================================================================
FUNCOES PARA FORMATACAO DE TELEFONES
================================================================================

Este modulo e responsavel por:
1. Coletar numeros de telefone do usuario
2. Formatar numeros no padrao brasileiro (XX) XXXXX-XXXX
3. Organizar multiplos telefones para exibicao no e-mail

Autor: Josue B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import re  # Expressoes regulares - para manipular padroes de texto

# ============================================================================
# FORMATACAO DE TELEFONE CELULAR (COM 9 DIGITOS)
# ============================================================================

def formatar_celular(telefone_str):
    """
    FUNCAO: formatar_celular
    ===========================================================================
    Formata um numero de telefone CELULAR no padrao brasileiro: (XX) 9XXXX-XXXX
    
    REGRAS:
    - Deve ter 11 digitos (DDD + 9 + 8 digitos)
    - Adiciona 9 na frente se necessario
    - Sempre adiciona hifen apos o 5º digito do numero
    
    EXEMPLOS:
    - "21979142434" -> "(21) 97914-2434"
    - "11 999123456" -> "(11) 99912-3456"
    """
    # Remove tudo que nao e numero
    numeros = re.sub(r'\D', '', telefone_str)
    
    # Verifica se tem pelo menos 10 digitos (DDD + numero minimo)
    if len(numeros) >= 10:
        # Fatiamento de strings (slicing)
        ddd = numeros[:2]        # Primeiros 2 digitos = DDD
        numero = numeros[2:]      # Restante = numero do telefone
        
        # Se o numero tem 8 digitos (telefone fixo), adiciona 9 na frente
        if len(numero) == 8:
            numero = f"9{numero}"
        
        # Se tem 9 digitos, adiciona hifen apos o 5º digito
        if len(numero) == 9:
            numero = f"{numero[:5]}-{numero[5:]}"
        
        # Retorna no formato padrao com parenteses e espaco
        return f"({ddd}) {numero}"
    else:
        return telefone_str

# ============================================================================
# FORMATACAO DE TELEFONE FIXO (SEM 9 DIGITOS)
# ============================================================================

def formatar_fixo(telefone_str):
    """
    FUNCAO: formatar_fixo
    ===========================================================================
    Formata um numero de telefone FIXO no padrao brasileiro: (XX) XXXX-XXXX
    
    REGRAS:
    - Deve ter 10 digitos (DDD + 8 digitos)
    - Nao adiciona 9 na frente
    - Adiciona hifen apos o 4º digito do numero
    
    EXEMPLOS:
    - "2133763562" -> "(21) 3376-3562"
    - "11 34313701" -> "(11) 3431-3701"
    """
    # Remove tudo que nao e numero
    numeros = re.sub(r'\D', '', telefone_str)
    
    # Verifica se tem pelo menos 10 digitos (DDD + numero minimo)
    if len(numeros) >= 10:
        # Fatiamento de strings (slicing)
        ddd = numeros[:2]        # Primeiros 2 digitos = DDD
        numero = numeros[2:]      # Restante = numero do telefone
        
        # Se o numero tem 9 digitos e comeca com 9 (celular), remove o 9
        if len(numero) == 9 and numero.startswith('9'):
            numero = numero[1:]   # Remove o primeiro digito (9)
        
        # Se tem 8 digitos, adiciona hifen apos o 4º digito
        if len(numero) == 8:
            numero = f"{numero[:4]}-{numero[4:]}"
        
        # Retorna no formato padrao com parenteses e espaco
        return f"({ddd}) {numero}"
    else:
        return telefone_str

# ============================================================================
# COLETA DE TELEFONES DO USUARIO (SEPARADO POR TIPO)
# ============================================================================

def obter_telefones():
    """
    FUNCAO: obter_telefones
    ===========================================================================
    Interage com o usuario para coletar os numeros de telefone do cliente,
    separando entre celulares e telefones fixos.
    
    COMO FUNCIONA:
    ===========================================================================
    1. Pergunta quantos celulares o cliente possui
    2. Para cada celular, pede o numero e formata
    3. Pergunta quantos telefones fixos o cliente possui
    4. Para cada fixo, pede o numero e formata
    5. Retorna a lista completa com todos os telefones
    
    RETORNO:
    ===========================================================================
    list - Lista de strings com os telefones ja formatados
            Exemplo: ["(11) 99999-9999", "(21) 3376-3562"]
    """
    telefones = []
    
    # ========================================================================
    # COLETA DE CELULARES (COM 9 DIGITOS)
    # ========================================================================
    print("\n" + "=" * 60)
    print("📱 TELEFONES CELULAR (com 9 dígitos)")
    print("=" * 60)
    
    while True:
        try:
            qtd_celular = int(input("Quantos celulares o cliente possui? "))
            if qtd_celular >= 0:
                break
            print("Digite um número válido (0 ou mais).")
        except ValueError:
            print("Digite um número válido.")
    
    for i in range(qtd_celular):
        print(f"\n--- Celular {i+1} ---")
        telefone_input = input("Digite o número (ex: 21979142434): ").strip()
        telefone_formatado = formatar_celular(telefone_input)
        telefones.append(telefone_formatado)
        print(f"  -> Formatado como: {telefone_formatado}")
    
    # ========================================================================
    # COLETA DE TELEFONES FIXOS (SEM 9 DIGITOS)
    # ========================================================================
    print("\n" + "=" * 60)
    print("🏠 TELEFONES FIXOS / CONVENCIONAIS (sem 9 na frente)")
    print("=" * 60)
    
    while True:
        try:
            qtd_fixo = int(input("Quantos telefones fixos o cliente possui? "))
            if qtd_fixo >= 0:
                break
            print("Digite um número válido (0 ou mais).")
        except ValueError:
            print("Digite um número válido.")
    
    for i in range(qtd_fixo):
        print(f"\n--- Telefone Fixo {i+1} ---")
        telefone_input = input("Digite o número (ex: 2133763562): ").strip()
        telefone_formatado = formatar_fixo(telefone_input)
        telefones.append(telefone_formatado)
        print(f"  -> Formatado como: {telefone_formatado}")
    
    return telefones

# ============================================================================
# FORMATACAO DE MULTIPLOS TELEFONES PARA O E-MAIL
# ============================================================================

def formatar_telefones(telefones):
    """
    FUNCAO: formatar_telefones
    ===========================================================================
    Formata a lista de telefones para aparecer no texto do e-mail.
    
    EXEMPLOS:
    - 1 telefone:  "(11) 99999-9999"
    - 2 telefones: "(11) 99999-9999 e (21) 98888-8888"
    - 3 telefones: "(11) 99999-9999, (21) 98888-8888 e (31) 97777-7777"
    """
    if len(telefones) == 1:
        return telefones[0]
    else:
        return ", ".join(telefones[:-1]) + " e " + telefones[-1]