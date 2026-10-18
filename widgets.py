# -*- coding: utf-8 -*-
"""
MÓDULO DE CRIAÇÃO DE WIDGETS
================================================================================
Layout: aviso de atualização (quando houver) + cabeçalho + barra de ações +
conteúdo rolável em cartões + barra de status.

Todas as cores são pares (claro, escuro) — a troca de tema é automática.
"""

import tkinter as tk

import customtkinter as ctk

from config import MAX_TELEFONES, VERSAO_ATUAL
from lista_telefones import criar_lista_telefones
from temas import cor, fonte
from tipo_email import TipoEmail
from widget_helpers import (
    aplicar_estilo_botao,
    criar_botao,
    criar_campo,
    criar_label,
    criar_linha_entrada_telefone,
    criar_linha_horario,
    criar_secao,
)

TEXTO_HORARIO_AUTOMATICO = (
    "A data e a hora serão as do momento em que você gerar ou copiar o e-mail."
)
TEXTO_HORARIO_MANUAL = (
    "Usando a data e a hora escolhidas acima. Ative a opção para voltar ao horário atual."
)


def criar_widgets(gui, tema_manager, funcoes):
    """Cria todos os elementos da interface gráfica."""

    gui.janela.configure(fg_color=cor("bg"))

    # Criada primeiro para não ser cortada quando a janela encolher
    _criar_status_bar(gui)

    gui.frame_root = ctk.CTkFrame(gui.janela, fg_color="transparent")
    gui.frame_root.pack(fill="both", expand=True, padx=16, pady=12)
    gui.frame_root.grid_columnconfigure(0, weight=1)
    gui.frame_root.grid_rowconfigure(3, weight=1)

    _criar_aviso_atualizacao(gui, funcoes)
    _criar_cabecalho(gui, tema_manager, funcoes)
    _criar_toolbar(gui, funcoes)
    _criar_conteudo(gui, tema_manager, funcoes)


# ============================================================================
# AVISO DE ATUALIZAÇÃO (oculto até existir versão nova)
# ============================================================================


def _criar_aviso_atualizacao(gui, funcoes):
    gui.frame_aviso = ctk.CTkFrame(
        gui.frame_root,
        fg_color=cor("banner_bg"),
        border_color=cor("banner_border"),
        border_width=1,
        corner_radius=10,
    )
    gui.frame_aviso.grid(row=0, column=0, sticky="ew", pady=(0, 10))
    gui.frame_aviso.grid_columnconfigure(0, weight=1)

    gui.label_aviso = ctk.CTkLabel(
        gui.frame_aviso, text="", font=fonte(13), text_color=cor("banner_fg"), anchor="w"
    )
    gui.label_aviso.grid(row=0, column=0, sticky="ew", padx=(14, 8), pady=8)

    criar_botao(
        gui.frame_aviso,
        "Baixar atualização",
        funcoes["baixar_atualizacao"],
        estilo="primario",
        altura=30,
        tamanho=12,
    ).grid(row=0, column=1, padx=(0, 6), pady=8)

    ctk.CTkButton(
        gui.frame_aviso,
        text="✕",
        width=30,
        height=30,
        corner_radius=6,
        font=fonte(13),
        fg_color="transparent",
        hover_color=cor("banner_border"),
        text_color=cor("banner_fg"),
        command=funcoes["dispensar_aviso"],
    ).grid(row=0, column=2, padx=(0, 8), pady=8)

    gui.frame_aviso.grid_remove()


# ============================================================================
# CABEÇALHO
# ============================================================================


def _criar_cabecalho(gui, tema_manager, funcoes):
    frame = ctk.CTkFrame(gui.frame_root, fg_color="transparent")
    frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
    frame.grid_columnconfigure(0, weight=1)

    titulos = ctk.CTkFrame(frame, fg_color="transparent")
    titulos.grid(row=0, column=0, sticky="w")
    criar_label(titulos, "Gerador de E-mails", 22, "bold", anchor="w").pack(fill="x")
    criar_label(
        titulos,
        "Suporte Hepta · avisos de tentativa de contato e fechamento",
        12,
        muted=True,
        anchor="w",
    ).pack(fill="x")

    acoes = ctk.CTkFrame(frame, fg_color="transparent")
    acoes.grid(row=0, column=1, sticky="e")

    gui.btn_atualizar = criar_botao(
        acoes, "Atualizações", funcoes["verificar_atualizacao"], altura=32, tamanho=12, width=120
    )
    gui.btn_atualizar.pack(side="left", padx=(0, 8))

    gui.btn_tema = criar_botao(
        acoes, "", lambda: funcoes["alternar_tema"](tema_manager), altura=32, tamanho=12, width=110
    )
    gui.btn_tema.pack(side="left")
    atualizar_texto_botao_tema(gui, tema_manager.tema_atual)


