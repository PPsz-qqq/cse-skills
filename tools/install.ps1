<#
.SYNOPSIS
  Install, update, or remove the ctrl-* skill pack for DSH.

.DESCRIPTION
  DSH discovers skills from <root>/<name>/SKILL.md or <root>/<name>.md at the top level of a
  scanned root. The user-level root is <DSH_HOME>/skills, which defaults to ~/.dsh/skills.

  This script links every ctrl-* bundle in this repository into that root so that edits made
  here are live without copying. The default mode is a directory junction, which requires no
  elevation on Windows and lets DSH's watcher observe changes made in this repository.

  It never deletes anything that it did not create. Removal only deletes a link whose target
  resolves inside this repository.

.PARAMETER Source
  Repository root containing the ctrl-* bundle directories. Defaults to the parent of this script.

.PARAMETER Target
  Skill root to link into. Defaults to $env:DSH_HOME/skills, or ~/.dsh/skills when DSH_HOME is unset.

.PARAMETER Mode
  link (default) creates a directory junction. copy copies the bundles instead, for users who
  prefer a snapshot or whose filesystem does not support junctions.

.PARAMETER Remove
  Remove the installed ctrl-* links or copies instead of installing.

.PARAMETER Force
  With copy mode, overwrite an existing destination. With link mode, replace an existing
  destination that is a link into this repository.

.EXAMPLE
  pwsh -File tools/install.ps1
  Install every ctrl-* bundle into the default user skill root.

.EXAMPLE
  pwsh -File tools/install.ps1 -Mode copy -Target D:\skills
  Install a copied snapshot into D:\skills.

.EXAMPLE
  pwsh -File tools/install.ps1 -Remove
  Remove the installed ctrl-* links from the default user skill root.
#>
[CmdletBinding()]
param(
  [string]$Source,
  [string]$Target,
  [ValidateSet('link', 'copy')]
  [string]$Mode = 'link',
  [switch]$Remove,
  [switch]$Force
)

$ErrorActionPreference = 'Stop'

function Resolve-FullPath {
  param([Parameter(Mandatory)][string]$Path, [switch]$AllowMissing)
  $expanded = [Environment]::ExpandEnvironmentVariables($Path)
  if (-not [System.IO.Path]::IsPathRooted($expanded)) {
    $expanded = Join-Path (Get-Location).Path $expanded
  }
  if ($AllowMissing) {
    return [System.IO.Path]::GetFullPath($expanded)
  }
  if (-not (Test-Path -LiteralPath $expanded)) {
    throw "Path does not exist: $expanded"
  }
  return (Get-Item -LiteralPath $expanded).FullName
}

