# -*- coding: utf-8 -*-
"""
LISTA DE TELEFONES (ESTILO LISTVIEW)
================================================================================
Lista em memória com linhas clicáveis em CustomTkinter.
"""

import customtkinter as ctk
from temas import CORES


MENSAGEM_VAZIA = "Nenhum telefone adicionado."

# Até 3 telefones visíveis; acima disso, scroll interno
LINHAS_VISIVEIS_MAX = 3
ALTURA_LINHA = 28
ESPACO_LINHA = 2
ALTURA_VAZIA = 32
ALTURA_MAXIMA = LINHAS_VISIVEIS_MAX * (ALTURA_LINHA + ESPACO_LINHA) + 4


def _calcular_altura_lista(quantidade):
    """Altura compacta: vazia = uma linha; cresce até o máximo de 3 linhas."""
    if quantidade == 0:
        return ALTURA_VAZIA
    linhas = min(quantidade, LINHAS_VISIVEIS_MAX)
    return min(
        linhas * (ALTURA_LINHA + ESPACO_LINHA) + 4,
        ALTURA_MAXIMA,
    )


def _aplicar_altura_lista(gui, altura):
    """Força a altura do painel (evita expansão do CTkScrollableFrame)."""
    gui.frame_lista_altura.configure(height=altura)
    gui.lista_scroll.configure(height=altura)


def _limpar_emoji(texto):
    """Remove emoji inicial (📞 ou 🏠) do texto exibido."""
    for prefix in ("📞 ", "🏠 "):
        if texto.startswith(prefix):
            return texto[len(prefix) :].strip()
    return texto.strip()


def criar_lista_telefones(gui, parent, tema_manager):
    """
    Cria o painel ListView de telefones e registra estado em gui.
    """
    gui.telefones = []
    gui.indice_selecionado = None

    gui.frame_lista_container = ctk.CTkFrame(parent, fg_color="transparent")
    gui.frame_lista_container.pack(fill="x", pady=(0, 4))
    tema_manager.registrar_widget(gui.frame_lista_container, "ctk_frame_transparent")

    altura_inicial = _calcular_altura_lista(0)
    gui.frame_lista_altura = ctk.CTkFrame(
        gui.frame_lista_container,
        height=altura_inicial,
        fg_color="transparent",
    )
    gui.frame_lista_altura.pack(fill="x")
    gui.frame_lista_altura.pack_propagate(False)

    gui.lista_scroll = ctk.CTkScrollableFrame(
        gui.frame_lista_altura,
        height=altura_inicial,
        fg_color="transparent",
    )
    gui.lista_scroll.pack(fill="both", expand=True)
    tema_manager.registrar_widget(gui.lista_scroll, "ctk_lista_scroll")


def atualizar_lista_telefones(gui, tema_manager):
    """Redesenha as linhas da lista conforme dados e seleção."""
    for widget in gui.lista_scroll.winfo_children():
        widget.destroy()

    _aplicar_altura_lista(gui, _calcular_altura_lista(len(gui.telefones)))

    cores = CORES[tema_manager.tema_atual]

    if not gui.telefones:
        gui.lista_label_vazio = ctk.CTkLabel(
            gui.lista_scroll,
            text=MENSAGEM_VAZIA,
            font=("Arial", 10),
            text_color=cores["list_empty_fg"],
            anchor="w",
        )
        gui.lista_label_vazio.pack(fill="x", padx=4, pady=4)
        return

    for indice, texto in enumerate(gui.telefones):
        selecionado = indice == gui.indice_selecionado
        fg = cores["list_row_selected_bg"] if selecionado else cores["list_row_bg"]
        hover = cores["list_row_hover_bg"]

        linha = ctk.CTkButton(
            gui.lista_scroll,
            text=texto,
            anchor="w",
            height=ALTURA_LINHA,
            corner_radius=6,
            fg_color=fg,
            hover_color=hover,
            text_color=cores["list_row_fg"],
            font=("Arial", 10),
            command=lambda i=indice: selecionar_telefone(gui, i, tema_manager),
        )
        linha.pack(fill="x", padx=2, pady=1)


def selecionar_telefone(gui, indice, tema_manager):
    """Marca a linha clicada como selecionada."""
    gui.indice_selecionado = indice
    atualizar_lista_telefones(gui, tema_manager)


def adicionar_telefone_lista(gui, texto, tema_manager):
    """Adiciona item e atualiza a ListView."""
    gui.telefones.append(texto)
    gui.indice_selecionado = len(gui.telefones) - 1
    atualizar_lista_telefones(gui, tema_manager)


def remover_telefone_selecionado(gui, tema_manager):
    """
    Remove o item selecionado.
    Retorna o texto removido ou None se nada selecionado.
    """
    if gui.indice_selecionado is None or not gui.telefones:
        return None
    removido = gui.telefones.pop(gui.indice_selecionado)
    if gui.telefones:
        gui.indice_selecionado = min(gui.indice_selecionado, len(gui.telefones) - 1)
    else:
        gui.indice_selecionado = None
    atualizar_lista_telefones(gui, tema_manager)
    return removido


def limpar_lista_telefones(gui, tema_manager):
    """Remove todos os telefones da lista."""
    gui.telefones.clear()
    gui.indice_selecionado = None
    atualizar_lista_telefones(gui, tema_manager)


def obter_todos_telefones_da_lista(gui):
    """Retorna números formatados sem emoji."""
    return [_limpar_emoji(item) for item in gui.telefones]
