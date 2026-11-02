# Leitura em blocos e escopo de leitura

## O que ler

Leia exatamente o que o usuário pediu:

- "Ficha a pasta X": todos os arquivos da pasta, inclusive subpastas.
- "Ficha X.pdf e Y.docx": só esses.
- Arquivos encontrados que ficarem de fora (nota de trabalho, duplicata, formato sem leitor) aparecem na tabela inicial e no índice, com o motivo.

## Quanto ler de cada documento

A regra depende do tipo, não do tamanho:

| Tipo | Leitura |
| --- | --- |
| Artigo, tese, dissertação, norma, relatório, análise de dados | Sempre integral. Se for longo, em blocos (abaixo). |
| Livro | Por capítulo: leia inteiros os capítulos ligados ao tema; registre os não lidos e o motivo. Se o usuário pedir o livro todo, integral em blocos. |
| Tabelas e anexos de dados | Extraídos para planilha (pdfplumber + openpyxl) e lidos linha a linha, não por amostragem. |

## Leitura em blocos (documento longo)

Use quando o texto extraído não couber de uma vez com folga, em geral acima de cerca de 60 páginas.

1. **Avise antes** em documentos acima de cerca de 300 páginas: "[arquivo], [N] páginas, cerca de [K] blocos; vai levar mais tempo." Depois siga, sem cortar conteúdo.
2. **Divida** o texto extraído em blocos de cerca de 40 páginas, respeitando os cabeçalhos de página (nunca corte uma página ao meio).
3. **Leia cada bloco por inteiro** e grave uma ficha parcial num arquivo temporário (`_parcial_<arquivo>_bloco<n>.md`), com:
   - afirmações relevantes, cada uma com página;
   - citações candidatas, literais, com página;
   - números, definições e siglas, com página;
   - tabelas e figuras citadas no texto;
   - o que o bloco diz sobre limitações, métodos e conclusões.
4. **Consolide**: escreva o fichamento final a partir das fichas parciais, escolhendo as citações e os dados mais relevantes. Volte ao texto do bloco quando precisar conferir contexto.
5. **Registre** no status: `✅ Lido por inteiro (em [K] blocos).`
6. Apague as fichas parciais ao terminar, a menos que o usuário peça para guardar.

Nada no fichamento final pode vir de fora das fichas parciais ou do texto lido.
