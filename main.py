# -*- coding: utf-8 -*-
"""
================================================================================
PONTO DE ENTRADA - GERADOR DE E-MAILS HEPTA
================================================================================

Abre a interface gráfica.
Com --autoteste, apenas verifica modelos e imagens e sai (usado no build).

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import sys

if __name__ == "__main__":
    if "--autoteste" in sys.argv:
        from autoteste import executar

        sys.exit(executar())

    from main_gui import GeradorEmailGUI

    app = GeradorEmailGUI()
    app.executar()
