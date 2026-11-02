<#
.SYNOPSIS
    Instala o plugin fichamento-academico-agy para o assistente Anti (Google Antigravity).
.DESCRIPTION
    Permite instalação no Workspace atual (.agents/plugins e .agents/skills) ou Global (~/.gemini/config/plugins).
.PARAMETER Global
    Instala no diretório global de plugins do usuário (~/.gemini/config/plugins/fichamento-academico-agy).
.PARAMETER Workspace
    Instala no workspace atual (.agents/plugins/fichamento-academico-agy e .agents/skills). Padrão se nenhum parâmetro for informado.
#>
param(
    [switch]$Global,
    [switch]$Workspace
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Instalador do Fichamento Acadêmico Rigoroso (Anti / AGY) ===" -ForegroundColor Cyan

if ($Global) {
    $TargetDir = Join-Path $env:USERPROFILE ".gemini\config\plugins\fichamento-academico-agy"
    Write-Host "[*] Instalando globalmente em: $TargetDir" -ForegroundColor Yellow
    if (Test-Path $TargetDir) {
        Remove-Item $TargetDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path (Split-Path $TargetDir) -Force | Out-Null
    Copy-Item -Path $ScriptDir -Destination $TargetDir -Recurse -Force -Exclude ".git", "__pycache__"
    Write-Host "[OK] Plugin instalado globalmente com sucesso! Reinicie ou inicie uma sessão do Antigravity." -ForegroundColor Green
} else {
    $WorkspaceRoot = Get-Location
    $PluginTarget = Join-Path $WorkspaceRoot ".agents\plugins\fichamento-academico-agy"
    $SkillsTarget = Join-Path $WorkspaceRoot ".agents\skills"
    $SharedTarget = Join-Path $WorkspaceRoot ".agents\shared"

    Write-Host "[*] Instalando no Workspace atual: $WorkspaceRoot" -ForegroundColor Yellow

    # 1. Copiar plugin completo para .agents/plugins/
    New-Item -ItemType Directory -Path (Split-Path $PluginTarget) -Force | Out-Null
    if (Test-Path $PluginTarget) {
        Remove-Item $PluginTarget -Recurse -Force
    }
    Copy-Item -Path $ScriptDir -Destination $PluginTarget -Recurse -Force -Exclude ".git", "__pycache__"

    # 2. Copiar skills para descoberta direta em .agents/skills/
    New-Item -ItemType Directory -Path $SkillsTarget -Force | Out-Null
    Copy-Item -Path (Join-Path $ScriptDir "skills\*") -Destination $SkillsTarget -Recurse -Force

    # 3. Copiar shared para .agents/shared/ (garantindo caminhos relativos ../../shared)
    New-Item -ItemType Directory -Path $SharedTarget -Force | Out-Null
    Copy-Item -Path (Join-Path $ScriptDir "shared\*") -Destination $SharedTarget -Recurse -Force

    Write-Host "[OK] Plugin e skills instalados no Workspace com sucesso!" -ForegroundColor Green
    Write-Host "     - Plugin: .agents/plugins/fichamento-academico-agy"
    Write-Host "     - Skills ativas: .agents/skills/"
    Write-Host "     - Módulo compartilhado: .agents/shared/"
}
