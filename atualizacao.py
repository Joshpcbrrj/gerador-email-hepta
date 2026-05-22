# -*- coding: utf-8 -*-
"""
MÓDULO DE AUTO-UPDATE
================================================================================
Gerencia a verificação de atualizações no GitHub.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import json
import urllib.request
import webbrowser
from threading import Thread
from tkinter import messagebox

# Importa as configurações do arquivo config.py
from config import VERSAO_ATUAL, GITHUB_API_URL


def verificar_atualizacao(parent_window, callback=None):
    """
    Verifica se há uma nova versão disponível no GitHub.
    
    Como funciona:
    1. Consulta a API do GitHub para obter a última release
    2. Compara a versão encontrada com a versão atual
    3. Se houver versão nova, pergunta se usuário quer abrir a página de download
    
    Parâmetros:
    - parent_window: janela principal (para exibir o popup)
    - callback: função opcional chamada após a verificação (se estiver atualizado)
    """
    
    def verificar():
        try:
            # Configura a requisição HTTP
            req = urllib.request.Request(GITHUB_API_URL)
            req.add_header('User-Agent', 'GeradorEmailHepta')
            
            # Faz a consulta à API do GitHub (timeout de 5 segundos)
            with urllib.request.urlopen(req, timeout=5) as response:
                dados = json.loads(response.read().decode('utf-8'))
                ultima_versao = dados.get('tag_name', '').replace('v', '')
                release_url = dados.get('html_url', '')
                release_notes = dados.get('body', 'Sem notas de versão disponíveis.')
                
                # Compara a versão encontrada com a versão atual
                if ultima_versao and ultima_versao > VERSAO_ATUAL:
                    # Nova versão encontrada! Mostra popup na thread principal
                    def perguntar():
                        resposta = messagebox.askyesno(
                            "🔄 Atualização Disponível",
                            f"Uma nova versão está disponível!\n\n"
                            f"Versão atual: {VERSAO_ATUAL}\n"
                            f"Nova versão: {ultima_versao}\n\n"
                            f"Notas da versão:\n{release_notes[:200]}...\n\n"
                            f"Deseja abrir a página de download?",
                            parent=parent_window
                        )
                        if resposta:
                            webbrowser.open(release_url)
                    
                    parent_window.after(0, perguntar)
                    
                else:
                    # Está atualizado - chama callback se existir
                    if callback:
                        parent_window.after(0, callback)
                        
        except Exception as e:
            # Erro na verificação (sem internet, API offline, etc.)
            print(f"Erro ao verificar atualização: {e}")
            if callback:
                parent_window.after(0, callback)
    
    # Executa a verificação em uma thread separada para não travar a interface
    thread = Thread(target=verificar)
    thread.daemon = True
    thread.start()