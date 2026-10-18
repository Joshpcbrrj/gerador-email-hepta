# Changelog

Todas as mudanças relevantes do projeto são registradas aqui.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e as versões seguem o padrão `MAIOR.MENOR` (ex: 2.6).

## [2.6] - 2026-10-17

### Adicionado
- Opção **Usar data e hora atuais**, ligada por padrão. Os campos acompanham o relógio; escolher um valor manualmente desliga a opção, e **Novo e-mail** volta ao automático.
- Verificação automática de atualizações ao abrir o programa e a cada 4 horas, com faixa de aviso no topo da janela e botão **Baixar atualização**.
- Botão **✕** para remover cada telefone e contador de telefones (x/10).
- Atalho **Ctrl+Enter** para gerar o e-mail.
- O tema escolhido (claro ou escuro) é lembrado na próxima vez que o programa abrir.

### Alterado
- Novo visual: seções em cartões, paleta clara e escura revisada, fonte Segoe UI e efeito ao passar o mouse nos botões.
- O seletor de tipo de e-mail mostra uma descrição de cada opção.
- **Novo e-mail** não abre mais uma janela de confirmação; a confirmação aparece na barra de status.
- Janela inicial maior (960×720) e tamanho mínimo de 680×520.

### Corrigido
- A hora do e-mail agora é a do momento em que você clica em **Gerar e-mail**. Antes era a hora em que o programa foi aberto: aberto às 10h e usado às 12h, o e-mail saía com 10h. A data também acompanha a virada do dia.
- O e-mail de **Fechamento** passa a respeitar a hora escolhida manualmente (antes usava sempre a hora atual).
- Datas inválidas (ex: 31/02) são recusadas com aviso, em vez de irem para o e-mail.
- Tema claro: fundos com cor errada atrás dos textos do rodapé, seções sem separação visual, lista de telefones vazia cortada e barra de rolagem aparecendo sem necessidade.
- O programa travava ao trocar o tema com o tipo **Fechamento** selecionado.
- A versão interna estava como 2.4 na release 2.5, o que fazia o programa sempre oferecer atualização.
- A comparação de versões passa a ser numérica (antes, `2.10` seria considerada mais antiga que `2.9`).
- O botão **Atualizações** não diz mais "versão mais recente" quando a verificação falha por falta de conexão.

## [2.5] - 2026-05-26

### Adicionado
- **Nota de Chamado Improdutivo**, aberta junto com o e-mail de fechamento (dois HTMLs: e-mail + nota).
- Data e hora preenchidas automaticamente com o horário atual, mantendo o ajuste manual.

### Alterado
- Janela inicial de 960×640 e mínimo de 640×480, para melhor uso em notebooks.
- Build do `.exe` com `--collect-all customtkinter`.

## [2.4] - 2026-05-25

### Alterado
- Interface redesenhada com **CustomTkinter** (botões arredondados).
- Layout de aplicativo desktop: barra de ações fixa (Gerar, Limpar, Novo) e barra de status.
- Lista de telefones em formato de lista clicável.

## [2.3] - 2026-05-22

### Adicionado
- Tema escuro e botões de tema e atualização no canto superior direito.
- Verificação de atualizações pelo GitHub.
- Indicação da opção de aviso escolhida.
- Mensagens temporárias na barra de status.
- Links para GitHub e LinkedIn no rodapé.
- Limite máximo de 10 telefones por chamado.
- Testes automatizados.

### Corrigido
- Formatação de telefones fixos (não adiciona mais o dígito 9).
- Limpeza automática dos arquivos temporários ao fechar.

## [2.2] - 2026-05-21

### Adicionado
- Campo separado para telefone fixo, com separação visual entre celular e fixo.

### Corrigido
- Telefones fixos não recebem mais o dígito 9 automaticamente.

## [2.0] - 2026-05-21

- Primeira versão publicada.

[2.6]: https://github.com/Joshpcbrrj/gerador-email-hepta/compare/v2.5...v2.6
[2.5]: https://github.com/Joshpcbrrj/gerador-email-hepta/compare/v2.4...v2.5
[2.4]: https://github.com/Joshpcbrrj/gerador-email-hepta/compare/v2.3...v2.4
[2.3]: https://github.com/Joshpcbrrj/gerador-email-hepta/compare/v2.2...v2.3
[2.2]: https://github.com/Joshpcbrrj/gerador-email-hepta/compare/v2.0...v2.2
[2.0]: https://github.com/Joshpcbrrj/gerador-email-hepta/releases/tag/v2.0
