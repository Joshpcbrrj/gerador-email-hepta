# -*- coding: utf-8 -*-
"""
MÓDULO DE EVENTOS
================================================================================
Funções de evento para a interface gráfica (adicionar, remover, limpar).

Versão compacta - lista única de telefones
"""

import tkinter as tk
from tkinter import messagebox
from telefones import formatar_celular, formatar_fixo


def mostrar_mensagem_temporaria(gui, mensagem, cor="green"):
    """Mostra uma mensagem temporária que desaparece após 2 segundos"""
    # Cancelar timer anterior
    if gui.timer_mensagem:
        gui.janela.after_cancel(gui.timer_mensagem)
    
    # Mostrar mensagem
    gui.status_label.config(text=mensagem, fg=cor)
    
    # Programar para limpar após 2 segundos
    def limpar_mensagem():
        gui.status_label.config(text="✅ Pronto para gerar e-mail", fg="green")
        gui.timer_mensagem = None
    
    gui.timer_mensagem = gui.janela.after(2000, limpar_mensagem)


def adicionar_celular(gui):
    """Adiciona celular à lista"""
    telefone = gui.entry_telefone.get().strip()
    if telefone:
        telefone_formatado = formatar_celular(telefone)
        gui.lista_telefones.insert(tk.END, f"📞 {telefone_formatado}")
        gui.entry_telefone.delete(0, tk.END)
        mostrar_mensagem_temporaria(gui, f"✅ Celular adicionado: {telefone_formatado}", "green")
    else:
        messagebox.showwarning("Aviso", "Digite um número de telefone!")


def adicionar_fixo(gui):
    """Adiciona telefone fixo à lista"""
    telefone = gui.entry_telefone.get().strip()
    if telefone:
        telefone_formatado = formatar_fixo(telefone)
        gui.lista_telefones.insert(tk.END, f"🏠 {telefone_formatado}")
        gui.entry_telefone.delete(0, tk.END)
        mostrar_mensagem_temporaria(gui, f"✅ Telefone fixo adicionado: {telefone_formatado}", "green")
    else:
        messagebox.showwarning("Aviso", "Digite um número de telefone!")


def remover_telefone(gui):
    """Remove telefone selecionado da lista"""
    selecionado = gui.lista_telefones.curselection()
    if selecionado:
        removido = gui.lista_telefones.get(selecionado)
        gui.lista_telefones.delete(selecionado)
        mostrar_mensagem_temporaria(gui, f"🗑️ Telefone removido: {removido}", "orange")
    else:
        messagebox.showwarning("Aviso", "Selecione um telefone para remover!")


def limpar_listas(gui):
    """Limpa apenas as listas de telefones"""
    gui.lista_telefones.delete(0, tk.END)
    gui.entry_telefone.delete(0, tk.END)
    mostrar_mensagem_temporaria(gui, "🗑️ Lista de telefones limpa!", "orange")


def obter_todos_telefones(gui):
    """Retorna lista com todos os telefones (remove emoji do início)"""
    telefones = []
    for item in gui.lista_telefones.get(0, tk.END):
        telefone_limpo = item[3:] if len(item) > 3 else item
        telefones.append(telefone_limpo)
    return telefones


def limpar_tudo(gui):
    """Limpa TODO o formulário para um novo e-mail"""
    gui.entry_req.delete(0, tk.END)
    gui.lista_telefones.delete(0, tk.END)
    gui.entry_telefone.delete(0, tk.END)
    gui.entry_nome.delete(0, tk.END)
    gui.entry_nome.insert(0, "Josué B. Almeida")
    gui.spin_hora.delete(0, tk.END)
    gui.spin_hora.insert(0, "14")
    gui.spin_minuto.delete(0, tk.END)
    gui.spin_minuto.insert(0, "00")
    gui.tipo_email.set("1")
    # Atualizar feedback label
    gui.feedback_label.config(text="✅ Opção escolhida: 1º Aviso")
    mostrar_mensagem_temporaria(gui, "✨ Formulário limpo! Pronto para novo e-mail.", "green")
    messagebox.showinfo("Novo E-mail", "Formulário limpo! Preencha os dados para um novo e-mail.")