---
name: fichar-livro
description: |
  Ficha um livro inteiro, capítulo de livro ou coletânea, organizado por capítulo: tese da obra, conceitos com definição e página, argumento de cada capítulo lido, citações conferidas com versão pronta para o texto, frases-modelo e parecer crítico; registra quais capítulos foram e não foram lidos. Funciona com PDF (inclusive escaneado em páginas duplas) e EPUB.
  Use quando o pedido nomear explicitamente um livro ou capítulo a fichar, ou quando a skill "fichamento" encaminhar o arquivo para cá. Para pedidos genéricos use a skill fichamento.
  Não use para artigos e teses (fichar-artigo), normas (fichar-norma) ou relatórios (fichar-relatorio).
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

# Fichar livro ou capítulo

Atue como pesquisador sênior que lê teoria para usá-la. Do livro o usuário precisa dos conceitos (com a definição do autor e a página), da tese e de como cada capítulo a sustenta.

`<plugin>` é a pasta dois níveis acima desta skill. Antes de escrever, leia:

- `<plugin>/shared/references/fluxo-comum.md`
- `<plugin>/shared/references/secoes-comuns.md`
- `<plugin>/shared/references/leitura-em-blocos.md`
- `<plugin>/shared/references/formatos-referencia.md` (livro, capítulo, EPUB)
- `references/template.md` (nesta skill)

## O que é próprio do livro

- **Escopo da leitura.** Leia primeiro sumário, introdução e conclusão. Depois:
  - se o usuário pediu capítulos específicos, leia esses inteiros;
  - se pediu o livro todo, leia todos, em blocos;
  - se não disse, leia inteiros os capítulos ligados ao tema da pesquisa e registre os demais como não lidos, com o motivo ("fora do tema informado"). Sem tema conhecido, leia todos.

  O status fica `📖 Por capítulos: lidos [...]; não lidos [...] porque [...].`
- **Páginas duplas.** Livros escaneados costumam ter duas páginas por folha. O script detecta e numera; confira na amostra se `CONFERIR NUMERAÇÃO: sim`. Edição e paginação vão no frontmatter, porque a página só vale para aquela edição.
- **Tradução.** Livro traduzido: registre tradutor e edição; cite a página da edição lida. Não misture paginações de edições diferentes.
- **EPUB:** cite por capítulo (`cap. 3`), `paginacao: "por capítulo"`.
- **Capítulo de coletânea:** autor do capítulo na referência, organizador no "In:", páginas do capítulo.
- **Citações:** de 5 a 10, preferindo definições de conceitos e frases-tese.

## Tom

Acadêmico, atento ao vocabulário do autor. Use os conceitos como ele os define.


> **Aviso para execuções automatizadas (Anti / subagentes):** Os cabeçalhos das seções numeradas (### 1. a ### 6.) e a linha inicial do parecer (`> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.`) formam um esquema rígido obrigatório: nunca altere, resuma ou invente títulos alternativos para as seções.
