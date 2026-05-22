# -*- coding: utf-8 -*-
"""
FUNÇÕES AUXILIARES PARA CRIAÇÃO DE WIDGETS
================================================================================
Funções reutilizáveis para criar elementos comuns da interface.
"""

import tkinter as tk


def criar_label_frame(parent, texto, tema_manager):
    """
    Cria um LabelFrame padronizado.
    O fundo será aplicado pelo TemaManager.
    """
    # Criar sem definir bg (será aplicado pelo tema)
    frame = tk.LabelFrame(parent, text=texto, font=("Arial", 10, "bold"), padx=15, pady=10)
    frame.pack(fill=tk.X, pady=8)
    tema_manager.registrar_widget(frame, 'frame')
    return frame


def criar_linha_entrada_com_exemplo(parent, label_text, entry_width, exemplo_texto, tema_manager):
    """Cria uma linha com label, entry e texto de exemplo"""
    frame = tk.Frame(parent)
    frame.pack()
    tema_manager.registrar_widget(frame, 'label')
    
    label = tk.Label(frame, text=label_text, font=("Arial", 10))
    label.pack(side=tk.LEFT)
    tema_manager.registrar_widget(label, 'label')
    
    entry = tk.Entry(frame, width=entry_width, font=("Arial", 10))
    entry.pack(side=tk.LEFT, padx=5)
    tema_manager.registrar_widget(entry, 'entry')
    
    label_exemplo = tk.Label(frame, text=exemplo_texto, font=("Arial", 9))
    label_exemplo.pack(side=tk.LEFT)
    tema_manager.registrar_widget(label_exemplo, 'label')
    
    return entry


def criar_linha_entrada_telefone(parent, tema_manager, funcoes):
    """Cria a linha de entrada para telefone com botões coloridos"""
    frame = tk.Frame(parent)
    frame.pack(fill=tk.X, pady=5)
    tema_manager.registrar_widget(frame, 'label')
    
    label = tk.Label(frame, text="Número:", font=("Arial", 10))
    label.pack(side=tk.LEFT)
    tema_manager.registrar_widget(label, 'label')
    
    entry = tk.Entry(frame, width=30, font=("Arial", 10))
    entry.pack(side=tk.LEFT, padx=5)
    tema_manager.registrar_widget(entry, 'entry')
    entry.bind('<Return>', lambda e: funcoes['adicionar_celular']())
    
    # Botão Celular
    btn_celular = tk.Button(frame, text="📱 Celular", 
                            command=funcoes['adicionar_celular'],
                            bg="#4CAF50", fg="white", font=("Arial", 9), padx=10, pady=3)
    btn_celular.pack(side=tk.LEFT, padx=2)
    tema_manager.registrar_widget(btn_celular, 'special_button')
    
    # Botão Fixo
    btn_fixo = tk.Button(frame, text="🏠 Fixo", 
                         command=funcoes['adicionar_fixo'],
                         bg="#FF9800", fg="white", font=("Arial", 9), padx=10, pady=3)
    btn_fixo.pack(side=tk.LEFT, padx=2)
    tema_manager.registrar_widget(btn_fixo, 'special_button')
    
    return entry, btn_celular, btn_fixo


def criar_linha_horario(parent, tema_manager):
    """Cria a linha de entrada para hora e minutos"""
    frame = tk.Frame(parent)
    frame.pack()
    tema_manager.registrar_widget(frame, 'label')
    
    label_hora = tk.Label(frame, text="Hora:", font=("Arial", 10))
    label_hora.pack(side=tk.LEFT)
    tema_manager.registrar_widget(label_hora, 'label')
    
    spin_hora = tk.Spinbox(frame, from_=0, to=23, width=6, font=("Arial", 10))
    spin_hora.pack(side=tk.LEFT, padx=5)
    spin_hora.delete(0, tk.END)
    spin_hora.insert(0, "14")
    tema_manager.registrar_widget(spin_hora, 'spinbox')
    
    label_minutos = tk.Label(frame, text="Minutos:", font=("Arial", 10))
    label_minutos.pack(side=tk.LEFT, padx=(10,0))
    tema_manager.registrar_widget(label_minutos, 'label')
    
    spin_minuto = tk.Spinbox(frame, from_=0, to=59, width=6, font=("Arial", 10))
    spin_minuto.pack(side=tk.LEFT, padx=5)
    spin_minuto.delete(0, tk.END)
    spin_minuto.insert(0, "00")
    tema_manager.registrar_widget(spin_minuto, 'spinbox')
    
    return spin_hora, spin_minuto


def criar_botao_remover(parent, texto, comando, tema_manager):
    """Cria um botão de remover"""
    btn = tk.Button(parent, text=texto, command=comando,
                    bg="#f44336", fg="white", font=("Arial", 9), padx=12, pady=3)
    btn.pack()
    tema_manager.registrar_widget(btn, 'special_button')
    return btn