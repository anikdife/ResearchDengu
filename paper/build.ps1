param([ValidateSet('draft','check','manuscript','supplementary')][string]$Mode='draft')
$py = 'python'
& $py (Join-Path $PSScriptRoot 'build_sources.py')
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'scripts\refresh_figures.ps1')
if ($Mode -eq 'check') {
  & $py (Join-Path $PSScriptRoot 'scripts\check_placeholders.py')
  & $py (Join-Path $PSScriptRoot 'scripts\check_manuscript_structure.py')
  & $py (Join-Path $PSScriptRoot 'scripts\check_professor_facing.py')
  exit $LASTEXITCODE
}
if (-not (Get-Command latexmk -ErrorAction SilentlyContinue)) {
  Write-Error 'latexmk is not available. Install a LaTeX distribution locally, then rerun this script.'
  exit 2
}
if ($Mode -eq 'manuscript') {
  & $py (Join-Path $PSScriptRoot 'scripts\check_placeholders.py') --strict
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
Push-Location $PSScriptRoot
$target = if ($Mode -eq 'supplementary') { 'supplementary.tex' } else { 'manuscript.tex' }
$outdir = if ($Mode -eq 'supplementary') { 'build\supplementary' } else { 'build\draft' }
New-Item -ItemType Directory -Force $outdir | Out-Null
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=$outdir $target
$code = $LASTEXITCODE
if ($code -eq 0 -and $Mode -eq 'draft') {
  Copy-Item -LiteralPath (Join-Path $outdir 'manuscript.pdf') -Destination (Join-Path (Join-Path $PSScriptRoot 'build') 'ResearchDengu_Manuscript_Professor_Draft.pdf') -Force
}
if ($code -eq 0 -and $Mode -eq 'supplementary') {
  Copy-Item -LiteralPath (Join-Path $outdir 'supplementary.pdf') -Destination (Join-Path (Join-Path $PSScriptRoot 'build') 'ResearchDengu_Supplementary_Material.pdf') -Force
}
Pop-Location
exit $code
