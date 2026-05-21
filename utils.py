# -*- coding: utf-8 -*-
"""
================================================================================
UTILIDADES GERAIS
================================================================================

Este modulo contem funcoes utilitarias que sao usadas em todo o programa.
Funcoes auxiliares que nao se encaixam especificamente em nenhuma outra categoria.

Autor: Josue B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import os  # Sistema operacional - para comandos como 'cls' (limpar tela)
import sys  # Sistema - para verificar se esta no Windows e configurar encoding

# ============================================================================
# CONFIGURACAO DO CONSOLE
# ============================================================================

def configurar_console():
    """
    FUNCAO: configurar_console
    ===========================================================================
    Configura o console do Windows para aceitar caracteres acentuados (UTF-8).
    
    POR QUE ISSO E NECESSARIO?
    ===========================================================================
    O PowerShell/CMD do Windows por padrao usa encoding Latin-1 (ISO-8859-1)
    que nao suporta acentos como "c", "a", "e" corretamente.
    
    O comando 'chcp 65001' muda a pagina de codigo para UTF-8.
    '65001' e o codigo do UTF-8 no Windows.
    
    COMO FUNCIONA:
    ===========================================================================
    - sys.platform retorna o sistema operacional
    - 'win32' indica Windows (32 ou 64 bits)
    - os.system() executa um comando no terminal
    - '> nul' esconde a mensagem de saida do comando
    """
    # Verifica se esta no Windows
    if sys.platform == 'win32':
        # chcp = change code page (muda a pagina de codigo)
        # 65001 = UTF-8
        # > nul redireciona a saida para "nada" (esconde a mensagem)
        os.system('chcp 65001 > nul')

def limpar_tela():
    """
    FUNCAO: limpar_tela
    ===========================================================================
    Limpa o console/terminal para deixar a interface mais organizada.
    
    COMO FUNCIONA:
    ===========================================================================
    - No Windows: usa o comando 'cls' (clear screen)
    - No Linux/Mac: usa o comando 'clear'
    
    os.name retorna:
    ===========================================================================
    - 'nt' para Windows (NT = Windows NT, o nucleo do Windows)
    - 'posix' para Linux/Mac (POSIX = Portable Operating System Interface)
    
    EXEMPLO:
    ===========================================================================
    Antes: Tela cheia de texto
    Depois: Tela vazia, apenas o prompt
    """
    # Expressao ternaria: valor_se_verdadeiro if condicao else valor_se_falso
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================================================
# FUNCAO PARA ENCONTRAR ARQUIVOS NO EXECUTAVEL
# ============================================================================

def resource_path(relative_path):
    """
    FUNCAO: resource_path
    ===========================================================================
    Encontra o caminho correto dos arquivos quando o programa e transformado em .exe.
    
    POR QUE ISSO E NECESSARIO?
    ===========================================================================
    Quando voce usa PyInstaller para criar um .exe com --add-data, os arquivos
    (como imagens) sao "embutidos" dentro do executavel.
    
    Na execucao, o PyInstaller extrai esses arquivos para uma pasta TEMPORARIA.
    O caminho dessa pasta e armazenado em sys._MEIPASS.
    
    COMO FUNCIONA:
    ===========================================================================
    - Se for .exe: sys._MEIPASS existe -> usa a pasta temporaria
    - Se for .py: sys._MEIPASS NAO existe -> usa a pasta atual (.)
    
    EXEMPLO:
    ===========================================================================
    resource_path('logo.png')
    
    - Como .py: retorna 'C:\\pasta_do_projeto\\logo.png'
    - Como .exe: retorna 'C:\\Users\\...\\Temp\\_MEI12345\\logo.png'
    
    PARAMETROS:
    ===========================================================================
    relative_path: str - Nome do arquivo (ex: "logo.png", "winvnc.png")
    
    RETORNO:
    ===========================================================================
    str - Caminho completo para o arquivo
    """
    try:
        # Tenta acessar sys._MEIPASS (so existe quando e .exe)
        # O PyInstaller cria esta variavel automaticamente
        base_path = sys._MEIPASS
    except Exception:
        # Se falhou (nao e .exe), usa a pasta atual
        # '.' significa "diretorio atual"
        base_path = os.path.abspath(".")  # . e a pasta atual
    
    # Junta o caminho base com o nome do arquivo
    # Exemplo: "C:\\pasta" + "logo.png" = "C:\\pasta\\logo.png"
    return os.path.join(base_path, relative_path)