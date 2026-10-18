# -*- coding: utf-8 -*-
"""
================================================================================
INTERFACE GRÁFICA - GERADOR DE E-MAILS HEPTA
================================================================================

Versão com CustomTkinter, layout em cartões e temas claro/escuro nativos.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import tkinter as tk
import customtkinter as ctk
import webbrowser

from config import VERSAO_ATUAL, INTERVALO_VERIFICAR_ATUALIZACAO_MS
from tema_manager import TemaManager
from widgets import (
    criar_widgets,
    atualizar_texto_botao_tema,
    TEXTO_HORARIO_AUTOMATICO,
    TEXTO_HORARIO_MANUAL,
)
from widget_helpers import aplicar_estilo_botao, preencher_horario
from eventos import (
    adicionar_celular,
    adicionar_fixo,
    remover_telefone,
    limpar_listas,
    limpar_tudo,
    obter_todos_telefones,
    mostrar_mensagem_temporaria,
)
from geracao_email import gerar_email, limpar_pasta_temp
from atualizacao import verificar_atualizacao, perguntar_download
from data_hora import resolver_data_hora

# De quanto em quanto tempo os campos de data/hora acompanham o relógio
INTERVALO_RELOGIO_MS = 15 * 1000


class GeradorEmailGUI:
    """Classe principal da interface gráfica"""

    def __init__(self):
        self.tema_manager = TemaManager(self)
        self.tema_manager.aplicar_tema()
        ctk.set_default_color_theme("blue")

        self.janela = ctk.CTk()
        self.janela.title("Gerador de E-mails - Suporte Hepta")
        self.janela.geometry("960x720")
        self.janela.resizable(True, True)
        self.janela.minsize(680, 520)
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_programa)

        self.tipo_email = tk.StringVar(value="1")
        self.timer_mensagem = None
        self.timer_relogio = None
        self.release_disponivel = None
        self.versao_aviso_dispensado = None

        funcoes = {
            "adicionar_celular": lambda: adicionar_celular(self),
            "adicionar_fixo": lambda: adicionar_fixo(self),
            "limpar_listas": lambda: limpar_listas(self),
            "limpar_tudo": lambda: limpar_tudo(self),
            "gerar_email": self.gerar_email,
            "verificar_atualizacao": self.verificar_atualizacao_manual,
            "baixar_atualizacao": self.baixar_atualizacao,
            "dispensar_aviso": self.dispensar_aviso_atualizacao,
            "alternar_tema": self.alternar_tema,
            "alternar_horario_automatico": self.alternar_horario_automatico,
            "definir_horario_manual": self.definir_horario_manual,
        }

        criar_widgets(self, self.tema_manager, funcoes)

        self.github_link.bind(
            "<Button-1>",
            lambda e: webbrowser.open("https://github.com/Joshpcbrrj/gerador-email-hepta"),
        )
        self.linkedin_link.bind(
            "<Button-1>",
            lambda e: webbrowser.open("https://www.linkedin.com/in/josualmeida/"),
        )
        self.janela.bind("<Control-Return>", lambda e: self.gerar_email())

        self._atualizar_relogio()
        # Verificação automática: logo após abrir e depois periodicamente
        self.janela.after(1500, self.verificar_atualizacao_automatica)
        self.entry_req.focus_set()

    # ------------------------------------------------------------------
    # Telefones
    # ------------------------------------------------------------------
    def remover_telefone(self, indice):
        remover_telefone(self, indice)

    # ------------------------------------------------------------------
    # Geração
    # ------------------------------------------------------------------
    def gerar_email(self):
        gerar_email(self, obter_todos_telefones)

    # ------------------------------------------------------------------
    # Data e hora do contato
    # ------------------------------------------------------------------
    def obter_data_hora_contato(self):
        """Data/hora do contato: agora (modo automático) ou a escolhida nos campos."""
        automatico = self.data_hora_automatica.get()
        momento = resolver_data_hora(
            automatico,
            self.spin_dia.get(),
            self.spin_mes.get(),
            self.spin_ano.get(),
            self.spin_hora.get(),
            self.spin_minuto.get(),
        )
        if automatico:
            self._preencher_campos_horario(momento)
        return momento

    def _preencher_campos_horario(self, momento=None):
        preencher_horario(
            self.spin_dia, self.spin_mes, self.spin_ano, self.spin_hora, self.spin_minuto, momento
        )

    def _atualizar_relogio(self):
        """No modo automático, mantém os campos mostrando o horário atual."""
        if self.data_hora_automatica.get():
            self._preencher_campos_horario()
        self.timer_relogio = self.janela.after(INTERVALO_RELOGIO_MS, self._atualizar_relogio)

    def alternar_horario_automatico(self):
        if self.data_hora_automatica.get():
            self.ativar_horario_automatico()
        else:
            self.label_horario.configure(text=TEXTO_HORARIO_MANUAL)

    def ativar_horario_automatico(self):
        self.data_hora_automatica.set(True)
        self._preencher_campos_horario()
        self.label_horario.configure(text=TEXTO_HORARIO_AUTOMATICO)

    def definir_horario_manual(self):
        """Chamado quando o usuário escolhe um valor em um dos campos."""
        if self.data_hora_automatica.get():
            self.data_hora_automatica.set(False)
            self.label_horario.configure(text=TEXTO_HORARIO_MANUAL)

    # ------------------------------------------------------------------
    # Status e tema
    # ------------------------------------------------------------------
    def mostrar_mensagem_temporaria(self, mensagem, cor="green"):
        mostrar_mensagem_temporaria(self, mensagem, cor)

    def atualizar_status(self, mensagem, cor="green"):
        """Atualiza a mensagem de status (mantém visível)."""
        if self.timer_mensagem:
            self.janela.after_cancel(self.timer_mensagem)
            self.timer_mensagem = None
        self.status_label.configure(text=mensagem, text_color=self.tema_manager.cor_status(cor))

    def alternar_tema(self, tema_manager):
        """Alterna entre tema claro e escuro."""
        novo_tema = tema_manager.alternar_tema()
        atualizar_texto_botao_tema(self, novo_tema)
        self.mostrar_mensagem_temporaria(
            "Tema escuro ativado!" if novo_tema == "escuro" else "Tema claro ativado!", "white"
        )

    # ------------------------------------------------------------------
    # Atualizações
    # ------------------------------------------------------------------
    def verificar_atualizacao_automatica(self):
        """Verifica em segundo plano, sem popup; reagenda a próxima verificação."""
        verificar_atualizacao(
            self.janela, ao_encontrar=self.mostrar_aviso_atualizacao, silencioso=True
        )
        self.janela.after(INTERVALO_VERIFICAR_ATUALIZACAO_MS, self.verificar_atualizacao_automatica)

    def verificar_atualizacao_manual(self):
        """Botão Atualizações: se já sabemos da versão nova, oferece o download direto."""
        if self.release_disponivel:
            perguntar_download(self.janela, self.release_disponivel)
            return

        self.atualizar_status("Verificando atualizações...", "blue")
        verificar_atualizacao(
            self.janela,
            callback=lambda: self.mostrar_mensagem_temporaria(
                f"Você está usando a versão mais recente (v{VERSAO_ATUAL}).", "green"
            ),
            ao_encontrar=self.mostrar_aviso_atualizacao,
            ao_falhar=lambda: self.mostrar_mensagem_temporaria(
                "Não foi possível verificar atualizações. Confira sua conexão.", "orange"
            ),
        )

    def mostrar_aviso_atualizacao(self, release):
        """Mostra a faixa de aviso e destaca o botão Atualizações."""
        self.release_disponivel = release
        aplicar_estilo_botao(self.btn_atualizar, "primario")
        self.btn_atualizar.configure(text=f"● Nova versão v{release['versao']}", width=170)
        self.atualizar_status(f"🔔 Nova versão v{release['versao']} disponível!", "blue")

        if self.versao_aviso_dispensado == release["versao"]:
            return
        self.label_aviso.configure(
            text=f"🔔  Nova versão v{release['versao']} disponível — "
                 f"você está usando a v{VERSAO_ATUAL}."
        )
        self.frame_aviso.grid()

    def baixar_atualizacao(self):
        """Abre a página da release no navegador."""
        if self.release_disponivel:
            webbrowser.open(self.release_disponivel["url"])

    def dispensar_aviso_atualizacao(self):
        """Esconde a faixa (o botão continua destacado)."""
        if self.release_disponivel:
            self.versao_aviso_dispensado = self.release_disponivel["versao"]
        self.frame_aviso.grid_remove()

    # ------------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------------
    def fechar_programa(self):
        """Fecha o programa e limpa arquivos temporários."""
        limpar_pasta_temp()
        self.janela.destroy()

    def executar(self):
        """Inicia a interface gráfica."""
        self.janela.mainloop()


if __name__ == "__main__":
    app = GeradorEmailGUI()
    app.executar()
