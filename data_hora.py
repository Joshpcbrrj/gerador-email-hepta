# -*- coding: utf-8 -*-
"""
MÓDULO DE DATA E HORA DO CONTATO
================================================================================
Resolve a data/hora que vai no e-mail.

- Modo automático: usa o horário do momento em que o e-mail é GERADO
  (e não o horário em que o programa foi aberto).
- Modo manual: usa exatamente os valores escolhidos nos campos.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

from datetime import datetime


def resolver_data_hora(automatico, dia, mes, ano, hora, minuto, agora=None):
    """
    Retorna um datetime com a data/hora do contato.

    Parâmetros:
    - automatico: True para usar o horário atual
    - dia, mes, ano, hora, minuto: valores (str ou int) dos campos manuais
    - agora: datetime de referência (usado nos testes)

    Lança ValueError se a data manual for inválida (ex: 31/02).
    """
    if automatico:
        return (agora or datetime.now()).replace(second=0, microsecond=0)

    try:
        return datetime(int(ano), int(mes), int(dia), int(hora), int(minuto))
    except (TypeError, ValueError):
        raise ValueError(
            f"Data/hora inválida: {str(dia).zfill(2)}/{str(mes).zfill(2)}/{ano} "
            f"{str(hora).zfill(2)}:{str(minuto).zfill(2)}"
        )


def formatar_data_hora(momento):
    """Formata no padrão dos e-mails: 'DD/MM/AAAA às HH:MM BRT'."""
    return f"{momento.strftime('%d/%m/%Y')} às {momento.strftime('%H:%M')} BRT"
