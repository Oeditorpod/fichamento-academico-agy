"""Extrai texto de DOCX, EPUB, HTML, TXT/MD e PDFs escaneados (via OCR).

Uso:
    python extract_other.py arquivo [--saida arquivo.txt]

Saída no mesmo estilo do extract_pages.py: resumo com "#" no topo e o texto
dividido em seções marcadas por cabeçalhos "===== ... =====".

- DOCX: não tem páginas; o texto é dividido pelos títulos do documento
  ("SEÇÃO"). Cite por seção, ou como "s.p.".
- EPUB: dividido por capítulo ("CAPÍTULO n"), na ordem do livro. Livros
  digitais não têm página fixa; cite por capítulo.
- HTML: texto visível da página web, sem menus e scripts. Cite como "s.p.".
- TXT/MD: lido como está.
- PDF escaneado: roda o ocrmypdf (precisa de Tesseract com português) e
  depois extrai como PDF normal. Se o OCR não estiver instalado, avisa.
- Imagens (JPG, PNG): não extraídas aqui; o Anti lê a imagem diretamente.

Formatos sem leitor (PPTX, XLSX, ODT etc.) recebem aviso de "não lido".
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def out_header(path, kind, extra=()):
    lines = [f"# ARQUIVO: {path.name}", f"# CAMINHO: {path.resolve().parent}", f"# TIPO: {kind}"]
    lines += [f"# {e}" for e in extra]
    return lines + [""]


def read_docx(path):
    import docx  # python-docx
    d = docx.Document(str(path))
    secs, cur, title = [], [], "INÍCIO"
    for p in d.paragraphs:
        style = (p.style.name or "").lower() if p.style is not None else ""
        if style.startswith(("heading", "título", "titulo")) and p.text.strip():
            if cur:
                secs.append((title, cur))
            title, cur = p.text.strip(), []
        elif p.text.strip():
            cur.append(p.text)
    if cur:
        secs.append((title, cur))
    for t in d.tables:
        rows = [" | ".join(c.text.strip() for c in r.cells) for r in t.rows]
        secs.append(("TABELA", rows))
    lines = out_header(path, "DOCX (sem paginação; citar por seção ou s.p.)",
                       [f"SEÇÕES: {len(secs)}"])
    for t, body in secs:
        lines += [f"===== SEÇÃO: {t} =====", *body, ""]
    return lines


def read_epub(path):
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    book = epub.read_epub(str(path))
    chapters = []
    for idref, _ in book.spine:
        item = book.get_item_with_id(idref)
        if item is None or item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue
        soup = BeautifulSoup(item.get_content(), "html.parser")
        text = soup.get_text("\n").strip()
        if len(text) > 50:
            h = soup.find(["h1", "h2", "h3"])
            chapters.append((h.get_text(" ").strip() if h else idref, text))
    lines = out_header(path, "EPUB (sem página fixa; citar por capítulo)",
                       [f"CAPÍTULOS: {len(chapters)}"])
    for i, (t, body) in enumerate(chapters, start=1):
        lines += [f"===== CAPÍTULO {i}: {t} =====", body, ""]
    return lines


def read_html(path):
    from bs4 import BeautifulSoup
    raw = path.read_bytes()
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "noscript", "form"]):
        tag.decompose()
    title = soup.title.get_text(" ").strip() if soup.title else "?"
    text = "\n".join(l.strip() for l in soup.get_text("\n").splitlines() if l.strip())
    return out_header(path, "HTML (página web; citar como s.p.)", [f"TÍTULO: {title}"]) + \
        ["===== TEXTO DA PÁGINA =====", text, ""]


def read_text(path):
    return out_header(path, "TEXTO (sem paginação)") + \
        ["===== TEXTO =====", path.read_text(encoding="utf-8", errors="replace"), ""]


def read_scanned_pdf(path):
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf  # type: ignore
    with pymupdf.open(path) as d:
        chars = sum(len(p.get_text("text").strip()) for p in d)
        npages = len(d)
    if chars > 100 * npages * 0.3:
        r = subprocess.run([sys.executable, str(HERE / "extract_pages.py"), str(path)],
                           capture_output=True, text=True, encoding="utf-8")
        return r.stdout.splitlines()
    if not shutil.which("ocrmypdf") and not _module("ocrmypdf"):
        return out_header(path, "PDF ESCANEADO", [
            "NÃO LIDO: o PDF não tem texto e o OCR não está instalado.",
            "Instale Tesseract (com português), Ghostscript e ocrmypdf; veja verificar_requisitos.py."])
    with tempfile.TemporaryDirectory() as tmp:
        ocr_pdf = Path(tmp) / "ocr.pdf"
        cmd = [sys.executable, "-m", "ocrmypdf", "-l", "por+eng", "--skip-text", str(path), str(ocr_pdf)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not ocr_pdf.exists():
            return out_header(path, "PDF ESCANEADO", [
                "NÃO LIDO: o OCR falhou.", f"Erro: {r.stderr.strip()[-300:]}"])
        r = subprocess.run([sys.executable, str(HERE / "extract_pages.py"), str(ocr_pdf)],
                           capture_output=True, text=True, encoding="utf-8")
        lines = r.stdout.splitlines()
        lines.insert(0, "# LIDO VIA OCR: o texto veio de reconhecimento óptico; conferir trechos citados no PDF original.")
        lines.insert(1, f"# ARQUIVO ORIGINAL: {path.name} | CAMINHO: {path.resolve().parent}")
        return lines


def _module(name):
    try:
        __import__(name)
        return True
    except Exception:
        return False


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivo")
    ap.add_argument("--saida")
    a = ap.parse_args()
    path = Path(a.arquivo)
    ext = path.suffix.lower()
    try:
        if ext == ".docx":
            lines = read_docx(path)
        elif ext == ".doc":
            lines = out_header(path, "DOC (binário legado)", [
                "NÃO LIDO: arquivo no formato binário legado do Word 97-2003 (.doc).",
                "Converta o arquivo para .docx ou .pdf para permitir a extração automática."
            ])
        elif ext == ".epub":
            lines = read_epub(path)
        elif ext in (".html", ".htm"):
            lines = read_html(path)
        elif ext in (".txt", ".md"):
            lines = read_text(path)
        elif ext == ".pdf":
            lines = read_scanned_pdf(path)
        elif ext in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            lines = out_header(path, "IMAGEM", ["Ler a imagem diretamente (não há texto a extrair). Citar como s.p."])
        else:
            lines = out_header(path, f"FORMATO {ext or '?'}", ["NÃO LIDO: formato sem leitor neste plugin."])
    except ImportError as e:
        lines = out_header(path, ext, [f"NÃO LIDO: falta a biblioteca {e.name}. Rode verificar_requisitos.py."])
    except Exception as e:  # arquivo corrompido, protegido etc.
        lines = out_header(path, ext, [f"NÃO LIDO: erro ao abrir ({type(e).__name__}: {e})."])
    text = "\n".join(lines)
    if a.saida:
        Path(a.saida).write_text(text, encoding="utf-8")
        head = []
        for l in lines:
            if l.startswith("====="):
                break
            if l.startswith("#"):
                head.append(l)
        print("\n".join(head))
    else:
        print(text)


if __name__ == "__main__":
    main()
