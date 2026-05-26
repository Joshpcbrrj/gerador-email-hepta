# -*- coding: utf-8 -*-
"""
MÓDULO DE CRIAÇÃO DE WIDGETS
================================================================================
Interface com layout desktop (toolbar + status) e CustomTkinter.
"""

import tkinter as tk
import customtkinter as ctk
from config import VERSAO_ATUAL
from widget_helpers import (
    criar_secao,
    criar_linha_entrada,
    criar_linha_entrada_telefone,
    criar_linha_horario,
    criar_botao_toolbar,
)
from lista_telefones import criar_lista_telefones, atualizar_lista_telefones

MAPA_TIPO_PARA_VALOR = {
    "1º Aviso": "1",
    "2º Aviso": "2",
    "3º Aviso": "3",
    "Fechamento": "4",
}

MAPA_VALOR_PARA_TIPO = {v: k for k, v in MAPA_TIPO_PARA_VALOR.items()}


def criar_widgets(gui, tema_manager, funcoes):
    """Cria todos os elementos da interface gráfica."""

    gui.frame_root = ctk.CTkFrame(gui.janela, fg_color="transparent")
    gui.frame_root.pack(fill="both", expand=True, padx=12, pady=10)
    gui.frame_root.grid_columnconfigure(0, weight=1)
    gui.frame_root.grid_rowconfigure(2, weight=1)
    tema_manager.registrar_widget(gui.frame_root, "ctk_frame_transparent")

    _criar_cabecalho(gui, tema_manager, funcoes)
    _criar_toolbar(gui, tema_manager, funcoes)
    _criar_conteudo(gui, tema_manager, funcoes)
    _criar_status_bar(gui, tema_manager)

    gui.atualizar_lista_telefones = lambda: atualizar_lista_telefones(gui, tema_manager)


def _criar_cabecalho(gui, tema_manager, funcoes):
    gui.frame_header = ctk.CTkFrame(gui.frame_root, fg_color="transparent")
    gui.frame_header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    gui.frame_header.grid_columnconfigure(0, weight=1)
    tema_manager.registrar_widget(gui.frame_header, "ctk_frame_transparent")

    titulo = ctk.CTkLabel(
        gui.frame_header,
        text="Gerador de E-mails — Suporte Hepta",
        font=("Arial", 18, "bold"),
        anchor="w",
    )
    titulo.grid(row=0, column=0, sticky="w")
    tema_manager.registrar_widget(titulo, "ctk_label_header")

    frame_acoes = ctk.CTkFrame(gui.frame_header, fg_color="transparent")
    frame_acoes.grid(row=0, column=1, sticky="e")
    tema_manager.registrar_widget(frame_acoes, "ctk_frame_transparent")

    gui.btn_tema = ctk.CTkButton(
        frame_acoes,
        text="Tema",
        width=90,
        command=lambda: funcoes["alternar_tema"](tema_manager),
        font=("Arial", 10),
        corner_radius=8,
    )
    gui.btn_tema.pack(side="left", padx=(0, 6))
    tema_manager.registrar_widget(gui.btn_tema, "ctk_button", "tema")

    gui.btn_atualizar = ctk.CTkButton(
        frame_acoes,
        text="Update",
        width=90,
        command=funcoes["verificar_atualizacao"],
        font=("Arial", 10),
        corner_radius=8,
    )
    gui.btn_atualizar.pack(side="left")
    tema_manager.registrar_widget(gui.btn_atualizar, "ctk_button", "update")


def _criar_toolbar(gui, tema_manager, funcoes):
    gui.frame_toolbar = ctk.CTkFrame(gui.frame_root, fg_color="transparent")
    gui.frame_toolbar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
    tema_manager.registrar_widget(gui.frame_toolbar, "ctk_frame_transparent")

    criar_botao_toolbar(
        gui.frame_toolbar, "Gerar e-mail", funcoes["gerar_email"], tema_manager, "gerar"
    )
    criar_botao_toolbar(
        gui.frame_toolbar, "Limpar listas", funcoes["limpar_listas"], tema_manager, "limpar"
    )
    criar_botao_toolbar(
        gui.frame_toolbar, "Novo e-mail", funcoes["limpar_tudo"], tema_manager, "novo"
    )


