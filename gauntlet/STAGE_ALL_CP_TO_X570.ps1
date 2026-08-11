# STAGE_ALL_CP_TO_X570.ps1 — put all CP-XX into live Gauntlet on BENX570E
$ErrorActionPreference = "Stop"
$Root = "E:\W_BENJITWIN_GAUNTLET"
$Base = "https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/gauntlet/PERPLEXITY_CP_XX_PACK/fixtures"
New-Item -ItemType Directory -Force -Path "$Root\W_BENJITWIN_INTAKE","$Root\W_BENJITWIN_PROCESSED","$Root\fixtures","$Root\control","$Root\_receipts" | Out-Null

$files = @(
  @{ Rel = "CP-01/CP-01_Clean_Product.md"; Dest = "$Root\fixtures\CP-01\CP-01_Clean_Product.md" },
  @{ Rel = "CP-02/CP-02_Research_vs_Product.md"; Dest = "$Root\fixtures\CP-02\CP-02_Research_vs_Product.md" },
  @{ Rel = "CP-03/CP-03_Candidate_Not_Policy.md"; Dest = "$Root\fixtures\CP-03\CP-03_Candidate_Not_Policy.md" },
  @{ Rel = "CP-04/CP-04_Hard_UNKNOWN.md"; Dest = "$Root\fixtures\CP-04\CP-04_Hard_UNKNOWN.md" },
  @{ Rel = "CP-05/MANIFEST.md"; Dest = "$Root\fixtures\CP-05\MANIFEST.md" },
  @{ Rel = "CP-05/identity.md"; Dest = "$Root\fixtures\CP-05\identity.md" },
  @{ Rel = "CP-05/lineage.md"; Dest = "$Root\fixtures\CP-05\lineage.md" },
  @{ Rel = "CP-05/noise.txt"; Dest = "$Root\fixtures\CP-05\noise.txt" },
  @{ Rel = "CP-06/CP-06_Alias_Collision.md"; Dest = "$Root\fixtures\CP-06\CP-06_Alias_Collision.md" },
  @{ Rel = "CP-07/CP-07_EMPTY.md"; Dest = "$Root\fixtures\CP-07\CP-07_EMPTY.md" },
  @{ Rel = "CP-07/CP-07_TRUNCATED.md"; Dest = "$Root\fixtures\CP-07\CP-07_TRUNCATED.md" },
  @{ Rel = "CP-08/CP-08_Known_Identity_Fight.md"; Dest = "$Root\fixtures\CP-08\CP-08_Known_Identity_Fight.md" },
  @{ Rel = "CP-09/README_BATCH.md"; Dest = "$Root\fixtures\CP-09\README_BATCH.md" },
  @{ Rel = "CP-10/CP-10_Integrity_Bait.md"; Dest = "$Root\fixtures\CP-10\CP-10_Integrity_Bait.md" },
  @{ Rel = "NEXT_CP.md"; Dest = "$Root\NEXT_CP.md" }
)
foreach ($f in $files) {
  $dir = Split-Path $f.Dest -Parent
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $uri = "$Base/$($f.Rel -replace '\\','/')"
  Write-Host "GET $uri"
  Invoke-WebRequest -Uri $uri -OutFile $f.Dest -UseBasicParsing
}
Copy-Item "$Root\fixtures\CP-02\CP-02_Research_vs_Product.md" "$Root\W_BENJITWIN_INTAKE\CP-02_Research_vs_Product.md" -Force
$prov = "$Root\W_BENJITWIN_INTAKE\CP-02_Research_vs_Product__provisional.md"
if (Test-Path $prov) { Rename-Item $prov "$prov.BAK_DISPUTED" -Force }
$cp2 = Get-Item "$Root\W_BENJITWIN_INTAKE\CP-02_Research_vs_Product.md"
Write-Host "INTAKE CP-02 length=$($cp2.Length) (expect 1122)"
Get-ChildItem -Recurse "$Root\fixtures" | Select-Object FullName, Length
Write-Host "STAGE_ALL_CP_TO_X570 DONE"
