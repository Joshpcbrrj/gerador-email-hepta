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
from telefones import (
    apenas_digitos,
    eh_celular,
    extrair_telefones,
    formatar_celular,
    formatar_fixo,
    normalizar_digitos,
    validar_telefone,
)

MENSAGEM_PRONTA = "Pronto para gerar e-mail"
EMOJI_CELULAR, EMOJI_FIXO = "📞", "🏠"


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


def _adicionar(gui, celular):
    """
    Adiciona o que foi digitado no campo de telefone.

    - Um número: valida e formata como celular ou fixo, conforme o botão.
    - Vários números colados de uma vez: adiciona todos, reconhecendo
      sozinho se cada um é celular ou fixo.
    """
    texto = gui.entry_telefone.get().strip()
    if not texto:
        messagebox.showwarning("Aviso", "Digite um número de telefone!")
        return
    if len(gui.telefones) >= MAX_TELEFONES:
        messagebox.showwarning("Aviso", f"O limite é de {MAX_TELEFONES} telefones por chamado.")
        return

    trechos = extrair_telefones(texto)
    if len(trechos) > 1:
        _adicionar_varios(gui, trechos)
        return

    digitos = normalizar_digitos(apenas_digitos(texto))
    problema = validar_telefone(digitos)
    if problema:
        messagebox.showwarning("Telefone inválido", f"{texto}\n\n{problema}")
        return

    formatado = formatar_celular(digitos) if celular else formatar_fixo(digitos)
    if formatado in obter_todos_telefones_da_lista(gui):
        gui.entry_telefone.delete(0, "end")  # nada a corrigir: o número já está na lista
        messagebox.showwarning("Telefone repetido", f"{formatado} já está na lista.")
        return

    emoji, descricao = (EMOJI_CELULAR, "Celular") if celular else (EMOJI_FIXO, "Telefone fixo")
    adicionar_telefone_lista(gui, f"{emoji} {formatado}", gui.tema_manager)
    gui.entry_telefone.delete(0, "end")
    mostrar_mensagem_temporaria(gui, f"{descricao} adicionado: {formatado}", "green")


def _adicionar_varios(gui, trechos):
    """Adiciona vários números de uma vez e informa os que ficaram de fora."""
    adicionados, ignorados = [], []
    for trecho in trechos:
        digitos = normalizar_digitos(apenas_digitos(trecho))
        if validar_telefone(digitos):
            ignorados.append(f"{trecho} (inválido)")
            continue
        celular = eh_celular(digitos)
        formatado = formatar_celular(digitos) if celular else formatar_fixo(digitos)
        if formatado in obter_todos_telefones_da_lista(gui):
            ignorados.append(f"{formatado} (repetido)")
            continue
        if len(gui.telefones) >= MAX_TELEFONES:
            ignorados.append(f"{formatado} (limite de {MAX_TELEFONES})")
            continue
        emoji = EMOJI_CELULAR if celular else EMOJI_FIXO
        adicionar_telefone_lista(gui, f"{emoji} {formatado}", gui.tema_manager)
        adicionados.append(formatado)

    if adicionados:
        gui.entry_telefone.delete(0, "end")
        mostrar_mensagem_temporaria(gui, f"{len(adicionados)} telefone(s) adicionado(s).", "green")
    if ignorados:
        messagebox.showwarning(
            "Alguns números não foram adicionados",
            "Não adicionados:\n\n" + "\n".join(ignorados),
        )


def adicionar_celular(gui):
    """Adiciona celular à lista (ou vários números colados de uma vez)."""
    _adicionar(gui, celular=True)


def adicionar_fixo(gui):
    """Adiciona telefone fixo à lista (ou vários números colados de uma vez)."""
    _adicionar(gui, celular=False)


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
