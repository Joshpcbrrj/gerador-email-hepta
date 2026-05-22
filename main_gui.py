# -*- coding: utf-8 -*-
"""
================================================================================
INTERFACE GRÁFICA - GERADOR DE E-MAILS HEPTA
================================================================================

Versão refatorada - usa TemaManager para gerenciamento de temas

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import tkinter as tk
import webbrowser

# Importações dos módulos
from config import VERSAO_ATUAL
from tema_manager import TemaManager
from widgets import criar_widgets
from eventos import (adicionar_celular, adicionar_fixo, remover_telefone,
                     limpar_listas, limpar_tudo, obter_todos_telefones)
from geracao_email import gerar_email, limpar_pasta_temp
from atualizacao import verificar_atualizacao


class GeradorEmailGUI:
    """Classe principal da interface gráfica"""
    
    def __init__(self):
        """Inicializa a janela principal"""
        self.janela = tk.Tk()
        self.janela.title("Gerador de E-mails - Suporte Hepta")
        self.janela.geometry("1020x920")  # Aumentado para 1020x920
        self.janela.resizable(False, False)
        self.janela.minsize(950, 800)
        
        # Configurar limpeza ao fechar a janela
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        
        # Inicializar gerenciador de temas
        self.tema_manager = TemaManager(self)
        
        # Variáveis
        self.tipo_email = tk.StringVar(value="1")
        
        # Timer para mensagens temporárias
        self.timer_mensagem = None
        
        # ====================================================================
        # DICIONÁRIO DE FUNÇÕES (callback)
        # ====================================================================
        funcoes = {
            'adicionar_celular': lambda: adicionar_celular(self),
            'adicionar_fixo': lambda: adicionar_fixo(self),
            'remover_telefone': lambda: remover_telefone(self),
            'limpar_listas': lambda: limpar_listas(self),
            'limpar_tudo': lambda: limpar_tudo(self),
            'gerar_email': lambda: gerar_email(self, obter_todos_telefones),
            'verificar_atualizacao': self.verificar_atualizacao_manual,
            'alternar_tema': self.alternar_tema
        }
        
        # Criar widgets (passando o tema_manager)
        criar_widgets(self, self.tema_manager, funcoes)
        
        # Aplicar tema inicial
        self.tema_manager.aplicar_tema()
        
        # Bind dos links do rodapé
        self.github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Joshpcbrrj/gerador-email-hepta"))
        self.linkedin_link.bind("<Button-1>", lambda e: webbrowser.open("https://www.linkedin.com/in/josualmeida/"))
    
    def mostrar_mensagem_temporaria(self, mensagem, cor="green"):
        """Mostra uma mensagem temporária que desaparece após 3 segundos"""
        # Cancelar timer anterior
        if self.timer_mensagem:
            self.janela.after_cancel(self.timer_mensagem)
        
        # Mostrar mensagem
        self.status_label.config(text=mensagem, fg=cor)
        
        # Programar para limpar após 3 segundos
        def limpar_mensagem():
            self.status_label.config(text="✅ Pronto para gerar e-mail", fg="green")
        
        self.timer_mensagem = self.janela.after(3000, limpar_mensagem)
    
    def alternar_tema(self, tema_manager):
        """Alterna entre tema claro e escuro (chamado pelo botão)"""
        novo_tema = tema_manager.alternar_tema()
        
        if novo_tema == "escuro":
            self.mostrar_mensagem_temporaria("🌙 Tema escuro ativado!", "white")
        else:
            self.mostrar_mensagem_temporaria("☀️ Tema claro ativado!", "black")
    
    def atualizar_status(self, mensagem, cor="green"):
        """Atualiza a mensagem de status (mantém visível)"""
        if self.timer_mensagem:
            self.janela.after_cancel(self.timer_mensagem)
        self.status_label.config(text=mensagem, fg=cor)
    
    def verificar_atualizacao_manual(self):
        """Verifica atualizações manualmente (chamado pelo botão)"""
        self.mostrar_mensagem_temporaria("🔍 Verificando atualizações...", "blue")
        
        def apos_verificacao():
            self.mostrar_mensagem_temporaria("✅ Você está usando a versão mais recente!", "green")
        
        verificar_atualizacao(self.janela, apos_verificacao)
    
    def fechar_programa(self):
        """Fecha o programa e limpa arquivos temporários"""
        limpar_pasta_temp()
        self.janela.destroy()
    
    def executar(self):
        """Inicia a interface gráfica"""
        self.janela.mainloop()


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    app = GeradorEmailGUI()
    app.executar()