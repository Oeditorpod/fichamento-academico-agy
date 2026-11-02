---
name: fichamento
description: |
  Porta de entrada do plugin de fichamento acadêmico. Recebe um ou vários arquivos, ou uma pasta, identifica o tipo de cada documento (artigo, tese, lei ou norma, relatório, notícia, infográfico, livro), mostra a tabela arquivo, tipo e skill, encaminha cada um para a skill certa (fichar-artigo, fichar-norma, fichar-relatorio, fichar-livro), procura fichamentos já existentes para completar em vez de duplicar e, ao fim, gera o índice com status de leitura e pendências.
  Use sempre que o usuário pedir para fichar, resumir, extrair citações, "ler" ou analisar documentos para a própria pesquisa sem dizer que tipo de documento é, mesmo sem a palavra "fichamento": "ficha essa pasta", "me passa os pontos principais desses PDFs", "tira as citações com página desses arquivos", "monta as fichas de leitura das referências", "resume isso para a minha dissertação". Também para fichar em lote.
  Não use para revisão por pares simulada, para redigir o texto do próprio usuário ou para buscar literatura nova.
  Gatilhos: fichamento, fichar, ficha de leitura, fichar pasta, fichar referências, resumo para dissertação, extrair citações, citações com página.
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
  - AskUserQuestion
---

# Fichamento: escolher a skill e organizar o lote

Esta skill não escreve fichamentos sozinha: decide o que ler, com qual skill, e mantém o lote organizado. `<plugin>` é a pasta dois níveis acima desta skill. Antes de começar, leia `<plugin>/shared/references/leitura-em-blocos.md` (escopo de leitura) e `<plugin>/shared/references/secoes-comuns.md` (status).

## 1. Escopo

Leia exatamente o que o usuário pediu: a pasta inteira, com subpastas, se ele indicou uma pasta; só os arquivos nomeados, se nomeou arquivos. Liste os arquivos com Glob.

Na primeira vez num lote, rode `python "<plugin>/shared/scripts/verificar_requisitos.py"` (sem `-I`). Se faltar algo, diga em uma linha o que falta e quais arquivos isso afeta, e siga: esses arquivos sairão como parcial ou não lido, com o motivo. Não instale nada sem o usuário pedir.

## 2. Tema da pesquisa

Use o tema se já for conhecido (pedido, contexto da conversa ou memória do Anti). Se não for, pergunte uma vez, junto com a tabela do passo 4, e diga que pode seguir sem: os fichamentos sairão com frases neutras e o convite para informar o tema.

## 3. Classificar cada arquivo

Decida o tipo nesta ordem e pare no primeiro sinal claro:

1. **Pasta e nome do arquivo.** Pastas como `artigos/`, `leis-e-normas/`, `relatorios/`, `livros/`, `noticias/`; nomes com `Lei`, `Decreto`, `IN`, `Portaria`, `Resolução`, `Regulamento`, `PL`, `tese`, `dissertação`.
2. **Primeira página** (extraia só ela: `extract_pages.py` e leia o começo). Sinais:
   - artigo: nome do periódico, DOI, resumo/abstract, palavras-chave, "Received/Accepted";
   - tese ou dissertação: "Programa de Pós-Graduação", "Tese apresentada", "Dissertação", banca;
   - norma: ementa, "O PRESIDENTE DA REPÚBLICA", "Art. 1º", "Regulamento (UE)", considerandos;
   - relatório: logotipo e nome de órgão, ONG ou empresa, "Relatório", "Nota técnica", "Sumário executivo", ISBN institucional;
   - notícia ou página web: nome do veículo, data e autor de matéria, HTML;
   - infográfico: uma ou poucas folhas, quase só números e imagens;
   - livro: editora, ISBN, ficha catalográfica, sumário com capítulos.
3. **Formato.** EPUB → livro. HTML → notícia ou página web, a menos que seja texto de lei (Planalto, DOU, EUR-Lex) → norma. Imagem → infográfico.

