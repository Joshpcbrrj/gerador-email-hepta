# -*- coding: utf-8 -*-
"""
MÓDULO GERENCIADOR DE TEMAS
================================================================================
Alterna entre tema claro e escuro usando o modo de aparência nativo do
CustomTkinter. Como todos os widgets recebem cores em par (claro, escuro),
a troca é feita pelo próprio CustomTkinter, sem repintar widget por widget.

A escolha do tema é lembrada entre execuções.
"""

import customtkinter as ctk

import preferencias
import temas


def carregar_tema_salvo() -> str:
    """Lê o tema salvo ('claro' ou 'escuro'); padrão: 'claro'."""
    tema = preferencias.ler("tema", "claro")
    return tema if tema in temas.CORES else "claro"


def salvar_tema(tema: str) -> None:
    """Salva o tema escolhido (falhas são ignoradas)."""
    preferencias.salvar("tema", tema)


class TemaManager:
    """Gerencia o tema da aplicação."""

    def __init__(self, gui, tema_inicial=None):
        self.gui = gui
        self.tema_atual = tema_inicial or carregar_tema_salvo()

    def aplicar_tema(self):
        """Aplica o tema atual."""
        ctk.set_appearance_mode("Dark" if self.tema_atual == "escuro" else "Light")

    def alternar_tema(self):
        """Alterna entre tema claro e escuro e salva a escolha."""
        self.tema_atual = "escuro" if self.tema_atual == "claro" else "claro"
        self.aplicar_tema()
        salvar_tema(self.tema_atual)
        return self.tema_atual

    def cor_status(self, nome_cor):
        """Retorna a cor (par claro/escuro) para mensagens de status."""
        return temas.cor_status(nome_cor)