def atualizar_texto_botao_tema(gui, tema_atual):
    """O botão mostra o tema para o qual vai trocar."""
    gui.btn_tema.configure(text="☀ Tema claro" if tema_atual == "escuro" else "☾ Tema escuro")


# ============================================================================
# BARRA DE AÇÕES
# ============================================================================


def _criar_toolbar(gui, funcoes):
    frame = ctk.CTkFrame(gui.frame_root, fg_color="transparent")
    frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))
    frame.grid_columnconfigure(0, weight=2, uniform="toolbar")
    frame.grid_columnconfigure((1, 2, 3), weight=1, uniform="toolbar")

    gui.btn_gerar = criar_botao(
        frame,
        "Gerar e-mail   (Ctrl+Enter)",
        funcoes["gerar_email"],
        estilo="primario",
        altura=42,
        tamanho=14,
    )
    gui.btn_gerar.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    # Copia direto para a área de transferência, sem abrir o navegador
    gui.btn_copiar = criar_botao(frame, "📋 Copiar e-mail", funcoes["copiar_email"], altura=42)
    gui.btn_copiar.grid(row=0, column=1, sticky="ew", padx=(0, 8))

    criar_botao(frame, "Limpar telefones", funcoes["limpar_listas"], altura=42).grid(
        row=0, column=2, sticky="ew", padx=(0, 8)
    )
    criar_botao(frame, "Novo e-mail", funcoes["limpar_tudo"], altura=42).grid(
        row=0, column=3, sticky="ew"
    )


# ============================================================================
# CONTEÚDO
# ============================================================================


def _criar_conteudo(gui, tema_manager, funcoes):
    gui.frame_conteudo = ctk.CTkScrollableFrame(
        gui.frame_root,
        fg_color="transparent",
        scrollbar_button_color=cor("sec_bg"),
        scrollbar_button_hover_color=cor("sec_hover"),
    )
    gui.frame_conteudo.grid(row=3, column=0, sticky="nsew")

    _secao_chamado(gui)
    _secao_tipo(gui)
    _secao_telefones(gui, tema_manager, funcoes)
    _secao_horario(gui, funcoes)


def _secao_chamado(gui):
    sec = criar_secao(gui.frame_conteudo, "Dados do chamado")
    sec.grid_columnconfigure(0, weight=3, uniform="chamado")
    sec.grid_columnconfigure(1, weight=2, uniform="chamado")

    frame_req, gui.entry_req = criar_campo(sec, "Requisição (REQ)", "Ex: 000008198188")
    frame_req.grid(row=0, column=0, sticky="ew", padx=(0, 12))

    frame_nome, gui.entry_nome = criar_campo(sec, "Funcionário", "Seu nome (assina o e-mail)")
    frame_nome.grid(row=0, column=1, sticky="ew")
    gui.entry_nome.insert(0, gui.funcionario_salvo())


def _secao_tipo(gui):
    sec = criar_secao(gui.frame_conteudo, "Tipo de e-mail")

    frame = ctk.CTkFrame(sec, fg_color="transparent")
    frame.pack(fill="x")
    gui.botoes_tipo = {}
    for coluna, tipo in enumerate(TipoEmail):
        frame.grid_columnconfigure(coluna, weight=1, uniform="tipo")
        botao = criar_botao(
            frame, tipo.rotulo, lambda v=tipo.value: gui.selecionar_tipo(v), altura=36
        )
        botao.grid(row=0, column=coluna, sticky="ew", padx=(0 if coluna == 0 else 6, 0))
        gui.botoes_tipo[tipo.value] = botao

    # Textos curtos (uma linha). Não ajustar wraplength em <Configure>: a mudança de
    # altura realimenta o redimensionamento e trava a janela (visto ao trocar o tema).
    gui.feedback_label = criar_label(sec, "", 12, muted=True, anchor="w")
    gui.feedback_label.pack(fill="x", pady=(8, 0))

    def selecionar_tipo(valor):
        gui.tipo_email.set(valor)
        for v, botao in gui.botoes_tipo.items():
            aplicar_estilo_botao(botao, "primario" if v == valor else "secundario")
        gui.feedback_label.configure(text=TipoEmail(valor).descricao)

    gui.selecionar_tipo = selecionar_tipo
    selecionar_tipo(gui.tipo_email.get())


