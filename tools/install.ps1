<#
.SYNOPSIS
  Install, update, or remove the ctrl-* skill pack for DSH without ever deleting data it does not own.

.DESCRIPTION
  DSH discovers skills from <root>/<name>/SKILL.md or <root>/<name>.md at the top level of a
  scanned root. The user-level root is <DSH_HOME>/skills, which defaults to ~/.dsh/skills.

  Link mode (default) creates one directory junction per ctrl-* bundle, so edits in this repository
  are visible without copying. Copy mode copies each bundle and writes an ownership record,
  .ctrl-skills-install.json, holding the SHA-256 of every copied file.

  Safety rules:
  - A destination is owned only when it is a link whose target is exactly this source's bundle
    directory, or a copy whose ownership record matches its current files.
  - Links are removed with a non-recursive call that deletes the link itself, never its target.
  - A dangling link (target missing) holds no data and may be replaced.
  - A foreign link, a modified copy, or a directory this script did not create is skipped. With
    -Force, a foreign link is unlinked (its target is untouched) and a real directory is MOVED to
    <Target>\.ctrl-skills-backup\<timestamp>\<name>; nothing is deleted. DSH scans only the top
    level of a root, so the backup folder is not discovered as a skill.
  - -WhatIf prints the plan without changing anything.

  Installing files does not enable a provider. The @deepseek-ai/dsh-skill-filesystem provider must
  be active and must scan the target root before a session can load the skills.

.PARAMETER Source
  Directory holding the ctrl-* bundle directories. Defaults to this package's skills/ directory,
  then a legacy sibling skills/ directory, then the package root.

.PARAMETER Target
  Skill root to install into. Defaults to $env:DSH_HOME\skills, or ~\.dsh\skills when DSH_HOME is unset.

.PARAMETER Mode
  link (default) creates directory junctions. copy creates owned snapshots that need re-running
  after source edits.

.PARAMETER Remove
  Remove the installed ctrl-* links or unmodified owned copies instead of installing.

.PARAMETER Force
  Also act on foreign links (unlink only, the target is untouched) and on directories this script
  does not own (moved to the backup folder). Their data is never deleted.

.EXAMPLE
  powershell -File tools/install.ps1 -WhatIf
  Show what an install into the default root would do.

.EXAMPLE
  powershell -File tools/install.ps1 -Mode copy -Target D:\skills
  Install owned copies into D:\skills.

.EXAMPLE
  powershell -File tools/install.ps1 -Remove
  Remove the links (or unmodified owned copies) this pack installed in the default root.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [string]$Source,
  [string]$Target,
  [ValidateSet('link', 'copy')]
  [string]$Mode = 'link',
  [switch]$Remove,
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$MarkerName = '.ctrl-skills-install.json'
$BackupDirName = '.ctrl-skills-backup'

