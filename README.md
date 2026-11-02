# Fichamento Acadêmico Rigoroso (Anti / AGY)

[![Plugin Antigravity](https://img.shields.io/badge/Plugin-Google%20Antigravity-blue)](https://github.com/Oeditorpod/fichamento-academico-agy)
[![Versão](https://img.shields.io/badge/versão-2.1.0-green.svg)](CHANGELOG.md)
[![Licença: MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-yellow.svg)](LICENSE)

Plugin oficial criado e mantido com exclusividade para o assistente **Anti** ([Google Antigravity](https://deepmind.google/)). Transforma referências bibliográficas de uma pesquisa acadêmica (artigos científicos, teses de doutorado, dissertações de mestrado, leis e normas, relatórios institucionais, notícias e livros) em fichamentos estruturados de alto rigor, com o número exato de página ou dispositivo de lei para cada afirmação e conferência estrita de 100% das citações literais.

Feito para pesquisadores que utilizam o Anti para construir um banco de dados confiável, reprodutível e livre de alucinações durante a redação de dissertações, teses e artigos científicos.

---

## 🤖 Arquitetura e Otimizações para o Anti

Esta edição (`fichamento-academico-agy`) foi desenvolvida sob medida para o fluxo do Anti:
1. **Manifesto Nativo `plugin.json`**: Total aderência ao sistema de plugins do Google Antigravity, tanto em nível global (`~/.gemini/config/plugins/`) quanto de projeto local (`.agents/plugins/`).
2. **Instalador e Atualizador em Um Comando**: Scripts `instalar.ps1` (PowerShell/Windows) e `instalar.sh` (Bash/Linux/macOS) que configuram os diretórios `.agents/plugins/`, `.agents/skills/` e `.agents/shared/` com um clique.
3. **Esquema Rígido para Subagentes**: Templates calibrados para execuções massivas e paralelas via `invoke_subagent`, garantindo que os subagentes preservem exatamente a numeração formal de cabeçalhos (`### 1.` a `### 6.`) e o parecer crítico separado.
4. **Conferência Estrita de Citações (`find_quote_page.py`)**: Script embutido que valida cada citação literal contra o texto extraído do documento original, garantindo tolerância zero para páginas incorretas ou citações truncadas.
5. **Homologado em Lote Extensivo**: Validado e aprovado em teste de estresse com **77 documentos acadêmicos (~2.350 páginas)**, cobrindo artigos em duas colunas, leitura em blocos e compilação automatizada de índice (`_indice.md`).

---

## As 6 Skills Integradas

| Skill | Escopo e Função |
| :--- | :--- |
| **`fichamento`** | **Porta de entrada e orquestrador de lote.** Recebe um arquivo ou pasta inteira, classifica o tipo de cada documento, identifica fichamentos existentes para completar, encaminha para a skill especialista e compila o `_indice.md` com status de leitura e pendências. |
| **`fichar-artigo`** | Artigos científicos, teses de doutorado, dissertações de mestrado e preprints: anatomia metodológica completa, variáveis, instrumentos, resultados quantitativos com página e parecer crítico. |
| **`fichar-norma`** | Leis, decretos, resoluções, portarias, instruções normativas e propostas legislativas: objeto, definições, obrigações, prazos, sanções e competências citados por artigo. |
| **`fichar-relatorio`** | Relatórios institucionais (governamentais, ONGs, empresas), notas técnicas, notícias e infográficos: análise da proveniência de cada número, metodologia, conflito de interesses e confiabilidade da fonte. |
| **`fichar-livro`** | Livros autorais, capítulos de livro e coletâneas: tese central, argumento capítulo a capítulo, conceitos e definições do autor com página. Suporta PDF e EPUB. |
| **`conferir-citacoes`** | Auditoria e conferência de citações literais de fichamentos existentes contra os documentos originais via `find_quote_page.py`, gerando relatório de conformidade. |

---

## O que cada fichamento traz

1. **Frontmatter YAML Canônico**: compatível com Obsidian, Notion, Zotero e scripts de indexação (tipo, tags, status de leitura, paginação, data, tema de pesquisa).
2. **Referência Bibliográfica Completa**: formatada rigorosamente em **ABNT NBR 6023:2018** e **APA 7**.
3. **Status da Leitura Transparente**: `✅ integral`, `📖 por capítulos`, `🟡 parcial` (com o motivo) ou `❌ não lido`.
4. **Conteúdo com Rastreabilidade de Página**: toda afirmação traz a página correspondente entre parênteses `(p. X)`.
5. **Conceitos, Dados e Definições**: termos-chave, siglas e métricas quantitativas com unidade, ano e recorte.
6. **Tabela Híbrida de Citações Literais**: trechos literais no idioma original, tradução/paráfrase, indicação de uso e versão pronta para o texto com citação indireta/direta em ABNT.
7. **Como Citar no Texto**: frases-modelo neutras e frases aplicadas ao tema informado pelo pesquisador.
8. **Parecer Crítico Separado**: iniciado expressamente com `> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.`, avaliando rigor, vieses, limitações e utilidade.

---

## Requisitos do Sistema

- **Python**: versão 3.9 ou superior.
- **Bibliotecas Python recomendadas**:
  ```bash
  pip install pymupdf pdfplumber openpyxl python-docx ebooklib beautifulsoup4
  ```
  - `pymupdf`: extração de texto de PDFs, reordenação de 2 colunas e páginas duplas (obrigatório).
  - `pdfplumber`: extração tabular de alta precisão em PDFs.
  - `python-docx`: leitura de documentos `.docx`.
  - `ebooklib` & `beautifulsoup4`: leitura de livros `.epub` e páginas `.html`.
  - `openpyxl`: exportação de tabelas para planilhas `.xlsx`.
  - `ocrmypdf`, `tesseract` e `ghostscript`: opcionais para OCR de PDFs escaneados sem camada de texto.

Para checar seu ambiente:
```bash
python shared/scripts/verificar_requisitos.py
```

---

## Instalação e Atualização

### Instalação no Workspace Atual (Recomendado para Projetos)
No terminal do seu projeto:
```powershell
# No Windows (PowerShell)
git clone https://github.com/Oeditorpod/fichamento-academico-agy .agents/plugins/fichamento-academico-agy
.\.agents\plugins\fichamento-academico-agy\instalar.ps1
```
```bash
# No Linux ou macOS (Bash)
git clone https://github.com/Oeditorpod/fichamento-academico-agy .agents/plugins/fichamento-academico-agy
./.agents/plugins/fichamento-academico-agy/instalar.sh
```

### Instalação Global no Antigravity
Para disponibilizar o plugin em qualquer projeto do seu usuário:
```powershell
# No Windows (PowerShell)
.\instalar.ps1 -Global
```
```bash
# No Linux ou macOS (Bash)
./instalar.sh --global
```

### Como Atualizar
Como o plugin é gerenciado via Git, basta rodar:
```bash
git pull
```
Ou simplesmente pedir ao Anti no chat:
> *"Anti, atualize o plugin de fichamento."*

---

## Como Usar com o Anti

Basta interagir com o Anti em linguagem natural:

- *"Anti, ficha todos os PDFs da pasta referencias/ e gera o índice com as pendências."*
- *"Anti, ficha este artigo científico [nome_do_arquivo.pdf] com base no tema da minha pesquisa."*
- *"Anti, confere se as citações do fichamento [fichamento_Silva_2024.md] batem exatamente com as páginas do PDF original."*
- *"Anti, resume este livro capítulo por capítulo dando ênfase aos conceitos do autor."*

O orquestrador `fichamento` inspecionará os arquivos, apresentará a tabela de roteamento de skills e executará a leitura com extração fiel e conferência estrita.

---

## Licença

Distribuído sob licença [MIT](LICENSE). Desenvolvido por [Oeditorpod](https://github.com/Oeditorpod) com exclusividade para o assistente **Anti** e a comunidade acadêmica.
