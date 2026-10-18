# -*- coding: utf-8 -*-
"""
TIPOS DE E-MAIL
================================================================================
Os quatro tipos de e-mail e os textos associados a cada um.

Os valores ("1" a "4") são os mesmos usados no nome dos arquivos gerados
(ex: email_000008198188_1.html), por isso não devem mudar.
"""

from enum import StrEnum


class TipoEmail(StrEnum):
    AVISO_1 = "1"
    AVISO_2 = "2"
    AVISO_3 = "3"
    FECHAMENTO = "4"

    @property
    def rotulo(self) -> str:
        """Texto do botão na interface."""
        return _ROTULOS[self]

    @property
    def descricao(self) -> str:
        """Explicação curta exibida abaixo dos botões."""
        return _DESCRICOES[self]

    @property
    def ordinal(self) -> str:
        """'1º', '2º', '3º' (apenas avisos)."""
        return f"{self.value}º"

    @property
    def extenso(self) -> str:
        """'primeira', 'segunda', 'terceira' (apenas avisos)."""
        return _EXTENSO[self]

    @property
    def exige_telefone(self) -> bool:
        return self is not TipoEmail.FECHAMENTO


_ROTULOS = {
    TipoEmail.AVISO_1: "1º Aviso",
    TipoEmail.AVISO_2: "2º Aviso",
    TipoEmail.AVISO_3: "3º Aviso",
    TipoEmail.FECHAMENTO: "Fechamento",
}

_DESCRICOES = {
    TipoEmail.AVISO_1: "Primeira tentativa de contato sem sucesso.",
    TipoEmail.AVISO_2: "Segunda tentativa de contato sem sucesso.",
    TipoEmail.AVISO_3: "Terceira tentativa — último aviso antes do fechamento.",
    TipoEmail.FECHAMENTO: "Fecha como improdutivo e abre também a nota. "
    "Telefones não são obrigatórios.",
}

_EXTENSO = {
    TipoEmail.AVISO_1: "primeira",
    TipoEmail.AVISO_2: "segunda",
    TipoEmail.AVISO_3: "terceira",
    TipoEmail.FECHAMENTO: "",
}