function Get-NormalizedPath {
  param([Parameter(Mandatory = $true)][string]$Path)
  $expanded = [Environment]::ExpandEnvironmentVariables($Path)
  if (-not [System.IO.Path]::IsPathRooted($expanded)) {
    $expanded = Join-Path (Get-Location).Path $expanded
  }
  $full = [System.IO.Path]::GetFullPath($expanded)
  if ($full.Length -gt 3) { $full = $full.TrimEnd('\', '/') }
  return $full
}

function Test-SamePath {
  param([string]$A, [string]$B)
  return [string]::Equals($A, $B, [System.StringComparison]::OrdinalIgnoreCase)
}

function Test-PathInside {
  # True when $Child equals $Parent or lies below it, compared on whole path segments.
  param([string]$Child, [string]$Parent)
  if (Test-SamePath $Child $Parent) { return $true }
  $prefix = $Parent.TrimEnd('\', '/') + '\'
  return $Child.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)
}

function Get-Entry {
  # Get-Item that also returns dangling links; Test-Path is unreliable for those.
  param([string]$Path)
  return Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
}

function Test-IsLink {
  # Only junctions and symbolic links count. Other reparse points (for example cloud-storage
  # placeholders) are real directories and are treated as foreign data.
  param($Item)
  if (-not $Item) { return $false }
  return ($Item.LinkType -eq 'Junction' -or $Item.LinkType -eq 'SymbolicLink')
}

function Get-LinkTargets {
  param($Item)
  $targets = @()
  foreach ($raw in @($Item.Target)) {
    if (-not $raw) { continue }
    $t = [string]$raw
    if ($t.StartsWith('\??\')) { $t = $t.Substring(4) }
    if (-not [System.IO.Path]::IsPathRooted($t)) { $t = Join-Path (Split-Path -Parent $Item.FullName) $t }
    try { $targets += (Get-NormalizedPath $t) } catch { }
  }
  return $targets
}

function Get-RelativeFiles {
  # Relative path (forward slashes) -> SHA-256 for every file below $Root except the marker.
  param([string]$Root)
  $map = @{}
  $rootFull = (Get-NormalizedPath $Root)
  foreach ($file in Get-ChildItem -LiteralPath $rootFull -Recurse -File -Force) {
    $rel = $file.FullName.Substring($rootFull.Length).TrimStart('\', '/').Replace('\', '/')
    if ($rel -eq $MarkerName) { continue }
    $map[$rel] = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
  }
  return $map
}

function Get-CopyState {
  # 'owned-clean', 'owned-modified', or 'foreign' for a real directory.
  param([string]$Dir, [string]$BundleName)
  $markerPath = Join-Path $Dir $MarkerName
  if (-not (Test-Path -LiteralPath $markerPath -PathType Leaf)) { return 'foreign' }
  try { $marker = Get-Content -LiteralPath $markerPath -Raw -Encoding UTF8 | ConvertFrom-Json }
  catch { return 'foreign' }
  if ($marker.pack -ne 'ctrl-skills' -or $marker.bundle -ne $BundleName -or -not $marker.files) { return 'foreign' }
  $nested = Get-ChildItem -LiteralPath $Dir -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Attributes -band [System.IO.FileAttributes]::ReparsePoint }
  if ($nested) { return 'owned-modified' }
  $expected = @{}
  foreach ($p in $marker.files.PSObject.Properties) { $expected[$p.Name] = [string]$p.Value }
  $actual = Get-RelativeFiles $Dir
  if ($expected.Count -ne $actual.Count) { return 'owned-modified' }
  foreach ($key in $expected.Keys) {
    if (-not $actual.ContainsKey($key) -or $actual[$key] -ne $expected[$key]) { return 'owned-modified' }
  }
  return 'owned-clean'
}

function Get-DestinationState {
  param([string]$Dest, [string]$BundleSource, [string]$BundleName)
  $item = Get-Entry $Dest
  if (-not $item) { return @{ Kind = 'absent' } }
  if (Test-IsLink $item) {
    $targets = @(Get-LinkTargets $item)
    foreach ($t in $targets) {
      if (Test-SamePath $t $BundleSource) { return @{ Kind = 'owned-link'; Target = $t } }
    }
    $live = $false
    foreach ($t in $targets) { if (Test-Path -LiteralPath $t) { $live = $true } }
    if (-not $live) { return @{ Kind = 'dangling-link'; Target = ($targets -join ';') } }
    return @{ Kind = 'foreign-link'; Target = ($targets -join ';') }
  }
  if (-not $item.PSIsContainer) { return @{ Kind = 'foreign-file' } }
  return @{ Kind = (Get-CopyState $Dest $BundleName) }
}

function Remove-LinkOnly {
  param([string]$Path)
  # Non-recursive delete removes the junction or directory symlink itself, never the target's files.
  [System.IO.Directory]::Delete($Path)
}

function Move-ToBackup {
  param([string]$Path, [string]$Name)
  $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $dir = Join-Path (Join-Path $script:targetRoot $BackupDirName) $stamp
  $candidate = Join-Path $dir $Name
  $n = 1
  while (Get-Entry $candidate) { $candidate = Join-Path $dir ("{0}.{1}" -f $Name, $n); $n++ }
  New-Item -ItemType Directory -Path (Split-Path -Parent $candidate) -Force | Out-Null
  Move-Item -LiteralPath $Path -Destination $candidate
  return $candidate
}

function Install-Copy {
  param([string]$BundleSource, [string]$Dest, [string]$Name)
  $staging = Join-Path $script:targetRoot ('.ctrl-skills-staging-' + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Path $staging | Out-Null
  try {
    $stagedBundle = Join-Path $staging $Name
    Copy-Item -LiteralPath $BundleSource -Destination $stagedBundle -Recurse
    $files = Get-RelativeFiles $stagedBundle
    $ordered = [ordered]@{}
    foreach ($key in ($files.Keys | Sort-Object)) { $ordered[$key] = $files[$key] }
    $record = [ordered]@{
      pack = 'ctrl-skills'; bundle = $Name; mode = 'copy'; source = $BundleSource
      installedAt = (Get-Date).ToString('o'); files = $ordered
    }
    $json = $record | ConvertTo-Json -Depth 4
    [System.IO.File]::WriteAllText((Join-Path $stagedBundle $MarkerName), $json, (New-Object System.Text.UTF8Encoding($false)))
    Move-Item -LiteralPath $stagedBundle -Destination $Dest
  } finally {
    # The staging directory was created above by this invocation; only it is removed here.
    if (Test-Path -LiteralPath $staging) { Remove-Item -LiteralPath $staging -Recurse -Force }
  }
}

# ---- resolve source and target -------------------------------------------------------------
if (-not $Source) {
  $pkgRoot = Split-Path -Parent $PSScriptRoot
  $candidates = @((Join-Path $pkgRoot 'skills'), (Join-Path (Split-Path -Parent $pkgRoot) 'skills'), $pkgRoot)
  $chosen = $null
  foreach ($candidate in $candidates) {
    if (-not (Test-Path -LiteralPath $candidate -PathType Container)) { continue }
    $hasBundle = Get-ChildItem -LiteralPath $candidate -Directory -ErrorAction SilentlyContinue |
      Where-Object { $_.Name -like 'ctrl-*' -and (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')) }
    if ($hasBundle) { $chosen = $candidate; break }
  }
  if (-not $chosen) { $chosen = Join-Path $pkgRoot 'skills' }
  $Source = $chosen
}
$sourceRoot = Get-NormalizedPath $Source
if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) { throw "Source does not exist: $sourceRoot" }

if (-not $Target) {
  $dshHome = $env:DSH_HOME
  if ([string]::IsNullOrWhiteSpace($dshHome)) { $dshHome = Join-Path $HOME '.dsh' }
  $Target = Join-Path $dshHome 'skills'
}
$script:targetRoot = Get-NormalizedPath $Target
if (Test-PathInside $script:targetRoot $sourceRoot) {
  throw "Refusing to install into the source tree itself: $($script:targetRoot)"
}

$bundles = @(Get-ChildItem -LiteralPath $sourceRoot -Directory |
  Where-Object { $_.Name -like 'ctrl-*' -and (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')) } |
  Sort-Object Name)
if ($bundles.Count -eq 0) { throw "No ctrl-* bundles with a SKILL.md were found under $sourceRoot" }

Write-Host "source     : $sourceRoot"
Write-Host "skill root : $($script:targetRoot)"
Write-Host ("mode       : {0}{1}" -f $(if ($Remove) { 'remove' } else { $Mode }), $(if ($WhatIfPreference) { ' (WhatIf: no changes)' } else { '' }))
Write-Host "bundles    : $($bundles.Count)"
Write-Host ''

if (-not $Remove -and -not (Test-Path -LiteralPath $script:targetRoot -PathType Container)) {
  if ($PSCmdlet.ShouldProcess($script:targetRoot, 'create skill root')) {
    New-Item -ItemType Directory -Path $script:targetRoot -Force | Out-Null
    Write-Host "created skill root: $($script:targetRoot)"
  }
}

$changed = 0; $skipped = 0; $failed = 0; $unchanged = 0

foreach ($bundle in $bundles) {
  $name = $bundle.Name
  $bundleSource = Get-NormalizedPath $bundle.FullName
  $dest = Join-Path $script:targetRoot $name
  try {
    $state = Get-DestinationState $dest $bundleSource $name
    $kind = $state.Kind

    # Step 1: clear the destination when this run is allowed to.
    $clear = $false
    switch ($kind) {
      'absent' { }
      'owned-link' { if ($Remove -or $Mode -eq 'copy') { $clear = $true } }
      'owned-clean' { $clear = $true }
      'dangling-link' { $clear = $true }
      'foreign-link' { if ($Force) { $clear = $true } }
      'owned-modified' { if ($Force) { $clear = $true } }
      'foreign' { if ($Force) { $clear = $true } }
      'foreign-file' { if ($Force) { $clear = $true } }
    }

    if ($kind -eq 'absent' -and $Remove) { Write-Host ("  skip   {0} (not installed)" -f $name); $skipped++; continue }
    if ($kind -eq 'owned-link' -and -not $Remove -and $Mode -eq 'link') { Write-Host ("  ok     {0} (already linked)" -f $name); $unchanged++; continue }
    if ($kind -ne 'absent' -and -not $clear) {
      $why = switch ($kind) {
        'foreign-link' { "link to another location ($($state.Target))" }
        'owned-modified' { 'installed copy was modified after installation' }
        default { 'not created by this installer' }
      }
      Write-Warning ("  skip   {0}: {1}; use -Force to unlink a link or move a directory to {2}" -f $name, $why, $BackupDirName)
      $skipped++
      continue
    }

    if ($clear) {
      if ($kind -in @('owned-link', 'dangling-link', 'foreign-link')) {
        if ($PSCmdlet.ShouldProcess($dest, "remove link only (target untouched: $($state.Target))")) {
          Remove-LinkOnly $dest
          Write-Host ("  unlink {0}" -f $name)
        }
      } elseif ($kind -eq 'owned-clean') {
        if ($PSCmdlet.ShouldProcess($dest, 'delete unmodified owned copy')) {
          Remove-Item -LiteralPath $dest -Recurse -Force
          Write-Host ("  delete {0} (unmodified owned copy)" -f $name)
        }
      } else {
        if ($PSCmdlet.ShouldProcess($dest, "move to $BackupDirName")) {
          $backup = Move-ToBackup $dest $name
          Write-Host ("  backup {0} -> {1}" -f $name, $backup)
        }
      }
      if ($Remove) { $changed++; continue }
    }

    # Step 2: install.
    if ($Mode -eq 'link') {
      if ($PSCmdlet.ShouldProcess($dest, "create junction to $bundleSource")) {
        New-Item -ItemType Junction -Path $dest -Target $bundleSource | Out-Null
        Write-Host ("  link   {0} -> {1}" -f $name, $bundleSource)
      }
    } else {
      if ($PSCmdlet.ShouldProcess($dest, "copy from $bundleSource with ownership record")) {
        Install-Copy $bundleSource $dest $name
        Write-Host ("  copy   {0}" -f $name)
      }
    }
    $changed++
  } catch {
    Write-Warning ("  FAIL   {0}: {1}" -f $name, $_.Exception.Message)
    $failed++
  }
}

Write-Host ''
Write-Host ("done: {0} changed, {1} unchanged, {2} skipped, {3} failed" -f $changed, $unchanged, $skipped, $failed)
Write-Host ''
Write-Host 'Next: files on disk are not the same as a loaded skill. The @deepseek-ai/dsh-skill-filesystem'
Write-Host 'provider must be active and must scan this root (or add the source skills/ directory to'
Write-Host 'customSkillDirs instead). Check offline parsing with:'
Write-Host ("  node tools/check-dsh-discovery.cjs `"{0}`"" -f $script:targetRoot)
Write-Host 'then confirm in a session that the skill tool can load ctrl-shared.'

if ($failed -gt 0) { exit 1 }
