Param()
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $Root

Write-Host "[cnpj-lakehouse] Starting local environment (Windows PowerShell)..."

if (-not (Test-Path -Path .venv)) {
  Write-Host "Creating Python virtualenv at .venv..."
  python -m venv .venv
}

$activate = Join-Path $Root ".venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
  Write-Host "Activating virtualenv in this PowerShell session..."
  & $activate
} else {
  Write-Warning "Could not find Activate.ps1. You can activate manually: .\.venv\Scripts\Activate.ps1"
}

if (Test-Path "local-requirements.txt") {
  Write-Host "Installing local development requirements (PySpark + Jupyter + pytest)..."
  pip install --upgrade pip
  pip install -r local-requirements.txt
} elseif (Test-Path "requirements.txt") {
  Write-Host "Installing Python requirements..."
  pip install --upgrade pip
  pip install -r requirements.txt
} else {
  Write-Host "No requirements.txt found; skipping pip install."
}

$composeDir = Join-Path $Root "local-infra"
if (Test-Path $composeDir) {
  Push-Location $composeDir
  Write-Host "Starting MinIO with Docker Compose..."
  $composeEnvArgs = @()
  $envFile = Join-Path $Root ".env"
  if (Test-Path $envFile) {
    $composeEnvArgs = @("--env-file", $envFile)
  }
  $composeCommand = "docker"
  $composeSubcommand = @("compose")
  docker compose version *> $null
  if ($LASTEXITCODE -ne 0) {
    $composeCommand = "docker-compose"
    $composeSubcommand = @()
  }
  try {
    & $composeCommand @composeSubcommand @composeEnvArgs up -d
    if ($LASTEXITCODE -ne 0) {
      throw "Docker Compose failed with exit code $LASTEXITCODE"
    }
  } finally {
    Pop-Location
  }
} else {
  Write-Warning "No local-infra folder found at $composeDir. Skipping Docker Compose start."
}

Write-Host "Local environment ready. Virtualenv active in this session."
Write-Host "MinIO Console: http://localhost:9001"
Write-Host "MinIO API: http://localhost:9000"
Write-Host "Credentials: minioadmin / minioadmin"
Write-Host "Buckets: cnpj-raw, cnpj-bronze, cnpj-silver, cnpj-gold, cnpj-checkpoints"
Write-Host "Spark UI: http://localhost:4040"
Write-Host "Use: python -m src.jobs.local_spark_runtime"
Pop-Location
