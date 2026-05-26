# -*- coding: utf-8 -*-
"""
TESTES PARA GERAÇÃO DE E-MAIL
================================================================================
Testa as funções de geração de HTML dos e-mails.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from email_html import gerar_email_aviso_html, gerar_email_fechamento_html
from geracao_email import gerar_nota_improdutivo_html


class TestEmailAviso:
    """Testes para geração do e-mail de aviso"""
    
    def test_email_aviso_contem_titulo(self):
        """Teste: e-mail de aviso contém o título correto"""
        html = gerar_email_aviso_html(
            "REQ123 - 1º aviso",
            "REQ123",
            "Josué B. Almeida",
            "(11) 99999-9999",
            "21/05/2026 às 14:00 BRT",
            "1"
        )
        assert "REQ123 - 1º aviso" in html
    
    def test_email_aviso_contem_saudacao(self):
        """Teste: e-mail de aviso contém saudação ao cliente"""
        html = gerar_email_aviso_html(
            "REQ123 - 1º aviso",
            "REQ123",
            "Josué B. Almeida",
            "(11) 99999-9999",
            "21/05/2026 às 14:00 BRT",
            "1"
        )
        assert "Prezado Cliente" in html
    
    def test_email_aviso_contem_instrucao_accept(self):
        """Teste: e-mail de aviso contém instrução para clicar em ACCEPT"""
        html = gerar_email_aviso_html(
            "REQ123 - 1º aviso",
            "REQ123",
            "Josué B. Almeida",
            "(11) 99999-9999",
            "21/05/2026 às 14:00 BRT",
            "1"
        )
        assert "ACCEPT" in html
    
    def test_email_aviso_contem_assinatura(self):
        """Teste: e-mail de aviso contém assinatura do funcionário"""
        html = gerar_email_aviso_html(
            "REQ123 - 1º aviso",
            "REQ123",
            "Josué B. Almeida",
            "(11) 99999-9999",
            "21/05/2026 às 14:00 BRT",
            "1"
        )
        assert "Josué B. Almeida" in html
        assert "Suporte Técnico II - Hepta" in html
    
    def test_email_aviso_contem_telefone(self):
        """Teste: e-mail de aviso contém o telefone informado"""
        html = gerar_email_aviso_html(
            "REQ123 - 1º aviso",
            "REQ123",
            "Josué B. Almeida",
            "(11) 99999-9999",
            "21/05/2026 às 14:00 BRT",
            "1"
        )
        assert "(11) 99999-9999" in html
    
    def test_email_aviso_tentativa_primeira(self):
        """Teste: e-mail de 1º aviso menciona 'primeira tentativa'"""
        html = gerar_email_aviso_html(
            "REQ123 - 1º aviso",
            "REQ123",
            "Josué B. Almeida",
            "(11) 99999-9999",
            "21/05/2026 às 14:00 BRT",
            "1"
        )
        assert "primeira tentativa" in html
    
    def test_email_aviso_tentativa_segunda(self):
        """Teste: e-mail de 2º aviso menciona 'segunda tentativa'"""
        html = gerar_email_aviso_html(
            "REQ123 - 2º aviso",
            "REQ123",
            "Josué B. Almeida",
            "(11) 99999-9999",
            "21/05/2026 às 14:00 BRT",
            "2"
        )
        assert "segunda tentativa" in html
    
    def test_email_aviso_tentativa_terceira(self):
        """Teste: e-mail de 3º aviso menciona 'terceira tentativa'"""
        html = gerar_email_aviso_html(
            "REQ123 - 3º aviso",
            "REQ123",
            "Josué B. Almeida",
            "(11) 99999-9999",
            "21/05/2026 às 14:00 BRT",
            "3"
        )
        assert "terceira tentativa" in html


class TestEmailFechamento:
    """Testes para geração do e-mail de fechamento"""
    
    def test_email_fechamento_contem_titulo(self):
        """Teste: e-mail de fechamento contém o título correto"""
        html = gerar_email_fechamento_html(
            "REQ123 - Chamado Fechado",
            "REQ123",
            "Josué B. Almeida",
            "21/05/2026 às 14:00 BRT"
        )
        assert "Chamado Fechado" in html
    
    def test_email_fechamento_contem_palavra_improdutivo(self):
        """Teste: e-mail de fechamento menciona 'improdutivo'"""
        html = gerar_email_fechamento_html(
            "REQ123 - Chamado Fechado",
            "REQ123",
            "Josué B. Almeida",
            "21/05/2026 às 14:00 BRT"
        )
        assert "improdutivo" in html
    
    def test_email_fechamento_contem_aviso_reabertura(self):
        """Teste: e-mail de fechamento contém aviso sobre reabertura indevida"""
        html = gerar_email_fechamento_html(
            "REQ123 - Chamado Fechado",
            "REQ123",
            "Josué B. Almeida",
            "21/05/2026 às 14:00 BRT"
        )
        assert "reabertura" in html
        assert "indevida" in html
    
    def test_email_fechamento_nao_tem_imagem_winvnc(self):
        """Teste: e-mail de fechamento NÃO contém imagem do WinVNC"""
        html = gerar_email_fechamento_html(
            "REQ123 - Chamado Fechado",
            "REQ123",
            "Josué B. Almeida",
            "21/05/2026 às 14:00 BRT"
        )
        assert "imagem-winvnc" not in html
        assert "WinVNC" not in html or "winvnc" not in html.lower()
    
    def test_email_fechamento_contem_agradecimento(self):
        """Teste: e-mail de fechamento contém agradecimento"""
        html = gerar_email_fechamento_html(
            "REQ123 - Chamado Fechado",
            "REQ123",
            "Josué B. Almeida",
            "21/05/2026 às 14:00 BRT"
        )
        assert "agradecemos" in html or "compreensão" in html


def test_nota_improdutivo_html_contem_texto_basico():
    html = gerar_nota_improdutivo_html("REQ123")
    assert "IMPRODUTIVO" in html
    assert "Foram realizadas 3 tentativas de contato" in html
    assert "reabertura será considerada indevida" in html


def test_nota_improdutivo_html_contem_titulo_fixo():
    html = gerar_nota_improdutivo_html("REQ123")
    assert "Nota de Chamado Improdutivo - E-mail fechamento chamado" in html
