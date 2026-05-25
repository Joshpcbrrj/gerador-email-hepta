# -*- coding: utf-8 -*-
"""
TESTES PARA EVENTOS
================================================================================
Testa as funções de eventos (mock da interface).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import MagicMock, patch
from eventos import (
    mostrar_mensagem_temporaria,
    obter_todos_telefones,
    adicionar_celular,
    adicionar_fixo,
    remover_telefone,
    limpar_listas,
)


class TestMensagensTemporarias:
    """Testes para mensagens temporárias"""

    def test_mostrar_mensagem_temporaria(self):
        mock_gui = MagicMock()
        mock_gui.timer_mensagem = None
        mock_gui.janela = MagicMock()
        mock_gui.status_label = MagicMock()
        mock_gui.tema_manager = MagicMock()
        mock_gui.tema_manager.cor_status.return_value = "#2e7d32"

        mostrar_mensagem_temporaria(mock_gui, "Teste", "green")

        mock_gui.status_label.configure.assert_called_once_with(
            text="Teste", text_color="#2e7d32"
        )

    def test_mensagem_cancela_timer_anterior(self):
        mock_gui = MagicMock()
        mock_gui.timer_mensagem = 123
        mock_gui.janela = MagicMock()
        mock_gui.status_label = MagicMock()
        mock_gui.tema_manager = MagicMock()
        mock_gui.tema_manager.cor_status.return_value = "#1565c0"

        mostrar_mensagem_temporaria(mock_gui, "Nova mensagem", "blue")

        mock_gui.janela.after_cancel.assert_called_once_with(123)


class TestObterTelefones:
    """Testes para obter telefones da lista"""

    def test_obter_telefones_lista_vazia(self):
        mock_gui = MagicMock()
        mock_gui.telefones = []

        resultado = obter_todos_telefones(mock_gui)
        assert resultado == []

    def test_obter_telefones_remove_emoji(self):
        mock_gui = MagicMock()
        mock_gui.telefones = ["📞 (11) 99999-9999"]

        resultado = obter_todos_telefones(mock_gui)
        assert "📞" not in resultado[0]
        assert resultado[0] == "(11) 99999-9999"

    def test_obter_telefones_funciona_com_qualquer_formato(self):
        mock_gui = MagicMock()
        telefones_teste = [
            "📞 (11) 99999-9999",
            "🏠 (21) 3376-3562",
            "📞 119991234567",
            "🏠 2133763562",
        ]
        mock_gui.telefones = telefones_teste

        resultado = obter_todos_telefones(mock_gui)

        for item in resultado:
            assert "📞" not in item
            assert "🏠" not in item

        assert len(resultado) == len(telefones_teste)


class TestAdicionarTelefone:
    """Testes para adicionar telefones"""

    def test_adicionar_celular_com_telefone_valido(self):
        mock_gui = MagicMock()
        mock_gui.entry_telefone = MagicMock()
        mock_gui.entry_telefone.get.return_value = "119991234567"
        mock_gui.tema_manager = MagicMock()
        mock_gui.timer_mensagem = None
        mock_gui.janela = MagicMock()
        mock_gui.status_label = MagicMock()
        mock_gui.tema_manager.cor_status.return_value = "#2e7d32"

        with patch("eventos.formatar_celular", return_value="(11) 99912-3456"):
            with patch("eventos.adicionar_telefone_lista") as mock_add:
                adicionar_celular(mock_gui)
                mock_add.assert_called_once()

    def test_adicionar_celular_sem_telefone(self):
        mock_gui = MagicMock()
        mock_gui.entry_telefone = MagicMock()
        mock_gui.entry_telefone.get.return_value = ""

        with patch("eventos.messagebox") as mock_messagebox:
            adicionar_celular(mock_gui)
            mock_messagebox.showwarning.assert_called_once()


class TestRemoverTelefone:
    """Testes para remover telefones"""

    def test_remover_telefone_selecionado(self):
        mock_gui = MagicMock()
        mock_gui.tema_manager = MagicMock()
        mock_gui.timer_mensagem = None
        mock_gui.janela = MagicMock()
        mock_gui.status_label = MagicMock()
        mock_gui.tema_manager.cor_status.return_value = "#ef6c00"

        with patch("eventos.remover_telefone_selecionado", return_value="📞 (11) 99999-9999"):
            remover_telefone(mock_gui)

    def test_remover_telefone_sem_selecao(self):
        mock_gui = MagicMock()
        mock_gui.tema_manager = MagicMock()

        with patch("eventos.remover_telefone_selecionado", return_value=None):
            with patch("eventos.messagebox") as mock_messagebox:
                remover_telefone(mock_gui)
                mock_messagebox.showwarning.assert_called_once()


class TestLimparListas:
    """Testes para limpar listas"""

    def test_limpar_listas(self):
        mock_gui = MagicMock()
        mock_gui.tema_manager = MagicMock()
        mock_gui.entry_telefone = MagicMock()
        mock_gui.timer_mensagem = None
        mock_gui.janela = MagicMock()
        mock_gui.status_label = MagicMock()
        mock_gui.tema_manager.cor_status.return_value = "#ef6c00"

        with patch("eventos.limpar_lista_telefones") as mock_limpar:
            limpar_listas(mock_gui)
            mock_limpar.assert_called_once_with(mock_gui, mock_gui.tema_manager)
            mock_gui.entry_telefone.delete.assert_called()
