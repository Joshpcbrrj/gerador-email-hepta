# -*- coding: utf-8 -*-
"""
COPIAR E-MAIL PARA A ÁREA DE TRANSFERÊNCIA
================================================================================
Alternativa ao "abrir no navegador + Ctrl+A + Ctrl+C": coloca o e-mail
direto na área de transferência do Windows, no mesmo formato que o navegador
usa ao copiar (CF_HTML), pronto para Ctrl+V no e-mail corporativo.

O que vai para a área de transferência é só o e-mail: sem a caixa
"Como copiar este e-mail" e sem o rodapé de créditos. Os estilos CSS são
aplicados direto em cada elemento (como o navegador faz ao copiar), para
que a formatação sobreviva à colagem.
"""

import ctypes
import html as html_lib
import re
import sys
import time

# ============================================================================
# PREPARAÇÃO DO HTML (funções puras)
# ============================================================================


def _regras_css(html: str) -> dict[str, str]:
    """Lê o <style> do e-mail: {'.titulo': 'font-size: 14pt; ...', '.legenda img': ...}."""
    estilo = re.search(r"<style>(.*?)</style>", html, re.S)
    regras = {}
    for seletor, corpo in re.findall(r"([^{}]+)\{([^{}]*)\}", estilo.group(1) if estilo else ""):
        declaracoes = "; ".join(d.strip() for d in corpo.split(";") if d.strip())
        regras[" ".join(seletor.split())] = declaracoes
    return regras


def _remover_div(html: str, classe: str) -> str:
    """Remove <div class="classe">...</div> (blocos sem divs internas)."""
    return re.sub(rf'\s*<div class="{classe}">.*?</div>', "", html, flags=re.S)


def html_para_colar(html_email: str) -> str:
    """Corpo do e-mail com estilos embutidos, sem instruções e sem créditos."""
    regras = _regras_css(html_email)
    corpo = re.search(r'<div class="container">(.*)</div>\s*</body>', html_email, re.S).group(1)
    corpo = _remover_div(corpo, "dica-copy")
    corpo = _remover_div(corpo, "creditos")

    # ".classe img { ... }": estilo das imagens dentro do bloco
    for seletor, declaracoes in regras.items():
        m = re.fullmatch(r"\.([\w-]+) img", seletor)
        if m:
            corpo = re.sub(
                rf'(<div class="{m.group(1)}">.*?)<img ',
                lambda achado, d=declaracoes: f'{achado.group(1)}<img style="{d}" ',
                corpo,
                flags=re.S,
            )

    # ".classe { ... }": troca class="..." pelo estilo correspondente
    def aplicar(achado: re.Match) -> str:
        declaracoes = regras.get(f".{achado.group(1)}")
        return f' style="{declaracoes}"' if declaracoes else ""

    corpo = re.sub(r' class="([\w-]+)"', aplicar, corpo)

    # Do <body>, só o que é do texto (margem e fundo são da página do navegador)
    estilo_corpo = "; ".join(
        d
        for d in regras.get("body", "").split("; ")
        if d.split(":")[0] in ("font-family", "font-size", "line-height", "color")
    )
    return f'<div style="{estilo_corpo}">{corpo.strip()}</div>'


def texto_simples(html: str) -> str:
    """Versão em texto puro (para destinos que não aceitam HTML)."""
    texto = re.sub(r"<(br|/p|/div)\s*/?>", "\n", html, flags=re.I)
    texto = html_lib.unescape(re.sub(r"<[^>]+>", "", texto))
    linhas = [" ".join(linha.split()) for linha in texto.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(linhas)).strip()


def montar_cf_html(fragmento: str) -> bytes:
    """
    Monta o formato "HTML Format" do Windows: um cabeçalho com as posições
    (em bytes UTF-8) do documento e do trecho copiado.
    """
    cabecalho = (
        "Version:0.9\r\n"
        "StartHTML:{:010d}\r\n"
        "EndHTML:{:010d}\r\n"
        "StartFragment:{:010d}\r\n"
        "EndFragment:{:010d}\r\n"
    )
    antes = '<html><head><meta charset="utf-8"></head><body>\r\n<!--StartFragment-->'
    depois = "<!--EndFragment-->\r\n</body></html>"

    tamanho_cabecalho = len(cabecalho.format(0, 0, 0, 0).encode("utf-8"))
    inicio_html = tamanho_cabecalho
    inicio_fragmento = inicio_html + len(antes.encode("utf-8"))
    fim_fragmento = inicio_fragmento + len(fragmento.encode("utf-8"))
    fim_html = fim_fragmento + len(depois.encode("utf-8"))

    return (
        cabecalho.format(inicio_html, fim_html, inicio_fragmento, fim_fragmento)
        + antes
        + fragmento
        + depois
    ).encode("utf-8")


# ============================================================================
# ÁREA DE TRANSFERÊNCIA DO WINDOWS
# ============================================================================

CF_UNICODETEXT = 13
GMEM_MOVEABLE = 0x0002


def _api():
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    vp, ui = ctypes.c_void_p, ctypes.c_uint
    kernel32.GlobalAlloc.argtypes, kernel32.GlobalAlloc.restype = [ui, ctypes.c_size_t], vp
    kernel32.GlobalLock.argtypes, kernel32.GlobalLock.restype = [vp], vp
    kernel32.GlobalUnlock.argtypes = [vp]
    kernel32.GlobalFree.argtypes = [vp]
    user32.OpenClipboard.argtypes = [vp]
    user32.SetClipboardData.argtypes, user32.SetClipboardData.restype = [ui, vp], vp
    user32.RegisterClipboardFormatW.argtypes = [ctypes.c_wchar_p]
    user32.RegisterClipboardFormatW.restype = ui
    return user32, kernel32


def _colocar(user32, kernel32, formato: int, dados: bytes) -> None:
    memoria = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(dados))
    if not memoria:
        raise OSError("Sem memória para a área de transferência")
    ponteiro = kernel32.GlobalLock(memoria)
    ctypes.memmove(ponteiro, dados, len(dados))
    kernel32.GlobalUnlock(memoria)
    if not user32.SetClipboardData(formato, memoria):
        kernel32.GlobalFree(memoria)
        raise OSError("Não foi possível gravar na área de transferência")


def copiar_html(fragmento: str, texto: str) -> None:
    """Coloca o HTML (com texto puro como alternativa) na área de transferência."""
    if sys.platform != "win32":
        raise OSError("Copiar e-mail está disponível apenas no Windows")

    user32, kernel32 = _api()
    for _ in range(10):  # outro programa pode estar usando a área de transferência
        if user32.OpenClipboard(None):
            break
        time.sleep(0.05)
    else:
        raise OSError("A área de transferência está em uso por outro programa")

    try:
        user32.EmptyClipboard()
        formato_html = user32.RegisterClipboardFormatW("HTML Format")
        _colocar(user32, kernel32, formato_html, montar_cf_html(fragmento) + b"\0")
        _colocar(user32, kernel32, CF_UNICODETEXT, (texto + "\0").encode("utf-16-le"))
    finally:
        user32.CloseClipboard()
