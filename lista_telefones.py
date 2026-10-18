# -*- coding: utf-8 -*-
"""
LISTA DE TELEFONES
================================================================================
Lista em memória exibida como linhas com botão de remover (✕).
Os itens são guardados como "📞 (XX) XXXXX-XXXX" (celular) ou
"🏠 (XX) XXXX-XXXX" (fixo).

Todas as linhas ficam visíveis (máximo de 10 telefones) e a rolagem é a da
página — sem uma segunda barra de rolagem aninhada dentro do conteúdo.
"""

import customtkinter as ctk

from temas import cor, fonte

MENSAGEM_VAZIA = "Nenhum telefone adicionado ainda."

ALTURA_LINHA = 36
ESPACO_LINHA = 4

TIPOS = {
    "📞 ": ("📱", "Celular"),
    "🏠 ": ("☎", "Fixo"),
}


def _limpar_emoji(texto):
    """Remove emoji inicial (📞 ou 🏠) do texto exibido."""
    for prefix in TIPOS:
        if texto.startswith(prefix):
            return texto[len(prefix) :].strip()
    return texto.strip()


def _tipo_do_item(texto):
    """Retorna (ícone, rótulo) do tipo do telefone."""
    for prefix, tipo in TIPOS.items():
        if texto.startswith(prefix):
            return tipo
    return ("📞", "Telefone")


def criar_lista_telefones(gui, parent, tema_manager=None):
    """Cria o painel da lista de telefones e registra o estado em gui."""
    gui.telefones = []
    gui.frame_lista_container = ctk.CTkFrame(parent, fg_color="transparent")
    gui.frame_lista_container.pack(fill="x", pady=(10, 0))
    atualizar_lista_telefones(gui, tema_manager)


def atualizar_lista_telefones(gui, tema_manager=None):
    """Redesenha as linhas da lista conforme os dados."""
    for widget in gui.frame_lista_container.winfo_children():
        widget.destroy()

    if hasattr(gui, "ao_mudar_telefones"):
        gui.ao_mudar_telefones()

    if not gui.telefones:
        vazio = ctk.CTkFrame(
            gui.frame_lista_container,
            fg_color=cor("list_row_bg"),
            corner_radius=8,
            height=ALTURA_LINHA,
        )
        vazio.pack(fill="x")
        ctk.CTkLabel(
            vazio,
            text=MENSAGEM_VAZIA,
            font=fonte(12),
            text_color=cor("fg_muted"),
            anchor="w",
        ).pack(fill="x", padx=12, pady=6)
        return

    for indice, texto in enumerate(gui.telefones):
        _criar_linha(gui, gui.frame_lista_container, indice, texto, tema_manager)


def _criar_linha(gui, parent, indice, texto, tema_manager):
    icone, rotulo = _tipo_do_item(texto)

    linha = ctk.CTkFrame(parent, fg_color=cor("list_row_bg"), corner_radius=8, height=ALTURA_LINHA)
    linha.pack(fill="x", pady=(0, ESPACO_LINHA))
    linha.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(linha, text=icone, font=fonte(14), text_color=cor("fg"), width=24).grid(
        row=0, column=0, padx=(10, 6), pady=4
    )
    ctk.CTkLabel(
        linha, text=_limpar_emoji(texto), font=fonte(13), text_color=cor("fg"), anchor="w"
    ).grid(row=0, column=1, sticky="ew")
    ctk.CTkLabel(linha, text=rotulo, font=fonte(12), text_color=cor("fg_muted")).grid(
        row=0, column=2, padx=8
    )
    ctk.CTkButton(
        linha,
        text="✕",
        width=28,
        height=28,
        corner_radius=6,
        font=fonte(13),
        fg_color="transparent",
        hover_color=cor("list_remove_hover"),
        text_color=cor("fg_muted"),
        command=lambda i=indice: gui.remover_telefone(i),
    ).grid(row=0, column=3, padx=(0, 4), pady=4)


def adicionar_telefone_lista(gui, texto, tema_manager=None):
    """Adiciona item e atualiza a lista."""
    gui.telefones.append(texto)
    atualizar_lista_telefones(gui, tema_manager)


def remover_telefone_indice(gui, indice, tema_manager=None):
    """
    Remove o item da posição informada.
    Retorna o texto removido ou None se o índice for inválido.
    """
    if indice is None or not 0 <= indice < len(gui.telefones):
        return None
    removido = gui.telefones.pop(indice)
    atualizar_lista_telefones(gui, tema_manager)
    return removido


def limpar_lista_telefones(gui, tema_manager=None):
    """Remove todos os telefones da lista."""
    gui.telefones.clear()
    atualizar_lista_telefones(gui, tema_manager)


def obter_todos_telefones_da_lista(gui):
    """Retorna números formatados sem emoji."""
    return [_limpar_emoji(item) for item in gui.telefones]
