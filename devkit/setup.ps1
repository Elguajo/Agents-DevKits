[CmdletBinding()]
param(
  [Parameter(Position = 0)]
  [string]$Command = "help",
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$Arguments
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$RepoRoot = $PSScriptRoot
$MachineName = if ($env:COMPUTERNAME) { $env:COMPUTERNAME } else { [Environment]::MachineName }
$MachineDir = Join-Path $RepoRoot ("machines/{0}" -f $MachineName)
$StateFile = Join-Path $MachineDir "enabled-mcps.txt"
$DefaultMcpFile = Join-Path $RepoRoot "mcp/profiles/default.txt"

function Write-Status([string]$Status, [string]$Message) {
  "{0,-8} {1}" -f $Status.ToUpperInvariant(), $Message | Write-Output
}

function Get-Tool([string]$Name) {
  $item = Get-Command $Name -ErrorAction SilentlyContinue
  if ($null -eq $item) { return $null }
  return $item.Source
}

function Get-SelectedMcps {
  $source = if (Test-Path $StateFile) { $StateFile } else { $DefaultMcpFile }
  $names = Get-Content $source | ForEach-Object {
    ($_ -replace '#.*$', '').Trim()
  } | Where-Object { $_ }
  return @{ Source = $source; Names = @($names) }
}

function Assert-McpName([string]$Name) {
  $definition = Join-Path $RepoRoot ("mcp/definitions/{0}.toml" -f $Name)
  if ($Name -notmatch '^[a-z0-9-]+$' -or -not (Test-Path $definition)) {
    $known = Get-ChildItem (Join-Path $RepoRoot "mcp/definitions") -Filter '*.toml' | ForEach-Object { $_.BaseName } | Sort-Object
    throw "Unknown MCP '$Name'. Known MCPs: $($known -join ', ')"
  }
}

function Write-SelectedMcps([string[]]$Names) {
  New-Item -ItemType Directory -Force -Path $MachineDir | Out-Null
  $body = @("# Local MCP selection for $MachineName. This file is ignored by Git.") + @($Names | Sort-Object -Unique)
  Set-Content -Path $StateFile -Value $body -Encoding utf8
}

function Add-ConfigLayer([System.Collections.Generic.List[string]]$Lines, [System.Collections.Generic.HashSet[string]]$Tables, [string]$Path) {
  if (-not (Test-Path $Path)) { throw "Missing configuration layer: $Path" }
  $relative = $Path.Substring($RepoRoot.Length).TrimStart([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
  $Lines.Add("# Source: $relative")
  foreach ($line in Get-Content $Path) {
    if ($line -match '^\[') {
      if (-not $Tables.Add($line)) { throw "Duplicate TOML table: $line" }
    }
    $Lines.Add($line)
  }
  $Lines.Add("")
}

function Compose-Config([string]$OutputPath) {
  $lines = [System.Collections.Generic.List[string]]::new()
  $tables = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
  Add-ConfigLayer $lines $tables (Join-Path $RepoRoot "config/portable/base.toml")
  Add-ConfigLayer $lines $tables (Join-Path $RepoRoot "config/portable/plugins.toml")
  $selection = Get-SelectedMcps
  foreach ($name in $selection.Names) {
    Assert-McpName $name
    Add-ConfigLayer $lines $tables (Join-Path $RepoRoot ("mcp/definitions/{0}.toml" -f $name))
  }
  Add-ConfigLayer $lines $tables (Join-Path $RepoRoot "config/platform/windows.toml")
  $machineLayer = Join-Path $MachineDir "codex.toml"
  if (Test-Path $machineLayer) { Add-ConfigLayer $lines $tables $machineLayer }
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputPath) | Out-Null
  Set-Content -Path $OutputPath -Value $lines -Encoding utf8
  Write-Output "Composed Codex config: $OutputPath"
}

function Import-LocalSecrets {
  $secrets = Join-Path $RepoRoot "secrets.local.env"
  if (-not (Test-Path $secrets)) { return }
  foreach ($line in Get-Content $secrets) {
    if ($line -match '^\s*(?:export\s+)?([A-Z0-9_]+)=(.*)$') {
      $value = $Matches[2].Trim()
      if ($value.Length -ge 2 -and (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'")))) { $value = $value.Substring(1, $value.Length - 2) }
      Set-Item -Path ("Env:{0}" -f $Matches[1]) -Value $value
    }
  }
}

function ConvertTo-TomlBasicString([string]$Value) {
  return $Value.Replace('\', '\\').Replace('"', '\"').Replace("`r`n", '\n').Replace("`n", '\n')
}

function Install-Serena([bool]$DryRun) {
  $source = Join-Path $RepoRoot "serena/serena_config.yml"
  $targetDir = Join-Path $HOME ".serena"
  $target = Join-Path $targetDir "serena_config.yml"
  if ($DryRun) { Write-Output "DRY-RUN Would adopt Serena dashboard settings at $target"; return }
  New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
  if (-not (Test-Path $target)) { Copy-Item $source $target; Write-Output "Installed Serena config to $target"; return }
  $backup = "$target.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
  Copy-Item $target $backup
  $content = Get-Content $target -Raw
  if ($content -match '(?m)^web_dashboard:') { $content = [regex]::Replace($content, '(?m)^web_dashboard:.*$', 'web_dashboard: true') } else { $content += "`nweb_dashboard: true`n" }
  if ($content -match '(?m)^web_dashboard_open_on_launch:') { $content = [regex]::Replace($content, '(?m)^web_dashboard_open_on_launch:.*$', 'web_dashboard_open_on_launch: false') } else { $content += "web_dashboard_open_on_launch: false`n" }
  Set-Content -Path $target -Value $content -Encoding utf8
  Write-Output "Backed up existing Serena config to $backup"
  Write-Output "Patched Serena dashboard settings in $target"
}

function Invoke-Install([string[]]$Args) {
  $dryRun = $Args -contains '--dry-run'
  if (@($Args | Where-Object { $_ -ne '--dry-run' }).Count -gt 0) { throw 'Usage: .\setup.ps1 install [--dry-run]' }
  Import-LocalSecrets
  $temp = Join-Path ([IO.Path]::GetTempPath()) ("agents-devkits-{0}.toml" -f [guid]::NewGuid())
  try {
    $codexDir = Join-Path $HOME '.codex'; $target = Join-Path $codexDir 'config.toml'
    if (-not $dryRun -and (Test-Path $target)) { Invoke-Backup }
    Compose-Config $temp
    $content = Get-Content $temp -Raw
    $substitutions = @{ '__HOME__' = $HOME; '__CONTEXT7_API_KEY__' = $env:CONTEXT7_API_KEY; '__ANYTYPE_HEADERS__' = $env:ANYTYPE_HEADERS; '__AFFINE_BASE_URL__' = $env:AFFINE_BASE_URL; '__AFFINE_TOOL_PROFILE__' = $env:AFFINE_TOOL_PROFILE }
    foreach ($key in $substitutions.Keys) { if ($substitutions[$key]) { $content = $content.Replace($key, (ConvertTo-TomlBasicString $substitutions[$key])) } }
    if ($dryRun) { Write-Output "DRY-RUN Would back up and install composed Codex config to $(Join-Path $HOME '.codex/config.toml')"; Install-Serena $true; return }
    New-Item -ItemType Directory -Force -Path $codexDir | Out-Null
    if (Test-Path $target) { $backup = "$target.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"; Copy-Item $target $backup; Write-Output "Backed up existing config to $backup" }
    Set-Content -Path $target -Value $content -Encoding utf8
    Write-Output "Installed composed Codex config to $target"
    Install-Serena $false
  } finally { Remove-Item $temp -Force -ErrorAction SilentlyContinue }
}

function Invoke-McpDoctor {
  $selection = Get-SelectedMcps
  Write-Output "MCP selection source: $($selection.Source)"
  $missing = 0
  foreach ($name in $selection.Names) {
    $tool = switch ($name) { 'serena' { 'uvx' } 'affine' { 'affine-mcp' } 'open-pencil' { 'openpencil-mcp' } 'chrome-devtools' { 'endpoint' } 'ideon' { 'endpoint' } default { 'npx' } }
    if ($tool -eq 'endpoint') { Write-Status WARN "$name requires its local HTTP endpoint"; continue }
    if (Get-Tool $tool) { Write-Status OK "$name ($tool)" } else { Write-Status WARN "$name requires $tool" }
  }
  foreach ($secret in @('CONTEXT7_API_KEY', 'ANYTYPE_HEADERS', 'AFFINE_BASE_URL', 'AFFINE_TOOL_PROFILE', 'IDEON_MCP_TOKEN')) {
    if (Get-Item "Env:$secret" -ErrorAction SilentlyContinue) { Write-Status OK "$secret configured" } else { Write-Status WARN "$secret is unset; placeholder remains" }
  }
}

function Invoke-Mcp([string[]]$Args) {
  $action = if ($Args.Count) { $Args[0] } else { 'list' }
  switch ($action) {
    'list' { $selection = Get-SelectedMcps; Write-Output "MCP selection source: $($selection.Source)"; $selection.Names | Write-Output }
    'enable' { if ($Args.Count -ne 2) { throw 'Usage: .\setup.ps1 mcp enable <name>' }; Assert-McpName $Args[1]; $selected = (Get-SelectedMcps).Names + $Args[1]; Write-SelectedMcps $selected; Write-Output "Enabled MCP '$($Args[1])'. Run install to regenerate Codex config." }
    'disable' { if ($Args.Count -ne 2) { throw 'Usage: .\setup.ps1 mcp disable <name>' }; Assert-McpName $Args[1]; Write-SelectedMcps @((Get-SelectedMcps).Names | Where-Object { $_ -ne $Args[1] }); Write-Output "Disabled MCP '$($Args[1])'. Run install to regenerate Codex config." }
    'doctor' { Invoke-McpDoctor }
    default { throw 'Usage: .\setup.ps1 mcp <list|enable|disable|doctor>' }
  }
}

function Get-Profiles([string[]]$Args) {
  $profiles = [System.Collections.Generic.List[string]]::new(); $dryRun = $false; $yes = $false
  for ($i = 0; $i -lt $Args.Count; $i++) {
    switch ($Args[$i]) {
      '--profile' { if ($i + 1 -ge $Args.Count) { throw '--profile requires a name' }; $i++; if (-not $profiles.Contains($Args[$i])) { $profiles.Add($Args[$i]) } }
      '--all' { $profiles.Clear(); @('base','web','ai','db','mobile') | ForEach-Object { $profiles.Add($_) } }
      '--dry-run' { $dryRun = $true }
      '--yes' { $yes = $true }
      default { throw "Unknown bootstrap argument: $($Args[$i])" }
    }
  }
  if ($profiles.Count -eq 0) { @('base','web','ai') | ForEach-Object { $profiles.Add($_) } }
  return @{ Profiles = @($profiles); DryRun = $dryRun; Yes = $yes }
}

function Invoke-Bootstrap([string[]]$Args) {
  $options = Get-Profiles $Args
  $manifest = Import-Csv (Join-Path $RepoRoot 'profiles/manifest.tsv') -Delimiter "`t"
  if (-not $options.DryRun -and -not (Get-Tool winget)) { throw 'winget is required for Windows bootstrap. Install App Installer, then rerun.' }
  Write-Output "Bootstrap profiles: $($options.Profiles -join ' ')"
  foreach ($profile in $options.Profiles) {
    $entries = @($manifest | Where-Object { $_.profile -eq $profile })
    if ($entries.Count -eq 0) { Write-Status SKIPPED "$profile has no native Windows adapter"; continue }
    foreach ($entry in $entries) {
      if (-not $entry.windows_winget) { Write-Status SKIPPED "$($entry.capability) has no Windows package mapping"; continue }
      $cmd = "winget install --id $($entry.windows_winget) --exact --accept-package-agreements --accept-source-agreements"
      if ($options.DryRun) { Write-Output "DRY-RUN $cmd" } else { & winget install --id $entry.windows_winget --exact --accept-package-agreements --accept-source-agreements }
    }
  }
  if ($options.Profiles -contains 'base') {
    if ($options.DryRun) { Write-Output 'DRY-RUN Would apply safe global Git defaults' } else { & git config --global init.defaultBranch main; & git config --global pull.rebase false; & git config --global push.autoSetupRemote true }
  }
  if ($options.Profiles -contains 'web') {
    if ($options.DryRun) { Write-Output 'DRY-RUN corepack enable' } elseif (Get-Tool corepack) { & corepack enable } else { Write-Status WARN 'corepack is unavailable after Node installation; reopen PowerShell and rerun web profile' }
  }
  if ($options.DryRun) { Invoke-Install @('--dry-run') } else { Invoke-Install @() }
  Invoke-Doctor
}

function Invoke-Auth {
  if (-not (Get-Tool gh)) { throw 'GitHub CLI (gh) is required for auth. Run bootstrap --profile base first.' }
  & gh auth status 2>$null
  if ($LASTEXITCODE -eq 0) { Write-Output 'GitHub CLI is already authenticated.'; return }
  & gh auth login --hostname github.com --git-protocol https --web
}

function Invoke-Backup {
  $source = Join-Path $HOME '.codex/config.toml'
  if (-not (Test-Path $source)) { throw "Missing Codex config: $source" }
  New-Item -ItemType Directory -Force -Path $MachineDir | Out-Null
  $target = Join-Path $MachineDir 'codex.toml'
  if (Test-Path $target) { Copy-Item $target "$target.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')" }
  $capture = $false; $output = [System.Collections.Generic.List[string]]::new()
  foreach ($line in Get-Content $source) {
    if ($line -match '^notify\s*=') { $output.Add($line); continue }
    if ($line -match '^\[') { $capture = $line -match '^\[projects\.' -or $line -match '^\[mcp_servers\.(node_repl|node_repl\.env|computer-use|pencil|illustrator)\]' }
    if ($capture) { $output.Add($line) }
  }
  if ($output.Count -eq 0) { $output.Add('# No project trust entries were found in the local Codex config.') }
  Set-Content -Path $target -Value $output -Encoding utf8
  Write-Output "Saved local project-trust layer to $target (ignored by Git)."
}

function Invoke-Snapshot {
  $dir = Join-Path $RepoRoot 'snapshots/current'; New-Item -ItemType Directory -Force -Path $dir | Out-Null
  @("# Generated by .\\setup.ps1 snapshot", '# Safe inventory only. No credentials, sessions, private keys, browser profiles, or caches.', "generated_at_utc=$((Get-Date).ToUniversalTime().ToString('o'))", "os=$([Environment]::OSVersion.VersionString)", "arch=$env:PROCESSOR_ARCHITECTURE") | Set-Content (Join-Path $dir 'metadata.txt') -Encoding utf8
  $versions = foreach ($tool in @('git','gh','node','npm','pnpm','bun','python','uv','uvx','rg')) { if (Get-Tool $tool) { "## $tool"; & $tool --version 2>$null | Select-Object -First 1; '' } }; Set-Content (Join-Path $dir 'cli-versions.txt') -Value $versions -Encoding utf8
  if (Get-Tool winget) { & winget list --accept-source-agreements 2>$null | Set-Content (Join-Path $dir 'winget-packages.txt') -Encoding utf8 } else { '# winget unavailable' | Set-Content (Join-Path $dir 'winget-packages.txt') -Encoding utf8 }
  Write-Output "Snapshot written to $dir"
}

function Invoke-Guard {
  $patterns = @('ctx7sk-[A-Za-z0-9_-]+','gho_[A-Za-z0-9_]+','ghp_[A-Za-z0-9_]+','github_pat_[A-Za-z0-9_]+','sk-[A-Za-z0-9_-]{20,}','Bearer\s+[A-Za-z0-9._-]+')
  $files = Get-ChildItem $RepoRoot -Recurse -File | Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' -and $_.Name -ne 'secrets.local.env' -and $_.Name -notmatch '\.backup\.' }
  $hits = foreach ($pattern in $patterns) { $files | Select-String -Pattern $pattern -ErrorAction SilentlyContinue }
  if ($hits) { $hits | ForEach-Object { $_.Path + ':' + $_.LineNumber }; throw 'Secret guard found possible secrets.' }
  Write-Output 'Secret guard passed'
}

function Invoke-Doctor {
  Import-LocalSecrets
  Write-Output 'Platform'
  Write-Status OK "Windows $([Environment]::OSVersion.Version) ($env:PROCESSOR_ARCHITECTURE)"
  Write-Status OK "PowerShell $($PSVersionTable.PSVersion)"
  if (Get-Tool winget) { Write-Status OK "winget $(Get-Tool winget)" } else { Write-Status MISSING 'winget (install App Installer)' }
  Write-Output "`nCore"
  foreach ($tool in @('git','gh','node','pnpm','bun','python','uv','uvx','codex')) { if (Get-Tool $tool) { Write-Status OK "$tool $(Get-Tool $tool)" } else { Write-Status MISSING $tool } }
  Write-Output "`nCodex"
  if (Test-Path (Join-Path $RepoRoot 'config/portable/base.toml')) { Write-Status OK 'portable config sources' } else { Write-Status ERROR 'portable config sources missing' }
  if (Test-Path (Join-Path $HOME '.codex/config.toml')) { Write-Status OK 'installed Codex config' } else { Write-Status WARN 'Codex config not installed' }
  if (Test-Path $MachineDir) { Write-Status OK "machine override directory $MachineDir" } else { Write-Status SKIPPED 'no machine override directory yet' }
  Write-Output "`nAI"
  if (Get-Tool uvx) { Write-Status OK 'Serena runtime (uvx)' } else { Write-Status MISSING 'Serena runtime (uvx)' }
  Invoke-McpDoctor
  Write-Status SKIPPED 'Gstack install: upstream currently requires Git Bash/MSYS; native PowerShell is unsupported.'
  $probe = Join-Path ([IO.Path]::GetTempPath()) ("devkit-link-{0}" -f [guid]::NewGuid())
  try { New-Item -ItemType Directory -Path $probe | Out-Null; New-Item -ItemType SymbolicLink -Path "$probe-link" -Target $probe -ErrorAction Stop | Out-Null; Write-Status OK 'symlink capability' } catch { Write-Status WARN 'symlink creation unavailable; enable Windows Developer Mode or use an elevated shell.' } finally { Remove-Item "$probe-link" -Force -ErrorAction SilentlyContinue; Remove-Item $probe -Force -ErrorAction SilentlyContinue }
}

function Invoke-Test {
  $tokens = $null; $errors = $null; [void][System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath, [ref]$tokens, [ref]$errors)
  if ($errors.Count -gt 0) { throw ($errors | Out-String) }
  $output = Join-Path ([IO.Path]::GetTempPath()) ("agents-devkits-test-{0}.toml" -f [guid]::NewGuid())
  try { Compose-Config $output; if (-not (Test-Path $output)) { throw 'Config composition did not create output.' }; Invoke-Mcp @('list') | Out-Null; Invoke-Guard } finally { Remove-Item $output -Force -ErrorAction SilentlyContinue }
  Write-Output 'PowerShell tests passed'
}

function Invoke-Export {
  $sourceConfig = Join-Path $HOME '.codex/config.toml'
  if (Test-Path $sourceConfig) { Invoke-Backup } else { Write-Status SKIPPED 'Codex backup (no installed config)' }  Invoke-Guard
  $stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
  $name = "agents-devkits-$stamp"
  $temp = Join-Path ([IO.Path]::GetTempPath()) ([guid]::NewGuid().ToString())
  $artifact = Join-Path $temp $name
  $exports = Join-Path $RepoRoot 'exports'
  try {
    New-Item -ItemType Directory -Force -Path $artifact, $exports | Out-Null
    foreach ($item in @('.gitignore','Brewfile','README.md','backup.sh','bootstrap.sh','doctor.sh','install.sh','restore.sh','setup.ps1','sync.sh','config','gstack','mcp','profiles','scripts','secrets.example.env','serena')) {
      $source = Join-Path $RepoRoot $item
      if (Test-Path $source) { Copy-Item $source (Join-Path $artifact $item) -Recurse -Force }
    }
    @("name=$name", "created_at_utc=$stamp", 'Safe export excludes Git history, local secrets, auth state, private keys, sessions, caches, and machine overrides.') | Set-Content (Join-Path $artifact 'MANIFEST.txt') -Encoding utf8
    $archive = Join-Path $exports "$name.zip"
    Compress-Archive -Path $artifact -DestinationPath $archive -Force
    $hash = (Get-FileHash $archive -Algorithm SHA256).Hash.ToLowerInvariant()
    "$hash  $(Split-Path -Leaf $archive)" | Set-Content (Join-Path $exports "$name.SHA256SUMS") -Encoding ascii
    Write-Output "Archive: $archive"
  } finally { Remove-Item $temp -Recurse -Force -ErrorAction SilentlyContinue }
}

function Show-Help {
  @'
Usage: .\setup.ps1 <command>

Commands: doctor, bootstrap, install, backup, restore, snapshot, export, auth,
          mcp, mcp-doctor, gstack, guard, test
'@ | Write-Output
}

switch ($Command) {
  'doctor' { Invoke-Doctor }
  'install' { Invoke-Install $Arguments }
  'bootstrap' { Invoke-Bootstrap $Arguments }
  'auth' { Invoke-Auth }
  'backup' { Invoke-Backup }
  'snapshot' { Invoke-Snapshot }
  'mcp' { Invoke-Mcp $Arguments }
  'mcp-doctor' { Invoke-McpDoctor }
  'gstack' { Write-Status SKIPPED 'Gstack native PowerShell install is unsupported upstream; see README.' }
  'guard' { Invoke-Guard }
  'test' { Invoke-Test }
  'restore' { if (-not (Test-Path (Join-Path $RepoRoot 'secrets.local.env'))) { Copy-Item (Join-Path $RepoRoot 'secrets.example.env') (Join-Path $RepoRoot 'secrets.local.env'); Write-Output 'Created secrets.local.env from the example.' }; Invoke-Bootstrap $Arguments }
  'export' { Invoke-Export }
  'help' { Show-Help }
  default { Show-Help; throw "Unknown command: $Command" }
}
