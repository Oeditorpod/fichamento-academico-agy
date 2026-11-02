# Seções comuns a todos os fichamentos

Todas as skills de fichamento (artigo, norma, relatório, livro) usam estas peças. O modelo de cada tipo diz onde cada uma entra.

## 1. Frontmatter YAML

```yaml
---
titulo: "[título completo original]"
autores: ["Sobrenome, N.", "Instituição"]
ano: AAAA
tipo: artigo | tese | norma | relatorio | noticia | infografico | livro
fonte: "[periódico, órgão, editora, portal]"
doi: "[10.xxxx/... | não informado | não se aplica]"
idioma: "[pt | en | es ...]"
paginacao: "[impressa | fisica | estimada | por artigo | por capítulo | s.p.]"
status_leitura: "[integral | parcial | por capítulos | via OCR | não lido]"
tema_pesquisa_usuario: "[tema informado, ou 'não informado']"
tags: [fichamento, ...]
data_fichamento: AAAA-MM-DD
arquivo_fonte: "[caminho relativo do arquivo lido]"
---
```

`paginacao: estimada` quando a numeração não pôde ser confirmada (ver seção 2).

## 2. Status da leitura (logo abaixo da referência)

Uma linha, sempre, com o status e o motivo. Use exatamente um destes:

- `✅ Lido por inteiro.`
- `🟡 Parcial: [o que ficou de fora] porque [motivo].` Ex.: "páginas 40-52 sem texto e OCR indisponível".
- `📖 Por capítulos: lidos [capítulos]; não lidos [capítulos] porque [motivo].`
- `🔎 Lido via OCR: o PDF era escaneado; páginas [n] com reconhecimento duvidoso, conferir no original.`
- `❌ Não lido: [motivo].` (formato sem leitor, arquivo corrompido, protegido por senha, nota de trabalho)

Quando a numeração não foi confirmada, acrescente:
`⚠ Paginação estimada: [arquivo] em [caminho]; estimativa [página do PDF X = p. Y]. Confira e corrija se preciso.`

Toda afirmação que dependa de um trecho não lido leva `[parte não lida]`.

## 3. Conceitos, dados e definições

Lista curta, para consulta rápida na hora de escrever. Cada item com página (ou artigo, ou capítulo):

- **Definições** usadas pela fonte, com as palavras dela quando forem curtas.
- **Números-chave**: valor, unidade, recorte e página. Mantenha a casa decimal do original.
- **Siglas e nomes** de sistemas, programas, órgãos e documentos citados.

Não repita aqui o relato inteiro: só o que se busca na hora de redigir.

## 4. Citações (tabela híbrida)

Tabela com quatro colunas e, abaixo, a forma pronta de cada citação:

```markdown
| Página | Citação literal | Tradução ou paráfrase | Onde usar |
| --- | --- | --- | --- |
| **p. 2** | "[trecho exato, no idioma original]" | [tradução fiel, se estrangeira; paráfrase, se em português] | **[Seção do trabalho]:** [para que serve] |

> **Prontas para o texto**
> - p. 2: Segundo os autores, [dado com número, unidade e recorte] (SOBRENOME et al., 2021, p. 2).
> - ...
```

Regras:

- De 5 a 10 citações em artigo, tese, norma longa e livro; de 2 a 5 em notícia, infográfico e página web.
- Citação literal sempre como está no documento; a tradução vai só na terceira coluna.
- **Uso estrito de aspas**: use aspas duplas exclusivamente na 2ª coluna da tabela de citações. Nunca use aspas duplas na 3ª ou 4ª coluna, nem em outras tabelas do fichamento (como tabelas de conceitos ou variáveis), para evitar que scripts automatizados (`find_quote_page.py`) as interpretem como citações literais a validar.
- Norma: a primeira coluna traz o dispositivo (`**art. 9º, I**`), não a página.
- Infográfico ou página web sem paginação: `**s.p.**`.
- Cada citação é conferida com `find_quote_page.py` antes de entregar (ver SKILL de conferir-citacoes).

## 5. Como citar no texto

Duas a três frases-modelo prontas, em ABNT:

- **Sempre**: uma frase neutra, que sirva a qualquer trabalho.
- **Se o tema da pesquisa foi informado**: mais uma ou duas frases voltadas ao tema, dizendo a seção onde entram.
- **Se o tema não foi informado**: termine com a linha `Informe o tema da sua pesquisa para receber frases voltadas a ela.` Não interrompa o trabalho para perguntar.

Use citação indireta (AUTOR, ano, p. X) e, quando couber, uma direta curta (até três linhas, entre aspas).

## 6. Parecer crítico (voz separada)

Sempre com o aviso: `> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.`

Tópicos mínimos: contribuição; fragilidades e vieses; limites da fonte (datas, recorte, quem produziu); lacunas; conexão com a pesquisa do usuário (ou "tema não informado").

## 7. Registro de mudanças (só quando completar um fichamento existente)

No fim do arquivo:

```markdown
### Registro de mudanças (completado a partir de `[caminho do fichamento original]`)

- Acrescentado: [seções ou itens].
- Corrigido: [o que estava errado] → [correção] ([como foi conferido]).
- Mantido sem alteração: [o restante].
```


## 8. Esquema rígido de cabeçalhos em execuções por IA (Anti / subagentes)

Em lotes, pipelines autônomos ou execuções por agentes de IA (como Anti e seus subagentes), os cabeçalhos das seções numeradas (definidos no `template.md` de cada skill: `### 1. Referência bibliográfica`, `### 2. Conteúdo e anatomia metodológica`, etc.) e o aviso inicial do parecer (`> **Voz do parecerista.** O que segue é análise crítica, não relato do documento.`) formam um esquema rígido obrigatório.

Nunca altere, resuma, omita a numeração ou invente títulos alternativos (como 'Resumo executivo' ou 'Síntese do artigo'). Isso garante a consistência sintática do lote e a interoperabilidade com scripts automatizados de conferência e compilação de índices.
