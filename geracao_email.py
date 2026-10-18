# -*- coding: utf-8 -*-
"""
MÓDULO DE GERAÇÃO DE E-MAIL
================================================================================
Valida o formulário, monta os HTMLs e abre no navegador.

- validar_formulario / normalizar_req / montar_emails: regras puras (testáveis)
- gerar_email: ligação com a interface (lê campos, salva e abre os arquivos)

Os arquivos ficam numa pasta temporária que é apagada ao fechar o programa.
"""

import logging
import os
import shutil
import tempfile
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from tkinter import messagebox

from area_transferencia import copiar_html, html_para_colar, texto_simples
from config import MAX_TELEFONES
from data_hora import formatar_data_hora
from email_html import (
    gerar_email_aviso_html,
    gerar_email_fechamento_html,
    gerar_nota_improdutivo_html,
)
from telefones import formatar_telefones
from tipo_email import TipoEmail

log = logging.getLogger(__name__)

# ============================================================================
# PASTA TEMPORÁRIA DO PROGRAMA
# ============================================================================
PASTA_TEMP = None


def obter_pasta_temp() -> str:
    """Retorna a pasta temporária do programa, criando se não existir"""
    global PASTA_TEMP
    if PASTA_TEMP is None:
        PASTA_TEMP = os.path.join(tempfile.gettempdir(), "gerador_email_hepta")
        os.makedirs(PASTA_TEMP, exist_ok=True)
    return PASTA_TEMP


def limpar_pasta_temp() -> None:
    """Remove todos os arquivos da pasta temporária"""
    global PASTA_TEMP
    if PASTA_TEMP and os.path.exists(PASTA_TEMP):
        try:
            shutil.rmtree(PASTA_TEMP)
            PASTA_TEMP = None
        except OSError as erro:
            log.warning("Erro ao limpar pasta temporária: %s", erro)


# ============================================================================
# REGRAS
# ============================================================================


@dataclass(frozen=True)
class ErroValidacao:
    status: str  # mensagem curta na barra de status
    detalhe: str  # mensagem da janela de erro


@dataclass(frozen=True)
class EmailGerado:
    nome_arquivo: str
    html: str


def normalizar_req(texto: str) -> tuple[str, str]:
    """
    Retorna (REQ completa, número) a partir do que foi digitado.

    "000123" -> ("REQ000123", "000123");  "req123" -> ("REQ123", "123")
    """
    texto = texto.strip()
    if texto.upper().startswith("REQ"):
        return texto.upper(), texto[3:]
    return f"REQ{texto}", texto


def validar_formulario(
    req: str, tipo: TipoEmail, telefones: list[str], nome: str
) -> ErroValidacao | None:
    """Retorna o primeiro problema encontrado no formulário, ou None se estiver ok."""
    if not req.strip():
        return ErroValidacao(
            "⚠️ Adicione a REQ para gerar o e-mail!", "Digite o número da requisição!"
        )

    if tipo.exige_telefone:
        if not telefones:
            return ErroValidacao(
                "⚠️ Adicione pelo menos um telefone!",
                "Adicione pelo menos um telefone (celular ou fixo)!",
            )
        if len(telefones) > MAX_TELEFONES:
            excesso = len(telefones) - MAX_TELEFONES
            return ErroValidacao(
                f"⚠️ Limite máximo de {MAX_TELEFONES} telefones excedido! (Atual: {len(telefones)})",
                f"Você adicionou {len(telefones)} telefones.\n\n"
                f"⚠️ O limite máximo permitido é {MAX_TELEFONES} telefones por chamado.\n\n"
                f"Remova {excesso} telefone(s) para continuar.",
            )

    if not nome.strip():
        return ErroValidacao(
            "⚠️ Informe o nome do funcionário!",
            "Informe o nome do funcionário que assina o e-mail.",
        )

    return None


def montar_emails(
    tipo: TipoEmail, req: str, nome: str, telefones: list[str], momento: datetime
) -> list[EmailGerado]:
    """Monta os arquivos HTML do e-mail (e a nota, no fechamento)."""
    req_completa, req_numero = normalizar_req(req)
    data_hora = formatar_data_hora(momento)
    nome = nome.strip()

    if tipo is TipoEmail.FECHAMENTO:
        titulo = f"{req_completa} - Chamado Fechado"
        return [
            EmailGerado(
                f"email_{req_numero}_{tipo.value}.html",
                gerar_email_fechamento_html(titulo, req_completa, nome, data_hora),
            ),
            EmailGerado(
                f"nota_improdutivo_{req_numero}.html",
                gerar_nota_improdutivo_html(req_completa),
            ),
        ]

    titulo = f"{req_completa} - {tipo.ordinal} aviso de tentativa de contato com o cliente"
    html = gerar_email_aviso_html(
        titulo, req_completa, nome, formatar_telefones(telefones), data_hora, tipo.value
    )
    return [EmailGerado(f"email_{req_numero}_{tipo.value}.html", html)]


