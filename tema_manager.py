# -*- coding: utf-8 -*-
"""
MÓDULO GERENCIADOR DE TEMAS
================================================================================
Gerencia a aplicação de temas em todos os widgets da interface.
"""

from temas import CORES


class TemaManager:
    """Gerencia a aplicação de temas em todos os widgets"""
    
    def __init__(self, gui):
        self.gui = gui
        self.tema_atual = "claro"
        self.widgets = []
    
    def registrar_widget(self, widget, tipo):
        """Registra um widget para ser afetado pelo tema"""
        self.widgets.append((widget, tipo))
    
    def aplicar_tema(self):
        """Aplica o tema atual a todos os widgets registrados"""
        cores = CORES[self.tema_atual]
        
        # Aplicar na janela principal
        self.gui.janela.configure(bg=cores['bg'])
        
        # Aplicar em todos os widgets registrados
        for widget, tipo in self.widgets:
            try:
                if tipo == 'frame':
                    # LabelFrame - aplicar fundo e cor do título
                    widget.configure(bg=cores['frame_bg'])
                    widget.configure(fg=cores['frame_title_fg'])
                    
                elif tipo == 'rodape_frame':
                    widget.configure(bg=cores['rodape_bg'])
                    
                elif tipo == 'header_frame':
                    widget.configure(bg=cores['header_bg'])
                    
                elif tipo == 'header_label':
                    widget.configure(bg=cores['header_bg'], fg=cores['header_fg'])
                    
                elif tipo == 'header_button':
                    widget.configure(bg=cores['button_sec_bg'], fg=cores['button_sec_fg'])
                    
                elif tipo == 'status_label':
                    widget.configure(bg=cores['status_bg'], fg=cores['status_fg'])
                    
                elif tipo == 'label':
                    widget.configure(bg=cores['label_bg'], fg=cores['label_fg'])
                    
                elif tipo == 'feedback_label':
                    widget.configure(bg=cores['label_bg'], fg=cores['feedback_fg'])
                    
                elif tipo == 'entry':
                    widget.configure(bg=cores['entry_bg'], fg=cores['entry_fg'],
                                   insertbackground=cores['entry_fg'])
                    
                elif tipo == 'listbox':
                    widget.configure(
                        bg=cores['listbox_bg'],
                        fg=cores['listbox_fg'],
                        selectbackground=cores['listbox_select_bg'],
                        selectforeground=cores['listbox_fg']
                    )
                    
                elif tipo == 'radiobutton':
                    widget.configure(
                        bg=cores['radiobutton_bg'],
                        fg=cores['radiobutton_fg'],
                        selectcolor=cores['radiobutton_select'],
                        activebackground=cores['radiobutton_active_bg'],
                        activeforeground=cores['radiobutton_fg']
                    )
                    
                elif tipo == 'spinbox':
                    widget.configure(bg=cores['entry_bg'], fg=cores['entry_fg'],
                                   insertbackground=cores['entry_fg'],
                                   buttonbackground=cores['button_sec_bg'])
                    
                elif tipo == 'action_button':
                    if 'GERAR' in widget.cget('text'):
                        widget.configure(bg=cores['button_gerar_bg'], fg=cores['button_gerar_fg'])
                    elif 'LIMPAR' in widget.cget('text'):
                        widget.configure(bg=cores['button_limpar_bg'], fg=cores['button_limpar_fg'])
                    elif 'NOVO' in widget.cget('text'):
                        widget.configure(bg=cores['button_novo_bg'], fg=cores['button_novo_fg'])
                    
                elif tipo == 'special_button':
                    # Botões especiais mantêm suas cores originais
                    pass
                        
                elif tipo == 'action_frame':
                    widget.configure(bg=cores['bg'])
                    
                elif tipo == 'rodape_label':
                    widget.configure(bg=cores['rodape_bg'], fg=cores['rodape_fg'])
                    
                elif tipo == 'rodape_link':
                    widget.configure(bg=cores['rodape_bg'], fg=cores['rodape_link_fg'])
                    
            except Exception:
                pass
    
    def alternar_tema(self):
        """Alterna entre tema claro e escuro"""
        self.tema_atual = "escuro" if self.tema_atual == "claro" else "claro"
        self.aplicar_tema()
        return self.tema_atual