# -*- coding: utf-8 -*-
"""
MÓDULO DE EVENTOS
================================================================================
Funções de evento para a interface gráfica (adicionar, remover, limpar).
"""

from tkinter import messagebox

from config import MAX_TELEFONES
from lista_telefones import (
    adicionar_telefone_lista,
    limpar_lista_telefones,
    obter_todos_telefones_da_lista,
    remover_telefone_indice,
)
from telefones import formatar_celular, formatar_fixo

MENSAGEM_PRONTA = "Pronto para gerar e-mail"


def mostrar_mensagem_temporaria(gui, mensagem, cor="green", duracao_ms=3000):
    """Mostra uma mensagem na barra de status que volta ao padrão depois de alguns segundos."""
    if gui.timer_mensagem:
        gui.janela.after_cancel(gui.timer_mensagem)

    gui.status_label.configure(text=mensagem, text_color=gui.tema_manager.cor_status(cor))

    def limpar_mensagem():
        gui.status_label.configure(
            text=MENSAGEM_PRONTA,
            text_color=gui.tema_manager.cor_status("green"),
        )
        gui.timer_mensagem = None

    gui.timer_mensagem = gui.janela.after(duracao_ms, limpar_mensagem)


def _adicionar(gui, formatar, emoji, descricao):
    telefone = gui.entry_telefone.get().strip()
    if not telefone:
        messagebox.showwarning("Aviso", "Digite um número de telefone!")
        return
    if len(gui.telefones) >= MAX_TELEFONES:
        messagebox.showwarning("Aviso", f"O limite é de {MAX_TELEFONES} telefones por chamado.")
        return

    telefone_formatado = formatar(telefone)
    adicionar_telefone_lista(gui, f"{emoji} {telefone_formatado}", gui.tema_manager)
    gui.entry_telefone.delete(0, "end")
    mostrar_mensagem_temporaria(gui, f"{descricao} adicionado: {telefone_formatado}", "green")


def adicionar_celular(gui):
    """Adiciona celular à lista."""
    _adicionar(gui, formatar_celular, "📞", "Celular")


def adicionar_fixo(gui):
    """Adiciona telefone fixo à lista."""
    _adicionar(gui, formatar_fixo, "🏠", "Telefone fixo")


def remover_telefone(gui, indice):
    """Remove o telefone da posição informada (botão ✕ da linha)."""
    removido = remover_telefone_indice(gui, indice, gui.tema_manager)
    if removido:
        mostrar_mensagem_temporaria(gui, f"Telefone removido: {removido}", "orange")


def limpar_listas(gui):
    """Limpa apenas a lista de telefones."""
    limpar_lista_telefones(gui, gui.tema_manager)
    gui.entry_telefone.delete(0, "end")
    mostrar_mensagem_temporaria(gui, "Lista de telefones limpa!", "orange")


def obter_todos_telefones(gui):
    """Retorna lista com todos os telefones (sem emoji)."""
    return obter_todos_telefones_da_lista(gui)


def limpar_tudo(gui):
    """Limpa TODO o formulário para um novo e-mail."""
    gui.entry_req.delete(0, "end")
    limpar_lista_telefones(gui, gui.tema_manager)
    gui.entry_telefone.delete(0, "end")
    gui.entry_nome.delete(0, "end")
    gui.entry_nome.insert(0, gui.funcionario_salvo())
    gui.ativar_horario_automatico()
    gui.selecionar_tipo("1")
    gui.entry_req.focus_set()
    mostrar_mensagem_temporaria(gui, "Formulário limpo! Pronto para um novo e-mail.", "green")
