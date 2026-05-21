# -*- coding: utf-8 -*-
"""
================================================================================
PROGRAMA PRINCIPAL - GERADOR DE E-MAILS HEPTA
================================================================================

Este é o ponto de entrada do programa. Ele coordena todos os outros módulos:
- Coleta informações do usuário
- Decide qual tipo de e-mail gerar (aviso ou fechamento)
- Para e-mails de aviso, permite digitar a hora e minutos do contato
- Chama as funções apropriadas para gerar o HTML
- Abre o navegador para o usuário copiar o e-mail

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import os
import sys
from datetime import datetime
import webbrowser

# Importações dos módulos criados
from utils import configurar_console, limpar_tela, resource_path
from telefones import obter_telefones, formatar_telefones
from imagens import verificar_imagens
from email_aviso import gerar_email_aviso_html
from email_fechamento import gerar_email_fechamento_html

# ============================================================================
# FUNÇÃO PARA GERAR E ABRIR O HTML
# ============================================================================

def gerar_e_abrir_html(html_content, num_req, tipo):
    """
    FUNÇÃO: gerar_e_abrir_html
    ===========================================================================
    Salva o conteúdo HTML em um arquivo e abre no navegador padrão.
    
    PARÂMETROS:
    - html_content: str - O código HTML do e-mail
    - num_req: str - Número da requisição (sem REQ, ex: "000008198188")
    - tipo: str - Tipo do e-mail ("1aviso", "2aviso", "3aviso" ou "fechamento")
    
    RETORNO:
    - caminho_html: str - Caminho completo do arquivo gerado
    """
    nome_html = f"email_{num_req}_{tipo}.html"
    caminho_html = os.path.abspath(nome_html)
    
    with open(caminho_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    webbrowser.open(f'file://{caminho_html}')
    return caminho_html

# ============================================================================
# FUNÇÃO PARA OBTER HORA E MINUTOS DO USUÁRIO
# ============================================================================

def obter_horario_contato():
    """
    FUNÇÃO: obter_horario_contato
    ===========================================================================
    Solicita ao usuário a hora e os minutos da tentativa de contato.
    Usada APENAS para e-mails de aviso (opções 1, 2 e 3).
    
    COMO FUNCIONA:
    ===========================================================================
    1. Pede a hora (0-23) - obrigatório
    2. Pede os minutos (0-59) - opcional, padrão é 00
    3. Valida as entradas para evitar valores inválidos
    4. Retorna uma string formatada como "HH:MM"
    
    TRATAMENTO DE ERROS:
    ===========================================================================
    - Se a hora for inválida (não numérica ou fora de 0-23), pede novamente
    - Se os minutos forem inválidos, usa 00 como padrão
    
    RETORNO:
    ===========================================================================
    str - Horário formatado (ex: "14:30" ou "09:00")
    """
    print("\n⏰ HORÁRIO DA TENTATIVA DE CONTATO")
    
    # ========================================================================
    # SOLICITA A HORA (OBRIGATÓRIA)
    # ========================================================================
    while True:
        try:
            hora = input("Digite a hora (0-23): ").strip()
            # Converte para inteiro para validar
            hora_int = int(hora)
            # Verifica se está no intervalo válido (0 a 23)
            if 0 <= hora_int <= 23:
                break  # Sai do loop se for válido
            else:
                print("❌ Hora inválida! Digite um valor entre 0 e 23.")
        except ValueError:
            # Se não for um número inteiro, cai aqui
            print("❌ Valor inválido! Digite um número entre 0 e 23.")
    
    # ========================================================================
    # SOLICITA OS MINUTOS (OPCIONAL, PADRÃO = 00)
    # ========================================================================
    minutos_input = input("Digite os minutos (0-59) [padrão: 00]: ").strip()
    
    if minutos_input == "":
        # Se o usuário não digitou nada, usa 00
        minutos = "00"
    else:
        try:
            minutos_int = int(minutos_input)
            if 0 <= minutos_int <= 59:
                # Formata com dois dígitos (ex: 5 vira "05")
                minutos = f"{minutos_int:02d}"
            else:
                print("⚠️ Minutos inválidos! Usando 00 como padrão.")
                minutos = "00"
        except ValueError:
            print("⚠️ Valor inválido! Usando 00 como padrão.")
            minutos = "00"
    
    # Formata a hora com dois dígitos (ex: 9 vira "09")
    hora_formatada = f"{hora_int:02d}"
    
    # Retorna o horário completo
    return f"{hora_formatada}:{minutos}"

# ============================================================================
# FUNÇÃO PARA OBTER DATA E HORA COMPLETA
# ============================================================================

def obter_data_hora_completa(para_fechamento=False, horario_contato=None):
    """
    FUNÇÃO: obter_data_hora_completa
    ===========================================================================
    Retorna a data e hora formatada para o e-mail.
    
    Para e-mails de AVISO: usa a data atual + horário digitado pelo usuário
    Para e-mails de FECHAMENTO: usa data e hora atual completas
    
    PARÂMETROS:
    ===========================================================================
    - para_fechamento: bool - True se for e-mail de fechamento, False para aviso
    - horario_contato: str - Horário digitado pelo usuário (ex: "14:30")
    
    RETORNO:
    ===========================================================================
    str - Data e hora formatada (ex: "21/05/2026 às 14:30 BRT")
    """
    # Obtém a data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    if para_fechamento:
        # Para fechamento, usa hora atual
        hora_atual = datetime.now().strftime("%H:%M")
        return f"{data_atual} às {hora_atual} BRT"
    else:
        # Para aviso, usa o horário digitado pelo usuário
        return f"{data_atual} às {horario_contato} BRT"

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def gerar_email():
    """
    FUNÇÃO: gerar_email
    ===========================================================================
    Função principal que interage com o usuário e gera o e-mail.
    
    FLUXO DE EXECUÇÃO:
    ===========================================================================
    1. Pergunta o número da requisição
    2. Pergunta o tipo de e-mail (1, 2, 3 ou 4)
    3. Se for AVISO (1,2,3):
       - Pergunta os telefones
       - Pergunta a hora e minutos do contato
       - Pergunta o nome do funcionário
       - Gera o e-mail de aviso com o horário personalizado
    4. Se for FECHAMENTO (4):
       - Pergunta apenas o nome do funcionário
       - Gera o e-mail de fechamento com a hora atual
    
    RETORNO:
    ===========================================================================
    bool - True se o usuário quer gerar outro e-mail, False caso contrário
    """
    print("=" * 60)
    print("GERADOR DE E-MAIL - AVISOS DE TENTATIVA DE CONTATO")
    print("=" * 60)
    
    # ------------------------------------------------------------------------
    # PERGUNTA 1: NÚMERO DA REQUISIÇÃO
    # ------------------------------------------------------------------------
    print("\n1️⃣  NÚMERO DA REQUISIÇÃO")
    num_req_completo = input("Digite a REQ completa (Ex: REQ000008194986): ").strip()
    
    # Verifica se o usuário digitou com ou sem "REQ" na frente
    if num_req_completo.upper().startswith('REQ'):
        num_req = num_req_completo[3:]  # Remove "REQ"
    else:
        num_req = num_req_completo
        num_req_completo = f"REQ{num_req}"  # Adiciona "REQ"
    
    # ------------------------------------------------------------------------
    # PERGUNTA 2: TIPO DE E-MAIL
    # ------------------------------------------------------------------------
    print("\n2️⃣  TIPO DE E-MAIL")
    print("Opções:")
    print("  [1] - 1º aviso de tentativa")
    print("  [2] - 2º aviso de tentativa")
    print("  [3] - 3º aviso de tentativa")
    print("  [4] - Fechamento (após 3 tentativas sem sucesso)")
    
    while True:
        opcao = input("Digite 1, 2, 3 ou 4: ").strip()
        if opcao in ['1', '2', '3', '4']:
            break
        print("Opção inválida.")
    
    # ------------------------------------------------------------------------
    # PROCESSAMENTO BASEADO NA OPÇÃO
    # ------------------------------------------------------------------------
    
    if opcao == '4':
        # ====================================================================
        # E-MAIL DE FECHAMENTO - NÃO PRECISA DE TELEFONES NEM HORÁRIO
        # ====================================================================
        
        print("\n3️⃣  NOME DO FUNCIONÁRIO")
        nome_funcionario = input("Nome (ex: Josué B. Almeida): ").strip()
        if not nome_funcionario:
            nome_funcionario = "Josué B. Almeida"
        
        # Para fechamento, usa data e hora atual
        data_hora_completa = obter_data_hora_completa(para_fechamento=True)
        
        # Gera o e-mail de fechamento
        tipo = "fechamento"
        titulo = f"{num_req_completo} - Chamado Fechado"
        
        print("\n🔧 Gerando e-mail de fechamento...")
        html_email = gerar_email_fechamento_html(
            titulo, num_req_completo, nome_funcionario, data_hora_completa
        )
        
        limpar_tela()
        print("=" * 60)
        print("✅ E-MAIL DE FECHAMENTO GERADO COM SUCESSO!")
        print("=" * 60)
        print(f"\n📧 TÍTULO:\n{titulo}")
        
    else:
        # ====================================================================
        # E-MAIL DE AVISO (1ª, 2ª ou 3ª tentativa) - PRECISA DE TELEFONES E HORÁRIO
        # ====================================================================
        
        # Define os textos baseados na opção
        tentativa_extenso = {'1': 'primeira', '2': 'segunda', '3': 'terceira'}[opcao]
        tentativa_ordinal = {'1': '1º', '2': '2º', '3': '3º'}[opcao]
        tipo = f"{opcao}aviso"
        
        titulo = f"{num_req_completo} - {tentativa_ordinal} aviso de tentativa de contato com o cliente"
        
        # Coleta os telefones
        print("\n3️⃣  TELEFONES PARA CONTATO")
        telefones = obter_telefones()
        telefone_str = formatar_telefones(telefones)
        
        # Coleta o horário do contato (hora e minutos)
        horario_contato = obter_horario_contato()
        
        # Coleta o nome do funcionário
        print("\n4️⃣  NOME DO FUNCIONÁRIO")
        nome_funcionario = input("Nome (ex: Josué B. Almeida): ").strip()
        if not nome_funcionario:
            nome_funcionario = "Josué B. Almeida"
        
        # Monta a data e hora completa (data atual + horário digitado)
        data_hora_completa = obter_data_hora_completa(
            para_fechamento=False, 
            horario_contato=horario_contato
        )
        
        print("\n🔧 Gerando e-mail de aviso...")
        html_email = gerar_email_aviso_html(
            titulo, num_req_completo, nome_funcionario, telefone_str, 
            data_hora_completa, tentativa_extenso
        )
        
        limpar_tela()
        print("=" * 60)
        print("✅ E-MAIL GERADO COM SUCESSO!")
        print("=" * 60)
        print(f"\n📧 TÍTULO:\n{titulo}")
    
    # ------------------------------------------------------------------------
    # ABRE O NAVEGADOR PARA COPIAR (COMUM PARA AMBOS OS TIPOS)
    # ------------------------------------------------------------------------
    
    print("\n🌐 Abrindo e-mail formatado no navegador...")
    caminho = gerar_e_abrir_html(html_email, num_req, tipo)
    
    print(f"\n✅ Arquivo HTML aberto: {caminho}")
    print("\n" + "=" * 50)
    print("🔓 COMO COPIAR O E-MAIL:")
    print("=" * 50)
    print("   1. No navegador, pressione Ctrl+A (seleciona tudo)")
    print("   2. Pressione Ctrl+C (copia)")
    print("   3. Vá para seu e-mail (Outlook/Gmail)")
    print("   4. Pressione Ctrl+V (cola)")
    print("=" * 50)
    
    print("\n🔁 Gerar outro e-mail?")
    return input("Digite 's' para continuar: ").strip().lower() == 's'

# ============================================================================
# PONTO DE ENTRADA PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    """
    BLOCO PRINCIPAL - PONTO DE ENTRADA
    ===========================================================================
    Este bloco só executa se o arquivo for rodado DIRETAMENTE.
    """
    try:
        configurar_console()
        
        print("\n📧 GERADOR DE E-MAILS - SUPORTE HEPTA")
        print("=" * 60)
        
        verificar_imagens()
        
        continuar = True
        while continuar:
            continuar = gerar_email()
            if continuar:
                print("\n" + "=" * 60)
        
        print("\n👋 Programa encerrado!")
        input("\nPressione Enter para sair...")
        
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione Enter para sair...")