# ============================================================================
# LIGAÇÃO COM A INTERFACE
# ============================================================================


@dataclass(frozen=True)
class Preparado:
    tipo: TipoEmail
    nome: str
    momento: datetime
    emails: list[EmailGerado]


def _preparar(gui, obter_telefones_func) -> Preparado | None:
    """Lê e valida o formulário e monta os e-mails; mostra o erro e retorna None se houver."""
    tipo = TipoEmail(gui.tipo_email.get())
    req = gui.entry_req.get().strip()
    nome = gui.entry_nome.get().strip()
    telefones = obter_telefones_func(gui) if tipo.exige_telefone else []

    erro = validar_formulario(req, tipo, telefones, nome)
    if erro:
        gui.atualizar_status(erro.status, "orange")
        messagebox.showerror("Erro", erro.detalhe)
        return None

    # Data e hora: horário do momento da geração (automático) ou manual
    try:
        momento = gui.obter_data_hora_contato()
    except ValueError as e:
        gui.atualizar_status(f"⚠️ {e}", "orange")
        messagebox.showerror("Erro", f"{e}\n\nVerifique a data e o horário do contato.")
        return None

    return Preparado(tipo, nome, momento, montar_emails(tipo, req, nome, telefones, momento))


def _salvar_e_abrir(emails: list[EmailGerado]) -> None:
    """Grava os HTMLs na pasta temporária e abre cada um no navegador."""
    pasta_temp = obter_pasta_temp()
    caminhos = []
    for email in emails:
        caminho = os.path.join(pasta_temp, email.nome_arquivo)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(email.html)
        caminhos.append(caminho)
    for caminho in caminhos:
        webbrowser.open(f"file://{caminho}")


def gerar_email(gui, obter_telefones_func) -> None:
    """Gera o e-mail com os dados do formulário e abre no navegador."""
    preparado = _preparar(gui, obter_telefones_func)
    if not preparado:
        return

    try:
        if preparado.tipo is TipoEmail.FECHAMENTO:
            gui.atualizar_status(
                f"🔒 E-mail de FECHAMENTO gerado e nota improdutivo salva em "
                f"{preparado.emails[1].nome_arquivo}",
                "blue",
            )
        else:
            gui.atualizar_status(
                f"🌐 E-mail aberto no navegador (contato: "
                f"{formatar_data_hora(preparado.momento)}). "
                f"Pressione Ctrl+A, Ctrl+C, Ctrl+V para copiar.",
                "blue",
            )
        _salvar_e_abrir(preparado.emails)
        gui.lembrar_funcionario(preparado.nome)

    except Exception as e:
        log.exception("Erro ao gerar/abrir o e-mail")
        gui.atualizar_status(f"❌ Erro ao abrir e-mail: {str(e)}", "red")
        messagebox.showerror(
            "Erro", f"Não foi possível abrir o e-mail no navegador.\n\nErro: {str(e)}"
        )


def copiar_email(gui, obter_telefones_func) -> None:
    """
    Gera o e-mail e copia direto para a área de transferência (sem navegador).
    No fechamento, a nota de improdutivo ainda abre no navegador.
    """
    preparado = _preparar(gui, obter_telefones_func)
    if not preparado:
        return

    email = preparado.emails[0]
    try:
        fragmento = html_para_colar(email.html)
        copiar_html(fragmento, texto_simples(fragmento))
    except Exception as e:
        log.exception("Erro ao copiar o e-mail")
        gui.atualizar_status(f"❌ Não foi possível copiar: {e}", "red")
        messagebox.showerror(
            "Erro",
            f"Não foi possível copiar o e-mail.\n\nErro: {e}\n\n"
            "Use o botão Gerar e-mail e copie pelo navegador.",
        )
        return

    if preparado.tipo is TipoEmail.FECHAMENTO:
        try:
            _salvar_e_abrir(preparado.emails[1:])
        except Exception:
            log.exception("Erro ao abrir a nota de improdutivo")
        gui.atualizar_status(
            "📋 E-mail de fechamento copiado! Cole com Ctrl+V. A nota abriu no navegador.",
            "blue",
        )
    else:
        gui.atualizar_status(
            f"📋 E-mail copiado (contato: {formatar_data_hora(preparado.momento)})! "
            "Cole no e-mail corporativo com Ctrl+V.",
            "blue",
        )
    gui.lembrar_funcionario(preparado.nome)
