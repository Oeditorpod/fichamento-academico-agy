#!/usr/bin/env bash
# Instalador do Fichamento Acadêmico Rigoroso (Anti / AGY) para Linux e macOS
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Instalador do Fichamento Acadêmico Rigoroso (Anti / AGY) ==="

if [[ "${1:-}" == "--global" || "${1:-}" == "-g" ]]; then
    TARGET_DIR="$HOME/.gemini/config/plugins/fichamento-academico-agy"
    echo "[*] Instalando globalmente em: $TARGET_DIR"
    mkdir -p "$(dirname "$TARGET_DIR")"
    rm -rf "$TARGET_DIR"
    cp -R "$SCRIPT_DIR" "$TARGET_DIR"
    rm -rf "$TARGET_DIR/.git" "$TARGET_DIR/__pycache__"
    echo "[OK] Plugin instalado globalmente com sucesso!"
else
    WORKSPACE_ROOT="$(pwd)"
    PLUGIN_TARGET="$WORKSPACE_ROOT/.agents/plugins/fichamento-academico-agy"
    SKILLS_TARGET="$WORKSPACE_ROOT/.agents/skills"
    SHARED_TARGET="$WORKSPACE_ROOT/.agents/shared"

    echo "[*] Instalando no Workspace atual: $WORKSPACE_ROOT"
    mkdir -p "$(dirname "$PLUGIN_TARGET")" "$SKILLS_TARGET" "$SHARED_TARGET"
    rm -rf "$PLUGIN_TARGET"
    cp -R "$SCRIPT_DIR" "$PLUGIN_TARGET"
    rm -rf "$PLUGIN_TARGET/.git" "$PLUGIN_TARGET/__pycache__"

    cp -R "$SCRIPT_DIR/skills/"* "$SKILLS_TARGET/"
    cp -R "$SCRIPT_DIR/shared/"* "$SHARED_TARGET/"

    echo "[OK] Plugin e skills instalados no Workspace com sucesso!"
    echo "     - Plugin: .agents/plugins/fichamento-academico-agy"
    echo "     - Skills ativas: .agents/skills/"
    echo "     - Módulo compartilhado: .agents/shared/"
fi
