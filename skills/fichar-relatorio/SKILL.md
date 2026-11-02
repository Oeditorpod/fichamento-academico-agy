---
name: fichar-relatorio
description: |
  Ficha relatório técnico ou institucional, nota técnica, boletim, base de dados com nota metodológica, notícia, página web ou infográfico: quem produziu e com que interesse, metodologia e fonte dos dados, números-chave com página, achados e recomendações, citações conferidas, frases-modelo e parecer crítico sobre a confiabilidade da fonte.
  Use quando o pedido nomear explicitamente um relatório, nota técnica, notícia ou infográfico a fichar, ou quando a skill "fichamento" encaminhar o arquivo para cá. Para pedidos genéricos use a skill fichamento.
  Não use para artigos revisados por pares (fichar-artigo), normas (fichar-norma) ou livros (fichar-livro).
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

# Fichar relatório, notícia ou infográfico

Atue como pesquisador que usa literatura cinzenta com cautela. Relatórios de ONGs, governos, associações e consultorias costumam trazer os dados mais atuais, mas não passam por revisão por pares e às vezes defendem uma posição. O fichamento precisa deixar claro de onde vem cada número e quem está falando.

`<plugin>` é a pasta dois níveis acima desta skill. Antes de escrever, leia:

- `<plugin>/shared/references/fluxo-comum.md`
- `<plugin>/shared/references/secoes-comuns.md`
- `<plugin>/shared/references/formatos-referencia.md` (documento institucional; página web, notícia e infográfico)
- `references/template.md` (nesta skill)

## O que é próprio deste tipo

- **Autoria e interesse.** Quem produziu (órgão, ONG, associação setorial, empresa, consultoria), quem financiou, se declarado, e qual posição o documento defende. Separe o que o documento declara do que você infere.
- **Proveniência de cada número.** Para cada dado-chave: valor, unidade, recorte, ano de referência, fonte primária (ex.: "IBGE, PNAD Contínua, 2º tri. 2024") e página. Se o documento não diz a fonte, escreva "fonte não informada".
- **Metodologia.** Em relatório: período, área, base de dados, método de cálculo, limitações. Em notícia: quem é a fonte ouvida e se o dado vem de documento identificável.
- **Datas.** Data de publicação e data de referência dos dados podem diferir; registre as duas.
- **Tamanho proporcional.** Relatório longo segue o modelo inteiro; notícia ou infográfico usam a versão curta do modelo (de 2 a 5 citações).
- **Sem paginação** (infográfico, página web): `paginacao: "s.p."`; cite (AUTOR, ano, s.p.).
- **Tabelas de dados:** extraia para planilha (pdfplumber + openpyxl) e leia todas as linhas que usar.

## Tom

Analítico. Atribua sempre: "segundo o Ipea (2023, p. 4)", nunca o dado solto como fato.


> **Aviso para execuções automatizadas (Anti / subagentes):** Os cabeçalhos das seções numeradas (### 1. a ### 6.) e a linha inicial do parecer (`> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.`) formam um esquema rígido obrigatório: nunca altere, resuma ou invente títulos alternativos para as seções.
