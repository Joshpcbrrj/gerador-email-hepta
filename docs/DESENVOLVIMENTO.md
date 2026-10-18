# Guia de desenvolvimento

Para quem vai rodar o programa pelo código, alterar, testar ou publicar uma nova versão. Para usar o programa, veja o [README](../README.md).

## Requisitos

- Windows 10 ou 11
- Python 3.13 ou superior (marque **Add Python to PATH** na instalação)

## Rodar pelo código

```bash
git clone https://github.com/Joshpcbrrj/gerador-email-hepta.git
cd gerador-email-hepta
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Testes

```bash
python -m pytest
```

Os testes também rodam automaticamente no GitHub a cada push na `main` e em cada pull request ([workflow](../.github/workflows/testes.yml)).

## Estrutura

| Módulo | Responsabilidade |
| --- | --- |
| `main.py` | Ponto de entrada |
| `main_gui.py` | Janela principal: liga eventos, relógio da data/hora e verificação de atualizações |
| `widgets.py` | Monta o layout (aviso, cabeçalho, ações, cartões, barra de status) |
| `widget_helpers.py` | Componentes padronizados: cartão, campo, botão, combos de data/hora |
| `lista_telefones.py` | Lista de telefones (estado e linhas com ✕) |
| `eventos.py` | Ações dos botões (adicionar, remover, limpar) |
| `geracao_email.py` | Valida o formulário, gera e abre os HTMLs na pasta temporária |
| `data_hora.py` | Regra da data/hora do contato (automática ou manual) |
| `email_html.py`, `email_aviso.py`, `email_fechamento.py` | Modelos HTML dos e-mails |
| `imagens.py`, `utils.py` | Imagens em base64 e caminho dos recursos dentro do `.exe` |
| `telefones.py` | Formatação de celular e fixo |
| `atualizacao.py` | Consulta a última release no GitHub e compara versões |
| `temas.py` | Paleta clara/escura e fontes |
| `tema_manager.py` | Troca de tema e preferência salva |
| `config.py` | Versão atual e configurações |
| `assets/` | Logo e imagem do WinVNC usadas nos e-mails |
| `tests/` | Testes automatizados (pytest) |

### Decisões importantes

- **Cores dos temas:** todo widget recebe a cor como par `(claro, escuro)` através de `cor("nome")`, em `temas.py`. O CustomTkinter troca sozinho ao mudar o tema. Não pinte widgets manualmente na troca de tema; adicione a cor na paleta e use `cor()`.
- **Data/hora:** no modo automático, o horário é lido no clique em gerar (`resolver_data_hora` em `data_hora.py`), nunca na abertura do programa.
- **Textos de uma linha nos labels:** não ajuste `wraplength` dinamicamente em eventos `<Configure>`. A mudança de altura realimenta o redimensionamento e trava a janela.

## Gerar o executável

```bash
pyinstaller --noconfirm --clean --onefile --windowed --name GeradorEmailHepta --collect-all customtkinter --add-data "assets;assets" main.py
```

O arquivo sai em `dist\GeradorEmailHepta.exe`. As pastas `build/` e `dist/` e o `.spec` gerado são ignorados pelo Git.

Antes de publicar, abra o `.exe` e gere um e-mail de aviso para conferir se o logo e a imagem do WinVNC aparecem.

## Publicar uma nova versão

O aviso de atualização dos usuários depende deste processo. Siga na ordem:

1. Atualize `VERSAO_ATUAL` em [`config.py`](../config.py) (ex: `"2.7"`).
2. Registre as mudanças no [CHANGELOG](../CHANGELOG.md), na seção da nova versão.
3. Rode `python -m pytest`.
4. Faça o commit e o push na `main`.
5. Gere o `.exe` (seção anterior).
6. Crie a release com a tag `v` + versão, anexando o `.exe` e usando a seção do CHANGELOG como descrição:

   ```bash
   gh release create v2.7 dist/GeradorEmailHepta.exe --title "v2.7" --notes-file notas.md
   ```

> **Atenção:** a tag da release precisa ser maior que `VERSAO_ATUAL` das versões instaladas para elas exibirem o aviso. Se `VERSAO_ATUAL` não for atualizada no código, a própria versão nova vai oferecer atualização para ela mesma.
