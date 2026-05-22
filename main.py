# -*- coding: utf-8 -*-
"""
================================================================================
PONTO DE ENTRADA - GERADOR DE E-MAILS HEPTA
================================================================================

Arquivo principal para executar o programa.
Redireciona para a interface gráfica.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

from main_gui import GeradorEmailGUI

if __name__ == "__main__":
    app = GeradorEmailGUI()
    app.executar()