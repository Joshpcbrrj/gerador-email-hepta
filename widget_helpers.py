# -*- coding: utf-8 -*-
"""
FUNÇÕES AUXILIARES PARA CRIAÇÃO DE WIDGETS (CUSTOMTKINTER)
================================================================================
Componentes padronizados (cartões, campos, botões) com as cores do tema.
"""

import customtkinter as ctk
from datetime import datetime
from temas import cor, fonte


# ============================================================================
# CARTÕES E TEXTOS
# ============================================================================

def criar_secao(parent, titulo, descricao=None):
    """
    Cria um cartão (seção) com título e retorna o frame de conteúdo.
    O label do título fica acessível em conteudo.label_titulo.
    """
    cartao = ctk.CTkFrame(
        parent,
        fg_color=cor("frame_bg"),
        border_color=cor("border"),
        border_width=1,
        corner_radius=12,
    )
    cartao.pack(fill="x", pady=(0, 12))

    label_titulo = ctk.CTkLabel(
        cartao, text=titulo, font=fonte(14, "bold"), text_color=cor("fg"), anchor="w"
    )
    label_titulo.pack(fill="x", padx=16, pady=(12, 0 if descricao else 8))

    if descricao:
        label_desc = ctk.CTkLabel(
            cartao, text=descricao, font=fonte(12), text_color=cor("fg_muted"), anchor="w"
        )
        label_desc.pack(fill="x", padx=16, pady=(0, 8))

    conteudo = ctk.CTkFrame(cartao, fg_color="transparent")
    conteudo.pack(fill="x", padx=16, pady=(0, 14))
    conteudo.label_titulo = label_titulo
    return conteudo


def criar_label(parent, texto, tamanho=13, peso="normal", muted=False, **kwargs):
    """Label padrão (fundo transparente, cor de texto do tema)."""
    return ctk.CTkLabel(
        parent,
        text=texto,
        font=fonte(tamanho, peso),
        text_color=cor("fg_muted" if muted else "fg"),
        fg_color="transparent",
        **kwargs,
    )


def criar_entry(parent, placeholder="", **kwargs):
    """Campo de texto padrão."""
    return ctk.CTkEntry(
        parent,
        font=fonte(13),
        height=36,
        corner_radius=8,
        border_width=1,
        fg_color=cor("entry_bg"),
        border_color=cor("entry_border"),
        text_color=cor("fg"),
        placeholder_text=placeholder,
        placeholder_text_color=cor("fg_muted"),
        **kwargs,
    )


def criar_campo(parent, rotulo, placeholder=""):
    """Campo com rótulo acima. Retorna o frame (para posicionar) e o entry."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    criar_label(frame, rotulo, 12, "bold", muted=True, anchor="w").pack(fill="x", pady=(0, 4))
    entry = criar_entry(frame, placeholder)
    entry.pack(fill="x")
    return frame, entry


# ============================================================================
# BOTÕES
# ============================================================================

ESTILOS_BOTAO = {
    "primario": ("primary", "primary_hover", "primary_fg"),
    "secundario": ("sec_bg", "sec_hover", "sec_fg"),
}


def criar_botao(parent, texto, comando, estilo="secundario", altura=36, tamanho=13, **kwargs):
    """Botão padrão: 'primario' (ação principal) ou 'secundario'."""
    fundo, hover, texto_cor = ESTILOS_BOTAO[estilo]
    return ctk.CTkButton(
        parent,
        text=texto,
        command=comando,
        height=altura,
        corner_radius=8,
        font=fonte(tamanho, "bold" if estilo == "primario" else "normal"),
        fg_color=cor(fundo),
        hover_color=cor(hover),
        text_color=cor(texto_cor),
        **kwargs,
    )


def aplicar_estilo_botao(botao, estilo):
    """Troca o estilo de um botão já criado (usado no seletor de tipo)."""
    fundo, hover, texto_cor = ESTILOS_BOTAO[estilo]
    botao.configure(fg_color=cor(fundo), hover_color=cor(hover), text_color=cor(texto_cor))


# ============================================================================
# TELEFONE
# ============================================================================

def criar_linha_entrada_telefone(parent, funcoes):
    """Entrada de telefone com botões Celular e Fixo."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x")
    frame.grid_columnconfigure(0, weight=1)

    entry = criar_entry(frame, "Digite o número com DDD (Enter adiciona como celular)")
    entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
    entry.bind("<Return>", lambda e: funcoes["adicionar_celular"]())

    btn_celular = criar_botao(frame, "📱 Celular", funcoes["adicionar_celular"], width=110)
    btn_celular.grid(row=0, column=1, padx=(0, 6))

    btn_fixo = criar_botao(frame, "☎ Fixo", funcoes["adicionar_fixo"], width=90)
    btn_fixo.grid(row=0, column=2)

    return entry, btn_celular, btn_fixo


