# DECODE + VERIFY QUAD_FINISHABLE_WORK_v1.0 for Claude
# Expected SHA-256: 9ab21fc8d1e40985b850ec505e6111ff8c28b0b712b6c425b0b3753dec59f2f4
$ErrorActionPreference = 'Stop'
$expected = '9ab21fc8d1e40985b850ec505e6111ff8c28b0b712b6c425b0b3753dec59f2f4'
$destRoot = 'E:\o2a-dev\mct_pre_runner\incoming_grok'
New-Item -ItemType Directory -Force -Path $destRoot | Out-Null

$rawB64 = 'https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/quad/QUAD_FINISHABLE_WORK_v1.0/QUAD_FINISHABLE_WORK_v1.0.zip.b64'
$b64Path = Join-Path $destRoot 'QUAD_FINISHABLE_WORK_v1.0.zip.b64'
$zipPath = Join-Path $destRoot 'QUAD_FINISHABLE_WORK_v1.0.zip'
$expandPath = Join-Path $destRoot 'QUAD_FINISHABLE_WORK_v1.0'

Write-Host "Downloading b64..."
Invoke-WebRequest -Uri $rawB64 -OutFile $b64Path -UseBasicParsing
$bytes = [Convert]::FromBase64String((Get-Content -Raw $b64Path))
[IO.File]::WriteAllBytes($zipPath, $bytes)
$h = (Get-FileHash -Algorithm SHA256 $zipPath).Hash.ToLower()
if ($h -ne $expected) { throw "SHA mismatch got=$h expected=$expected" }
Write-Host "PASS SHA256=$h"
if (Test-Path $expandPath) { Remove-Item -Recurse -Force $expandPath }
Expand-Archive -Path $zipPath -DestinationPath $expandPath -Force
Write-Host "Expanded to $expandPath"
Get-ChildItem -Recurse $expandPath | Select-Object FullName, Length
