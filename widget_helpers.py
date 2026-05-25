# -*- coding: utf-8 -*-
"""
FUNÇÕES AUXILIARES PARA CRIAÇÃO DE WIDGETS (CUSTOMTKINTER)
================================================================================
"""

import customtkinter as ctk


def criar_secao(parent, titulo, tema_manager):
    """Cria um bloco de seção com título."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", pady=(0, 8))
    tema_manager.registrar_widget(frame, "ctk_frame_transparent")

    label_titulo = ctk.CTkLabel(
        frame,
        text=titulo,
        font=("Arial", 11, "bold"),
        anchor="w",
    )
    label_titulo.pack(fill="x", pady=(0, 6))
    tema_manager.registrar_widget(label_titulo, "ctk_label_section")

    conteudo = ctk.CTkFrame(frame, corner_radius=10)
    conteudo.pack(fill="x")
    tema_manager.registrar_widget(conteudo, "ctk_section")

    return conteudo


def criar_linha_entrada(parent, label_text, placeholder, tema_manager):
    """Linha com rótulo e CTkEntry."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", pady=5)
    tema_manager.registrar_widget(frame, "ctk_frame_transparent")

    label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 10))
    label.pack(side="left", padx=(0, 8))
    tema_manager.registrar_widget(label, "ctk_label")

    entry = ctk.CTkEntry(frame, font=("Arial", 11), placeholder_text=placeholder)
    entry.pack(side="left", fill="x", expand=True)
    tema_manager.registrar_widget(entry, "ctk_entry")

    return entry


def criar_linha_entrada_telefone(parent, tema_manager, funcoes):
    """Entrada de telefone com botões Celular e Fixo."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", pady=5)
    tema_manager.registrar_widget(frame, "ctk_frame_transparent")

    label = ctk.CTkLabel(frame, text="Número:", font=("Arial", 10))
    label.pack(side="left", padx=(0, 8))
    tema_manager.registrar_widget(label, "ctk_label")

    entry = ctk.CTkEntry(frame, font=("Arial", 11), placeholder_text="Digite o número")
    entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
    tema_manager.registrar_widget(entry, "ctk_entry")
    entry.bind("<Return>", lambda e: funcoes["adicionar_celular"]())

    btn_celular = ctk.CTkButton(
        frame,
        text="Celular",
        width=88,
        command=funcoes["adicionar_celular"],
        font=("Arial", 10, "bold"),
        corner_radius=8,
    )
    btn_celular.pack(side="left", padx=2)
    tema_manager.registrar_widget(btn_celular, "ctk_button", "celular")

    btn_fixo = ctk.CTkButton(
        frame,
        text="Fixo",
        width=72,
        command=funcoes["adicionar_fixo"],
        font=("Arial", 10, "bold"),
        corner_radius=8,
    )
    btn_fixo.pack(side="left", padx=2)
    tema_manager.registrar_widget(btn_fixo, "ctk_button", "fixo")

    return entry, btn_celular, btn_fixo


def criar_linha_horario(parent, tema_manager):
    """Combos de hora e minuto."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", pady=5)
    tema_manager.registrar_widget(frame, "ctk_frame_transparent")

    horas = [f"{h:02d}" for h in range(24)]
    minutos = [f"{m:02d}" for m in range(60)]

    label_hora = ctk.CTkLabel(frame, text="Hora:", font=("Arial", 10))
    label_hora.pack(side="left", padx=(0, 6))
    tema_manager.registrar_widget(label_hora, "ctk_label")

    spin_hora = ctk.CTkComboBox(
        frame, values=horas, width=72, font=("Arial", 11), state="readonly"
    )
    spin_hora.set("14")
    spin_hora.pack(side="left", padx=(0, 12))
    tema_manager.registrar_widget(spin_hora, "ctk_combobox")

    label_min = ctk.CTkLabel(frame, text="Minutos:", font=("Arial", 10))
    label_min.pack(side="left", padx=(0, 6))
    tema_manager.registrar_widget(label_min, "ctk_label")

    spin_minuto = ctk.CTkComboBox(
        frame, values=minutos, width=72, font=("Arial", 11), state="readonly"
    )
    spin_minuto.set("00")
    spin_minuto.pack(side="left")
    tema_manager.registrar_widget(spin_minuto, "ctk_combobox")

    return spin_hora, spin_minuto


def criar_botao_toolbar(parent, texto, comando, tema_manager, papel):
    """Botão da barra de ferramentas."""
    btn = ctk.CTkButton(
        parent,
        text=texto,
        command=comando,
        font=("Arial", 11, "bold"),
        height=36,
        corner_radius=10,
    )
    btn.pack(side="left", expand=True, fill="x", padx=4)
    tema_manager.registrar_widget(btn, "ctk_button", papel)
    return btn
