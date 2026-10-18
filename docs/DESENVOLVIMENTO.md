# Guia de desenvolvimento

Para quem vai rodar o programa pelo código, alterar, testar ou publicar uma nova versão. Para usar o programa, veja o [README](../README.md).

## Requisitos

- Windows 10 ou 11
- **Python 3.13** (marque **Add Python to PATH** na instalação)

Use a mesma versão do Python que gera as releases (3.13, indicada em [`.python-version`](../.python-version) e nos workflows). Versões mais novas trazem outra versão do Tk, que já se comportou diferente na interface. Se tiver mais de uma versão instalada, crie o ambiente com `py -3.13`.

## Rodar pelo código

```bash
git clone https://github.com/Joshpcbrrj/gerador-email-hepta.git
cd gerador-email-hepta
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Qualidade: testes e lint

```bash
python -m pytest        # testes
ruff check .            # lint (erros e más práticas)
ruff format .           # formatação automática
```

A configuração do `ruff` fica no [`pyproject.toml`](../pyproject.toml). Os três comandos também rodam no GitHub a cada push na `main` e em cada pull request ([workflow de testes](../.github/workflows/testes.yml)).

O [Dependabot](../.github/dependabot.yml) abre, uma vez por mês, um pull request com as dependências atualizadas (pip e GitHub Actions). Os testes rodam no próprio PR: se passarem, basta fazer o merge.

### Snapshots: o e-mail não pode mudar sem querer

Os e-mails são copiados e colados no e-mail corporativo, então o HTML gerado precisa continuar idêntico. Os arquivos em [`tests/snapshots/`](../tests/snapshots/) guardam o resultado esperado de vários casos, e o [`test_snapshots.py`](../tests/test_snapshots.py) falha se qualquer caractere mudar. As imagens em base64 aparecem como `{{WINVNC_BASE64}}` e `{{LOGO_BASE64}}`.

Se você alterar um texto **de propósito**, atualize os snapshots e revise a diferença antes do commit:

```bash
python tests/test_snapshots.py --atualizar
git diff tests/snapshots
```

## Estrutura

| Módulo | Responsabilidade |
| --- | --- |
| `main.py` | Ponto de entrada (com `--autoteste`, só verifica modelos e imagens) |
| `main_gui.py` | Janela principal: liga eventos, relógio da data/hora, atualizações, nome lembrado e erros inesperados |
| `widgets.py` | Monta o layout (aviso, cabeçalho, ações, cartões, barra de status) |
| `widget_helpers.py` | Componentes padronizados: cartão, campo, botão, combos de data/hora |
| `lista_telefones.py` | Lista de telefones (estado e linhas com ✕) |
| `eventos.py` | Ações dos botões (adicionar, remover, limpar) |
| `geracao_email.py` | Regras (`validar_formulario`, `normalizar_req`, `montar_emails`) e os botões Gerar e Copiar |
| `area_transferencia.py` | Botão **Copiar e-mail**: prepara o HTML (estilos embutidos, sem instruções/créditos) e grava na área de transferência do Windows |
| `email_html.py` | Preenche os modelos de `templates/` |
| `templates/` | **Textos dos e-mails** (`aviso.html`, `fechamento.html`, `nota_improdutivo.html`) e a assinatura comum (`partes/assinatura.html`) |
| `tipo_email.py` | Os quatro tipos de e-mail (`TipoEmail`) e seus textos |
| `data_hora.py` | Regra da data/hora do contato (automática ou manual) |
| `telefones.py` | Validação, formatação de celular e fixo, e separação de vários números colados juntos |
| `imagens.py`, `utils.py` | Imagens em base64 e localização dos arquivos (inclusive dentro do `.exe`) |
| `atualizacao.py` | Consulta a última release no GitHub e compara versões |
| `preferencias.py` | Tema e nome do funcionário salvos em `%APPDATA%\GeradorEmailHepta` |
| `registro.py` | Log de erros em `%APPDATA%\GeradorEmailHepta\gerador.log` |
| `temas.py`, `tema_manager.py` | Paleta clara/escura, fontes e troca de tema |
| `config.py` | Versão atual, limites e configurações |
| `autoteste.py` | Verificação do executável usada no workflow de release |
| `assets/` | Logo e imagem do WinVNC usadas nos e-mails |

### Alterar o texto de um e-mail

Edite o arquivo em `templates/`. Os campos variáveis aparecem como `$titulo`, `$telefones`, `$data_hora`, `$num_req`, `$tentativa_texto` e `$imagem_winvnc`. O bloco de assinatura (nome, cargo, telefone `(61) 3424-4800` e logo) fica num só lugar, `templates/partes/assinatura.html`, e entra nos e-mails pelo campo `$assinatura`. Para escrever um `$` literal no texto, use `$$`. Depois, atualize os snapshots (seção anterior).

O botão **Copiar e-mail** usa o mesmo HTML: ele remove os blocos `dica-copy` e `creditos` e embute o CSS do `<style>` em cada elemento. Se criar uma classe CSS nova num modelo, ela é embutida automaticamente.

### Decisões importantes

- **Cores dos temas:** todo widget recebe a cor como par `(claro, escuro)` através de `cor("nome")`, em `temas.py`. O CustomTkinter troca sozinho ao mudar o tema. Não pinte widgets manualmente na troca de tema; adicione a cor na paleta e use `cor()`.
- **Data/hora:** no modo automático, o horário é lido no clique em gerar (`resolver_data_hora` em `data_hora.py`), nunca na abertura do programa.
- **Textos de uma linha nos labels:** não ajuste `wraplength` dinamicamente em eventos `<Configure>`. A mudança de altura realimenta o redimensionamento e trava a janela.
- **Texto digitado vai escapado no HTML** (`html.escape` em `email_html.py`), para que `<` ou `&` num nome não quebrem o e-mail.
- **Erros:** use `logging` (`log = logging.getLogger(__name__)`), não `print()`. O executável não tem console.

## Gerar o executável localmente

```bash
pyinstaller --noconfirm --clean --onefile --windowed --name GeradorEmailHepta --collect-all customtkinter --add-data "assets;assets" --add-data "templates;templates" main.py
dist\GeradorEmailHepta.exe --autoteste
```

O autoteste não abre janela: sai com código 0 se os modelos e as imagens estiverem dentro do `.exe` (confira com `echo %ERRORLEVEL%` no cmd ou `$LASTEXITCODE` no PowerShell). As pastas `build/` e `dist/` e o `.spec` gerado são ignorados pelo Git.

## Publicar uma nova versão

A publicação é automática pelo [workflow de release](../.github/workflows/release.yml), disparado por uma tag:

1. Atualize `VERSAO_ATUAL` em [`config.py`](../config.py) (ex: `"2.7"`).
2. Registre as mudanças no [CHANGELOG](../CHANGELOG.md), numa seção `## [2.7] - AAAA-MM-DD`.
3. Faça o commit e o push na `main`.
4. Crie e envie a tag:

   ```bash
   git tag v2.7
   git push origin v2.7
   ```

O GitHub então confere se a tag bate com `VERSAO_ATUAL`, roda lint e testes, gera o `.exe`, roda o autoteste nele e publica a release com o `.exe` anexado e a seção do CHANGELOG como descrição. Se qualquer etapa falhar, nada é publicado. Acompanhe na aba **Actions** do repositório.

Assim que a release aparece, os programas abertos nas máquinas da equipe mostram o aviso de atualização em até 4 horas (ou ao abrir).

> **Atenção:** a versão da tag precisa ser maior que a das versões instaladas para elas exibirem o aviso. Se `VERSAO_ATUAL` não for atualizada no código, o workflow falha na primeira etapa.
