# -*- coding: utf-8 -*-
"""
================================================================================
INTERFACE GRÁFICA - GERADOR DE E-MAILS HEPTA
================================================================================

Versão completa com interface gráfica amigável usando Tkinter.
Inclui todos os módulos integrados.

Autor: Josué B. Almeida
GitHub: https://github.com/Joshpcbrrj
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import webbrowser
import os
import sys
import re
import base64

# ============================================================================
# FUNÇÕES DOS MÓDULOS (integradas aqui para funcionar no .exe)
# ============================================================================

def resource_path(relative_path):
    """Encontra o caminho correto dos arquivos quando em .exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def formatar_telefone_individual(telefone_str):
    """Formata número de telefone no padrão (XX) XXXXX-XXXX"""
    numeros = re.sub(r'\D', '', telefone_str)
    if len(numeros) >= 10:
        ddd = numeros[:2]
        numero = numeros[2:]
        if len(numero) == 8:
            numero = f"9{numero}"
        if len(numero) == 9:
            numero = f"{numero[:5]}-{numero[5:]}"
        return f"({ddd}) {numero}"
    return telefone_str

def imagem_to_base64(caminho_imagem):
    """Converte imagem para base64"""
    try:
        if os.path.exists(caminho_imagem):
            with open(caminho_imagem, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        caminho_resource = resource_path(caminho_imagem)
        if os.path.exists(caminho_resource):
            with open(caminho_resource, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        return None
    except:
        return None

def gerar_email_aviso_html(titulo, num_req, nome, telefones, data_hora, tentativa):
    """Gera HTML do e-mail de aviso"""
    winvnc_base64 = imagem_to_base64('winvnc.png')
    logo_base64 = imagem_to_base64('logo.png')
    
    # Mapeamento para texto ordinal
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

# ============================================================================
# CLASSE DA INTERFACE GRÁFICA
# ============================================================================

class GeradorEmailGUI:
    """Classe principal da interface gráfica"""
    
    def __init__(self):
        """Inicializa a janela principal"""
        self.janela = tk.Tk()
        self.janela.title("Gerador de E-mails - Suporte Hepta")
        self.janela.geometry("800x750")
        self.janela.resizable(True, True)
        
        # Configurar cor de fundo
        self.janela.configure(bg='#f0f0f0')
        
        # Variáveis
        self.tipo_email = tk.StringVar(value="1")
        self.telefones_lista = []
        
        # Criar widgets
        self.criar_widgets()
        
    def criar_widgets(self):
        """Cria todos os elementos da interface"""
        
        # Frame principal com scroll
        canvas = tk.Canvas(self.janela, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(self.janela, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título principal
        titulo = tk.Label(self.scrollable_frame, text="📧 GERADOR DE E-MAILS - SUPORTE HEPTA", 
                         font=("Arial", 16, "bold"), fg="#2196F3", bg='#f0f0f0')
        titulo.pack(pady=15)
        
        # ====================================================================
        # LINHA 1: NÚMERO DA REQUISIÇÃO
        # ====================================================================
        frame_req = tk.LabelFrame(self.scrollable_frame, text="1️⃣ NÚMERO DA REQUISIÇÃO", 
                                   font=("Arial", 10, "bold"), bg='#f0f0f0', padx=10, pady=10)
        frame_req.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_req, text="REQ:", font=("Arial", 10), bg='#f0f0f0').pack(side=tk.LEFT)
        self.entry_req = tk.Entry(frame_req, width=30, font=("Arial", 10))
        self.entry_req.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_req, text="Ex: 000008198188", font=("Arial", 9), fg="gray", bg='#f0f0f0').pack(side=tk.LEFT)
        
        # ====================================================================
        # LINHA 2: TIPO DE E-MAIL
        # ====================================================================
        frame_tipo = tk.LabelFrame(self.scrollable_frame, text="2️⃣ TIPO DE E-MAIL", 
                                    font=("Arial", 10, "bold"), bg='#f0f0f0', padx=10, pady=10)
        frame_tipo.pack(fill=tk.X, padx=20, pady=10)
        
        tipos = [
            ("📞 1º Aviso de Tentativa", "1"),
            ("📞 2º Aviso de Tentativa", "2"),
            ("📞 3º Aviso de Tentativa", "3"),
            ("🔒 Fechamento (após 3 tentativas)", "4")
        ]
        
        for texto, valor in tipos:
            rb = tk.Radiobutton(frame_tipo, text=texto, variable=self.tipo_email, 
                               value=valor, bg='#f0f0f0', font=("Arial", 10))
            rb.pack(anchor=tk.W, pady=3)
        
        # ====================================================================
        # LINHA 3: TELEFONES
        # ====================================================================
        frame_telefones = tk.LabelFrame(self.scrollable_frame, text="3️⃣ TELEFONES PARA CONTATO", 
                                         font=("Arial", 10, "bold"), bg='#f0f0f0', padx=10, pady=10)
        frame_telefones.pack(fill=tk.X, padx=20, pady=10)
        
        # Frame para entrada
        frame_add = tk.Frame(frame_telefones, bg='#f0f0f0')
        frame_add.pack(fill=tk.X, pady=5)
        
        tk.Label(frame_add, text="Número:", bg='#f0f0f0', font=("Arial", 10)).pack(side=tk.LEFT)
        self.entry_telefone = tk.Entry(frame_add, width=25, font=("Arial", 10))
        self.entry_telefone.pack(side=tk.LEFT, padx=5)
        self.entry_telefone.bind('<Return>', self.adicionar_telefone)
        
        btn_adicionar = tk.Button(frame_add, text="➕ Adicionar", command=self.adicionar_telefone,
                                  bg="#4CAF50", fg="white", font=("Arial", 9), padx=10)
        btn_adicionar.pack(side=tk.LEFT, padx=5)
        
        # Lista de telefones
        self.lista_telefones = tk.Listbox(frame_telefones, height=4, width=50, font=("Arial", 10))
        self.lista_telefones.pack(fill=tk.X, pady=5)
        
        # Botão remover
        btn_remover = tk.Button(frame_telefones, text="❌ Remover selecionado", command=self.remover_telefone,
                                bg="#f44336", fg="white", font=("Arial", 9), padx=10)
        btn_remover.pack()
        
        # ====================================================================
        # LINHA 4: HORÁRIO
        # ====================================================================
        frame_horario = tk.LabelFrame(self.scrollable_frame, text="⏰ HORÁRIO DO CONTATO (para avisos)", 
                                       font=("Arial", 10, "bold"), bg='#f0f0f0', padx=10, pady=10)
        frame_horario.pack(fill=tk.X, padx=20, pady=10)
        
        frame_hora_min = tk.Frame(frame_horario, bg='#f0f0f0')
        frame_hora_min.pack()
        
        tk.Label(frame_hora_min, text="Hora:", bg='#f0f0f0', font=("Arial", 10)).pack(side=tk.LEFT)
        self.spin_hora = tk.Spinbox(frame_hora_min, from_=0, to=23, width=5, font=("Arial", 10))
        self.spin_hora.pack(side=tk.LEFT, padx=5)
        self.spin_hora.delete(0, tk.END)
        self.spin_hora.insert(0, "14")
        
        tk.Label(frame_hora_min, text="Minutos:", bg='#f0f0f0', font=("Arial", 10)).pack(side=tk.LEFT, padx=(10,0))
        self.spin_minuto = tk.Spinbox(frame_hora_min, from_=0, to=59, width=5, font=("Arial", 10))
        self.spin_minuto.pack(side=tk.LEFT, padx=5)
        self.spin_minuto.delete(0, tk.END)
        self.spin_minuto.insert(0, "00")
        
        # ====================================================================
        # LINHA 5: NOME DO FUNCIONÁRIO
        # ====================================================================
        frame_nome = tk.LabelFrame(self.scrollable_frame, text="4️⃣ NOME DO FUNCIONÁRIO", 
                                    font=("Arial", 10, "bold"), bg='#f0f0f0', padx=10, pady=10)
        frame_nome.pack(fill=tk.X, padx=20, pady=10)
        
        self.entry_nome = tk.Entry(frame_nome, width=40, font=("Arial", 10))
        self.entry_nome.pack(fill=tk.X)
        self.entry_nome.insert(0, "Josué B. Almeida")
        
        # ====================================================================
        # BOTÕES DE AÇÃO
        # ====================================================================
        frame_botoes = tk.Frame(self.scrollable_frame, bg='#f0f0f0')
        frame_botoes.pack(fill=tk.X, padx=20, pady=15)
        
        btn_gerar = tk.Button(frame_botoes, text="🚀 GERAR E-MAIL", command=self.gerar_email,
                              bg="#2196F3", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        btn_gerar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        btn_limpar = tk.Button(frame_botoes, text="🗑️ LIMPAR FORMULÁRIO", command=self.limpar_formulario,
                               bg="#FF9800", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        btn_limpar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        btn_novo = tk.Button(frame_botoes, text="✨ NOVO E-MAIL", command=self.novo_email,
                             bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        btn_novo.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # ====================================================================
        # ÁREA DE PREVIEW
        # ====================================================================
        frame_preview = tk.LabelFrame(self.scrollable_frame, text="📋 PREVIEW DO E-MAIL", 
                                       font=("Arial", 10, "bold"), bg='#f0f0f0', padx=10, pady=10)
        frame_preview.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.text_preview = scrolledtext.ScrolledText(frame_preview, height=12, width=70, 
                                                       font=("Consolas", 9), wrap=tk.WORD)
        self.text_preview.pack(fill=tk.BOTH, expand=True)
        
        # ====================================================================
        # STATUS
        # ====================================================================
        self.status_label = tk.Label(self.scrollable_frame, text="✅ Pronto para gerar e-mail", 
                                      bg='#f0f0f0', fg="green", font=("Arial", 9))
        self.status_label.pack(pady=5)
        
        # ====================================================================
        # RODAPÉ COM DEDICATÓRIA
        # ====================================================================
        # Frame do rodapé
        frame_rodape = tk.Frame(self.scrollable_frame, bg='#e0e0e0', height=50)
        frame_rodape.pack(fill=tk.X, side=tk.BOTTOM, pady=(10,0))
        
        # Linha separadora
        separador = tk.Frame(frame_rodape, height=2, bg='#cccccc')
        separador.pack(fill=tk.X, pady=(5,5))
        
        # Texto da dedicatória com link clicável
        rodape_texto = tk.Label(frame_rodape, 
                                text="✨ Criado por: Josué B. Almeida ✨", 
                                font=("Arial", 9, "bold"), 
                                fg="#333333", 
                                bg='#e0e0e0')
        rodape_texto.pack(pady=(0,2))
        
        # Link do GitHub (clicável)
        github_link = tk.Label(frame_rodape, 
                               text="🔗 GitHub: https://github.com/Joshpcbrrj", 
                               font=("Arial", 8), 
                               fg="#2196F3", 
                               bg='#e0e0e0',
                               cursor="hand2")  # Muda o cursor para mãozinha
        github_link.pack(pady=(0,5))
        
        # Função para abrir o link do GitHub
        def abrir_github(event):
            webbrowser.open("https://github.com/Joshpcbrrj")
        
        github_link.bind("<Button-1>", abrir_github)
        
        # Versão do programa
        versao_label = tk.Label(frame_rodape, 
                                text="Versão 2.0 - Maio/2026", 
                                font=("Arial", 7), 
                                fg="#999999", 
                                bg='#e0e0e0')
        versao_label.pack(pady=(0,5))
        
    def log(self, mensagem, cor="green"):
        """Atualiza o status"""
        self.status_label.config(text=mensagem, fg=cor)
        
    def adicionar_telefone(self, event=None):
        """Adiciona telefone à lista"""
        telefone = self.entry_telefone.get().strip()
        if telefone:
            telefone_formatado = formatar_telefone_individual(telefone)
            self.lista_telefones.insert(tk.END, telefone_formatado)
            self.entry_telefone.delete(0, tk.END)
            self.log(f"✅ Telefone adicionado: {telefone_formatado}")
        else:
            messagebox.showwarning("Aviso", "Digite um número de telefone!")
            
    def remover_telefone(self):
        """Remove telefone selecionado da lista"""
        selecionado = self.lista_telefones.curselection()
        if selecionado:
            removido = self.lista_telefones.get(selecionado)
            self.lista_telefones.delete(selecionado)
            self.log(f"🗑️ Telefone removido: {removido}")
        else:
            messagebox.showwarning("Aviso", "Selecione um telefone para remover!")
            
    def obter_telefones(self):
        """Retorna lista de telefones"""
        return list(self.lista_telefones.get(0, tk.END))
    
    def formatar_telefones(self, telefones):
        """Formata lista de telefones para texto"""
        if len(telefones) == 0:
            return ""
        elif len(telefones) == 1:
            return telefones[0]
        else:
            return ", ".join(telefones[:-1]) + " e " + telefones[-1]
    
    def limpar_formulario(self):
        """Limpa todos os campos"""
        self.entry_req.delete(0, tk.END)
        self.lista_telefones.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, "Josué B. Almeida")
        self.spin_hora.delete(0, tk.END)
        self.spin_hora.insert(0, "14")
        self.spin_minuto.delete(0, tk.END)
        self.spin_minuto.insert(0, "00")
        self.tipo_email.set("1")
        self.text_preview.delete(1.0, tk.END)
        self.log("🗑️ Formulário limpo!")
        
    def novo_email(self):
        """Limpa e prepara para novo e-mail"""
        self.limpar_formulario()
        messagebox.showinfo("Novo E-mail", "Formulário limpo! Preencha os dados para um novo e-mail.")
        
    def gerar_email(self):
        """Gera o e-mail com os dados do formulário"""
        
        # Validações
        num_req = self.entry_req.get().strip()
        if not num_req:
            messagebox.showerror("Erro", "Digite o número da requisição!")
            return
            
        tipo = self.tipo_email.get()
        nome = self.entry_nome.get().strip()
        if not nome:
            nome = "Josué B. Almeida"
            
        # Monta REQ completo
        if num_req.upper().startswith('REQ'):
            num_req_completo = num_req.upper()
            num_req_num = num_req[3:]
        else:
            num_req_completo = f"REQ{num_req}"
            num_req_num = num_req
        
        # Data atual
        data_atual = datetime.now().strftime("%d/%m/%Y")
        hora = self.spin_hora.get().zfill(2)
        minuto = self.spin_minuto.get().zfill(2)
        
        self.text_preview.delete(1.0, tk.END)
        
        if tipo == '4':
            # E-MAIL DE FECHAMENTO
            data_hora = f"{data_atual} às {datetime.now().strftime('%H:%M')} BRT"
            titulo = f"{num_req_completo} - Chamado Fechado"
            
            html = gerar_email_fechamento_html(titulo, num_req_completo, nome, data_hora)
            
            self.text_preview.insert(tk.END, f"📧 E-MAIL DE FECHAMENTO\n")
            self.text_preview.insert(tk.END, f"{'='*50}\n")
            self.text_preview.insert(tk.END, f"Título: {titulo}\n\n")
            self.text_preview.insert(tk.END, "HTML gerado com sucesso! Abrindo no navegador...\n")
            
            self.log(f"🔒 E-mail de FECHAMENTO gerado para {num_req_completo}")
            
        else:
            # E-MAIL DE AVISO
            telefones = self.obter_telefones()
            if not telefones:
                messagebox.showerror("Erro", "Adicione pelo menos um telefone!")
                return
                
            telefone_str = self.formatar_telefones(telefones)
            tentativa_ordinal = {'1': '1º', '2': '2º', '3': '3º'}[tipo]
            
            data_hora = f"{data_atual} às {hora}:{minuto} BRT"
            titulo = f"{num_req_completo} - {tentativa_ordinal} aviso de tentativa de contato com o cliente"
            
            html = gerar_email_aviso_html(titulo, num_req_completo, nome, telefone_str, data_hora, tipo)
            
            self.text_preview.insert(tk.END, f"📧 E-MAIL DE {tentativa_ordinal} AVISO\n")
            self.text_preview.insert(tk.END, f"{'='*50}\n")
            self.text_preview.insert(tk.END, f"Título: {titulo}\n\n")
            self.text_preview.insert(tk.END, f"Telefone(s): {telefone_str}\n")
            self.text_preview.insert(tk.END, f"Data/Hora: {data_hora}\n\n")
            self.text_preview.insert(tk.END, "HTML gerado com sucesso! Abrindo no navegador...\n")
            
            self.log(f"📧 E-mail de {tentativa_ordinal} AVISO gerado para {num_req_completo} às {hora}:{minuto}")
        
        # Salvar e abrir HTML
        nome_arquivo = f"email_{num_req_num}_{tipo}.html"
        caminho = os.path.abspath(nome_arquivo)
        
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(html)
        
        webbrowser.open(f'file://{caminho}')
        
        self.log(f"🌐 HTML aberto: {nome_arquivo}", "blue")
        messagebox.showinfo("Sucesso", f"E-mail gerado com sucesso!\n\nO navegador foi aberto.\nSelecione tudo (Ctrl+A) e copie (Ctrl+C)\n\nArquivo salvo: {nome_arquivo}")
        
    def executar(self):
        """Inicia a interface gráfica"""
        self.janela.mainloop()

# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    app = GeradorEmailGUI()
    app.executar()