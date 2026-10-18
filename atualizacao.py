# -*- coding: utf-8 -*-
"""
MÓDULO DE AUTO-UPDATE
================================================================================
Gerencia a verificação de atualizações no GitHub.

- Verificação automática ao abrir o programa e periodicamente (sem popup:
  a interface mostra uma faixa de aviso quando há versão nova).
- Verificação manual pelo botão "Atualizações".

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import json
import logging
import re
import urllib.request
import webbrowser
from threading import Thread
from tkinter import messagebox

# Importa as configurações do arquivo config.py
from config import GITHUB_API_URL, VERSAO_ATUAL

log = logging.getLogger(__name__)


def versao_para_tupla(versao: str | None) -> tuple[int, ...]:
    """Converte '2.10' / 'v2.6.1' em (2, 10) / (2, 6, 1) para comparar numericamente."""
    return tuple(int(n) for n in re.findall(r"\d+", versao or ""))


def versao_mais_nova(remota: str | None, atual: str = VERSAO_ATUAL) -> bool:
    """True se a versão remota for maior que a atual (comparação numérica)."""
    remota_t = versao_para_tupla(remota)
    return bool(remota_t) and remota_t > versao_para_tupla(atual)


def consultar_ultima_release() -> dict:
    """
    Consulta a API do GitHub e retorna um dict com
    'versao', 'url' e 'notas' da última release.
    Lança exceção em caso de erro de rede.
    """
    req = urllib.request.Request(GITHUB_API_URL)
    req.add_header("User-Agent", "GeradorEmailHepta")

    with urllib.request.urlopen(req, timeout=5) as response:
        dados = json.loads(response.read().decode("utf-8"))

    return {
        "versao": dados.get("tag_name", "").lstrip("vV"),
        "url": dados.get("html_url", ""),
        "notas": dados.get("body") or "Sem notas de versão disponíveis.",
    }


def perguntar_download(parent_window, release):
    """Popup perguntando se o usuário quer abrir a página de download."""
    resposta = messagebox.askyesno(
        "🔄 Atualização Disponível",
        f"Uma nova versão está disponível!\n\n"
        f"Versão atual: {VERSAO_ATUAL}\n"
        f"Nova versão: {release['versao']}\n\n"
        f"Notas da versão:\n{release['notas'][:300]}...\n\n"
        f"Deseja abrir a página de download?",
        parent=parent_window,
    )
    if resposta:
        webbrowser.open(release["url"])


def verificar_atualizacao(
    parent_window, callback=None, ao_encontrar=None, silencioso=False, ao_falhar=None
):
    """
    Verifica se há uma nova versão disponível no GitHub (em thread separada).

    Parâmetros:
    - parent_window: janela principal (para exibir o popup / agendar callbacks)
    - callback: chamado quando o programa já está na versão mais recente
    - ao_encontrar: chamado com o dict da release quando há versão nova
    - silencioso: se True, não abre popup (usado na verificação automática)
    - ao_falhar: chamado em caso de erro (sem internet, API offline, etc.).
      Se não for informado, o callback é usado no lugar.
    """

    def verificar():
        try:
            release = consultar_ultima_release()

            if versao_mais_nova(release["versao"]):
                if ao_encontrar:
                    parent_window.after(0, lambda: ao_encontrar(release))
                if not silencioso:
                    parent_window.after(0, lambda: perguntar_download(parent_window, release))
            elif callback:
                parent_window.after(0, callback)

        except Exception as e:
            log.warning("Erro ao verificar atualização: %s", e)
            tratar_erro = ao_falhar or callback
            if tratar_erro:
                parent_window.after(0, tratar_erro)

    thread = Thread(target=verificar)
    thread.daemon = True
    thread.start()
