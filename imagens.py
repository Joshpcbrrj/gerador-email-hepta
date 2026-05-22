# -*- coding: utf-8 -*-
"""
================================================================================
FUNÇÕES PARA MANIPULAÇÃO DE IMAGENS
================================================================================

Este módulo é responsável por:
1. Converter imagens para formato base64 (embutir no HTML)
2. Verificar se as imagens existem na pasta

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import os
import base64
from utils import resource_path

# ============================================================================
# CONSTANTES COM OS CAMINHOS DAS IMAGENS
# ============================================================================

# Caminho para a imagem do WinVNC (agora dentro da pasta assets)
CAMINHO_WINVNC = os.path.join("assets", "winvnc.png")
# Caminho para a logo (agora dentro da pasta assets)
CAMINHO_LOGO = os.path.join("assets", "logo.png")

# ============================================================================
# CONVERSÃO DE IMAGEM PARA BASE64
# ============================================================================

def imagem_to_base64(caminho_imagem):
    """
    FUNÇÃO: imagem_to_base64
    ===========================================================================
    Converte uma imagem para o formato base64 (texto).
    
    O QUE É BASE64?
    ===========================================================================
    Base64 é um método para representar dados binários (como imagens) como texto.
    Ele converte bytes (0s e 1s) em caracteres ASCII (letras, números, +, /).
    
    POR QUE ISSO É NECESSÁRIO PARA E-MAILS?
    ===========================================================================
    E-mails tradicionais não suportam imagens "soltas" no corpo do texto.
    
    Duas opções para colocar imagens no e-mail:
    1. Anexar a imagem (fica separada do texto)
    2. Embutir a imagem no HTML usando base64 (recomendado para este caso)
    
    COMO FICA A IMAGEM EM BASE64 NO HTML?
    ===========================================================================
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...">
    
    O prefixo "data:image/png;base64," diz ao navegador/cliente de e-mail:
    - "data:" = os dados estão aqui mesmo (não é um link externo)
    - "image/png" = o formato da imagem é PNG
    - "base64" = os dados estão codificados em base64
    - O resto é o texto base64 da imagem
    
    COMO FUNCIONA O CÓDIGO:
    ===========================================================================
    1. Tenta encontrar a imagem na pasta atual (executando como .py)
    2. Se não encontrar, tenta no resource_path (executando como .exe)
    3. Abre a imagem em modo binário ("rb" = read binary)
    4. Lê todos os bytes da imagem (.read())
    5. Converte para base64 (.b64encode())
    6. Decodifica de bytes para string UTF-8 (.decode('utf-8'))
    
    PARÂMETROS:
    ===========================================================================
    caminho_imagem: str - Caminho do arquivo de imagem (ex: "assets/logo.png")
    
    RETORNO:
    ===========================================================================
    str or None - String base64 da imagem, ou None se não encontrou
    """
    try:
        # PRIMEIRA TENTATIVA: procurar no caminho especificado
        if os.path.exists(caminho_imagem):
            with open(caminho_imagem, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        
        # SEGUNDA TENTATIVA: tentar sem a pasta assets (fallback)
        nome_arquivo = os.path.basename(caminho_imagem)
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        
        # TERCEIRA TENTATIVA: procurar via resource_path (para .exe)
        caminho_resource = resource_path(caminho_imagem)
        if os.path.exists(caminho_resource):
            with open(caminho_resource, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        
        # Se não encontrou em lugar nenhum, retorna None
        return None
        
    except Exception as e:
        print(f"Erro ao carregar imagem {caminho_imagem}: {e}")
        return None


def obter_winvnc_base64():
    """
    FUNÇÃO: obter_winvnc_base64
    ===========================================================================
    Retorna a imagem do WinVNC em base64.
    Centraliza o caminho da imagem em um único lugar.
    """
    return imagem_to_base64(CAMINHO_WINVNC)


def obter_logo_base64():
    """
    FUNÇÃO: obter_logo_base64
    ===========================================================================
    Retorna a logo em base64.
    Centraliza o caminho da imagem em um único lugar.
    """
    return imagem_to_base64(CAMINHO_LOGO)


# ============================================================================
# VERIFICAÇÃO DE IMAGENS
# ============================================================================

def verificar_imagens():
    """
    FUNÇÃO: verificar_imagens
    ===========================================================================
    Verifica se as imagens necessárias existem na pasta do programa.
    
    Esta função é chamada no início do programa para informar ao usuário
    se as imagens estão disponíveis ou se faltam arquivos.
    
    COMO FUNCIONA:
    ===========================================================================
    - Usa os.path.exists() para verificar cada imagem
    - Mostra ✅ (verde) se encontrou
    - Mostra ⚠️ ou ❌ (amarelo/vermelho) se não encontrou
    
    QUAIS IMAGENS SÃO VERIFICADAS:
    ===========================================================================
    - winvnc.png: Imagem da janela do WinVNC (necessária para e-mails de aviso)
    - logo.png: Logo da empresa (usada em todos os e-mails)
    
    OBSERVAÇÃO:
    ===========================================================================
    A função não para o programa se faltar imagem, apenas avisa.
    Isso permite gerar e-mails mesmo sem as imagens (só com texto).
    """
    print("\n📁 Verificando imagens:")
    
    # Verifica a imagem do WinVNC
    if os.path.exists(CAMINHO_WINVNC):
        print("  ✅ winvnc.png encontrada em assets/")
    elif os.path.exists("winvnc.png"):
        print("  ✅ winvnc.png encontrada (na raiz)")
    else:
        print("  ⚠️ winvnc.png nao encontrada (so necessaria para avisos)")
    
    # Verifica a logo
    if os.path.exists(CAMINHO_LOGO):
        print("  ✅ logo.png encontrada em assets/")
    elif os.path.exists("logo.png"):
        print("  ✅ logo.png encontrada (na raiz)")
    else:
        print("  ❌ logo.png nao encontrada!")
    
    print()