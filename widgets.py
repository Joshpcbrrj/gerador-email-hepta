# -*- coding: utf-8 -*-
"""
MÓDULO DE CRIAÇÃO DE WIDGETS
================================================================================
Funções para criar todos os elementos da interface gráfica.
"""

import tkinter as tk
from config import VERSAO_ATUAL
from widget_helpers import (
    criar_label_frame, criar_linha_entrada_com_exemplo,
    criar_linha_entrada_telefone, criar_linha_horario, criar_botao_remover
)


def criar_widgets(gui, tema_manager, funcoes):
    """
    Cria todos os elementos da interface gráfica e registra no TemaManager.
    """
    
    # ====================================================================
    # FRAME PRINCIPAL
    # ====================================================================
    gui.main_frame = tk.Frame(gui.janela)
    gui.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
    tema_manager.registrar_widget(gui.main_frame, 'frame')
    
    # ====================================================================
    # CABEÇALHO
    # ====================================================================
    gui.frame_header = tk.Frame(gui.main_frame)
    gui.frame_header.pack(fill=tk.X, pady=(0,15))
    tema_manager.registrar_widget(gui.frame_header, 'header_frame')
    
    titulo = tk.Label(gui.frame_header, text="📧 GERADOR DE E-MAILS - SUPORTE HEPTA", 
                     font=("Arial", 16, "bold"))
    titulo.pack(side=tk.LEFT)
    tema_manager.registrar_widget(titulo, 'header_label')
    
    # Botões do cabeçalho
    frame_botoes_header = tk.Frame(gui.frame_header)
    frame_botoes_header.pack(side=tk.RIGHT)
    tema_manager.registrar_widget(frame_botoes_header, 'header_frame')
    
    gui.btn_tema = tk.Button(frame_botoes_header, text="🌓 Tema", 
                              command=lambda: funcoes['alternar_tema'](tema_manager),
                              font=("Arial", 9), padx=12, pady=4)
    gui.btn_tema.pack(side=tk.LEFT, padx=(0,5))
    tema_manager.registrar_widget(gui.btn_tema, 'header_button')
    
    gui.btn_atualizar = tk.Button(frame_botoes_header, text="🔄 Update", 
                                   command=funcoes['verificar_atualizacao'],
                                   font=("Arial", 9), padx=12, pady=4)
    gui.btn_atualizar.pack(side=tk.LEFT)
    tema_manager.registrar_widget(gui.btn_atualizar, 'header_button')
    
    # ====================================================================
    # STATUS
    # ====================================================================
    gui.status_label = tk.Label(gui.main_frame, text="✅ Pronto para gerar e-mail", 
                                  font=("Arial", 10), pady=5)
    gui.status_label.pack(fill=tk.X, pady=(0,15))
    tema_manager.registrar_widget(gui.status_label, 'status_label')
    
    # Timer para mensagens temporárias
    gui.timer_mensagem = None
    
    # ====================================================================
    # 1ª ETAPA: NÚMERO DA REQUISIÇÃO
    # ====================================================================
    gui.frame_req = criar_label_frame(gui.main_frame, "🔢 1ª Etapa -> NÚMERO DA REQUISIÇÃO", 
                                       tema_manager)
    gui.entry_req = criar_linha_entrada_com_exemplo(gui.frame_req, "REQ:", 35, 
                                                     "Ex: 000008198188", 
                                                     tema_manager)
    
    # ====================================================================
    # 2ª ETAPA: TIPO DE E-MAIL (com feedback visual)
    # ====================================================================
    gui.frame_tipo = criar_label_frame(gui.main_frame, "📧 2ª Etapa -> TIPO DE E-MAIL", 
                                        tema_manager)
    
    frame_tipo_inner = tk.Frame(gui.frame_tipo)
    frame_tipo_inner.pack()
    tema_manager.registrar_widget(frame_tipo_inner, 'frame')
    
    opcoes_tipo = [
        ("📞 1º Aviso", "1"),
        ("📞 2º Aviso", "2"),
        ("📞 3º Aviso", "3"),
        ("🔒 Fechamento", "4")
    ]
    
    def on_tipo_selected():
        valor = gui.tipo_email.get()
        textos = {"1": "1º Aviso", "2": "2º Aviso", "3": "3º Aviso", "4": "Fechamento"}
        texto_opcao = textos.get(valor, "")
        gui.feedback_label.config(text=f"✅ Opção escolhida: {texto_opcao}")
        tema_manager.aplicar_tema()
    
    for texto, valor in opcoes_tipo:
        rb = tk.Radiobutton(
            frame_tipo_inner, 
            text=texto, 
            variable=gui.tipo_email, 
            value=valor, 
            font=("Arial", 10),
            command=on_tipo_selected,
            indicatoron=1,
            padx=5,
            pady=2
        )
        rb.pack(side=tk.LEFT, padx=10)
        tema_manager.registrar_widget(rb, 'radiobutton')
    
    gui.feedback_label = tk.Label(gui.frame_tipo, 
                                   text="✅ Opção escolhida: 1º Aviso", 
                                   font=("Arial", 9, "bold"),
                                   pady=5)
    gui.feedback_label.pack()
    tema_manager.registrar_widget(gui.feedback_label, 'feedback_label')
    
    # ====================================================================
    # 3ª ETAPA: TELEFONES
    # ====================================================================
    gui.frame_telefones = criar_label_frame(gui.main_frame, "📱 3ª Etapa -> TELEFONES", 
                                             tema_manager)
    
    # Linha de entrada de telefone
    gui.entry_telefone, gui.btn_add_cel, gui.btn_add_fixo = criar_linha_entrada_telefone(
        gui.frame_telefones, tema_manager, funcoes)
    
    # Label da lista
    label_lista = tk.Label(gui.frame_telefones, text="Telefones adicionados:", font=("Arial", 9))
    label_lista.pack(anchor=tk.W)
    tema_manager.registrar_widget(label_lista, 'label')
    
    # Listbox
    gui.lista_telefones = tk.Listbox(gui.frame_telefones, height=5, width=70, font=("Arial", 10))
    gui.lista_telefones.pack(fill=tk.X, pady=5)
    tema_manager.registrar_widget(gui.lista_telefones, 'listbox')
    
    # Botão remover
    gui.btn_remover = criar_botao_remover(gui.frame_telefones, "❌ Remover Selecionado", 
                                           funcoes['remover_telefone'], tema_manager)
    
    # ====================================================================
    # 4ª ETAPA: HORÁRIO DO CONTATO
    # ====================================================================
    gui.frame_horario = criar_label_frame(gui.main_frame, "⏰ 4ª Etapa -> HORÁRIO DO CONTATO", 
                                           tema_manager)
    gui.spin_hora, gui.spin_minuto = criar_linha_horario(gui.frame_horario, tema_manager)
    
    # ====================================================================
    # 5ª ETAPA: NOME DO FUNCIONÁRIO
    # ====================================================================
    gui.frame_nome = criar_label_frame(gui.main_frame, "✍️ 5ª Etapa -> NOME DO FUNCIONÁRIO", 
                                        tema_manager)
    gui.entry_nome = tk.Entry(gui.frame_nome, width=60, font=("Arial", 10))
    gui.entry_nome.pack(fill=tk.X)
    gui.entry_nome.insert(0, "Josué B. Almeida")
    tema_manager.registrar_widget(gui.entry_nome, 'entry')
    
    # ====================================================================
    # BOTÕES DE AÇÃO
    # ====================================================================
    gui.frame_botoes_acao = tk.Frame(gui.main_frame)
    gui.frame_botoes_acao.pack(fill=tk.X, pady=25)
    tema_manager.registrar_widget(gui.frame_botoes_acao, 'action_frame')
    
    gui.btn_gerar = tk.Button(gui.frame_botoes_acao, text="🚀 GERAR E-MAIL",
                               command=funcoes['gerar_email'],
                               font=("Arial", 10, "bold"), padx=20, pady=8)
    gui.btn_gerar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=8)
    tema_manager.registrar_widget(gui.btn_gerar, 'action_button')
    
    gui.btn_limpar = tk.Button(gui.frame_botoes_acao, text="🗑️ LIMPAR LISTAS",
                                command=funcoes['limpar_listas'],
                                font=("Arial", 10, "bold"), padx=20, pady=8)
    gui.btn_limpar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=8)
    tema_manager.registrar_widget(gui.btn_limpar, 'action_button')
    
    gui.btn_limpar_tudo = tk.Button(gui.frame_botoes_acao, text="✨ NOVO E-MAIL",
                                     command=funcoes['limpar_tudo'],
                                     font=("Arial", 10, "bold"), padx=20, pady=8)
    gui.btn_limpar_tudo.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=8)
    tema_manager.registrar_widget(gui.btn_limpar_tudo, 'action_button')
    
    # ====================================================================
    # RODAPÉ
    # ====================================================================
    gui.frame_rodape = tk.Frame(gui.main_frame)
    gui.frame_rodape.pack(fill=tk.X, side=tk.BOTTOM, pady=(20,0))
    tema_manager.registrar_widget(gui.frame_rodape, 'rodape_frame')
    
    separador = tk.Frame(gui.frame_rodape, height=1)
    separador.pack(fill=tk.X, pady=(10,8))
    tema_manager.registrar_widget(separador, 'rodape_label')
    
    rodape_texto = tk.Label(gui.frame_rodape, 
                            text="✨ Criado por: Josué B. Almeida ✨", 
                            font=("Arial", 9, "bold"))
    rodape_texto.pack(pady=(5,3))
    tema_manager.registrar_widget(rodape_texto, 'rodape_label')
    
    frame_links = tk.Frame(gui.frame_rodape)
    frame_links.pack(pady=(5,3))
    tema_manager.registrar_widget(frame_links, 'rodape_frame')
    
    gui.github_link = tk.Label(frame_links, text="🐙 GitHub", font=("Arial", 8, "bold"), cursor="hand2")
    gui.github_link.pack(side=tk.LEFT, padx=10)
    tema_manager.registrar_widget(gui.github_link, 'rodape_link')
    
    sep = tk.Label(frame_links, text="|", font=("Arial", 8))
    sep.pack(side=tk.LEFT)
    tema_manager.registrar_widget(sep, 'rodape_label')
    
    gui.linkedin_link = tk.Label(frame_links, text="🔗 LinkedIn", font=("Arial", 8, "bold"), cursor="hand2")
    gui.linkedin_link.pack(side=tk.LEFT, padx=10)
    tema_manager.registrar_widget(gui.linkedin_link, 'rodape_link')
    
    versao_label = tk.Label(gui.frame_rodape, text=f"Versão {VERSAO_ATUAL} - Maio/2026", font=("Arial", 9, "bold"))
    versao_label.pack(pady=(5,12))
    tema_manager.registrar_widget(versao_label, 'rodape_label')