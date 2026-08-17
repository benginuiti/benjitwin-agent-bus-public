# RUN_GREENLY_UNREAL_JOIN.ps1
# BEN P0 2026-08-17 — Local Claude on BENX570E
# Measure UE, stand localhost-only verb host, hello, write receipt.
# NEVER bind Unreal or the verb host to 0.0.0.0 / WAN.
# NEVER UAC Tailscale / netplwiz / PLACE production.

$ErrorActionPreference = 'Continue'
$ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$receiptDir = 'E:\o2a\receipts\greenly'
$hostDir = 'E:\o2a-dev\GREENLY\host'
New-Item -ItemType Directory -Force -Path $receiptDir | Out-Null
New-Item -ItemType Directory -Force -Path $hostDir | Out-Null

$result = [ordered]@{
  order_id           = 'CLAUDE-ORD-GREENLY-UNREAL-RELAY-JOIN-2026-08-17'
  work_id            = 'wrk_e05ca129c096'
  timestamp          = $ts
  ue_found           = $false
  ue_path            = $null
  ue_process         = $false
  ue_pid             = $null
  remote_control     = 'DOWN'
  remote_control_url = 'http://127.0.0.1:30010'
  verb_host          = 'DOWN'
  verb_host_url      = 'http://127.0.0.1:49410/health'
  hello              = 'FAIL'
  hello_body         = $null
  tailscale_100      = $null
  receipt_path       = $null
  blocker            = $null
}

$candidates = New-Object System.Collections.Generic.List[string]
foreach ($hint in @(
    'E:\Epic\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe',
    'E:\Epic\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe',
    'E:\Epic\UE_5.6\Engine\Binaries\Win64\UnrealEditor.exe'
  )) {
  $candidates.Add($hint)
}
if (Test-Path 'E:\Epic') {
  Get-ChildItem 'E:\Epic' -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $p = Join-Path $_.FullName 'Engine\Binaries\Win64\UnrealEditor.exe'
    if (Test-Path $p) { $candidates.Add($p) }
  }
}
$ue = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($ue) {
  $result.ue_found = $true
  $result.ue_path = $ue
}

$proc = Get-Process -Name 'UnrealEditor' -ErrorAction SilentlyContinue
if ($proc) {
  $result.ue_process = $true
  $result.ue_pid = @($proc)[0].Id
}

function Test-LocalHttp([string]$Url) {
  try {
    $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3
    return $r
  } catch {
    return $null
  }
}

$rc = Test-LocalHttp 'http://127.0.0.1:30010/remote/info'
if (-not $rc) { $rc = Test-LocalHttp 'http://127.0.0.1:30010/' }
if ($rc) {
  $result.remote_control = 'UP'
} elseif ($result.ue_process) {
  $result.remote_control = 'MISSING_PLUGIN'
} else {
  $result.remote_control = 'DOWN'
}

try {
  $ip = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -like '100.*' } |
    Select-Object -First 1
  if ($ip) { $result.tailscale_100 = $ip.IPAddress }
} catch {}

$pyUrl = 'https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/greenly/host/greenly_verb_host.py'
$pyPath = Join-Path $hostDir 'greenly_verb_host.py'
try {
  Invoke-WebRequest -Uri $pyUrl -OutFile $pyPath -UseBasicParsing -TimeoutSec 20
} catch {
  if (-not (Test-Path $pyPath)) {
    $result.blocker = 'VERB_HOST_DOWNLOAD_FAILED'
  }
}

$listening = Get-NetTCPConnection -LocalPort 49410 -State Listen -ErrorAction SilentlyContinue
if (-not $listening -and (Test-Path $pyPath)) {
  $pyCandidates = @(
    'E:\LIVEBENCH\.venv312\Scripts\python.exe',
    'E:\LIVEBENCH\python312\python\python.exe'
  )
  $python = $pyCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
  if (-not $python) {
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd) { $python = $cmd.Source }
  }
  if ($python) {
    Start-Process -FilePath $python -ArgumentList "`"$pyPath`"" -WindowStyle Hidden | Out-Null
    Start-Sleep -Seconds 2
  } else {
    if (-not $result.blocker) { $result.blocker = 'PYTHON_NOT_FOUND' }
  }
}

$health = Test-LocalHttp 'http://127.0.0.1:49410/health'
if ($health) { $result.verb_host = 'UP' } else { $result.verb_host = 'DOWN' }

try {
  $hello = Invoke-RestMethod -Method POST -Uri 'http://127.0.0.1:49410/verb/hello' -TimeoutSec 8
  $result.hello_body = ($hello | ConvertTo-Json -Compress)
  if ($hello.ok -eq $true) { $result.hello = 'PASS' }
} catch {}

if (-not $result.blocker) {
  $bits = @()
  if (-not $result.ue_found) { $bits += 'UE_NOT_FOUND' }
  if (-not $result.ue_process) { $bits += 'UE_NOT_RUNNING' }
  if ($result.remote_control -ne 'UP') { $bits += ('REMOTE_CONTROL_' + $result.remote_control) }
  if ($result.verb_host -ne 'UP') { $bits += 'VERB_HOST_DOWN' }
  if ($result.hello -ne 'PASS') { $bits += 'HELLO_FAIL' }
  if ($bits.Count -gt 0) { $result.blocker = ($bits -join ',') }
}

$yaml = @"
order_id: $($result.order_id)
work_id: $($result.work_id)
timestamp: $($result.timestamp)
ue_found: $($result.ue_found.ToString().ToLower())
ue_path: $($result.ue_path)
ue_process: $($result.ue_process.ToString().ToLower())
ue_pid: $($result.ue_pid)
remote_control: $($result.remote_control)
verb_host: $($result.verb_host)
hello: $($result.hello)
hello_body: $($result.hello_body)
tailscale_100: $($result.tailscale_100)
blocker: $($result.blocker)
"@

$out = Join-Path $receiptDir "UNREAL_JOIN_$stamp.yaml"
Set-Content -Path $out -Value $yaml -Encoding UTF8
Copy-Item $out (Join-Path $receiptDir 'UNREAL_JOIN_LATEST.yaml') -Force
$result.receipt_path = $out

Write-Output $yaml
Write-Output "RECEIPT=$out"
