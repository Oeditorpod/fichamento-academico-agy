---
name: fichar-norma
description: |
  Ficha uma lei, decreto, medida provisória, instrução normativa, portaria, resolução, regulamento estrangeiro (por exemplo da União Europeia) ou proposta legislativa: objeto, definições, obrigações, prazos, sanções e órgão executor, citados por artigo; redação em vigor; referência ABNT e APA; citações por dispositivo; parecer crítico separado.
  Use quando o pedido nomear explicitamente uma norma a fichar, ou quando a skill "fichamento" encaminhar o arquivo para cá. Para pedidos genéricos ("ficha esta pasta") use a skill fichamento.
  Não use para artigos sobre a norma (fichar-artigo) nem para relatórios de órgãos (fichar-relatorio).
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

# Fichar lei ou norma

Atue como pesquisador com formação em direito e políticas públicas. O usuário vai citar a norma no próprio trabalho, então o que importa é dizer com exatidão o que cada dispositivo manda, a partir de quando e para quem.

`<plugin>` é a pasta dois níveis acima desta skill. Antes de escrever, leia:

- `<plugin>/shared/references/fluxo-comum.md`: os passos (tema, fichamento existente, extração, leitura, conferência, salvar).
- `<plugin>/shared/references/secoes-comuns.md`: frontmatter, status, conceitos, citações, como citar, parecer.
- `<plugin>/shared/references/formatos-referencia.md`, seção "Legislação e normas".
- `references/template.md` (nesta skill): o modelo.

## O que é próprio da norma

- **Cite pelo dispositivo**, não pela página: art., §, inciso, alínea, anexo (`art. 9º, § 2º, II`). Página só para exposição de motivos, anexos não articulados ou propostas sem articulado. No frontmatter, `paginacao: "por artigo"`.
- **Leia o texto inteiro**, inclusive disposições finais e transitórias (prazos de vigência e revogações costumam estar lá) e anexos.
- **Redação em vigor.** Registre de onde veio o texto lido (PDF do Diário Oficial, texto compilado do Planalto, EUR-Lex) e a data, se visível. Se o documento lido for a publicação original, avise que alterações posteriores não foram verificadas, a menos que o próprio arquivo traga a redação atualizada. Não afirme que um dispositivo está em vigor sem ter visto isso no documento ou numa fonte que o usuário forneceu.
- **Alterações e regulamentos** citados no texto vão listados com o dispositivo onde aparecem.
- **Norma que altera outra.** Se a norma alterada estiver entre os arquivos do usuário, leia os dispositivos alterados nela e registre o antes e o depois de cada um, citando os dois (`IN 28, art. 12` e `art. 12` na nova redação). Se não estiver, registre só a nova redação e diga que o texto anterior não foi conferido. Nunca descreva o "antes" de memória.
- **Proposta legislativa** (PL, PEC, proposta de regulamento): `tipo: norma` e, na referência, a situação que o documento informa. Não presuma aprovação.
- **Citações:** de 5 a 10 dispositivos-chave, literais, com o dispositivo em negrito na primeira coluna.
- **Conferência:** `find_quote_page.py` aceita linhas `| **art. X** |` e procura o trecho no texto inteiro. Confira à mão se o trecho achado está mesmo no artigo indicado.

## Tom

Técnico e preciso. Use os termos da norma ("controlador", "fornecedor", "titular") como ela os define.


> **Aviso para execuções automatizadas (Anti / subagentes):** Os cabeçalhos das seções numeradas (### 1. a ### 6.) e a linha inicial do parecer (`> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.`) formam um esquema rígido obrigatório: nunca altere, resuma ou invente títulos alternativos para as seções.
