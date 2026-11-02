# Changelog

## [2.1.0] - 2026-11-02
### Edição Oficial e Exclusiva: Anti (Google Antigravity)
- **Repositório oficial dedicado:** `Oeditorpod/fichamento-academico-agy`, construído e otimizado com exclusividade para o assistente autônomo Anti (Google Antigravity).
- **Manifesto raiz Antigravity:** Plugin configurado nativamente via `plugin.json` na raiz com metadados oficiais (`displayName`, `author`, `repository`, `suggestedPrompts`).
- **Scripts automatizados de instalação e atualização:** Adicionados `instalar.ps1` (PowerShell/Windows) e `instalar.sh` (Bash/Linux/macOS) com modos de instalação no Workspace (`.agents/plugins` + `.agents/skills`) ou Global (`~/.gemini/config/plugins`).
- **Blindagem de tabelas em `find_quote_page.py`:** Filtragem estrita de linhas de tabela para validar unicamente linhas que iniciem com localizadores reconhecidos (`p.`, `art.`, `cap.`, `s.p.`, `seção`, `considerando`) ou travessão (`—`), prevenindo falsos alertas causados por aspas em tabelas de conceitos ou variáveis.
- **Suporte a aspas tipográficas:** Normalização de aspas duplas tipográficas (`“...”`) e retas (`"..."`) na extração de citações.
- **Tratamento de formatos legados em `extract_other.py`:** Adicionada mensagem de diagnóstico clara ao detectar arquivos binários antigos do Word 97-2003 (`.doc`), orientando a conversão para `.docx` ou `.pdf`.
- **Esquema rígido de cabeçalhos em `secoes-comuns.md` e `SKILL.md`:** Instrução expressa para o Anti e seus subagentes preservarem rigorosamente a numeração de seções (`### 1.` a `### 6.`) e o cabeçalho canônico da voz do parecerista, garantindo conformidade estrutural em execuções massivas em lote.
- **Homologação em lote:** Validado em teste de estresse real com 77 artigos e teses científicas (~2.350 páginas), com 100% de citações literais conferidas e aprovadas.

## [2.0.1] - 2026-10-31
- Ajuste de referências e exemplos neutros.

## [2.0.0] - 2026-10-30
- Arquitetura de plugin com seis skills integradas (`fichamento`, `fichar-artigo`, `fichar-norma`, `fichar-relatorio`, `fichar-livro`, `conferir-citacoes`).
