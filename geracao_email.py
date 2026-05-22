# -*- coding: utf-8 -*-
"""
MÓDULO DE GERAÇÃO DE E-MAIL
================================================================================
Funções para gerar o e-mail a partir dos dados do formulário.

Versão: Salva em pasta temporária que é limpa ao fechar o programa
"""

import tkinter as tk
from datetime import datetime
import webbrowser
import tempfile
import os
import shutil
from tkinter import messagebox
from email_html import gerar_email_aviso_html, gerar_email_fechamento_html
from telefones import formatar_telefones  # IMPORT ADICIONADO

# ============================================================================
# PASTA TEMPORÁRIA DO PROGRAMA
# ============================================================================
PASTA_TEMP = None

def obter_pasta_temp():
    """Retorna a pasta temporária do programa, criando se não existir"""
    global PASTA_TEMP
    if PASTA_TEMP is None:
        # Criar uma pasta única para este programa
        PASTA_TEMP = os.path.join(tempfile.gettempdir(), "gerador_email_hepta")
        os.makedirs(PASTA_TEMP, exist_ok=True)
    return PASTA_TEMP

def limpar_pasta_temp():
    """Remove todos os arquivos da pasta temporária"""
    global PASTA_TEMP
    if PASTA_TEMP and os.path.exists(PASTA_TEMP):
        try:
            shutil.rmtree(PASTA_TEMP)
            PASTA_TEMP = None
        except Exception as e:
            print(f"Erro ao limpar pasta temporária: {e}")


# ============================================================================
# FUNÇÃO formatar_telefones FOI REMOVIDA DAQUI
# Agora está em telefones.py e é importada acima
# ============================================================================


def gerar_email(gui, obter_telefones_func):
    """
    Gera o e-mail com os dados do formulário e abre no navegador
    
    Parâmetros:
    - gui: instância da classe GeradorEmailGUI
    - obter_telefones_func: função para obter a lista de telefones
    """
    
    # ====================================================================
    # VALIDAÇÃO 1: NÚMERO DA REQUISIÇÃO
    # ====================================================================
    num_req = gui.entry_req.get().strip()
    if not num_req:
        gui.atualizar_status("⚠️ Adicione a REQ para gerar o e-mail!", "orange")
        messagebox.showerror("Erro", "Digite o número da requisição!")
        return
    
    # ====================================================================
    # VALIDAÇÃO 2: TIPO DE E-MAIL e TELEFONES
    # ====================================================================
    tipo = gui.tipo_email.get()
    
    if tipo != '4':  # Só valida telefone se NÃO for fechamento
        telefones = obter_telefones_func(gui)
        
        # Validação: pelo menos um telefone
        if not telefones:
            gui.atualizar_status("⚠️ Adicione pelo menos um telefone!", "orange")
            messagebox.showerror("Erro", "Adicione pelo menos um telefone (celular ou fixo)!")
            return
        
        # VALIDAÇÃO: Limite máximo de 10 telefones
        MAX_TELEFONES = 10
        if len(telefones) > MAX_TELEFONES:
            gui.atualizar_status(f"⚠️ Limite máximo de {MAX_TELEFONES} telefones excedido! (Atual: {len(telefones)})", "orange")
            messagebox.showerror(
                "Erro", 
                f"Você adicionou {len(telefones)} telefones.\n\n"
                f"⚠️ O limite máximo permitido é {MAX_TELEFONES} telefones por chamado.\n\n"
                f"Remova {len(telefones) - MAX_TELEFONES} telefone(s) para continuar."
            )
            return
    
    nome = gui.entry_nome.get().strip()
    if not nome:
        nome = "Josué B. Almeida"
        
    # Monta REQ completo
    if num_req.upper().startswith('REQ'):
        num_req_completo = num_req.upper()
        num_req_num = num_req[3:]
    else:
        num_req_completo = f"REQ{num_req}"
        num_req_num = num_req
    
    # Data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")
    hora = gui.spin_hora.get().zfill(2)
    minuto = gui.spin_minuto.get().zfill(2)
    
    if tipo == '4':
        # ====================================================================
        # E-MAIL DE FECHAMENTO
        # ====================================================================
        data_hora = f"{data_atual} às {datetime.now().strftime('%H:%M')} BRT"
        titulo = f"{num_req_completo} - Chamado Fechado"
        
        html = gerar_email_fechamento_html(titulo, num_req_completo, nome, data_hora)
        
        gui.atualizar_status(f"🔒 E-mail de FECHAMENTO gerado para {num_req_completo}", "blue")
        
    else:
        # ====================================================================
        # E-MAIL DE AVISO (1º, 2º ou 3º)
        # ====================================================================
        telefones = obter_telefones_func(gui)
        telefone_str = formatar_telefones(telefones)  # Agora importada de telefones.py
        tentativa_ordinal = {'1': '1º', '2': '2º', '3': '3º'}[tipo]
        
        data_hora = f"{data_atual} às {hora}:{minuto} BRT"
        titulo = f"{num_req_completo} - {tentativa_ordinal} aviso de tentativa de contato com o cliente"
        
        html = gerar_email_aviso_html(titulo, num_req_completo, nome, telefone_str, data_hora, tipo)
        
        gui.atualizar_status(f"📧 E-mail de {tentativa_ordinal} AVISO gerado para {num_req_completo} às {hora}:{minuto}", "blue")
    
    # ====================================================================
    # SALVAR NA PASTA TEMPORÁRIA E ABRIR
    # ====================================================================
    
    # Obter a pasta temporária do programa
    pasta_temp = obter_pasta_temp()
    nome_arquivo = f"email_{num_req_num}_{tipo}.html"
    caminho_completo = os.path.join(pasta_temp, nome_arquivo)
    
    try:
        # Salvar na pasta temporária
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Abrir no navegador
        webbrowser.open(f'file://{caminho_completo}')
        
        gui.atualizar_status(f"🌐 E-mail aberto no navegador! Pressione Ctrl+A, Ctrl+C, Ctrl+V para copiar.", "blue")
        
    except Exception as e:
        gui.atualizar_status(f"❌ Erro ao abrir e-mail: {str(e)}", "red")
        messagebox.showerror("Erro", f"Não foi possível abrir o e-mail no navegador.\n\nErro: {str(e)}")