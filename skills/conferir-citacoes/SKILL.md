---
name: conferir-citacoes
description: |
  Confere as citações de fichamentos já prontos contra o documento original: acha cada trecho literal no texto extraído, diz se a página (ou o artigo de lei) bate, aponta citações não encontradas ou transcritas com erro e propõe a correção. Funciona com um fichamento ou uma pasta inteira, gerando um relatório.
  Use quando o usuário pedir para conferir, checar, verificar ou validar as citações ou as páginas de um fichamento, ou antes de levar citações para um texto que vai para banca ou periódico.
  Não use para conferir as referências bibliográficas de um artigo do próprio usuário contra bases externas, nem para fichar documentos novos (skill fichamento).
license: MIT
metadata:
  version: "2.0.0"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Conferir citações de fichamentos

`<plugin>` é a pasta dois níveis acima desta skill. Rode os scripts com `python`, sem `-I`.

## Fluxo

1. **Juntar os pares.** Para cada fichamento, ache o documento original: campo `arquivo_fonte` do frontmatter; senão, pelo nome (autor e ano) na pasta de referências. Fichamento sem original encontrado vai para o relatório como "original não localizado", com o caminho procurado.

2. **Extrair o original**, se ainda não houver `.txt`:
   - PDF: `python "<plugin>/shared/scripts/extract_pages.py" "doc.pdf" --saida "doc.txt"`
   - outros formatos: `python "<plugin>/shared/scripts/extract_other.py" "doc.ext" --saida "doc.txt"`

3. **Conferir:**
   ```bash
   python "<plugin>/shared/scripts/find_quote_page.py" "fichamento.md" "doc.txt" --saida "conferencia.md"
   ```
   O script lê as linhas da tabela de citações que começam com `| **p.`, `| **art.`, `| **cap.`, `| **s.p.**`, `| **seção` ou `| **considerando`.

4. **Investigar cada problema:**
   - `PÁGINA DIVERGE` ou `ARTIGO DIVERGE`: o script mostra onde o trecho está. Confirme abrindo a página no PDF (Read com `pages`) antes de propor a correção; a numeração do texto extraído pode estar estimada.
   - `NÃO ACHADA`: procure partes menores do trecho com `--trecho "..."`. Se achar, a transcrição tem erro: mostre a forma certa. Se não achar nada, abra o PDF: pode ser erro de extração (tabela, figura, coluna). Se o trecho não existir no documento, diga isso com clareza.
   - `PARCIAL`: em geral ruído de OCR ou quebra de coluna. Confira visualmente e diga se está certo.
   - Citações fora da tabela (no corpo do texto, com página entre parênteses) não são lidas pelo script; confira por amostragem as que tiverem número ou frase entre aspas.

5. **Relatório.** Um arquivo `_conferencia_citacoes.md` na pasta dos fichamentos, com uma tabela: fichamento, total de citações, OK, divergentes, não achadas, e a lista de correções propostas (trecho, como está, como deveria ser, como foi confirmado).

6. **Não altere os fichamentos sem pedido.** Pergunte uma vez se deve aplicar as correções. Aplicando, grave um registro de mudanças no fim de cada arquivo alterado (`shared/references/secoes-comuns.md`, seção 7).


> **Aviso para execuções automatizadas (Anti / subagentes):** Os cabeçalhos das seções numeradas (### 1. a ### 6.) e a linha inicial do parecer (`> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.`) formam um esquema rígido obrigatório: nunca altere, resuma ou invente títulos alternativos para as seções.
