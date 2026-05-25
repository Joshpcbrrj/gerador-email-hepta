# -*- coding: utf-8 -*-
"""
================================================================================
INTERFACE GRÁFICA - GERADOR DE E-MAILS HEPTA
================================================================================

Versão com CustomTkinter, layout desktop e lista estilo ListView.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import tkinter as tk
import customtkinter as ctk
import webbrowser

from config import VERSAO_ATUAL
from tema_manager import TemaManager
from widgets import criar_widgets
from eventos import (
    adicionar_celular,
    adicionar_fixo,
    remover_telefone,
    limpar_listas,
    limpar_tudo,
    obter_todos_telefones,
    MENSAGEM_PRONTA,
)
from geracao_email import gerar_email, limpar_pasta_temp
from atualizacao import verificar_atualizacao


class GeradorEmailGUI:
    """Classe principal da interface gráfica"""

    def __init__(self):
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.janela = ctk.CTk()
        self.janela.title("Gerador de E-mails - Suporte Hepta")
        self.janela.geometry("960x640")
        self.janela.resizable(True, True)
        self.janela.minsize(640, 480)
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_programa)

        self.tema_manager = TemaManager(self)
        self.tipo_email = tk.StringVar(value="1")
        self.timer_mensagem = None

        funcoes = {
            "adicionar_celular": lambda: adicionar_celular(self),
            "adicionar_fixo": lambda: adicionar_fixo(self),
            "remover_telefone": lambda: remover_telefone(self),
            "limpar_listas": lambda: limpar_listas(self),
            "limpar_tudo": lambda: limpar_tudo(self),
            "gerar_email": lambda: gerar_email(self, obter_todos_telefones),
            "verificar_atualizacao": self.verificar_atualizacao_manual,
            "alternar_tema": self.alternar_tema,
        }

        criar_widgets(self, self.tema_manager, funcoes)
        self.tema_manager.aplicar_tema()

        self.github_link.bind(
            "<Button-1>",
            lambda e: webbrowser.open("https://github.com/Joshpcbrrj/gerador-email-hepta"),
        )
        self.linkedin_link.bind(
            "<Button-1>",
            lambda e: webbrowser.open("https://www.linkedin.com/in/josualmeida/"),
        )

    def mostrar_mensagem_temporaria(self, mensagem, cor="green"):
        """Mostra uma mensagem temporária que desaparece após 2 segundos."""
        if self.timer_mensagem:
            self.janela.after_cancel(self.timer_mensagem)

        self.status_label.configure(text=mensagem, text_color=self.tema_manager.cor_status(cor))

        def limpar_mensagem():
            from temas import CORES
            self.status_label.configure(
                text=MENSAGEM_PRONTA,
                text_color=CORES[self.tema_manager.tema_atual]["status_ok"],
            )
            self.timer_mensagem = None

        self.timer_mensagem = self.janela.after(3000, limpar_mensagem)

    def alternar_tema(self, tema_manager):
        """Alterna entre tema claro e escuro."""
        novo_tema = tema_manager.alternar_tema()
        if novo_tema == "escuro":
            self.mostrar_mensagem_temporaria("Tema escuro ativado!", "white")
        else:
            self.mostrar_mensagem_temporaria("Tema claro ativado!", "black")

    def atualizar_status(self, mensagem, cor="green"):
        """Atualiza a mensagem de status (mantém visível)."""
        if self.timer_mensagem:
            self.janela.after_cancel(self.timer_mensagem)
        self.status_label.configure(
            text=mensagem, text_color=self.tema_manager.cor_status(cor)
        )

    def verificar_atualizacao_manual(self):
        """Verifica atualizações manualmente."""
        self.mostrar_mensagem_temporaria("Verificando atualizações...", "blue")

        def apos_verificacao():
            self.mostrar_mensagem_temporaria(
                "Você está usando a versão mais recente!", "green"
            )

        verificar_atualizacao(self.janela, apos_verificacao)

    def fechar_programa(self):
        """Fecha o programa e limpa arquivos temporários."""
        limpar_pasta_temp()
        self.janela.destroy()

    def executar(self):
        """Inicia a interface gráfica."""
        self.janela.mainloop()


if __name__ == "__main__":
    app = GeradorEmailGUI()
    app.executar()
