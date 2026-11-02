# Modelo do fichamento de artigo, tese ou dissertação

Use esta estrutura. Troque o conteúdo entre colchetes e mantenha os cabeçalhos. As partes marcadas com (comum) seguem `shared/references/secoes-comuns.md`.

````markdown
---
[frontmatter (comum), seção 1; tipo: artigo | tese; acrescente:]
periodico: "[nome do periódico, volume(número)]"
---

# [Título] ([SOBRENOME, ano])

### 1. Referência bibliográfica

- **ABNT (NBR 6023:2018):** SOBRENOME, N.; SOBRENOME, N. Título do artigo. **Nome do Periódico**, v. X, n. Y, p. A-B, AAAA. DOI: 10.xxxx/xxxxx.
- **APA 7:** Sobrenome, N., & Sobrenome, N. (AAAA). Título do artigo. *Nome do Periódico*, *X*(Y), A–B. https://doi.org/10.xxxx/xxxxx

[status da leitura (comum), seção 2]

### 2. Conteúdo e anatomia metodológica

> Relato fiel do documento. Toda afirmação traz a página entre parênteses.

- **Problema de pesquisa / pergunta central:** [...] (p. X).
- **Objetivo geral e específicos:** [...] (p. X).
- **Arcabouço teórico:** [conceitos e autores nomeados] (p. X).
- **Recorte espacial e temporal:** [...] (p. X).
- **Desenho metodológico:**
  - *Tipo de estudo:* [...] (p. X).
  - *Amostragem / n:* [...] (p. X).
  - *Dados, variáveis, instrumentos, equipamentos:* [...] (p. X).
  - *Análise:* [testes, modelos, softwares e versões, nível de significância] (p. X).
- **Principais resultados:**
  - [resultado com número exato, unidade e métrica] (p. X).
- **Conclusões dos autores:** [...] (p. X).
- **Limitações declaradas pelos autores:** [...] (p. X). [Se não houver: "Os autores não declaram limitações."]

### 3. Conceitos, dados e definições

[(comum), seção 3]

### 4. Citações

[tabela híbrida e "Prontas para o texto" (comum), seção 4]

### 5. Como citar no texto

[(comum), seção 5]

### 6. Parecer crítico

> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.

- **Rigor e contribuição:** [...]
- **Fragilidades metodológicas e vieses:** [...] (página do trecho criticado).
- **Premissas questionáveis:** [...]
- **Lacunas de pesquisa:** [...]
- **Conexão com a pesquisa do usuário:** [seção do trabalho onde entra, o que sustenta e o que não cobre; ou "tema não informado"].

[registro de mudanças (comum), seção 7, só ao completar um fichamento existente]
````

## Notas

- Números: na citação literal, mantenha separador e casas do original; na paráfrase, vírgula decimal.
- Tese ou dissertação: no lugar do periódico, use o programa e a instituição; a referência segue o modelo de tese em `formatos-referencia.md`.
- Se o usuário pedir só uma parte (só citações, só parecer), entregue a parte pedida sem perder as páginas.
