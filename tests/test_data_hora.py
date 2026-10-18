# -*- coding: utf-8 -*-
"""
TESTES PARA DATA E HORA DO CONTATO
================================================================================
Garante que o modo automático usa o horário do momento da geração
(e não o da abertura do programa) e que o modo manual é respeitado.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from unittest.mock import patch

import pytest
from data_hora import resolver_data_hora, formatar_data_hora


class TestModoAutomatico:

    def test_usa_horario_do_momento_da_geracao(self):
        """Campos mostrando 10:00 (abertura) não importam no modo automático."""
        agora = datetime(2026, 10, 17, 12, 34, 56)
        momento = resolver_data_hora(True, "17", "10", "2026", "10", "00", agora=agora)
        assert momento == datetime(2026, 10, 17, 12, 34)

    def test_consulta_relogio_a_cada_chamada(self):
        """Duas gerações em horários diferentes trazem horários diferentes."""
        with patch("data_hora.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 10, 17, 10, 0)
            primeira = resolver_data_hora(True, "", "", "", "", "")
            mock_dt.now.return_value = datetime(2026, 10, 17, 12, 0)
            segunda = resolver_data_hora(True, "", "", "", "", "")
        assert primeira.hour == 10
        assert segunda.hour == 12

    def test_virada_de_dia(self):
        """Programa aberto antes da meia-noite: a data também acompanha."""
        agora = datetime(2026, 10, 18, 0, 5)
        momento = resolver_data_hora(True, "17", "10", "2026", "23", "50", agora=agora)
        assert momento.day == 18


class TestModoManual:

    def test_usa_valores_escolhidos(self):
        momento = resolver_data_hora(False, "05", "03", "2026", "09", "07")
        assert momento == datetime(2026, 3, 5, 9, 7)

    def test_data_invalida_lanca_erro(self):
        with pytest.raises(ValueError) as erro:
            resolver_data_hora(False, "31", "02", "2026", "10", "00")
        assert "31/02/2026" in str(erro.value)

    def test_campo_vazio_lanca_erro(self):
        with pytest.raises(ValueError):
            resolver_data_hora(False, "", "02", "2026", "10", "00")


class TestFormatacao:

    def test_formato_do_email(self):
        assert formatar_data_hora(datetime(2026, 1, 2, 3, 4)) == "02/01/2026 às 03:04 BRT"
