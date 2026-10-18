# -*- coding: utf-8 -*-
"""
MÓDULO GERENCIADOR DE TEMAS
================================================================================
Alterna entre tema claro e escuro usando o modo de aparência nativo do
CustomTkinter. Como todos os widgets recebem cores em par (claro, escuro),
a troca é feita pelo próprio CustomTkinter, sem repintar widget por widget.

A escolha do tema é lembrada entre execuções.
"""

import json
import os

import customtkinter as ctk
import temas

PASTA_PREFERENCIAS = os.path.join(
    os.environ.get("APPDATA") or os.path.expanduser("~"), "GeradorEmailHepta"
)
ARQUIVO_PREFERENCIAS = os.path.join(PASTA_PREFERENCIAS, "preferencias.json")


def carregar_tema_salvo():
    """Lê o tema salvo ('claro' ou 'escuro'); padrão: 'claro'."""
    try:
        with open(ARQUIVO_PREFERENCIAS, encoding="utf-8") as f:
            tema = json.load(f).get("tema")
        return tema if tema in temas.CORES else "claro"
    except (OSError, ValueError, AttributeError):
        return "claro"


def salvar_tema(tema):
    """Salva o tema escolhido (falhas são ignoradas)."""
    try:
        os.makedirs(PASTA_PREFERENCIAS, exist_ok=True)
        with open(ARQUIVO_PREFERENCIAS, "w", encoding="utf-8") as f:
            json.dump({"tema": tema}, f)
    except OSError:
        pass


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