def _criar_conteudo(gui, tema_manager, funcoes):
    gui.frame_conteudo = ctk.CTkScrollableFrame(gui.frame_root, fg_color="transparent")
    gui.frame_conteudo.grid(row=2, column=0, sticky="nsew")
    tema_manager.registrar_widget(gui.frame_conteudo, "ctk_frame_transparent")

    # Requisição
    sec_req = criar_secao(gui.frame_conteudo, "Requisição", tema_manager)
    gui.entry_req = criar_linha_entrada(sec_req, "REQ:", "Ex: 000008198188", tema_manager)

    # Tipo de e-mail
    sec_tipo = criar_secao(gui.frame_conteudo, "Tipo de e-mail", tema_manager)

    def on_tipo_change(valor_label):
        gui.tipo_email.set(MAPA_TIPO_PARA_VALOR[valor_label])
        gui.feedback_label.configure(text=f"Opção escolhida: {valor_label}")
        tema_manager.atualizar_segmented(gui.seg_tipo)

    gui.seg_tipo = ctk.CTkSegmentedButton(
        sec_tipo,
        values=list(MAPA_TIPO_PARA_VALOR.keys()),
        command=on_tipo_change,
        font=("Arial", 10),
        corner_radius=8,
    )
    gui.seg_tipo.set("1º Aviso")
    gui.seg_tipo.pack(fill="x", pady=(0, 6))
    tema_manager.registrar_widget(gui.seg_tipo, "ctk_segmented")

    gui.feedback_label = ctk.CTkLabel(
        sec_tipo,
        text="Opção escolhida: 1º Aviso",
        font=("Arial", 10),
        anchor="w",
    )
    gui.feedback_label.pack(fill="x")
    tema_manager.registrar_widget(gui.feedback_label, "ctk_label_feedback")

    # Telefones
    sec_tel = criar_secao(gui.frame_conteudo, "Telefones", tema_manager)
    gui.entry_telefone, gui.btn_add_cel, gui.btn_add_fixo = criar_linha_entrada_telefone(
        sec_tel, tema_manager, funcoes
    )

    label_lista = ctk.CTkLabel(sec_tel, text="Telefones adicionados:", font=("Arial", 10), anchor="w")
    label_lista.pack(fill="x", pady=(6, 2))
    tema_manager.registrar_widget(label_lista, "ctk_label")

    criar_lista_telefones(gui, sec_tel, tema_manager)

    gui.btn_remover = ctk.CTkButton(
        sec_tel,
        text="Remover selecionado",
        command=funcoes["remover_telefone"],
        font=("Arial", 10, "bold"),
        height=30,
        corner_radius=8,
    )
    gui.btn_remover.pack(fill="x", pady=(6, 0))
    tema_manager.registrar_widget(gui.btn_remover, "ctk_button", "remover")

    # Data, horário e funcionário (empilhados — melhor em notebook)
    sec_horario = criar_secao(gui.frame_conteudo, "Data e horário do contato", tema_manager)
    gui.spin_dia, gui.spin_mes, gui.spin_ano, gui.spin_hora, gui.spin_minuto = criar_linha_horario(sec_horario, tema_manager)

    sec_nome = criar_secao(gui.frame_conteudo, "Funcionário", tema_manager)
    gui.entry_nome = ctk.CTkEntry(sec_nome, font=("Arial", 11))
    gui.entry_nome.pack(fill="x")
    gui.entry_nome.insert(0, "Josué B. Almeida")
    tema_manager.registrar_widget(gui.entry_nome, "ctk_entry")


def _criar_status_bar(gui, tema_manager):
    gui.frame_status = ctk.CTkFrame(gui.frame_root, corner_radius=0)
    gui.frame_status.grid(row=3, column=0, sticky="ew", pady=(10, 0))
    gui.frame_status.grid_columnconfigure(0, weight=1)
    tema_manager.registrar_widget(gui.frame_status, "ctk_frame")

    gui.status_label = ctk.CTkLabel(
        gui.frame_status,
        text="Pronto para gerar e-mail",
        font=("Arial", 10),
        anchor="w",
    )
    gui.status_label.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 2))
    tema_manager.registrar_widget(gui.status_label, "ctk_label_status")

    frame_rodape = ctk.CTkFrame(gui.frame_status, fg_color="transparent")
    frame_rodape.grid(row=1, column=0, sticky="ew", padx=4, pady=(0, 8))
    frame_rodape.grid_columnconfigure(0, weight=1)
    frame_rodape.grid_columnconfigure(1, weight=0)
    frame_rodape.grid_columnconfigure(2, weight=1)
    tema_manager.registrar_widget(frame_rodape, "ctk_frame_transparent")

    frame_centro = ctk.CTkFrame(frame_rodape, fg_color="transparent")
    frame_centro.grid(row=0, column=1)
    tema_manager.registrar_widget(frame_centro, "ctk_frame_transparent")

    creditos_label = ctk.CTkLabel(
        frame_centro,
        text="Criado por: Josué B. Almeida",
        font=("Arial", 9, "bold"),
    )
    creditos_label.pack(side="left", padx=(0, 10))
    tema_manager.registrar_widget(creditos_label, "ctk_label_footer")

    gui.github_link = ctk.CTkLabel(
        frame_centro, text="GitHub", font=("Arial", 10, "bold"), cursor="hand2"
    )
    gui.github_link.pack(side="left", padx=6)
    tema_manager.registrar_widget(gui.github_link, "ctk_label_link")

    sep1 = ctk.CTkLabel(frame_centro, text="|", font=("Arial", 10))
    sep1.pack(side="left")
    tema_manager.registrar_widget(sep1, "ctk_label_footer")

    gui.linkedin_link = ctk.CTkLabel(
        frame_centro, text="LinkedIn", font=("Arial", 10, "bold"), cursor="hand2"
    )
    gui.linkedin_link.pack(side="left", padx=6)
    tema_manager.registrar_widget(gui.linkedin_link, "ctk_label_link")

    sep2 = ctk.CTkLabel(frame_centro, text="|", font=("Arial", 10))
    sep2.pack(side="left", padx=(2, 6))
    tema_manager.registrar_widget(sep2, "ctk_label_footer")

    versao_label = ctk.CTkLabel(
        frame_centro, text=f"v{VERSAO_ATUAL}", font=("Arial", 10, "bold")
    )
    versao_label.pack(side="left")
    tema_manager.registrar_widget(versao_label, "ctk_label_footer")
