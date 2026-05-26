# -*- coding: utf-8 -*-
"""
MÓDULO DE EVENTOS
================================================================================
Funções de evento para a interface gráfica (adicionar, remover, limpar).
"""

from datetime import datetime
from tkinter import messagebox
from telefones import formatar_celular, formatar_fixo
from lista_telefones import (
    adicionar_telefone_lista,
    remover_telefone_selecionado,
    limpar_lista_telefones,
    obter_todos_telefones_da_lista,
)

MENSAGEM_PRONTA = "Pronto para gerar e-mail"


def mostrar_mensagem_temporaria(gui, mensagem, cor="green"):
    """Mostra uma mensagem temporária que desaparece após 2 segundos."""
    if gui.timer_mensagem:
        gui.janela.after_cancel(gui.timer_mensagem)

    cor_hex = gui.tema_manager.cor_status(cor)
    gui.status_label.configure(text=mensagem, text_color=cor_hex)

    def limpar_mensagem():
        cores = gui.tema_manager.tema_atual
        from temas import CORES
        gui.status_label.configure(
            text=MENSAGEM_PRONTA,
            text_color=CORES[cores]["status_ok"],
        )
        gui.timer_mensagem = None

    gui.timer_mensagem = gui.janela.after(2000, limpar_mensagem)


def adicionar_celular(gui):
    """Adiciona celular à lista."""
    telefone = gui.entry_telefone.get().strip()
    if telefone:
        telefone_formatado = formatar_celular(telefone)
        adicionar_telefone_lista(gui, f"📞 {telefone_formatado}", gui.tema_manager)
        gui.entry_telefone.delete(0, "end")
        mostrar_mensagem_temporaria(gui, f"Celular adicionado: {telefone_formatado}", "green")
    else:
        messagebox.showwarning("Aviso", "Digite um número de telefone!")


def adicionar_fixo(gui):
    """Adiciona telefone fixo à lista."""
    telefone = gui.entry_telefone.get().strip()
    if telefone:
        telefone_formatado = formatar_fixo(telefone)
        adicionar_telefone_lista(gui, f"🏠 {telefone_formatado}", gui.tema_manager)
        gui.entry_telefone.delete(0, "end")
        mostrar_mensagem_temporaria(gui, f"Telefone fixo adicionado: {telefone_formatado}", "green")
    else:
        messagebox.showwarning("Aviso", "Digite um número de telefone!")


def remover_telefone(gui):
    """Remove telefone selecionado da lista."""
    removido = remover_telefone_selecionado(gui, gui.tema_manager)
    if removido:
        mostrar_mensagem_temporaria(gui, f"Telefone removido: {removido}", "orange")
    else:
        messagebox.showwarning("Aviso", "Selecione um telefone para remover!")


def limpar_listas(gui):
    """Limpa apenas as listas de telefones."""
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
    gui.entry_nome.insert(0, "Josué B. Almeida")
    hoje = datetime.now()
    gui.spin_dia.set(f"{hoje.day:02d}")
    gui.spin_mes.set(f"{hoje.month:02d}")
    gui.spin_ano.set(str(hoje.year))
    gui.spin_hora.set(f"{hoje.hour:02d}")
    gui.spin_minuto.set(f"{hoje.minute:02d}")
    gui.tipo_email.set("1")
    gui.seg_tipo.set("1º Aviso")
    gui.tema_manager.atualizar_segmented(gui.seg_tipo)
    gui.feedback_label.configure(text="Opção escolhida: 1º Aviso")
    mostrar_mensagem_temporaria(gui, "Formulário limpo! Pronto para novo e-mail.", "green")
    messagebox.showinfo("Novo E-mail", "Formulário limpo! Preencha os dados para um novo e-mail.")
