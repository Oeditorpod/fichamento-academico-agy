# Modelo do fichamento de relatório, notícia ou infográfico

As partes marcadas com (comum) seguem `shared/references/secoes-comuns.md`.

````markdown
---
[frontmatter (comum), seção 1; tipo: relatorio | noticia | infografico; acrescente:]
produtor: "[órgão, ONG, associação, empresa, veículo]"
natureza_produtor: "[governo | ONG | setor privado | academia | imprensa | multilateral]"
data_publicacao: "[AAAA-MM-DD ou AAAA]"
periodo_dados: "[período de referência dos dados]"
---

# [Título] ([PRODUTOR, ano])

### 1. Referência bibliográfica

- **ABNT:** [...]
- **APA 7:** [...]

[status da leitura (comum), seção 2]

### 2. Conteúdo

> Relato fiel do documento. Toda afirmação traz a página (ou s.p.).

- **Quem produziu e com que propósito:** [declarado no documento] (p. X).
- **Pergunta ou objetivo:** [...] (p. X).
- **Recorte:** [área, período, setor] (p. X).
- **Metodologia e fontes de dados:** [bases, método, período, limitações declaradas] (p. X).
- **Principais achados:**
  - [número com unidade, recorte, ano de referência e fonte primária] (p. X).
- **Recomendações ou posições defendidas:** [...] (p. X).
- **Limitações declaradas:** [...] (p. X).

### 3. Conceitos, dados e definições

[(comum), seção 3; para cada número: valor | unidade | recorte | ano | fonte primária | página]

### 4. Citações

[tabela híbrida (comum), seção 4]

### 5. Como citar no texto

[(comum), seção 5; atribuindo a fonte: "Segundo o [PRODUTOR] (ano, p. X), ..."]

### 6. Parecer crítico

> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.

- **Confiabilidade:** [transparência metodológica, fonte primária identificável, revisão externa].
- **Interesse e viés possível:** [posição do produtor; o que isso pode afetar].
- **Atualidade:** [defasagem entre dados e publicação].
- **Como triangular:** [que outra fonte confirmaria os números principais].
- **Conexão com a pesquisa do usuário:** [...]

[registro de mudanças (comum), seção 7, só ao completar]
````

## Versão curta (notícia, infográfico, página web)

Mesmo frontmatter, referência e status; depois:

- **Conteúdo** em até seis itens (quem, o quê, dados, fonte ouvida, data).
- **Conceitos, dados e definições** só com os números.
- **Citações**: de 2 a 5.
- **Como citar** e **Parecer** em até quatro itens.
