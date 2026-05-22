# -*- coding: utf-8 -*-
"""
MÓDULO DE GERAÇÃO DE HTML
================================================================================
Gera os e-mails em formato HTML (aviso e fechamento).
"""

from imagens import imagem_to_base64


def gerar_email_aviso_html(titulo, num_req, nome, telefones, data_hora, tentativa):
    """Gera HTML do e-mail de aviso"""
    winvnc_base64 = imagem_to_base64('winvnc.png')
    logo_base64 = imagem_to_base64('logo.png')
    
    tentativa_texto = {
        '1': 'primeira', '2': 'segunda', '3': 'terceira'
    }.get(tentativa, 'primeira')
    
    tentativa_ordinal = {
        '1': '1º', '2': '2º', '3': '3º'
    }.get(tentativa, '1º')
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{
        font-family: Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.5;
        color: #333;
        margin: 20px;
        background-color: #fff;
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
    
    <p>A equipe de Suporte Técnico Remoto informa que não obteve sucesso na {tentativa_texto} tentativa de contato pelo(s) telefone(s) {telefones}, realizada no dia {data_hora}, com o objetivo de iniciar o atendimento da {num_req}.</p>
    
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
            <b>{nome}</b><br/>
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
    return html


def gerar_email_fechamento_html(titulo, num_req, nome, data_hora):
    """Gera HTML do e-mail de fechamento"""
    logo_base64 = imagem_to_base64('logo.png')
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{
        font-family: Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.5;
        color: #333;
        margin: 20px;
        background-color: #fff;
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
    
    <p>A equipe de Suporte Técnico Remoto informa que, após 3 tentativas de contato (por telefone e e-mail) para atendimento da {num_req}, não foi possível proceder com o atendimento do chamado, sendo concluído como improdutivo. Esta informação é registrada em {data_hora}.</p>
    
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
            <b>{nome}</b><br/>
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
    return html