# -*- coding: utf-8 -*-
"""
TESTES PARA AUTO-UPDATE
================================================================================
Testa as funções de verificação de atualização no GitHub.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock, patch
from config import VERSAO_ATUAL, GITHUB_REPO, GITHUB_API_URL


class TestConfiguracoes:
    """Testes para configurações do auto-update"""

    def test_versao_atual_definida(self):
        """Teste: VERSAO_ATUAL está definida"""
        assert VERSAO_ATUAL is not None
        assert len(VERSAO_ATUAL) > 0

    def test_versao_atual_formato_valido(self):
        """Teste: VERSAO_ATUAL tem formato válido (ex: 2.2, 2.3)"""
        partes = VERSAO_ATUAL.split(".")
        assert len(partes) >= 2
        assert partes[0].isdigit()
        assert partes[1].isdigit()

    def test_github_repo_definido(self):
        """Teste: GITHUB_REPO está definido"""
        assert GITHUB_REPO is not None
        assert "/" in GITHUB_REPO

    def test_github_api_url_valida(self):
        """Teste: GITHUB_API_URL é uma URL válida"""
        assert GITHUB_API_URL.startswith("https://")
        assert "api.github.com" in GITHUB_API_URL


class TestVerificarAtualizacao:
    """Testes para função verificar_atualizacao"""

    @patch("atualizacao.urllib.request.urlopen")
    def test_verificar_atualizacao_sem_internet(self, mock_urlopen):
        """Teste: sem internet, não deve lançar exceção"""
        from atualizacao import verificar_atualizacao

        mock_urlopen.side_effect = Exception("Sem internet")

        mock_gui = MagicMock()

        verificar_atualizacao(mock_gui)  # não deve lançar exceção

    @patch("atualizacao.urllib.request.urlopen")
    def test_verificar_atualizacao_chama_callback(self, mock_urlopen):
        """Teste: callback é chamado quando está atualizado"""
        from atualizacao import verificar_atualizacao

        import json

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {
                "tag_name": f"v{VERSAO_ATUAL}",
                "html_url": "https://github.com/test/repo",
                "body": "Notas da versão",
            }
        ).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        mock_gui = MagicMock()
        mock_callback = MagicMock()

        verificar_atualizacao(mock_gui, mock_callback)

        # Aguardar um pouco para a thread executar
        import time

        time.sleep(0.5)

        # O callback deve ser chamado (está atualizado)
        mock_gui.after.assert_called()


class TestComparacaoVersoes:
    """Comparação numérica de versões (texto falharia em '2.10' > '2.9')"""

    def test_versao_maior(self):
        from atualizacao import versao_mais_nova

        assert versao_mais_nova("2.7", "2.6")

    def test_versao_igual_nao_e_mais_nova(self):
        from atualizacao import versao_mais_nova

        assert not versao_mais_nova("2.6", "2.6")

    def test_versao_dois_digitos(self):
        from atualizacao import versao_mais_nova

        assert versao_mais_nova("2.10", "2.9")
        assert not versao_mais_nova("2.9", "2.10")

    def test_versao_com_prefixo_e_patch(self):
        from atualizacao import versao_mais_nova

        assert versao_mais_nova("v2.6.1", "2.6")

    def test_versao_vazia(self):
        from atualizacao import versao_mais_nova

        assert not versao_mais_nova("", "2.6")


class TestAvisoAutomatico:
    """Verificação silenciosa: avisa a interface sem abrir popup"""

    @patch("atualizacao.perguntar_download")
    @patch("atualizacao.consultar_ultima_release")
    def test_versao_nova_chama_ao_encontrar_sem_popup(self, mock_consulta, mock_popup):
        from atualizacao import verificar_atualizacao
        import time

        release = {"versao": "99.0", "url": "https://github.com/x", "notas": "novidades"}
        mock_consulta.return_value = release
        mock_janela = MagicMock()
        mock_janela.after.side_effect = lambda _ms, func: func()
        ao_encontrar = MagicMock()

        verificar_atualizacao(mock_janela, ao_encontrar=ao_encontrar, silencioso=True)
        time.sleep(0.3)

        ao_encontrar.assert_called_once_with(release)
        mock_popup.assert_not_called()

    @patch("atualizacao.consultar_ultima_release")
    def test_erro_chama_ao_falhar(self, mock_consulta):
        from atualizacao import verificar_atualizacao
        import time

        mock_consulta.side_effect = Exception("Sem internet")
        mock_janela = MagicMock()
        mock_janela.after.side_effect = lambda _ms, func: func()
        callback, ao_falhar = MagicMock(), MagicMock()

        verificar_atualizacao(mock_janela, callback=callback, ao_falhar=ao_falhar)
        time.sleep(0.3)

        ao_falhar.assert_called_once()
        callback.assert_not_called()
