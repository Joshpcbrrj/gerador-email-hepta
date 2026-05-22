# -*- coding: utf-8 -*-
"""
TESTES PARA PASTA TEMPORÁRIA
================================================================================
Testa as funções de gerenciamento da pasta temporária.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import tempfile
from unittest.mock import MagicMock, patch


class TestPastaTemporaria:
    """Testes para gerenciamento da pasta temporária"""
    
    def test_obter_pasta_temp_cria_pasta(self):
        """Teste: obter_pasta_temp cria a pasta se não existir"""
        from geracao_email import obter_pasta_temp, limpar_pasta_temp
        
        # Limpar primeiro
        limpar_pasta_temp()
        
        # Obter pasta
        pasta = obter_pasta_temp()
        
        # Verificar que a pasta foi criada
        assert os.path.exists(pasta)
        assert "gerador_email_hepta" in pasta
    
    def test_obter_pasta_temp_mesma_pasta(self):
        """Teste: chamadas sucessivas retornam a mesma pasta"""
        from geracao_email import obter_pasta_temp, limpar_pasta_temp
        
        limpar_pasta_temp()
        
        pasta1 = obter_pasta_temp()
        pasta2 = obter_pasta_temp()
        
        assert pasta1 == pasta2
    
    def test_limpar_pasta_temp_remove_pasta(self):
        """Teste: limpar_pasta_temp remove a pasta temporária"""
        from geracao_email import obter_pasta_temp, limpar_pasta_temp
        
        # Criar pasta
        obter_pasta_temp()
        
        # Limpar
        limpar_pasta_temp()
        
        # Verificar que a pasta não existe mais
        assert not os.path.exists(os.path.join(tempfile.gettempdir(), "gerador_email_hepta"))
    
    def test_limpar_pasta_temp_sem_pasta(self):
        """Teste: limpar_pasta_temp não dá erro se pasta não existe"""
        from geracao_email import limpar_pasta_temp
        
        # Chamar sem pasta existente
        try:
            limpar_pasta_temp()
            assert True
        except Exception:
            assert False, "limpar_pasta_temp levantou exceção quando a pasta não existia"


class TestArquivosGerados:
    """Testes para arquivos gerados na pasta temporária"""
    
    def test_salvar_html_na_pasta_temp(self):
        """Teste: arquivo HTML é salvo na pasta temporária"""
        from geracao_email import obter_pasta_temp, limpar_pasta_temp
        
        limpar_pasta_temp()
        pasta = obter_pasta_temp()
        
        # Criar arquivo de teste
        test_file = os.path.join(pasta, "test.html")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("<html><body>Teste</body></html>")
        
        assert os.path.exists(test_file)
        
        # Limpar
        limpar_pasta_temp()
    
    def test_limpeza_remove_arquivos_html(self):
        """Teste: limpeza remove todos os arquivos HTML"""
        from geracao_email import obter_pasta_temp, limpar_pasta_temp
        
        limpar_pasta_temp()
        pasta = obter_pasta_temp()
        
        # Criar alguns arquivos
        for i in range(3):
            test_file = os.path.join(pasta, f"test_{i}.html")
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(f"<html>Teste {i}</html>")
        
        # Verificar que foram criados
        assert len(os.listdir(pasta)) == 3
        
        # Limpar
        limpar_pasta_temp()
        
        # Verificar que a pasta foi removida
        assert not os.path.exists(pasta)