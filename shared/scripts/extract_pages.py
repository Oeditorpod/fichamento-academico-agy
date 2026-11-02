"""Extrai o texto de um PDF página a página, com a página impressa de cada uma.

Uso:
    python extract_pages.py arquivo.pdf [--saida arquivo.txt] [--amostra PASTA]
                            [--duplas auto|sim|nao] [--colunas auto|sim|nao]

Cada página sai precedida de um cabeçalho:
    ===== PÁGINA 214 | FÍSICA 107 (esq.) | NUMERAÇÃO: lida =====

O que o script faz:
- Páginas duplas: quando a folha é mais larga que alta e há texto nas duas
  metades, corta ao meio e trata cada metade como uma página do livro.
- Duas colunas: quando os blocos de texto se dividem em coluna esquerda e
  direita, extrai a esquerda inteira e depois a direita.
- Numeração impressa: procura um número isolado no cabeçalho ou no rodapé de
  cada página. Se a sequência for consistente, usa a lida; se não houver
  número numa página, estima pela vizinhança e marca "estimada"; se nada
  for confiável, usa a ordem e marca "fisica".
- --amostra PASTA: salva imagens PNG de três páginas (início, meio e fim)
  para conferir a numeração a olho.
- Avisa quando o PDF parece escaneado (quase sem texto), caso em que é
  preciso OCR.

Com --saida, o texto vai para o arquivo e só o resumo (linhas com "#") sai
na tela. O resumo diz se é preciso conferir a numeração.
"""
import argparse
import re
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:  # versões antigas
    import fitz as pymupdf  # type: ignore

NUM_RE = re.compile(r"^(?:p\.?\s*|pág\.?\s*|página\s*|page\s*)?(\d{1,4})$", re.I)
LABEL_RE = re.compile(r"(?:página|pág\.|page)\s*(\d{1,4})\s*$", re.I)
RANGE_RE = re.compile(r"\bpp?\.\s*(\d{1,4})\s*[-\u2013]\s*(\d{1,4})\b")


def dehyphenate(text):
    # hífen suave (U+00AD) usado por editoras nas quebras de linha
    text = re.sub("­\\s*\\n\\s*", "", text)
    text = text.replace("­", "")
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)


def is_spread(page, mode):
    """Folha com duas páginas lado a lado."""
    if mode == "sim":
        return True
    if mode == "nao":
        return False
    r = page.rect
    if r.width < r.height * 1.15:
        return False
    mid = r.x0 + r.width / 2
    left = right = 0
    for b in page.get_text("blocks"):
        if b[6] != 0:
            continue
        n = len(b[4].strip())
        if b[2] <= mid + 5:
            left += n
        elif b[0] >= mid - 5:
            right += n
    return left > 200 and right > 200


def column_order(blocks, x0, x1):
    """Ordena blocos em uma ou duas colunas. Devolve (blocos, duas_colunas)."""
    mid = (x0 + x1) / 2
    tol = (x1 - x0) * 0.05
    left = [b for b in blocks if b[2] <= mid + tol]
    right = [b for b in blocks if b[0] >= mid - tol]
    spanning = [b for b in blocks if b not in left and b not in right]
    total = sum(len(b[4]) for b in blocks) or 1
    two = (len(left) >= 3 and len(right) >= 3
           and sum(len(b[4]) for b in left) > 0.2 * total
           and sum(len(b[4]) for b in right) > 0.2 * total
           and sum(len(b[4]) for b in spanning) < 0.3 * total)
    if not two:
        return sorted(blocks, key=lambda b: (round(b[1]), b[0])), False
    top = min(b[1] for b in left + right)
    head = sorted([b for b in spanning if b[1] < top], key=lambda b: b[1])
    rest = sorted([b for b in spanning if b[1] >= top], key=lambda b: b[1])
    return head + sorted(left, key=lambda b: b[1]) + sorted(right, key=lambda b: b[1]) + rest, True


def extract_region(page, clip, col_mode):
    blocks = [b for b in page.get_text("blocks", clip=clip) if b[6] == 0 and b[4].strip()]
    if col_mode == "nao" or not blocks:
        ordered, two = sorted(blocks, key=lambda b: (round(b[1]), b[0])), False
    else:
        ordered, two = column_order(blocks, clip.x0, clip.x1)
    return "\n".join(b[4].rstrip() for b in ordered), two


