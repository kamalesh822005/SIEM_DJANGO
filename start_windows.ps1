param(
    [switch]$SkipCompose,
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$djangoRoot = Join-Path $projectRoot "siem_project"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$dockerExe = "C:\Program Files\Docker\Docker\resources\bin\docker.exe"
$dockerCredExe = "C:\Program Files\Docker\Docker\resources\bin\docker-credential-desktop.exe"

$dockerBin = "C:\Program Files\Docker\Docker\resources\bin"
if (Test-Path $dockerBin) {
    if ($env:Path -notlike "*$dockerBin*") {
        $env:Path += ";$dockerBin"
    }
}

if (-not $SkipCompose) {
    if (-not (Test-Path $dockerExe)) {
        throw "Docker Desktop not found. Install Docker Desktop first."
    }

    if (Test-Path $dockerCredExe) {
        & $dockerCredExe version | Out-Null
    }

    Push-Location $projectRoot
    try {
        & $dockerExe compose up -d
    }
    finally {
        Pop-Location
    }
}

if (-not (Test-Path $pythonExe)) {
    py -m venv (Join-Path $projectRoot ".venv")
}

if (-not $SkipInstall) {
    & $pythonExe -m pip install -r (Join-Path $djangoRoot "requirements.txt")
}

& $pythonExe (Join-Path $djangoRoot "manage.py") migrate
& $pythonExe (Join-Path $djangoRoot "manage.py") runserver 0.0.0.0:8000
