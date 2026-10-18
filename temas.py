# -*- coding: utf-8 -*-
"""
MÓDULO DE CORES E FONTES DOS TEMAS
================================================================================
Paleta dos temas claro e escuro.

Os widgets recebem as cores como par (claro, escuro) através de cor(nome).
O próprio CustomTkinter troca entre as duas quando o modo de aparência muda,
então nenhum widget precisa ser repintado manualmente.
"""

FONTE_FAMILIA = "Segoe UI"

CORES = {
    'claro': {
        # Base
        'bg': '#f3f4f6',
        'fg': '#1f2937',
        'fg_muted': '#6b7280',
        'frame_bg': '#ffffff',          # Cartões (seções)
        'border': '#e2e5ea',
        # Ação principal
        'primary': '#2563eb',
        'primary_hover': '#1d4ed8',
        'primary_fg': '#ffffff',
        # Ação secundária
        'sec_bg': '#e9ecf1',
        'sec_hover': '#dde1e8',
        'sec_fg': '#1f2937',
        # Campos
        'entry_bg': '#ffffff',
        'entry_border': '#cfd4dc',
        # Lista de telefones
        'listbox_bg': '#ffffff',
        'list_row_bg': '#f5f7fa',
        'list_row_hover_bg': '#eceff4',
        'list_remove_hover': '#fde2e2',
        # Status
        'success': '#15803d',
        'warning': '#b45309',
        'info': '#1d4ed8',
        'danger': '#dc2626',
        # Rodapé
        'statusbar_bg': '#ffffff',
        'link_fg': '#2563eb',
        # Aviso de atualização
        'banner_bg': '#eff6ff',
        'banner_border': '#bfdbfe',
        'banner_fg': '#1e3a8a',
    },
    'escuro': {
        # Base
        'bg': '#111318',
        'fg': '#e6e8ec',
        'fg_muted': '#9aa3b2',
        'frame_bg': '#1a1d24',
        'border': '#2a2f3a',
        # Ação principal
        'primary': '#3b82f6',
        'primary_hover': '#2563eb',
        'primary_fg': '#ffffff',
        # Ação secundária
        'sec_bg': '#262a33',
        'sec_hover': '#313643',
        'sec_fg': '#e6e8ec',
        # Campos
        'entry_bg': '#13161c',
        'entry_border': '#363c49',
        # Lista de telefones
        'listbox_bg': '#13161c',
        'list_row_bg': '#20242c',
        'list_row_hover_bg': '#2a2f3a',
        'list_remove_hover': '#4c1d1d',
        # Status
        'success': '#4ade80',
        'warning': '#fbbf24',
        'info': '#60a5fa',
        'danger': '#f87171',
        # Rodapé
        'statusbar_bg': '#1a1d24',
        'link_fg': '#60a5fa',
        # Aviso de atualização
        'banner_bg': '#172554',
        'banner_border': '#1e3a8a',
        'banner_fg': '#dbeafe',
    },
}

# Nomes de cor usados nas mensagens de status -> chave da paleta
COR_STATUS = {
    'green': 'success',
    'orange': 'warning',
    'blue': 'info',
    'red': 'danger',
    'white': 'fg',
    'black': 'fg',
    'muted': 'fg_muted',
}


def cor(nome):
    """Retorna o par (claro, escuro) de uma cor da paleta, no formato do CustomTkinter."""
    return (CORES['claro'][nome], CORES['escuro'][nome])


def cor_status(nome_cor):
    """Retorna o par (claro, escuro) para um nome de cor de status ('green', 'orange'...)."""
    return cor(COR_STATUS.get(nome_cor, 'success'))


def fonte(tamanho=13, peso="normal"):
    """Fonte padrão da interface (tamanho em pixels, como no CustomTkinter)."""
    return (FONTE_FAMILIA, tamanho, peso)