Se os sinais discordarem (um livro guardado em `artigos/`, um arquivo com nome sem sentido), vale a primeira página. Na dúvida entre dois tipos, escolha e marque a linha da tabela com "(conferir)".

Mapa de skills: artigo, tese, dissertação, preprint → `fichar-artigo`; norma e proposta legislativa → `fichar-norma`; relatório, nota técnica, notícia, página web, infográfico, base de dados → `fichar-relatorio`; livro e capítulo de livro → `fichar-livro`.

Fora do lote, com o motivo: notas de trabalho do próprio usuário (rascunhos, anotações, listas), duplicatas (mesmo conteúdo com outro nome), arquivos vazios, formatos sem leitor.

## 4. Fichamentos existentes

Para cada arquivo, procure fichamento do mesmo documento na pasta de saída e em pastas próximas (`fichamentos*`), por `arquivo_fonte` no frontmatter ou por autor e ano no nome. Achando, a ação padrão é **completar**.

Mostre ao usuário, antes de começar, uma tabela única:

| Arquivo | Tipo | Skill | Fichamento existente | Ação |
| --- | --- | --- | --- | --- |
| artigos/Silva_2024.pdf | artigo | fichar-artigo | fichamentos/fichamento_Silva_2024.md | completar |
| leis/Lei_12651.pdf | norma | fichar-norma | não | fichar |
| notas/rascunho.md | nota de trabalho | — | — | pular (não é referência) |

Pergunte uma vez se pode seguir assim; o usuário pode mudar tipo ou ação (completar, refazer, pular) de qualquer linha. Num pedido de um só arquivo sem fichamento existente, não pergunte: siga.

- **Completar:** parta do fichamento existente, acrescente o que falta pelo modelo novo, corrija o que a conferência mostrar errado, e grave em arquivo novo (ou na pasta nova pedida) com o registro de mudanças no fim. O original não é tocado.
- **Refazer:** fichamento novo do zero, em arquivo novo. O antigo fica.
- **Nunca sobrescreva** um fichamento existente.

## 5. Fichar

Para cada arquivo da tabela, carregue a skill do tipo e siga o fluxo dela por inteiro. Um arquivo por vez; cada fichamento com a mesma densidade, sem encurtar para caber o lote. Documentos acima de cerca de 300 páginas: avise antes ("[arquivo], [N] páginas, vai demorar") e siga.

Avisos que dependem do usuário (paginação estimada, documento parcial) não param o lote: registre no fichamento e junte para o índice.

## 6. Índice

No fim, grave `_indice.md` na pasta de saída:

```markdown
# Índice de fichamentos ([data])

Tema da pesquisa: [tema ou "não informado"]

| Fichamento | Referência curta | Tipo | Status da leitura | Utilidade principal |
| --- | --- | --- | --- | --- |
| [fichamento_Silva_2024.md](fichamento_Silva_2024.md) | SILVA, 2024 | artigo | ✅ integral | [...] |

## Pendências

- **Paginação estimada:** [arquivo] em [pasta]; estimativa [página do PDF X = p. Y]. Confira e corrija.
- **Referências a decidir:** [mesmo autor e ano (2025a/2025b), DOI não localizado, data incerta].
- **Leitura parcial:** [arquivo]: [o que ficou de fora e por quê].

## Arquivos não fichados

| Arquivo | Motivo |
| --- | --- |
| notas/rascunho.md | nota de trabalho, não é referência |
```

Se já existir `_indice.md`, grave `_indice_<data>.md` e diga isso.

## 7. Resposta ao usuário

Curta: quantos fichamentos por tipo, onde estão, quantos completados e quantos novos, e as pendências que pedem ação dele (com nome do arquivo e pasta). O detalhe fica no índice.


> **Aviso para execuções automatizadas (Anti / subagentes):** Os cabeçalhos das seções numeradas (### 1. a ### 6.) e a linha inicial do parecer (`> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.`) formam um esquema rígido obrigatório: nunca altere, resuma ou invente títulos alternativos para as seções.
