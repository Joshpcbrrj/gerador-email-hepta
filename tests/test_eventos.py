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
    limpar_listas
)


class TestMensagensTemporarias:
    """Testes para mensagens temporárias"""
    
    def test_mostrar_mensagem_temporaria(self):
        mock_gui = MagicMock()
        mock_gui.timer_mensagem = None
        mock_gui.janela = MagicMock()
        mock_gui.status_label = MagicMock()
        
        mostrar_mensagem_temporaria(mock_gui, "Teste", "green")
        
        mock_gui.status_label.config.assert_called_once_with(text="Teste", fg="green")
    
    def test_mensagem_cancela_timer_anterior(self):
        mock_gui = MagicMock()
        mock_gui.timer_mensagem = 123
        mock_gui.janela = MagicMock()
        mock_gui.status_label = MagicMock()
        
        mostrar_mensagem_temporaria(mock_gui, "Nova mensagem", "blue")
        
        mock_gui.janela.after_cancel.assert_called_once_with(123)


class TestObterTelefones:
    """Testes para obter telefones da lista"""
    
    def test_obter_telefones_lista_vazia(self):
        mock_gui = MagicMock()
        mock_gui.lista_telefones = MagicMock()
        mock_gui.lista_telefones.get.return_value = []
        
        resultado = obter_todos_telefones(mock_gui)
        assert resultado == []
    
    def test_obter_telefones_remove_emoji(self):
        """Teste: verifica que remove o emoji (qualquer que seja o formato)"""
        mock_gui = MagicMock()
        mock_gui.lista_telefones = MagicMock()
        # Simula o formato real que está na lista
        mock_gui.lista_telefones.get.return_value = ["📞 (11) 99999-9999"]
        
        resultado = obter_todos_telefones(mock_gui)
        # O importante é que o emoji foi removido
        assert "📞" not in resultado[0]
    
    def test_obter_telefones_funciona_com_qualquer_formato(self):
        """Teste: função deve funcionar com qualquer formato de telefone"""
        mock_gui = MagicMock()
        mock_gui.lista_telefones = MagicMock()
        
        # Testa com diferentes formatos
        telefones_teste = [
            "📞 (11) 99999-9999",
            "🏠 (21) 3376-3562",
            "📞 119991234567",
            "🏠 2133763562"
        ]
        
        mock_gui.lista_telefones.get.return_value = telefones_teste
        
        resultado = obter_todos_telefones(mock_gui)
        
        # Verifica que todos os emojis foram removidos
        for item in resultado:
            assert "📞" not in item
            assert "🏠" not in item
        
        # Verifica que a quantidade de itens é a mesma
        assert len(resultado) == len(telefones_teste)


class TestAdicionarTelefone:
    """Testes para adicionar telefones"""
    
    def test_adicionar_celular_com_telefone_valido(self):
        mock_gui = MagicMock()
        mock_gui.entry_telefone = MagicMock()
        mock_gui.entry_telefone.get.return_value = "119991234567"
        mock_gui.lista_telefones = MagicMock()
        mock_gui.timer_mensagem = None
        mock_gui.janela = MagicMock()
        mock_gui.status_label = MagicMock()
        
        with patch('eventos.formatar_celular', return_value="(11) 99912-3456"):
            adicionar_celular(mock_gui)
            mock_gui.lista_telefones.insert.assert_called_once()
    
    def test_adicionar_celular_sem_telefone(self):
        mock_gui = MagicMock()
        mock_gui.entry_telefone = MagicMock()
        mock_gui.entry_telefone.get.return_value = ""
        
        with patch('eventos.messagebox') as mock_messagebox:
            adicionar_celular(mock_gui)
            mock_messagebox.showwarning.assert_called_once()


class TestRemoverTelefone:
    """Testes para remover telefones"""
    
    def test_remover_telefone_selecionado(self):
        mock_gui = MagicMock()
        mock_gui.lista_telefones = MagicMock()
        mock_gui.lista_telefones.curselection.return_value = (0,)
        mock_gui.lista_telefones.get.return_value = "📞 (11) 99999-9999"
        mock_gui.timer_mensagem = None
        mock_gui.janela = MagicMock()
        mock_gui.status_label = MagicMock()
        
        remover_telefone(mock_gui)
        
        mock_gui.lista_telefones.delete.assert_called()
    
    def test_remover_telefone_sem_selecao(self):
        mock_gui = MagicMock()
        mock_gui.lista_telefones = MagicMock()
        mock_gui.lista_telefones.curselection.return_value = ()
        
        with patch('eventos.messagebox') as mock_messagebox:
            remover_telefone(mock_gui)
            mock_messagebox.showwarning.assert_called_once()


class TestLimparListas:
    """Testes para limpar listas"""
    
    def test_limpar_listas(self):
        mock_gui = MagicMock()
        mock_gui.lista_telefones = MagicMock()
        mock_gui.entry_telefone = MagicMock()
        mock_gui.timer_mensagem = None
        mock_gui.janela = MagicMock()
        mock_gui.status_label = MagicMock()
        
        limpar_listas(mock_gui)
        
        mock_gui.lista_telefones.delete.assert_called()
        mock_gui.entry_telefone.delete.assert_called()