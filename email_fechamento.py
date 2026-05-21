# -*- coding: utf-8 -*-
"""
================================================================================
E-MAIL DE FECHAMENTO DE CHAMADO
================================================================================

Este módulo gera o e-mail de fechamento, enviado quando o cliente não atendeu
após 3 tentativas de contato (telefone e e-mail).

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

from imagens import imagem_to_base64


def gerar_email_fechamento_html(titulo, num_req_completo, nome_funcionario, data_hora_completa):
    """
    FUNÇÃO: gerar_email_fechamento_html
    ===========================================================================
    Gera o e-mail de FECHAMENTO (após 3 tentativas sem sucesso) em HTML.
    
    PARÂMETROS:
    ===========================================================================
    - titulo: str - Título do e-mail (ex: "REQ123 - Chamado Fechado")
    - num_req_completo: str - Número da requisição (ex: "REQ123")
    - nome_funcionario: str - Nome do funcionário que assina o e-mail
    - data_hora_completa: str - Data e hora atuais formatadas
    """
    
    logo_base64 = imagem_to_base64('logo.png')
    
    html_email = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{
        font-family: Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.5;
        color: #333;
        margin: 0;
        padding: 20px;
    }}
    .container {{
        max-width: 700px;
        margin: 0 auto;
    }}
    .titulo {{
        font-size: 14pt;
        font-weight: bold;
        margin-bottom: 20px;
        color: #000;
    }}
    .assinatura-conteudo {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 2px solid #e0e0e0;
    }}
    .assinatura-logo img {{
        max-width: 100px;
        height: auto;
    }}
    .creditos {{
        font-size: 8pt;
        color: #999;
        text-align: center;
        margin-top: 40px;
        padding-top: 10px;
        border-top: 1px solid #eee;
    }}
    .dica-copy {{
        background-color: #e8f4f8;
        border-left: 4px solid #2196F3;
        padding: 10px 15px;
        margin: 20px 0;
    }}
    .aviso-importante {{
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 10px 15px;
        margin: 20px 0;
    }}
</style>
</head>
<body>
<div class="container">
    
    <div class="dica-copy">
        <b>📋 COMO COPIAR ESTE E-MAIL:</b><br/>
        1. Selecione TODO o texto abaixo (Ctrl+A)<br/>
        2. Copie (Ctrl+C)<br/>
        3. Cole no seu e-mail (Ctrl+V)
    </div>
    
    <div class="titulo">{titulo}</div>
    
    <p>Prezado Cliente,</p>
    
    <p>A equipe de Suporte Técnico Remoto informa que, após 3 tentativas de contato (por telefone e e-mail) para atendimento da {num_req_completo}, não foi possível proceder com o atendimento do chamado, sendo concluído como improdutivo. Esta informação é registrada em {data_hora_completa}.</p>
    
    <div class="aviso-importante">
        <b>⚠️ ATENÇÃO:</b> Caso ainda necessite de suporte técnico, solicitamos registrar um novo chamado, uma vez que a reabertura deste será considerada indevida.
    </div>
    
    <p>Ressaltamos que a equipe de Suporte Técnico preza pela segurança das informações do usuário e, por isso, adota procedimentos relacionados às tentativas de contato e à autorização do usuário para a realização do atendimento.</p>
    
    <p>Com o objetivo de evitarmos outros chamados improdutivos, solicitamos que sejam informados outro(s) número(s) telefônico(s) (se possível, inclusive celular) para que você possa ser facilmente encontrado. O(s) e-mail(s) permanecerá(ão) sendo enviado(s) como forma alternada de contato e localização.</p>
    
    <p>Desde já, agradecemos a compreensão.</p>
    
    <div class="assinatura-conteudo">
        <div>
            <p>Atenciosamente,</p>
            <p>
            <b>{nome_funcionario}</b><br/>
            Suporte Técnico II - Hepta<br/>
            (61) 3424-4800<br/>
            <span style="font-size: 9pt; color: #666;">Importante: Telefone exclusivo para realização de ligações. De acordo com o contrato, este número não recebe chamadas.</span>
            </p>
        </div>
        <div class="assinatura-logo">
            {f'<img src="data:image/png;base64,{logo_base64}" alt="Hepta Tecnologia"/>' if logo_base64 else '<b>Hepta Tecnologia</b>'}
        </div>
    </div>
    
    <div class="creditos">
        <hr/>
        Programa feito por: Josué B. Almeida | GitHub: https://github.com/Joshpcbrrj<br/>
        Documento gerado automaticamente pelo sistema de suporte Hepta
    </div>
    
</div>
</body>
</html>"""
    
    return html_email