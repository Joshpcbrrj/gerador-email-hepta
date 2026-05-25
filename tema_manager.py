# -*- coding: utf-8 -*-
"""
MÓDULO GERENCIADOR DE TEMAS
================================================================================
Gerencia tema claro/escuro com CustomTkinter e widgets da interface.
"""

import customtkinter as ctk
from temas import CORES
from lista_telefones import atualizar_lista_telefones


class TemaManager:
    """Gerencia a aplicação de temas em todos os widgets"""

    def __init__(self, gui):
        self.gui = gui
        self.tema_atual = "claro"
        self.widgets = []

    def registrar_widget(self, widget, tipo, papel=None):
        """Registra um widget para ser afetado pelo tema."""
        self.widgets.append((widget, tipo, papel))

    def aplicar_tema(self):
        """Aplica o tema atual a todos os widgets registrados."""
        cores = CORES[self.tema_atual]
        modo = "Dark" if self.tema_atual == "escuro" else "Light"
        ctk.set_appearance_mode(modo)
        ctk.set_default_color_theme("blue")

        self.gui.janela.configure(fg_color=cores["bg"])

        for widget, tipo, papel in self.widgets:
            try:
                self._aplicar_em_widget(widget, tipo, papel, cores)
            except Exception:
                pass

        if hasattr(self.gui, "telefones"):
            atualizar_lista_telefones(self.gui, self)

        self._aplicar_status_padrao(cores)

    def _aplicar_status_padrao(self, cores):
        if hasattr(self.gui, "status_label"):
            texto = self.gui.status_label.cget("text")
            if texto.startswith("✅ Pronto"):
                self.gui.status_label.configure(text_color=cores["status_ok"])

    def _aplicar_em_widget(self, widget, tipo, papel, cores):
        if tipo == "ctk_frame" or tipo == "ctk_frame_transparent":
            cor = "transparent" if tipo == "ctk_frame_transparent" else cores["frame_bg"]
            widget.configure(fg_color=cor)

        elif tipo == "ctk_section":
            widget.configure(fg_color=cores["frame_bg"])

        elif tipo == "ctk_label":
            widget.configure(fg_color=cores["label_bg"], text_color=cores["label_fg"])

        elif tipo == "ctk_label_header":
            widget.configure(fg_color=cores["bg"], text_color=cores["header_fg"])

        elif tipo == "ctk_label_section":
            widget.configure(fg_color=cores["frame_bg"], text_color=cores["section_title_fg"])

        elif tipo == "ctk_label_feedback":
            widget.configure(fg_color=cores["frame_bg"], text_color=cores["feedback_fg"])

        elif tipo == "ctk_label_status":
            widget.configure(fg_color=cores["rodape_bg"], text_color=cores["status_ok"])

        elif tipo == "ctk_label_footer":
            widget.configure(fg_color=cores["rodape_bg"], text_color=cores["rodape_fg"])

        elif tipo == "ctk_label_link":
            widget.configure(fg_color=cores["rodape_bg"], text_color=cores["rodape_link_fg"])

        elif tipo == "ctk_entry":
            widget.configure(
                fg_color=cores["entry_bg"],
                text_color=cores["entry_fg"],
                border_color=cores["button_sec_bg"],
            )

        elif tipo == "ctk_combobox":
            widget.configure(
                fg_color=cores["entry_bg"],
                text_color=cores["entry_fg"],
                border_color=cores["button_sec_bg"],
                button_color=cores["button_sec_bg"],
                button_hover_color=cores["list_row_hover_bg"],
                dropdown_fg_color=cores["entry_bg"],
                dropdown_text_color=cores["entry_fg"],
                dropdown_hover_color=cores["list_row_selected_bg"],
            )

        elif tipo == "ctk_lista_scroll":
            widget.configure(fg_color=cores["list_scroll_bg"])

        elif tipo == "ctk_segmented":
            widget.configure(
                fg_color=cores["button_sec_bg"],
                selected_color=cores["button_gerar_bg"],
                selected_hover_color=cores["button_gerar_bg"],
                unselected_color=cores["entry_bg"],
                unselected_hover_color=cores["list_row_hover_bg"],
            )
            self._aplicar_cores_texto_segmented(widget, cores)

        elif tipo == "ctk_button":
            self._aplicar_botao(widget, papel, cores)

    def _aplicar_cores_texto_segmented(self, widget, cores):
        """
        CTkSegmentedButton usa a mesma text_color em todos os botões.
        Ajusta: selecionado = texto escuro no fundo verde (modo escuro),
        não selecionado = cor padrão do tema.
        """
        if not hasattr(widget, "_buttons_dict"):
            return

        selecionado = getattr(widget, "_current_value", None)
        cor_selecionado = cores["button_gerar_fg"]
        cor_nao_selecionado = cores["entry_fg"]

        for valor, botao in widget._buttons_dict.items():
            if valor == selecionado:
                botao.configure(text_color=cor_selecionado)
            else:
                botao.configure(text_color=cor_nao_selecionado)

    def atualizar_segmented(self, widget):
        """Atualiza cores de texto após troca de opção no segmented button."""
        cores = CORES[self.tema_atual]
        self._aplicar_cores_texto_segmented(widget, cores)

    def _aplicar_botao(self, widget, papel, cores):
        mapa = {
            "gerar": (cores["button_gerar_bg"], cores["button_gerar_fg"]),
            "limpar": (cores["button_limpar_bg"], cores["button_limpar_fg"]),
            "novo": (cores["button_novo_bg"], cores["button_novo_fg"]),
            "tema": (cores["button_sec_bg"], cores["button_sec_fg"]),
            "update": (cores["button_sec_bg"], cores["button_sec_fg"]),
            "celular": (cores["button_celular"], "#ffffff" if self.tema_atual == "claro" else cores["bg"]),
            "fixo": (cores["button_fixo"], "#ffffff" if self.tema_atual == "claro" else cores["bg"]),
            "remover": (cores["button_remover"], "#ffffff" if self.tema_atual == "claro" else cores["bg"]),
        }
        if papel in mapa:
            fg, text = mapa[papel]
            widget.configure(fg_color=fg, text_color=text, hover_color=fg)

    def alternar_tema(self):
        """Alterna entre tema claro e escuro."""
        self.tema_atual = "escuro" if self.tema_atual == "claro" else "claro"
        self.aplicar_tema()
        return self.tema_atual

    def cor_status(self, nome_cor):
        """Retorna cor hexadecimal para mensagens de status."""
        from temas import COR_STATUS_CLARO, COR_STATUS_ESCURO
        mapa = COR_STATUS_ESCURO if self.tema_atual == "escuro" else COR_STATUS_CLARO
        return mapa.get(nome_cor, mapa.get("green"))
