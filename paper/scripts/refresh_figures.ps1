$ErrorActionPreference = 'Continue'
$paper = Split-Path -Parent $PSScriptRoot
$chrome = (Get-Command chrome.exe -ErrorAction SilentlyContinue).Source
if (-not $chrome) { $chrome = Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe' }
if (-not (Test-Path $chrome)) { throw "Chrome is required for deterministic SVG-to-PDF conversion: $chrome" }
$pairs = @(
  @('figure1.html','figure1_acquisition_workflow'),
  @('figure2.html','figure2_snapshot_structure'),
  @('figure3.html','figure3_quality_findings'),
  @('figure4.html','figure4_restricted_headline_observations')
)
foreach ($pair in $pairs) {
  $html = Join-Path $paper $pair[0]
  $output = Join-Path $paper "figures\$($pair[1]).pdf"
  if (-not (Test-Path $html)) { throw "Missing conversion wrapper: $html" }
  & $chrome --headless=new --disable-gpu --no-sandbox --disable-cache --no-pdf-header-footer --print-to-pdf="$output" "file:///$($html.Replace('\','/'))?refresh=1" 2>$null | Out-Null
  if (-not (Test-Path $output)) { throw "Figure conversion failed: $output" }
  Write-Output "WROTE: $output"
}
