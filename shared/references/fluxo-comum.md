# Fluxo comum das skills de fichamento

As skills fichar-norma, fichar-relatorio e fichar-livro seguem estes passos; cada uma acrescenta o que é próprio do tipo. `<plugin>` é a pasta dois níveis acima da pasta da skill. Rode os scripts com `python`, sem `-I`.

1. **Tema da pesquisa.** Use o que já se sabe (pedido, memória, skill fichamento). Se não houver, siga sem perguntar; o fichamento termina com o convite para informar o tema (secoes-comuns, seção 5).

2. **Fichamento existente.** Se a skill fichamento não verificou, procure um fichamento do mesmo documento na pasta de saída e vizinhas. Havendo, pergunte uma vez: completar (padrão), refazer em arquivo novo ou pular. Nunca sobrescreva.

3. **Extrair.**
   - PDF: `python "<plugin>/shared/scripts/extract_pages.py" "doc.pdf" --saida "doc.txt" --amostra "<pasta temporária>"`
   - Outros formatos: `python "<plugin>/shared/scripts/extract_other.py" "doc.ext" --saida "doc.txt"`
   - Imagem (infográfico em JPG/PNG): leia a imagem diretamente com Read; cite como s.p.
   Leia o resumo. `CONFERIR NUMERAÇÃO: sim` → abra a amostra e confira; sem confirmação, siga com a estimativa e registre o aviso. `NÃO LIDO` → registre o status com o motivo e pare neste arquivo.

4. **Ler** conforme `leitura-em-blocos.md` (integral, em blocos se longo; livro por capítulo).

5. **Escrever** pelo modelo da skill, com as seções comuns de `secoes-comuns.md`.

6. **Conferir citações:** `python "<plugin>/shared/scripts/find_quote_page.py" "fichamento.md" "doc.txt"`. Corrija `PÁGINA DIVERGE` e `NÃO ACHADA`; confira `PARCIAL` no original.

7. **Salvar** como `fichamento_<autor-ou-órgão>_<ano>.md` (letra se já existir: `_2025b`) e dizer o caminho e o status da leitura.

Regra geral: nada de página, artigo de lei, número, data ou autor que não tenha sido lido no documento.