def printed_candidates(page, clip):
    """Números isolados nas faixas de cabeçalho e rodapé (10% de cada lado)."""
    h = clip.height
    bands = [pymupdf.Rect(clip.x0, clip.y0, clip.x1, clip.y0 + h * 0.10),
             pymupdf.Rect(clip.x0, clip.y1 - h * 0.10, clip.x1, clip.y1)]
    nums = []
    for band in bands:
        for b in page.get_text("blocks", clip=band):
            for ln in b[4].splitlines():
                s = re.sub(r"(?<=\d) (?=\d)", "", ln.strip())  # "1 6 5" -> "165"
                m = NUM_RE.match(s)
                if m:
                    nums.append(int(m.group(1)))
                    continue
                # "..., ago. 2023, Página 131": rótulo explícito, vale em linha longa
                m = LABEL_RE.search(s)
                if m:
                    nums.append(int(m.group(1)))
                    continue
                # número no início ou no fim de um cabeçalho ("246  17 JULY 2020",
                # "17 JULY 2020 VOL 369  247"); os dois entram, os vizinhos decidem
                if len(s) < 120:
                    for m in (re.match(r"^(\d{1,4})\s+\S", s), re.search(r"\S\s+(\d{1,4})$", s)):
                        if m:
                            nums.append(int(m.group(1)))
    return nums


def range_numbers(doc, units):
    """Plano B: o intervalo "p. 47-54" repetido no rodapé ou cabeçalho.

    Se o número de páginas que trazem o intervalo bate com o tamanho dele, a
    primeira delas é a página inicial. O resultado é estimado, nunca "lida".
    """
    found = []
    for i, side, clip in units:
        page = doc[i - 1]
        h = clip.height
        hit = None
        for band in (pymupdf.Rect(clip.x0, clip.y0, clip.x1, clip.y0 + h * 0.10),
                     pymupdf.Rect(clip.x0, clip.y1 - h * 0.10, clip.x1, clip.y1)):
            m = RANGE_RE.search(page.get_text("text", clip=band))
            if m:
                hit = (int(m.group(1)), int(m.group(2)))
        found.append(hit)
    hits = [f for f in found if f]
    if not hits:
        return None
    a, b = max(set(hits), key=hits.count)
    idx = [k for k, f in enumerate(found) if f == (a, b)]
    if b <= a or abs(len(idx) - (b - a + 1)) > 1:
        return None
    first = idx[0]
    nums = []
    for k in range(len(units)):
        nums.append((a + k - first, "estimada") if a + k - first >= 1 else (k + 1, "fisica"))
    return nums, (a, b)


