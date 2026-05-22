# -*- coding: utf-8 -*-
"""
MÓDULO DE TEMAS - CORES E ESTILOS
================================================================================
Gerencia os temas claro e escuro da interface gráfica.
"""

# ============================================================================
# CORES DOS TEMAS
# ============================================================================

CORES = {
    'claro': {
        'bg': '#f0f0f0',
        'fg': '#333333',
        'frame_bg': '#f0f0f0',
        'frame_fg': '#333333',
        'frame_title_fg': '#333333',
        'header_bg': '#f0f0f0',
        'header_fg': '#2196F3',
        'status_fg': 'green',
        'status_bg': '#f0f0f0',
        'label_bg': '#f0f0f0',
        'label_fg': '#333333',
        'radiobutton_bg': '#f0f0f0',
        'radiobutton_fg': '#333333',
        'radiobutton_select': '#2196F3',
        'entry_bg': 'white',
        'entry_fg': '#333333',
        'listbox_bg': 'white',
        'listbox_fg': '#333333',
        'rodape_bg': '#e0e0e0',
        'rodape_fg': '#333333',
        'button_sec_bg': '#6c757d',
        'button_sec_fg': 'white',
        'button_gerar_bg': '#2196F3',
        'button_gerar_fg': 'white',
        'button_limpar_bg': '#FF9800',
        'button_limpar_fg': 'white',
        'button_novo_bg': '#9C27B0',
        'button_novo_fg': 'white'
    },
    'escuro': {
        'bg': '#2d2d2d',
        'fg': '#f0f0f0',
        'frame_bg': '#2d2d2d',           # Fundo do frame igual ao fundo geral
        'frame_fg': '#f0f0f0',
        'frame_title_fg': '#90CAF9',     # Azul bem claro (mais suave)
        'header_bg': '#2d2d2d',
        'header_fg': '#90CAF9',          # Azul claro no título
        'status_fg': '#81C784',
        'status_bg': '#2d2d2d',
        'label_bg': '#2d2d2d',
        'label_fg': '#f0f0f0',
        'radiobutton_bg': '#2d2d2d',     # Fundo escuro (mesmo do frame)
        'radiobutton_fg': '#f0f0f0',     # Texto claro
        'radiobutton_select': '#90CAF9', # Azul claro no círculo
        'entry_bg': '#3c3c3c',           # Fundo levemente mais claro que o frame
        'entry_fg': '#f0f0f0',
        'listbox_bg': '#3c3c3c',
        'listbox_fg': '#f0f0f0',
        'rodape_bg': '#3c3c3c',
        'rodape_fg': '#f0f0f0',
        'button_sec_bg': '#555555',
        'button_sec_fg': '#f0f0f0',
        'button_gerar_bg': '#4CAF50',
        'button_gerar_fg': 'white',
        'button_limpar_bg': '#FFC107',
        'button_limpar_fg': '#333333',
        'button_novo_bg': '#BA68C8',
        'button_novo_fg': 'white'
    }
}


def obter_cores(tema):
    """Retorna o dicionário de cores para o tema especificado"""
    return CORES.get(tema, CORES['claro'])