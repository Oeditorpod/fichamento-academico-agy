"""Verifica o que está instalado para ler cada tipo de arquivo. Não instala nada.

Uso:
    python verificar_requisitos.py

Rode SEM o modo isolado do Python (não use "python -I"): esse modo esconde
os pacotes instalados na pasta do usuário e faria o script dizer que falta
algo que já está instalado.
"""
import importlib
import shutil
import sys

ITENS = [
    # (módulo, pacote pip, para quê, obrigatório)
    ("pymupdf", "pymupdf", "PDF: texto, páginas duplas, imagens de conferência", True),
    ("pdfplumber", "pdfplumber", "PDF: tabelas", False),
    ("docx", "python-docx", "DOCX", False),
    ("ebooklib", "ebooklib", "EPUB", False),
    ("bs4", "beautifulsoup4", "EPUB e HTML", False),
    ("openpyxl", "openpyxl", "tabelas exportadas para planilha", False),
    ("ocrmypdf", "ocrmypdf", "OCR de PDF escaneado (também precisa de Tesseract e Ghostscript)", False),
]


def tem_modulo(nome):
    try:
        importlib.import_module("fitz" if nome == "pymupdf" and False else nome)
        return True
    except Exception:
        if nome == "pymupdf":
            try:
                importlib.import_module("fitz")
                return True
            except Exception:
                return False
        return False


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    if sys.flags.isolated:
        print("AVISO: rodando com 'python -I'; pacotes da pasta do usuário ficam invisíveis. Rode sem -I.\n")
    print(f"Python {sys.version.split()[0]}\n")
    faltam_pip = []
    for mod, pip, uso, obrig in ITENS:
        ok = tem_modulo(mod)
        print(f"[{'ok' if ok else 'FALTA'}] {pip:<15} {uso}{' (obrigatório)' if obrig else ''}")
        if not ok:
            faltam_pip.append(pip)
    tess = shutil.which("tesseract")
    gs = shutil.which("gswin64c") or shutil.which("gswin32c") or shutil.which("gs")
    print(f"[{'ok' if tess else 'FALTA'}] {'tesseract':<15} programa de OCR (com o pacote de idioma português)")
    print(f"[{'ok' if gs else 'FALTA'}] {'ghostscript':<15} usado pelo ocrmypdf")

    print()
    if faltam_pip:
        print("Para instalar os pacotes Python que faltam:")
        print(f"  {sys.executable} -m pip install {' '.join(faltam_pip)}")
    if not tess or not gs:
        print("OCR (opcional, só para PDF escaneado):")
        if not tess:
            print("  Tesseract: Windows -> instalador da UB Mannheim (marque 'Portuguese');"
                  " macOS -> brew install tesseract tesseract-lang; Linux -> apt install tesseract-ocr tesseract-ocr-por")
        if not gs:
            print("  Ghostscript: Windows -> ghostscript.com; macOS -> brew install ghostscript; Linux -> apt install ghostscript")
    if not faltam_pip and tess and gs:
        print("Tudo instalado.")
    print("\nSem um item, a skill continua e marca os arquivos afetados como parcial ou não lido, com o motivo.")


if __name__ == "__main__":
    main()