def _secao_telefones(gui, tema_manager, funcoes):
    sec = criar_secao(gui.frame_conteudo, "Telefones")
    gui.label_titulo_telefones = sec.label_titulo

    gui.entry_telefone, gui.btn_add_cel, gui.btn_add_fixo = criar_linha_entrada_telefone(
        sec, funcoes
    )

    def ao_mudar_telefones():
        qtd = len(gui.telefones)
        gui.label_titulo_telefones.configure(
            text=f"Telefones  ({qtd}/{MAX_TELEFONES})" if qtd else "Telefones"
        )

    gui.ao_mudar_telefones = ao_mudar_telefones
    criar_lista_telefones(gui, sec, tema_manager)


def _secao_horario(gui, funcoes):
    sec = criar_secao(gui.frame_conteudo, "Data e horário do contato")

    gui.data_hora_automatica = tk.BooleanVar(value=True)
    gui.switch_horario = ctk.CTkSwitch(
        sec,
        text="Usar data e hora atuais",
        variable=gui.data_hora_automatica,
        command=funcoes["alternar_horario_automatico"],
        font=fonte(13),
        text_color=cor("fg"),
        progress_color=cor("primary"),
        button_color=("#ffffff", "#e6e8ec"),
        button_hover_color=("#f3f4f6", "#ffffff"),
        fg_color=cor("entry_border"),
    )
    gui.switch_horario.pack(anchor="w")

    (
        gui.spin_dia,
        gui.spin_mes,
        gui.spin_ano,
        gui.spin_hora,
        gui.spin_minuto,
    ) = criar_linha_horario(sec, funcoes["definir_horario_manual"])

    gui.label_horario = criar_label(sec, TEXTO_HORARIO_AUTOMATICO, 12, muted=True, anchor="w")
    gui.label_horario.pack(fill="x", pady=(8, 0))


# ============================================================================
# BARRA DE STATUS
# ============================================================================


def _criar_status_bar(gui):
    gui.frame_status = ctk.CTkFrame(
        gui.janela, fg_color=cor("statusbar_bg"), corner_radius=0, border_width=0, height=36
    )
    gui.frame_status.pack(fill="x", side="bottom")
    gui.frame_status.grid_columnconfigure(0, weight=1)

    # Linha separadora no topo da barra
    ctk.CTkFrame(gui.frame_status, height=1, corner_radius=0, fg_color=cor("border")).grid(
        row=0, column=0, columnspan=2, sticky="ew"
    )

    gui.status_label = ctk.CTkLabel(
        gui.frame_status,
        text="Pronto para gerar e-mail",
        font=fonte(12),
        text_color=cor("success"),
        anchor="w",
    )
    gui.status_label.grid(row=1, column=0, sticky="ew", padx=16, pady=6)

    links = ctk.CTkFrame(gui.frame_status, fg_color="transparent")
    links.grid(row=1, column=1, sticky="e", padx=16, pady=6)

    criar_label(links, "Criado por Josué B. Almeida", 12, muted=True).pack(side="left")
    criar_label(links, "·", 12, muted=True).pack(side="left", padx=6)
    gui.github_link = ctk.CTkLabel(
        links, text="GitHub", font=fonte(12, "bold"), text_color=cor("link_fg"), cursor="hand2"
    )
    gui.github_link.pack(side="left")
    criar_label(links, "·", 12, muted=True).pack(side="left", padx=6)
    gui.linkedin_link = ctk.CTkLabel(
        links, text="LinkedIn", font=fonte(12, "bold"), text_color=cor("link_fg"), cursor="hand2"
    )
    gui.linkedin_link.pack(side="left")
    criar_label(links, "·", 12, muted=True).pack(side="left", padx=6)
    criar_label(links, f"v{VERSAO_ATUAL}", 12, "bold", muted=True).pack(side="left")