def assign_numbers(cands):
    """Numera cada página aceitando várias sequências (ex.: anexos renumerados).

    Um número lido só vale se a página vizinha confirma a mesma sequência.
    Páginas sem número confirmado herdam a sequência mais próxima ("estimada").
    Devolve (lista de (número, status), quantidade de sequências).
    """
    n = len(cands)
    offs = [{c - i for c in cs} for i, cs in enumerate(cands)]
    chosen = [None] * n
    for i in range(n):
        near = set()
        for j in (i - 2, i - 1, i + 1, i + 2):
            if 0 <= j < n:
                near |= offs[j]
        ok = offs[i] & near
        if ok:
            prev = chosen[i - 1] if i else None
            chosen[i] = prev if prev in ok else min(ok, key=lambda o: abs(o))
    # sequência curta (menos de 3 páginas seguidas) é tratada como ruído de leitura
    i = 0
    while i < n:
        if chosen[i] is None:
            i += 1
            continue
        j = i
        while j < n and (chosen[j] == chosen[i] or chosen[j] is None):
            j += 1
        # (em documento de 1 ou 2 páginas, basta que todas confirmem)
        if sum(1 for k in range(i, j) if chosen[k] == chosen[i]) < min(3, n):
            for k in range(i, j):
                chosen[k] = None
        i = j
    # sequência que volta atrás e é curta (menos de 8 páginas) também é ruído;
    # anexos renumerados de verdade costumam ser longos
    present = [o for o in chosen if o is not None]
    if present:
        main_off = max(set(present), key=present.count)
        i = 0
        while i < n:
            if chosen[i] is None or chosen[i] == main_off:
                i += 1
                continue
            j = i
            while j < n and chosen[j] == chosen[i]:
                j += 1
            if j - i < 8 and chosen[i] < main_off:
                for k in range(i, j):
                    chosen[k] = None
            i = j
    if not any(o is not None for o in chosen):
        return [(i + 1, "fisica") for i in range(n)], 0
    status = ["lida" if o is not None else "estimada" for o in chosen]
    last = next(o for o in chosen if o is not None)
    filled = []
    for o in chosen:
        last = o if o is not None else last
        filled.append(last)
    nums = [i + filled[i] for i in range(n)]
    # página estimada nunca volta atrás em relação à anterior
    for i in range(1, n):
        if status[i] == "estimada" and nums[i] <= nums[i - 1]:
            nums[i] = nums[i - 1] + 1
    seqs = 1 + sum(1 for i in range(1, n) if nums[i] != nums[i - 1] + 1)
    return [(nums[i], status[i]) for i in range(n)], seqs


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--saida")
    ap.add_argument("--amostra")
    ap.add_argument("--duplas", default="auto", choices=["auto", "sim", "nao"])
    ap.add_argument("--colunas", default="auto", choices=["auto", "sim", "nao"])
    a = ap.parse_args()

    path = Path(a.pdf)
    doc = pymupdf.open(path)

    units = []  # (indice_fisico, lado, clip)
    spreads = 0
    # se a maioria das folhas largas é dupla, corta todas as largas (capas e
    # páginas de figura também ocupam meia folha), para não desalinhar a contagem
    wide = [p for p in doc if p.rect.width >= p.rect.height * 1.15]
    # só no automático: precisa de pelo menos 4 folhas e de maioria de folhas largas
    # com texto nas duas metades (infográficos e tabelas deitadas não são cortados)
    mode = a.duplas
    if mode == "auto":
        if (len(doc) >= 4 and len(wide) > len(doc) * 0.5
                and sum(is_spread(p, "auto") for p in wide) > len(wide) * 0.5):
            mode = "largas"
        else:
            mode = "nao"
    for i, page in enumerate(doc, start=1):
        r = page.rect
        if (mode == "largas" and r.width >= r.height * 1.15) or (mode != "largas" and is_spread(page, mode)):
            spreads += 1
            mid = r.x0 + r.width / 2
            units.append((i, "esq.", pymupdf.Rect(r.x0, r.y0, mid, r.y1)))
            units.append((i, "dir.", pymupdf.Rect(mid, r.y0, r.x1, r.y1)))
        else:
            units.append((i, "", r))

    texts, cands, twocol = [], [], 0
    for i, side, clip in units:
        page = doc[i - 1]
        t, two = extract_region(page, clip, a.colunas)
        twocol += two
        texts.append(dehyphenate(t))
        cands.append(printed_candidates(page, clip))

    numbers, seqs = assign_numbers(cands)
    from_range = None
    if seqs == 0:
        r = range_numbers(doc, units)
        if r:
            numbers, from_range = r
            seqs = 1
    read = sum(1 for _, s in numbers if s == "lida")
    est = sum(1 for _, s in numbers if s == "estimada")
    empty = sum(1 for t in texts if len(t.strip()) < 30)

    out = []
    meta = doc.metadata or {}
    out.append(f"# ARQUIVO: {path.name}")
    out.append(f"# CAMINHO: {path.resolve().parent}")
    out.append(f"# FOLHAS NO PDF: {len(doc)} | PÁGINAS EXTRAÍDAS: {len(units)}")
    out.append(f"# TÍTULO (metadado): {meta.get('title') or '?'}")
    out.append(f"# AUTOR (metadado): {meta.get('author') or '?'}")
    if spreads:
        out.append(f"# PÁGINAS DUPLAS: {spreads} folhas cortadas ao meio (cada metade = uma página)")
    if twocol:
        out.append(f"# DUAS COLUNAS: {twocol} páginas extraídas coluna por coluna")
    if seqs == 0:
        out.append("# NUMERAÇÃO: não detectada; páginas numeradas pela ordem (fisica)")
        conferir = True
    else:
        if from_range:
            out.append(f"# NUMERAÇÃO: estimada pelo intervalo p. {from_range[0]}-{from_range[1]} do rodapé ou cabeçalho"
                       " (a primeira página com o intervalo é a inicial)")
        else:
            out.append(f"# NUMERAÇÃO: {read} páginas com número lido, {est} estimadas")
        if seqs > 1:
            out.append(f"# SEQUÊNCIAS DE NUMERAÇÃO: {seqs} (ex.: anexos renumerados ou falhas de leitura)")
        conferir = read < len(units) * 0.5 or seqs > 3
    out.append("# CONFERIR NUMERAÇÃO: " + ("sim (gere imagens com --amostra e confira)" if conferir else "não necessário"))
    if empty > len(units) * 0.5:
        out.append(f"# AVISO: {empty} de {len(units)} páginas sem texto. PDF provavelmente escaneado; precisa de OCR.")
    elif empty:
        out.append(f"# PÁGINAS SEM TEXTO: {empty} (capas, figuras ou páginas escaneadas; conferir)")
    out.append("")

    for (i, side, _), t, (n, status) in zip(units, texts, numbers):
        lado = f" ({side})" if side else ""
        out.append(f"===== PÁGINA {n} | FÍSICA {i}{lado} | NUMERAÇÃO: {status} =====")
        out.append(t.rstrip())
        out.append("")

    result = "\n".join(out)
    if a.saida:
        Path(a.saida).write_text(result, encoding="utf-8")
        print("\n".join(l for l in out if l.startswith("#")))
    else:
        print(result)

    if a.amostra:
        dest = Path(a.amostra)
        dest.mkdir(parents=True, exist_ok=True)
        for k in sorted({min(4, len(units) - 1), len(units) // 2, len(units) - 1}):
            i, side, clip = units[k]
            half = pymupdf.Rect(clip.x0, clip.y0, clip.x1, clip.y0 + clip.height * 0.5)
            name = dest / f"{path.stem}_p{numbers[k][0]}_fis{i}{side.rstrip('.')}.png"
            doc[i - 1].get_pixmap(dpi=60, clip=half).save(name)
            print(f"# AMOSTRA: {name} (página {numbers[k][0]}, {numbers[k][1]})")


if __name__ == "__main__":
    main()
