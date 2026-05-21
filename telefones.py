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
# FORMATACAO DE TELEFONE INDIVIDUAL
# ============================================================================

def formatar_telefone_individual(telefone_str):
    """
    FUNCAO: formatar_telefone_individual
    ===========================================================================
    Formata um numero de telefone no padrao brasileiro: (XX) XXXXX-XXXX
    
    O QUE SAO EXPRESSOES REGULARES (REGEX)?
    ===========================================================================
    Expressoes regulares sao padroes para buscar e substituir texto.
    A funcao re.sub(r'\\D', '', telefone_str) significa:
    - r'\\D' : procure qualquer caractere que NAO seja digito (0-9)
    - O 'r' antes da string significa "raw string" (trata barras como literais)
    
    EXEMPLOS DE ENTRADA E SAIDA:
    ===========================================================================
    Entrada: "21979142434"       -> Saida: "(21) 97914-2434"
    Entrada: "21 979142434"      -> Saida: "(21) 97914-2434"
    Entrada: "119991234567"      -> Saida: "(11) 99912-3456"
    Entrada: "11343137015"       -> Saida: "(11) 34313-7015" (fixo)
    Entrada: "(11) 99999-9999"   -> Saida: "(11) 99999-9999" (ja formatado)
    
    COMO FUNCIONA PASSO A PASSO:
    ===========================================================================
    1. Remove tudo que nao e numero (espacos, tracos, parenteses)
    2. Verifica se tem pelo menos 10 digitos (DDD + numero)
    3. Separa DDD (2 primeiros) e numero (restante)
    4. Se numero tem 8 digitos (telefone fixo antigo), adiciona 9 na frente
    5. Adiciona hifen apos o 5º digito do numero
    6. Retorna no formato (DDD) NUMERO
    """
    # re.sub() = substitute (substituir)
    # r'\\D' = qualquer caractere que NAO e numero
    # '' = substitui por vazio (remove)
    # Exemplo: "(11) 99999-9999" vira "11999999999"
    numeros = re.sub(r'\D', '', telefone_str)
    
    # Verifica se tem pelo menos 10 digitos (DDD + numero minimo)
    # Telefone brasileiro tem DDD (2 digitos) + numero (8 ou 9 digitos) = 10-11 total
    if len(numeros) >= 10:
        # Fatiamento de strings (slicing)
        # [:2] = do inicio ate o indice 2 (excluindo o 2) -> pega os 2 primeiros
        ddd = numeros[:2]        # Exemplo: "21979142434" -> "21"
        
        # [2:] = do indice 2 ate o final -> pega todo o resto
        numero = numeros[2:]      # Exemplo: "21979142434" -> "979142434"
        
        # Se o numero tem 8 digitos (telefone fixo antigo)
        # Exemplo: "34313701" (8 digitos)
        if len(numero) == 8:
            # f-string: formatacao de strings com variaveis
            # Adiciona "9" na frente para virar celular
            numero = f"9{numero}"   # "934313701" (9 digitos)
        
        # Se tem 9 digitos, adiciona hifen apos o 5º digito
        if len(numero) == 9:
            # [:5] = primeiros 5 digitos
            # [5:] = do 5º ate o final
            # Exemplo: "979142434" -> "97914" + "-" + "2434" = "97914-2434"
            numero = f"{numero[:5]}-{numero[5:]}"
        
        # Retorna no formato padrao com parenteses e espaco
        return f"({ddd}) {numero}"
    else:
        # Se nao tem formato valido (menos de 10 digitos), retorna o original
        # Isso evita erros com numeros incompletos
        return telefone_str

# ============================================================================
# COLEÇÃO DE TELEFONES DO USUARIO
# ============================================================================

def obter_telefones():
    """
    FUNCAO: obter_telefones
    ===========================================================================
    Interage com o usuario para coletar os numeros de telefone do cliente.
    
    COMO FUNCIONA:
    ===========================================================================
    1. Pergunta quantos telefones o cliente possui (loop ate resposta valida)
    2. Para cada telefone, pede o numero
    3. Formata cada telefone usando formatar_telefone_individual
    4. Armazena em uma lista
    5. Retorna a lista completa
    
    TRATAMENTO DE ERROS:
    ===========================================================================
    - try/except: captura se o usuario digitar letras em vez de numeros
    - while True: repete ate receber uma resposta valida
    
    ESTRUTURAS USADAS:
    ===========================================================================
    - try/except: captura excecoes (erros)
    - ValueError: erro quando int() recebe texto nao numerico
    - list.append(): adiciona item ao final da lista
    - for loop: repete para cada telefone
    
    RETORNO:
    ===========================================================================
    list - Lista de strings com os telefones ja formatados
            Exemplo: ["(11) 99999-9999", "(21) 98888-8888"]
    """
    while True:
        try:
            # Tenta converter a entrada para numero inteiro
            qtd = int(input("Quantos telefones o cliente possui? "))
            
            # Verifica se e pelo menos 1
            if qtd >= 1:
                break  # Sai do loop se for valido
            print("Digite pelo menos 1 telefone.")
        except ValueError:
            # Se digitar letras ou algo nao-numerico, cai aqui
            print("Digite um numero valido.")
    
    # Lista vazia para armazenar os telefones
    telefones = []
    
    # Loop para coletar cada telefone
    # range(qtd) cria uma sequencia de 0 ate qtd-1
    for i in range(qtd):
        print(f"\n--- Telefone {i+1} ---")
        
        # strip() remove espacos no inicio e fim da string
        telefone_input = input("Digite o telefone (ex: 119991234567): ").strip()
        
        # Formata o telefone usando a funcao anterior
        telefone_formatado = formatar_telefone_individual(telefone_input)
        
        # Adiciona a lista
        telefones.append(telefone_formatado)
        
        # Mostra como ficou formatado (feedback para o usuario)
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
    
    Esta funcao cria uma string legivel com todos os telefones.
    
    EXEMPLOS DE SAIDA:
    ===========================================================================
    - 1 telefone:  "(11) 99999-9999"
    - 2 telefones: "(11) 99999-9999 e (21) 98888-8888"
    - 3 telefones: "(11) 99999-9999, (21) 98888-8888 e (31) 97777-7777"
    
    EXPLICACAO DO CODIGO:
    ===========================================================================
    telefones[:-1]  -> Todos os elementos, exceto o ultimo (slicing)
                      Exemplo: [A, B, C] -> [A, B]
    
    ", ".join()     -> Junta os elementos com virgula e espaco
                      Exemplo: [A, B] -> "A, B"
    
    telefones[-1]   -> O ultimo elemento da lista (indice -1)
                      Exemplo: [A, B, C] -> "C"
    
    PARAMETROS:
    ===========================================================================
    telefones: list - Lista de strings com telefones formatados
    
    RETORNO:
    ===========================================================================
    str - String com todos os telefones formatados para o e-mail
    """
    if len(telefones) == 1:
        # Apenas um telefone, retorna ele direto
        return telefones[0]
    else:
        # Multiplos telefones
        # Exemplo: ["A", "B", "C"] -> "A, B e C"
        # telefones[:-1] pega [A, B]
        # join junta com ", " -> "A, B"
        # adiciona " e " + ultimo -> "A, B e C"
        return ", ".join(telefones[:-1]) + " e " + telefones[-1]