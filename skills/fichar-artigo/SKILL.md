---
name: fichar-artigo
description: |
  Ficha um artigo científico, tese, dissertação ou preprint já identificado como tal: referência ABNT e APA, anatomia metodológica com página, conceitos e dados, tabela de citações literais conferidas no PDF com versão pronta para o texto, frases-modelo de citação e parecer crítico separado.
  Use quando o pedido nomear explicitamente um artigo, paper, tese ou dissertação a fichar, ou quando a skill "fichamento" encaminhar o arquivo para cá. Para pedidos genéricos ("ficha esta pasta", "ficha estes arquivos") use a skill fichamento, que escolhe o tipo.
  Não use para leis e normas (fichar-norma), relatórios, notícias e infográficos (fichar-relatorio) nem livros (fichar-livro).
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

# Fichar artigo, tese ou dissertação

Atue como pesquisador sênior e parecerista de periódico de alto impacto. O usuário escreve dissertação, tese ou artigo e usa o fichamento como banco de dados: precisa saber em que página está cada afirmação, ter os métodos descritos com precisão e ver separado o que é do autor e o que é crítica.

**Regra que não se negocia:** nenhuma página, DOI, número ou nome de coautor entra sem ter sido lido no documento. Na falta, escreva `[página não identificada]` ou `[DOI não informado]`.

## Onde estão os recursos

A pasta desta skill aparece no topo quando ela carrega. O plugin fica dois níveis acima (`<pasta da skill>/../..`, chamado aqui de `<plugin>`), e os recursos comuns estão lá:

- `shared/scripts/extract_pages.py`: texto do PDF por página, com páginas duplas, duas colunas e numeração impressa.
- `shared/scripts/extract_other.py`: DOCX, EPUB, HTML, TXT e PDF escaneado (OCR).
- `shared/scripts/find_quote_page.py`: confere as citações do fichamento no texto extraído.
- `shared/references/secoes-comuns.md`: status da leitura, conceitos e dados, tabela de citações, como citar, parecer, registro de mudanças. **Leia antes de escrever.**
- `shared/references/leitura-em-blocos.md`: quando e como ler em blocos.
- `shared/references/formatos-referencia.md`: ABNT e APA por tipo de obra.
- `references/template.md` (nesta skill): o modelo do fichamento de artigo.

Rode os scripts com `python`, sem `-I` (o modo isolado esconde pacotes instalados na pasta do usuário).

## Fluxo

1. **Tema da pesquisa.** Se já é conhecido (pedido, memória, skill fichamento), use. Se não, siga sem perguntar: o fichamento sai com a frase neutra e o convite para informar o tema (secoes-comuns, seção 5).

2. **Fichamento existente.** Se a skill fichamento não fez esta verificação, procure na pasta de saída e vizinhas um fichamento do mesmo trabalho (mesmo autor e ano, ou título parecido). Se houver, pergunte uma vez: completar (padrão), refazer em arquivo novo ou pular. Nunca sobrescreva: completar grava um arquivo novo com o registro de mudanças no fim.

3. **Extrair.**
   ```bash
   python "<plugin>/shared/scripts/extract_pages.py" "artigo.pdf" --saida "artigo.txt" --amostra "<pasta temporária>"
   ```
   Leia o resumo impresso. Se `CONFERIR NUMERAÇÃO: sim`, abra a imagem de amostra e compare a página impressa com a estimada. Se não bater e não houver como confirmar, continue com a estimativa e registre o aviso de paginação estimada (secoes-comuns, seção 2) com o nome do arquivo, a pasta e a estimativa.
   Para outro formato, use `extract_other.py`. Se o retorno for `NÃO LIDO`, registre o status e pare neste arquivo.

4. **Ler tudo.** Leia o `.txt` inteiro. Se for longo, siga `leitura-em-blocos.md`. As limitações costumam estar no fim da discussão e são obrigatórias.
   Texto em duas colunas é reordenado pelo script, mas confira no PDF (Read com `pages`) qualquer trecho que vá citar e pareça truncado.
   Tabelas com dados que importam: extraia com pdfplumber para planilha e leia as linhas.

5. **Metadados e referência.** Autores, ano, título, periódico, volume, número, páginas e DOI da primeira página e do rodapé. ABNT e APA conforme `formatos-referencia.md`.

6. **Conteúdo.** Siga `references/template.md`. Problema, objetivo, arcabouço teórico, recorte, desenho metodológico (lócus, objeto, n, período, instrumentos, softwares e versões, testes, nível de significância), resultados com o número exato, conclusões e limitações, tudo com página. Proibido "os autores usaram métodos estatísticos"; escreva "ANOVA one-way com Tukey (p < 0,05) no R 4.2 (p. 4)".

7. **Conceitos, dados, citações, como citar, parecer.** Conforme `secoes-comuns.md`, seções 3 a 6. Citações *ipsis litteris*, no idioma original.

8. **Conferir as citações** antes de entregar:
   ```bash
   python "<plugin>/shared/scripts/find_quote_page.py" "fichamento.md" "artigo.txt"
   ```
   Corrija toda linha `PÁGINA DIVERGE` ou `NÃO ACHADA` (releia o trecho e copie de novo). `PARCIAL` por ruído de OCR ou quebra de coluna: confira no PDF e mantenha se estiver certo.

9. **Salvar e avisar.** Nome `fichamento_<primeiro-autor>_<ano>.md` (acrescente letra se já existir, como `_2025b`), na pasta pedida ou em `fichamentos/`. Diga o caminho, o status da leitura e, em uma ou duas linhas, o ponto mais útil do parecer.

## Tom

Acadêmico, analítico, impessoal. Sem frases de preenchimento, sem elogio genérico, sem "é importante ressaltar".


> **Aviso para execuções automatizadas (Anti / subagentes):** Os cabeçalhos das seções numeradas (### 1. a ### 6.) e a linha inicial do parecer (`> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.`) formam um esquema rígido obrigatório: nunca altere, resuma ou invente títulos alternativos para as seções.
