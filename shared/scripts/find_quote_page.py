"""Confere as citações de um fichamento contra o texto extraído do documento.

Uso:
    python find_quote_page.py fichamento.md texto_extraido.txt [--saida relatorio.md]
    python find_quote_page.py --trecho "texto da citação" texto_extraido.txt

O texto extraído é a saída do extract_pages.py ou do extract_other.py.
O script lê as citações entre aspas da tabela de citações do fichamento
(linhas que começam com "| **p.", "| **art.", "| **cap.", "| **s.p.**",
"| **seção" ou "| **considerando"), procura cada uma no texto, ignorando
quebras de linha, hifenização e espaços, e diz em que página (ou artigo)
ela está.

Resultado por citação:
- OK: achada no lugar indicado no fichamento.
- PÁGINA DIVERGE: achada, mas em outra página (mostra a certa).
- ARTIGO DIVERGE (normas): achada, mas dentro de outro artigo (mostra qual).
- NÃO ACHADA: não está no texto como foi transcrita (conferir no PDF;
  pode ser erro de transcrição ou de extração).
- PARCIAL: só o início da citação foi achado.

Capítulo, seção e s.p. não são conferidos: basta a citação ser achada.
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

GAP = "\u0000"
# Início de artigo: linha que começa com "Art. 12" ou "Artigo 12.º". Uma remissão
# no meio da frase ("conforme o art. 24") não conta.
# Norma que altera outra traz os artigos novos entre aspas: '"Art. 12.' ou '«Artigo 38.º'.
HEAD_ART = re.compile(r"^[ \t\"“«']*(?:Art\.?|Artigo)\s*(\d+)", re.M)
MARK = "⟦art{}⟧"
MARK_RE = re.compile("⟦art(\\d+)⟧")
ELLIPSIS = re.compile(r"\[\s*\.\.\.\s*\]|\[…\]|\.\.\.|…")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("­", "")
    s = re.sub(r"-\s*\n\s*", "", s)
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = s.replace("—", "-").replace("–", "-")
    s = re.sub("[​‌‍⁠﻿]", "", s)
    # Sem espaço nenhum: há PDFs que perdem os espaços ("buttheﬁrst(andinsome")
    # e outros que os inserem no meio da palavra.
    s = re.sub(r"\s+", "", s)
    return s.lower()


def build_index(text):
    """Texto normalizado + lista de (posição inicial, rótulo da página)."""
    parts, labels = [], []
    pos = 0
    chunks = re.split(r"^(===== .* =====)$", text, flags=re.M)
    label = "?"
    for c in chunks:
        if c.startswith("===== ") and c.endswith(" ====="):
            m = re.match(r"===== PÁGINA (\S+)", c)
            label = m.group(1) if m else c.strip("= ").split(" | ")[0]
            continue
        c = HEAD_ART.sub(lambda m: MARK.format(m.group(1)) + " " + m.group(0), c)
        n = norm(c)
        if not n:
            continue
        labels.append((pos, label))
        parts.append(n)
        pos += len(n)
    return "".join(parts), labels


def label_at(labels, idx):
    lab = "?"
    for p, l in labels:
        if p > idx:
            break
        lab = l
    return lab


def pieces_of(quote):
    q = norm(quote.strip('"“” '))
    q = ELLIPSIS.sub(GAP, q)
    return [p.strip() for p in q.split(GAP) if len(p.strip()) > 8]


def unmark(full):
    """Texto sem as marcas de artigo, com o mapa de posições para o texto marcado."""
    out, pos_map, i = [], [], 0
    for m in MARK_RE.finditer(full):
        seg = full[i:m.start()]
        out.append(seg)
        pos_map.extend(range(i, m.start()))
        i = m.end() + 1 if full[m.end():m.end() + 1] == " " else m.end()
    out.append(full[i:])
    pos_map.extend(range(i, len(full)))
    return "".join(out), pos_map


def find_all(quote, plain, pos_map, labels):
    """Todas as ocorrências: lista de (status, rótulo, posição no texto marcado)."""
    pieces = pieces_of(quote)
    if not pieces:
        return [("CURTA", None, -1)]
    hits = []
    i = plain.find(pieces[0])
    while i >= 0:
        ok = all(plain.find(p, i) >= 0 for p in pieces[1:])
        j = pos_map[i]
        hits.append(("ACHADA" if ok else "PARCIAL", label_at(labels, j), j))
        i = plain.find(pieces[0], i + 1)
    if hits:
        return hits
    # Trechos de 30 caracteres ao longo da citação: acha a que cruza uma quebra
    # de página com cabeçalho no meio, ou que tem ruído de OCR ou erro de transcrição
    # num ponto só.
    q = "".join(pieces)
    for k in range(0, max(1, len(q) - 29), 10):
        i = plain.find(q[k:k + 30])
        if i >= 0:
            j = pos_map[i]
            return [("PARCIAL", label_at(labels, j), j)]
    return [("NÃO ACHADA", None, -1)]


def article_at(full, idx):
    """Número do último início de artigo antes da posição."""
    last = None
    for m in MARK_RE.finditer(full, 0, idx + 1):
        last = m.group(1)
    return last


ROW = re.compile(r"^\|\s*([^|]*?)\s*\|\s*(.+?)\s*\|")
KIND = re.compile(r"^(p\.|art\.|cap\.|s\.p\.|se[çc][ãa]o|considerando)\s*(.*)$", re.I)


def quotes_from_fichamento(md):
    """Linhas de tabela cuja segunda coluna tem trecho entre aspas.

    O localizador da primeira coluna ("p. 4", "art. 9º", "cap. 2", "s.p.") diz o
    que conferir; qualquer outro ("—", vazio) é tratado como s.p.
    Tabelas não citacionais (conceitos, variáveis) são ignoradas.
    """
    rows = []
    for line in md.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        loc = m.group(1).strip("* ").strip()
        k = KIND.match(loc)
        # Se não for localizador e não for travessão/vazio, não é linha de citação
        if not k and loc not in ("—", "-", ""):
            continue
        cell = m.group(2).replace("“", '"').replace("”", '"')
        if not re.search(r'"[^"]{12,}"', cell):
            continue
        cited = (k.group(1).lower() + " " + k.group(2).strip()).strip() if k else "s.p."
        for q in re.findall(r'"([^"]{12,})"', cell) or [cell]:
            rows.append((cited, q))
    return rows


def same_page(cited, found):
    if found is None:
        return False
    nums = re.findall(r"\d+", cited)
    if not nums:
        return False
    try:
        f = int(re.findall(r"-?\d+", found)[0])
    except (IndexError, ValueError):
        return False
    lo, hi = int(nums[0]), int(nums[-1])
    return lo - 1 <= f <= hi  # citação que começa no fim da página anterior


def check(cited, quote, full, plain, pos_map, labels):
    hits = find_all(quote, plain, pos_map, labels)
    found = [h for h in hits if h[0] == "ACHADA"]
    if not found:
        status, page, _ = hits[0]
        return status, page
    if cited.startswith("art."):
        want = re.findall(r"\d+", cited)
        arts = [article_at(full, j) for _, _, j in found]
        if not any(arts):  # texto sem cabeçalhos de artigo reconhecíveis
            return "OK", found[0][1]
        if not want or want[0] in arts:
            return "OK", f"art. {want[0] if want else arts[0]}"
        return "ARTIGO DIVERGE", f"art. {next(a for a in arts if a)}"
    if cited.startswith("p.") and not re.search(r"\d", cited):
        # página em romano (prefácio, introdução): o texto extraído não a numera assim
        return "ACHADA, PÁGINA NÃO CONFERIDA", f"física {found[0][1]}"
    if cited.startswith("p."):
        for _, page, _ in found:
            if same_page(cited, page):
                return "OK", page
        return "PÁGINA DIVERGE", found[0][1]
    return "OK", found[0][1]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichamento", nargs="?")
    ap.add_argument("texto")
    ap.add_argument("--trecho")
    ap.add_argument("--saida")
    a = ap.parse_args()
    full, labels = build_index(Path(a.texto).read_text(encoding="utf-8"))
    plain, pos_map = unmark(full)

    if a.trecho:
        hits = find_all(a.trecho, plain, pos_map, labels)
        for status, page, j in hits:
            art = article_at(full, j) if j >= 0 else None
            where = f"página {page}" + (f", art. {art}" if art else "") if page else ""
            print(f"{status}: {where}" if where else status)
        return

    rows = quotes_from_fichamento(Path(a.fichamento).read_text(encoding="utf-8"))
    out = [f"# Conferência de citações: {Path(a.fichamento).name}", "",
           "| Citada como | Resultado | Encontrada em | Início da citação |", "| --- | --- | --- | --- |"]
    counts = {}
    for cited, q in rows:
        status, page = check(cited, q, full, plain, pos_map, labels)
        counts[status] = counts.get(status, 0) + 1
        out.append(f"| {cited} | {status} | {page or '-'} | {q[:60].replace('|', '/')}… |")
    out += ["", "Resumo: " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))]
    text = "\n".join(out)
    if a.saida:
        Path(a.saida).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
