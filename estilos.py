# -*- coding: utf-8 -*-
"""
MÓDULO DE ESTILOS
================================================================================
Funções para aplicar estilos diretamente nos widgets.
"""

import tkinter as tk


def aplicar_estilo_listbox(listbox, tema):
    """Aplica estilo diretamente no Listbox"""
    cores = {
        'claro': {
            'bg': '#ffffff',
            'fg': '#333333',
            'select_bg': '#e3f2fd',
            'select_fg': '#1976d2'
        },
        'escuro': {
            'bg': '#1e1e2e',
            'fg': '#cdd6f4',
            'select_bg': '#313244',
            'select_fg': '#89b4fa'
        }
    }
    
    c = cores[tema]
    listbox.configure(
        bg=c['bg'],
        fg=c['fg'],
        selectbackground=c['select_bg'],
        selectforeground=c['select_fg'],
        relief=tk.FLAT,
        borderwidth=0,
        highlightthickness=0
    )


def aplicar_estilo_entry(entry, tema):
    """Aplica estilo diretamente no Entry"""
    cores = {
        'claro': {
            'bg': '#ffffff',
            'fg': '#333333'
        },
        'escuro': {
            'bg': '#313244',
            'fg': '#cdd6f4'
        }
    }
    
    c = cores[tema]
    entry.configure(
        bg=c['bg'],
        fg=c['fg'],
        insertbackground=c['fg']
    )


def aplicar_estilo_label(label, tema, especial=False):
    """Aplica estilo diretamente no Label"""
    cores = {
        'claro': {
            'bg': '#f0f0f0',
            'fg': '#333333'
        },
        'escuro': {
            'bg': '#1e1e2e',
            'fg': '#cdd6f4'
        }
    }
    
    # Labels especiais (feedback) tem cor diferente
    if especial:
        cores['claro']['fg'] = '#000000'
        cores['escuro']['fg'] = '#ffffff'
    
    c = cores[tema]
    label.configure(
        bg=c['bg'],
        fg=c['fg']
    )


def aplicar_estilo_frame(frame, tema):
    """Aplica estilo diretamente no Frame"""
    cores = {
        'claro': {'bg': '#f0f0f0'},
        'escuro': {'bg': '#1e1e2e'}
    }
    
    frame.configure(bg=cores[tema]['bg'])


def aplicar_estilo_radiobutton(rb, tema):
    """Aplica estilo diretamente no Radiobutton"""
    cores = {
        'claro': {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'select': '#2196F3',
            'active_bg': '#e3f2fd'
        },
        'escuro': {
            'bg': '#1e1e2e',
            'fg': '#cdd6f4',
            'select': '#f5c2e7',
            'active_bg': '#313244'
        }
    }
    
    c = cores[tema]
    rb.configure(
        bg=c['bg'],
        fg=c['fg'],
        selectcolor=c['select'],
        activebackground=c['active_bg'],
        activeforeground=c['fg'],
        highlightthickness=0
    )


def aplicar_estilo_button(btn, tema, tipo='normal'):
    """Aplica estilo diretamente no Button"""
    cores = {
        'claro': {
            'normal': {'bg': '#2196F3', 'fg': 'white'},
            'limpar': {'bg': '#FF9800', 'fg': 'white'},
            'novo': {'bg': '#9C27B0', 'fg': 'white'},
            'sec': {'bg': '#6c757d', 'fg': 'white'}
        },
        'escuro': {
            'normal': {'bg': '#a6e3a1', 'fg': '#1e1e2e'},
            'limpar': {'bg': '#f9e2af', 'fg': '#1e1e2e'},
            'novo': {'bg': '#cba6f7', 'fg': '#1e1e2e'},
            'sec': {'bg': '#313244', 'fg': "#9eb1f1"}
        }
    }
    
    c = cores[tema][tipo]
    btn.configure(bg=c['bg'], fg=c['fg'])