#Requires -Version 5.1
# poll_agent_bus.ps1 — fetch public NEXT.md, detect changes, write local bus files.
# No secrets. No remote code execution. Order body is saved for Claude/operator to run.
# Default: one poll. -Loop polls until stopped.

param(
    [string]$BusUrl = "https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/orders/NEXT.md",
    [string]$LocalRoot = "E:\o2a-dev\benjitwin_media",
    [int]$IntervalSec = 120,
    [switch]$Loop
)

$ErrorActionPreference = "Stop"
$ordersDir = Join-Path $LocalRoot "orders"
$stateDir = Join-Path $LocalRoot "bus_state"
$nextLocal = Join-Path $ordersDir "NEXT.md"
$hashFile = Join-Path $stateDir "next.sha256"
$logFile = Join-Path $stateDir "poll_log.txt"
$flagNew = Join-Path $stateDir "NEW_ORDER.flag"

New-Item -ItemType Directory -Force -Path $ordersDir | Out-Null
New-Item -ItemType Directory -Force -Path $stateDir | Out-Null

function Write-Log([string]$msg) {
    $line = "{0:o}  {1}" -f (Get-Date).ToUniversalTime(), $msg
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    Write-Host $line
}

function Get-RemoteNext {
    $resp = Invoke-WebRequest -Uri $BusUrl -UseBasicParsing -TimeoutSec 30
    if ($resp.StatusCode -ne 200) { throw "HTTP $($resp.StatusCode) from $BusUrl" }
    return [string]$resp.Content
}

function Get-ContentSha([string]$text) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($text)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $hash = $sha.ComputeHash($bytes)
        return ([BitConverter]::ToString($hash) -replace "-", "").ToLowerInvariant()
    } finally { $sha.Dispose() }
}

function Invoke-OnePoll {
    $body = Get-RemoteNext
    $sha = Get-ContentSha $body
    $prev = $null
    if (Test-Path $hashFile) { $prev = (Get-Content $hashFile -Raw).Trim() }

    Set-Content -Path $nextLocal -Value $body -Encoding UTF8

    if ($sha -ne $prev) {
        Set-Content -Path $hashFile -Value $sha -Encoding ASCII
        $flagObj = [ordered]@{
            measuredAt = (Get-Date).ToUniversalTime().ToString("o")
            sha256     = $sha
            path       = $nextLocal
            url        = $BusUrl
        }
        Set-Content -Path $flagNew -Value ($flagObj | ConvertTo-Json) -Encoding UTF8
        Write-Log "NEW_ORDER sha=$sha bytes=$($body.Length) -> $nextLocal"
        return "NEW_ORDER"
    }

    Write-Log "UNCHANGED sha=$sha"
    return "UNCHANGED"
}

Write-Log "poll start Loop=$Loop IntervalSec=$IntervalSec"
do {
    try {
        $status = Invoke-OnePoll
    } catch {
        Write-Log "ERROR $($_.Exception.Message)"
        $status = "ERROR"
    }
    if (-not $Loop) { break }
    Start-Sleep -Seconds $IntervalSec
} while ($true)

Write-Log "poll end status=$status"
exit 0
