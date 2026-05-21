# -*- coding: utf-8 -*-
"""
================================================================================
E-MAIL DE AVISO (1ª, 2ª e 3ª TENTATIVA)
================================================================================

Este módulo é responsável por gerar os e-mails de aviso de tentativa de contato.
São os e-mails enviados quando o cliente não atende o telefone nas 1ª, 2ª ou 3ª
tentativas. Este e-mail contém a imagem do WinVNC para o cliente autorizar o
acesso remoto.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

from imagens import imagem_to_base64


def gerar_email_aviso_html(titulo, num_req_completo, nome_funcionario, 
                           telefone_str, data_hora_completa, tentativa_extenso):
    """
    FUNÇÃO: gerar_email_aviso_html
    ===========================================================================
    Gera o e-mail de AVISO (1ª, 2ª ou 3ª tentativa) em formato HTML.
    
    PARÂMETROS:
    ===========================================================================
    - titulo: str - Título do e-mail (ex: "REQ123 - 1º aviso...")
    - num_req_completo: str - Número da requisição completa (ex: "REQ123")
    - nome_funcionario: str - Nome do funcionário que assina o e-mail
    - telefone_str: str - Telefone(s) formatado(s) (ex: "(11) 99999-9999")
    - data_hora_completa: str - Data e hora formatada (ex: "21/05/2026 às 14:30 BRT")
    - tentativa_extenso: str - "primeira", "segunda" ou "terceira"
    
    RETORNO:
    ===========================================================================
    str - String contendo o HTML completo do e-mail
    """
    
    winvnc_base64 = imagem_to_base64('winvnc.png')
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
    .imagem-winvnc {{
        text-align: center;
        margin: 20px 0;
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
    }}
    .imagem-winvnc img {{
        max-width: 100%;
        height: auto;
        border: 1px solid #ccc;
        border-radius: 5px;
    }}
    .legenda {{
        font-size: 10pt;
        color: #666;
        text-align: center;
        font-style: italic;
        margin-top: 8px;
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
    
    <p>A equipe de Suporte Técnico Remoto informa que não obteve sucesso na {tentativa_extenso} tentativa de contato pelo(s) telefone(s) {telefone_str}, realizada no dia {data_hora_completa}, com o objetivo de iniciar o atendimento da {num_req_completo}.</p>
    
    <p>Dessa forma, realizaremos mais uma tentativa de atendimento sem contato telefônico, aplicando procedimento técnico com o objetivo de solucionar a demanda do chamado sem que haja interferência na utilização do seu microcomputador.</p>
    
    <p>Eventualmente, poderá ser necessária autorização para acessar a sua área de trabalho. Se for o caso, enviaremos uma nova solicitação de acesso que aparecerá no centro do seu monitor, conforme a janela apresentada abaixo:</p>
    
    <div class="imagem-winvnc">
        {f'<img src="data:image/png;base64,{winvnc_base64}" alt="WinVNC"/>' if winvnc_base64 else '<p>⚠️ IMAGEM NÃO ENCONTRADA</p>'}
        <div class="legenda">Figura 1: Janela do WinVNC - Clique em ACCEPT para autorizar o acesso remoto</div>
    </div>
    
    <p>Neste caso, basta clicar no botão "<b>ACCEPT</b>" para que o atendimento seja iniciado.</p>
    
    <p>Caso não seja possível atender diretamente à demanda sem contato telefônico, ou caso não seja respondido ou não seja autorizado o acesso remoto, no intervalo de 40 minutos a 1 hora será efetuada uma nova tentativa de contato para se proceder com o atendimento do chamado.</p>
    
    <p>Por favor, caso tenha algum outro número de telefone, informe-o respondendo a este e-mail.</p>
    
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