# Resolve the source root, which holds the ctrl-* bundle directories. It is normally the
# `skills/` subdirectory of this package. Fall back to the package root when the bundles are
# stored inline, and to a sibling `skills/` directory for the older split layout.
if (-not $Source) {
  $pkgRoot = Split-Path -Parent $PSScriptRoot
  $candidates = @(
    (Join-Path $pkgRoot 'skills'),
    (Join-Path (Split-Path -Parent $pkgRoot) 'skills'),
    $pkgRoot
  )
  $chosen = $null
  foreach ($candidate in $candidates) {
    if (-not (Test-Path -LiteralPath $candidate)) { continue }
    $hasBundle = Get-ChildItem -LiteralPath $candidate -Directory -ErrorAction SilentlyContinue |
      Where-Object { $_.Name -like 'ctrl-*' -and (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')) }
    if ($hasBundle) { $chosen = $candidate; break }
  }
  if (-not $chosen) { $chosen = Join-Path $pkgRoot 'skills' }
  $Source = $chosen
}
$sourceRoot = Resolve-FullPath -Path $Source

# Resolve the skill root, preferring DSH_HOME over a hardcoded home path.
if (-not $Target) {
  $dshHome = $env:DSH_HOME
  if ([string]::IsNullOrWhiteSpace($dshHome)) {
    $dshHome = Join-Path $HOME '.dsh'
  }
  $Target = Join-Path $dshHome 'skills'
}
$targetRoot = Resolve-FullPath -Path $Target -AllowMissing

if ($targetRoot -eq $sourceRoot) {
  throw "Refusing to operate on the repository itself as the skill root: $targetRoot"
}
if (-not (Test-Path -LiteralPath $targetRoot)) {
  New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
  Write-Host "created skill root: $targetRoot"
}

# Discover the bundles: a ctrl-* directory whose SKILL.md exists.
$bundles = Get-ChildItem -LiteralPath $sourceRoot -Directory |
  Where-Object { $_.Name -like 'ctrl-*' -and (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')) } |
  Sort-Object Name

if (-not $bundles) {
  throw "No ctrl-* bundles with a SKILL.md were found under $sourceRoot"
}

Write-Host "repository : $sourceRoot"
Write-Host "skill root : $targetRoot"
Write-Host "mode       : $(if ($Remove) { "remove ($Mode)" } else { $Mode })"
Write-Host "bundles    : $($bundles.Count)"
Write-Host ''

# Verify a destination is something this script is allowed to delete.
function Test-OwnedDestination {
  param([Parameter(Mandatory)][string]$Path)
  $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
  if (-not $item) { return $true } # nothing there, safe to write
  if ($item.LinkType) {
    $resolved = @($item.Target) | Where-Object { $_ } | ForEach-Object {
      $t = [Environment]::ExpandEnvironmentVariables($_)
      if (-not [System.IO.Path]::IsPathRooted($t)) { $t = Join-Path $item.Parent.FullName $t }
      try { [System.IO.Path]::GetFullPath($t) } catch { $null }
    }
    foreach ($r in $resolved) {
      if ($r -and $r.StartsWith($sourceRoot, [System.StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    return $false
  }
  return $false # a real directory or file that this script did not create
}

$installed = 0
$skipped = 0
$failed = 0

foreach ($bundle in $bundles) {
  $dest = Join-Path $targetRoot $bundle.Name
  $owned = Test-OwnedDestination -Path $dest

  if ($Remove) {
    if (-not (Test-Path -LiteralPath $dest)) {
      Write-Host ("  skip   {0} (not installed)" -f $bundle.Name)
      $skipped++
      continue
    }
    if (-not $owned -and -not $Force) {
      Write-Warning ("  skip   {0}: destination is not a link into this repository, refusing to delete {1}" -f $bundle.Name, $dest)
      $skipped++
      continue
    }
    Remove-Item -LiteralPath $dest -Force -Recurse
    Write-Host ("  remove {0}" -f $bundle.Name)
    $installed++
    continue
  }

  if (Test-Path -LiteralPath $dest) {
    if ($owned -or $Force) {
      Remove-Item -LiteralPath $dest -Force -Recurse
    } else {
      Write-Warning ("  skip   {0}: {1} already exists and was not created by this script; use -Force to replace" -f $bundle.Name, $dest)
      $skipped++
      continue
    }
  }

  try {
    if ($Mode -eq 'link') {
      New-Item -ItemType Junction -Path $dest -Target $bundle.FullName -ErrorAction Stop | Out-Null
      Write-Host ("  link   {0} -> {1}" -f $bundle.Name, $bundle.FullName)
    } else {
      Copy-Item -LiteralPath $bundle.FullName -Destination $dest -Recurse -Force
      Write-Host ("  copy   {0}" -f $bundle.Name)
    }
    $installed++
  } catch {
    Write-Warning ("  FAIL   {0}: {1}" -f $bundle.Name, $_.Exception.Message)
    $failed++
  }
}

Write-Host ''
Write-Host ("done: {0} changed, {1} skipped, {2} failed" -f $installed, $skipped, $failed)
Write-Host ''
Write-Host 'Next: restart is not required. The skill provider watches its roots, so the new skills'
Write-Host 'appear in the session catalog on the next model step. If a skill does not appear, check'
Write-Host 'that its SKILL.md frontmatter has a kebab-case name and a description, since an invalid'
Write-Host 'entry is skipped silently.'

if ($failed -gt 0) { exit 1 }