# ============================================================================
# DATA E HORA
# ============================================================================

def valores_ano(referencia=None):
    """Anos disponíveis: anterior, atual e próximo."""
    ano = (referencia or datetime.now()).year
    return [str(ano - 1), str(ano), str(ano + 1)]


def criar_combobox(parent, valores, largura, ao_escolher):
    """Combo somente-leitura com as cores do tema."""
    return ctk.CTkComboBox(
        parent,
        values=valores,
        width=largura,
        height=34,
        corner_radius=8,
        border_width=1,
        font=fonte(13),
        dropdown_font=fonte(13),
        state="readonly",
        fg_color=cor("entry_bg"),
        border_color=cor("entry_border"),
        button_color=cor("sec_bg"),
        button_hover_color=cor("sec_hover"),
        text_color=cor("fg"),
        dropdown_fg_color=cor("frame_bg"),
        dropdown_hover_color=cor("sec_hover"),
        dropdown_text_color=cor("fg"),
        command=lambda _valor: ao_escolher(),
    )


def criar_linha_horario(parent, ao_escolher_manual):
    """
    Combos de data (dia/mês/ano) e horário (hora:minuto).
    ao_escolher_manual é chamado quando o usuário escolhe um valor.
    """
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", pady=(8, 0))

    dias = [f"{d:02d}" for d in range(1, 32)]
    meses = [f"{m:02d}" for m in range(1, 13)]
    horas = [f"{h:02d}" for h in range(24)]
    minutos = [f"{m:02d}" for m in range(60)]

    criar_label(frame, "Data", 12, "bold", muted=True).pack(side="left", padx=(0, 8))
    spin_dia = criar_combobox(frame, dias, 68, ao_escolher_manual)
    spin_dia.pack(side="left")
    criar_label(frame, "/", muted=True).pack(side="left", padx=4)
    spin_mes = criar_combobox(frame, meses, 68, ao_escolher_manual)
    spin_mes.pack(side="left")
    criar_label(frame, "/", muted=True).pack(side="left", padx=4)
    spin_ano = criar_combobox(frame, valores_ano(), 84, ao_escolher_manual)
    spin_ano.pack(side="left", padx=(0, 24))

    criar_label(frame, "Hora", 12, "bold", muted=True).pack(side="left", padx=(0, 8))
    spin_hora = criar_combobox(frame, horas, 68, ao_escolher_manual)
    spin_hora.pack(side="left")
    criar_label(frame, ":", muted=True).pack(side="left", padx=4)
    spin_minuto = criar_combobox(frame, minutos, 68, ao_escolher_manual)
    spin_minuto.pack(side="left")

    preencher_horario(spin_dia, spin_mes, spin_ano, spin_hora, spin_minuto)
    return spin_dia, spin_mes, spin_ano, spin_hora, spin_minuto


def preencher_horario(spin_dia, spin_mes, spin_ano, spin_hora, spin_minuto, momento=None):
    """Preenche os combos com a data/hora informada (padrão: agora)."""
    momento = momento or datetime.now()
    if str(momento.year) not in spin_ano.cget("values"):
        spin_ano.configure(values=valores_ano(momento))
    spin_dia.set(f"{momento.day:02d}")
    spin_mes.set(f"{momento.month:02d}")
    spin_ano.set(str(momento.year))
    spin_hora.set(f"{momento.hour:02d}")
    spin_minuto.set(f"{momento.minute:02d}")
